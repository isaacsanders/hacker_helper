from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth

from db import conn, get_hacker, get_friends
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

@app.route("/distances")
def get_distances():
    return 0


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
    return render_template("import_hackathons.html")

@app.route("/import_hackathons", methods=["POST"])
def import_hackathons():
    csvfile = request.files["data"]
    process_hackathon_data(csvfile)
    return render_template("import_hackathons.html")


@app.route("/users/<user_id>", methods=["GET"])
def user_page(user_id):
    user = get_hacker(user_id)
    friends = get_friends(user_id)
    return render_template("user_profile.html", user=user, friends=friends)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=Config.get_port(), threaded=True,debug=True)

