from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
import requests
import json

import os

import sys

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
    # return render_template("index.html")
    return render_template("pages/login.html")

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
    # return render_template("location_entry.html")
    return render_template("pages/location.html")

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
    return redirect(url_for('dashboard'))


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

@app.route("/dashboard", methods=["GET"])
def dashboard():
    me = facebook.get('/me')
    id = get_hacker_from_oauth(me.data["id"])["id"]
    return user_page(id)


@app.route("/users/<user_id>", methods=["GET"])
def user_page(user_id):
    user = get_hacker(user_id)

    me = facebook.get('/me')

    friends = get_friends(user_id)

    print friends

    hackathons_attended = get_hackathons_attended(user_id)

    friend = is_friends(me.data["id"],user_id)

    # return render_template("users/show.html"
    #                        , user=user
    #                        , friend=friend
    #                        , user_id=user_id
    #                        , hackathons_attended=hackathons_attended
    #                        , friends=friends)
    return render_template("pages/dashboard.html"
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

    for k,hackathon in enumerate(hackathons):
        registered = is_going(facebook.get('/me').data["id"], hackathon["id"])
        hackathons[k]["registered"] = registered


    # return render_template("hackathons/index.html", hackathons=hackathons)
    return render_template("pages/browse-hackathons.html", hackathons=hackathons)

@app.route("/hackathons/<int:hackathon_id>", methods=["GET"])
def hackathon_page(hackathon_id):
    hackathon = get_hackathon(hackathon_id)

    registered = is_going(facebook.get('/me').data["id"],hackathon_id)

    #Need to get registered here

    # return render_template("hackathons/show.html", hackathon=hackathon, registered=registered)
    return render_template("pages/hackathon.html", hackathon=hackathon, registered=registered)

@app.route("/teams/new", methods=["GET"])
def new_team():
    id = current_user()['id']
    friends = get_friends(id)
    return render_template("teams/new.html", friends=friends)

@app.route("/teams/<int:team_id>", methods=["GET"])
def show_team(team_id):
    user_id = current_user()['id']
    team = get_teams(user_id, for_team=team_id)
    return render_template("teams/show.html", team=team)

@app.route("/teams/<int:team_id>/invite", methods=["GET"])
def invite_members_to_team(team_id):
    user_id = current_user()['id']
    team = get_teams(user_id, for_team=team_id)
    teammate_ids = map(lambda x: x["id"], team["members"])
    friends = filter(lambda friend: friend["id"] not in teammate_ids,get_friends(user_id))
    return render_template("teams/invite.html", friends=friends, team=team)

@app.route("/teams/<int:team_id>/invite", methods=["POST"])
def commit_invitations_members_to_team(team_id):
    user_id = current_user()['id']
    team = get_teams(user_id, for_team=int(team_id))
    member_ids = request.form['members']
    me = facebook.get('/me')
    for member_id in member_ids:
        add_hacker_to_team(member_id, team["id"])

    return redirect(url_for('team_index'))

@app.route("/teams", methods=["GET"])
def team_index():
    user_id = current_user()['id']
    return render_template("teams/index.html", teams=get_teams(user_id))

@app.route("/teams", methods=["POST"])
def create_team():
    team_name = request.form['name']
    member_ids = request.form['members']
    user_id = current_user()['id']
    team_id = add_team(user_id, team_name)
    for member_id in member_ids:
        add_hacker_to_team(member_id, team_id)
    return render_template("teams/index.html", teams=get_teams(user_id))

@app.route("/hackathons/<int:hackathon_id>/register", methods=["GET"])
def answer_questions(hackathon_id):
    questions =  get_questions_for_hackathon(current_user()["id"], hackathon_id)
    hackathon = get_hackathon(hackathon_id)
    print(questions)
    hackathon["questions"] = questions
    return render_template("hackathons/register.html", hackathon=hackathon)


@app.route("/hackathons/<int:hackathon_id>/register", methods=["POST"])
def register_for_thon(hackathon_id):
    fid = facebook.get('/me').data["id"]
    user_id = current_user()['id']
    for field in request.form:
        _, qid = field.split("-")
        answer_question(user_id, qid, request.form[field])
    # register_for_hackathon(hackathon_id, user_id)
    print "about to make the call"
    f = os.popen(str("python scripts/sample1.py "+str(hackathon_id)+" "+str(fid)))
    return redirect(url_for("hackathon_index"))


# view helpers

@app.template_filter("datetimeformat")
def datetimeformat(value, format='%b %d, %Y'):
    return value.strftime(format)

# other helpers

def current_user():
    fid = facebook.get('/me').data["id"]
    return get_hacker_from_oauth(fid)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=Config.get_port(), threaded=True,debug=True)

