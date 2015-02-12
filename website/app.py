from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
import requests
import json

from db import *
from util import process_hackathon_data

from facebook import GraphAPI

app = Flask(__name__)

import Config
secret = Config.return_secrets()
SECRET_KEY = secret["SECRET_KEY"]
FACEBOOK_APP_ID = secret["FACEBOOK_APP_ID"]
FACEBOOK_APP_SECRET = secret["FACEBOOK_APP_SECRET"]

app = Flask(__name__)

app.secret_key = SECRET_KEY
oauth = OAuth()

facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key=FACEBOOK_APP_ID,
                            consumer_secret=FACEBOOK_APP_SECRET,
                            request_token_params={'scope': 'email'}
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/submit_location", methods=["POST"])
def submit_location():
    j = request.get_json()
    cur = conn.cursor()
    #route, street_number, state, city, zipcode, country
    me = facebook.get('/me')
    for k in j.keys():
        if j[k]=="Null":
            j[k]=None
    cur.execute("SELECT * FROM add_location_hacker(%s,%s,%s,%s,%s,%s,%s)", [me.data["id"], j["route"],j["street_number"],j["administrative_area_level_1"],j["locality"],j["postal_code"],j["country"]])
    for record in cur:
        print record
    cur.close()
    conn.commit()
    return "success"

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
                                               next=request.args.get('next') or request.referrer or None,
                                               _external=True))

@app.route("/location")
def location():
    return render_template("location_entry.html")

@app.route("/info")
def info():
    me = facebook.get('/me')
    print me.data
    return me.data['name']+" and what we are storing "+me.data["id"]

@app.route("/get_distance", methods=["POST"])
def get_distance():
    j = request.get_json()
    return get_distance(j)

@app.route("/add_friend/<id>")
def add_friends(id):
    return add_friend(str(facebook.get('/me').data["id"]),id)


def get_directions(j):
    j = j.replace(",","+")
    j = j.replace(" ","")
    print j
    me = facebook.get('/me')
    cur = conn.cursor()

    cur.execute("SELECT * from get_hacker_from_oauth(%s)",[str(me.data["id"])])
    person = cur.next()
    print person
    person = person[0]

    cur.execute("SELECT * from get_my_location(%s)",[str(person)])
    loc = ""
    address = cur.next()
    for l in address:
        loc+=str(l)+"+"
    loc = loc[:-1]
    r = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins="+j+"&destinations="+loc+"&key=AIzaSyDlqdpDbe7zYZfl6du0V2TeUR8cxu9eZ5c")
    print r.text
    return r.text.replace("\u","")

def get_distance_string(j):
    j = j.replace(",","+")
    j = j.replace(" ","")
    print j
    me = facebook.get('/me')
    cur = conn.cursor()

    cur.execute("SELECT * from get_hacker_from_oauth(%s)",[str(me.data["id"])])
    person = cur.next()
    print person
    person = person[0]
    MY_ID = person

    cur.execute("SELECT * from get_my_location(%s)",[str(person)])
    loc = ""
    address = cur.next()
    for l in address:
        loc+=str(l)+"+"
    loc = loc[:-1]
    r = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins="+j+"&destinations="+loc+"&key=AIzaSyDlqdpDbe7zYZfl6du0V2TeUR8cxu9eZ5c")
    j = json.loads(r.text)
    if "duration" not in j["rows"][0]["elements"][0]:
        return "Unknown"
    return j["rows"][0]["elements"][0]["duration"]["text"]


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    print "Adding user to database"
    import time
    cur = conn.cursor()
    cur.execute("SELECT * FROM register_hacker(%s,%s,%s)", [str(me.data["email"]),str(me.data["id"]),str(me.data["name"]),])
    for record in cur:
        print record
    cur.close()
    conn.commit()
    print "Done executing"
    return redirect(url_for('info'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@app.route("/import_hackathons", methods=["GET"])
def import_hackathons_page():
    return render_template("hackathons/import.html")

@app.route("/import_hackathons", methods=["POST"])
def import_hackathons():
    csvfile = request.files["data"]
    process_hackathon_data(csvfile)
    return render_template("hackathons/import.html")


@app.route("/users/<user_id>", methods=["GET"])
def user_page(user_id):
    user = get_hacker(user_id)

    me = facebook.get('/me')

    friends = get_friends(user_id)

    hackathons_attended = get_hackathons_attended(user_id)

    friend = is_friends(me.data["id"],user_id)


    return render_template("users/show.html"
                           , user=user
                           , friend=friend
                           , user_id=user_id
                           , hackathons_attended=hackathons_attended
                           , friends=friends)

@app.route("/hackathons", methods=["GET"])
def hackathon_index():

    me = facebook.get('/me')
    id = get_hacker_from_oauth(me.data["id"])["id"]

    hackathons = get_hackathons()

    print hackathons
    for k,hackathon in enumerate(hackathons):
        dist = get_distance_string(hackathon["location"])
        hackathons[k]["distance"] = dist
        hackathons[k]["friends"] = get_friends_at_hackathon(id, hackathon["id"])


    return render_template("hackathons/index.html", hackathons=hackathons)

@app.route("/hackathons/<hackathon_id>", methods=["GET"])
def hackathon_page(hackathon_id):
    hackathon = get_hackathon(hackathon_id)

    registered = is_going(facebook.get('/me').data["id"],hackathon_id)
    print registered
    #Need to get registered here

    return render_template("hackathons/show.html", hackathon=hackathon, registered=True)

@app.route("/teams/new", methods=["GET"])
def new_team():
    return render_template("teams/new.html")

@app.route("/teams", methods=["POST"])
def create_team():
    team_name = request.form['name']
    member_ids = request.form['members']
    (id, _email, _location, _name) = get_hacker_from_oauth(session['oauth_token'])
    team_id = add_team(id, team_name)
    for member_id in member_ids:
        add_hacker_to_team(member_id, team_id)

@app.route("/register/<hackathon_id>")
def register_for_hackathon():
    return ""


# view helpers

@app.template_filter("datetimeformat")
def datetimeformat(value, format='%b %d, %Y'):
    return value.strftime(format)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=Config.get_port(), threaded=True,debug=True)

