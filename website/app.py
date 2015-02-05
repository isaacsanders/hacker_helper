from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth

from db import conn
from util import process_hackathon_data

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


@app.route("/user/<user_id>", methods=["GET"])
def user_page(user_id):
    user = get_user(user_id)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=Config.get_port(), threaded=True,debug=True)

