from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
import requests
import json

import psycopg2
import psycopg2.extensions
import logging


app = Flask(__name__)



import Config
secret = Config.return_secrets()
SECRET_KEY = secret["SECRET_KEY"]
FACEBOOK_APP_ID = secret["FACEBOOK_APP_ID"]
FACEBOOK_APP_SECRET = secret["FACEBOOK_APP_SECRET"]

conn = psycopg2.connect(database="hacker", user="dax", password="daxiscool")

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

@app.route("/add_friend", methods=["POST"])
def add_friend():
    j = request.get_json()


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

def get_distance(j):
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

def get_distance2(j):
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
    return j["rows"][0]["elements"][0]["duration"]["text"]

@app.route("/friends")
def add_friends():
    # print request.form["email"]
    if "email" in request.form:
        print request.form["email"]
    return render_template("friends.html")


@app.route("/hackathons")
def get_distances():
    j= request.get_json()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_hackathons()")
    hackathons = []
    for record in cur:
        print record
        hackathons.append(record)
    distances = []

    for hackathon in hackathons:
        loc = hackathon[11]+","+hackathon[12]+","+hackathon[8]+","+hackathon[9]+","+hackathon[7] +","+hackathon[10]
        distance = get_distance2(loc)
        distances.append(distance)
    cur.close()

    cur = conn.cursor()

    me = facebook.get('/me')
    cur.execute("SELECT * from get_hacker_from_oauth(%s)",[str(me.data["id"])])
    person = cur.next()
    print person
    person = person[0]
    cur.execute("SELECT * from get_friends(%s)",[int(person)])
    friends = []
    for friend in cur:
        friends.append(friend)
        
    conn.commit()
    return render_template("hackathons.html", hd = zip(hackathons,distances),friends = friends)


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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=Config.get_port(), threaded=True, debug=True)
