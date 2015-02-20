
from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
import requests
import json


from facebook import GraphAPI

app = Flask(__name__)



@app.route("/")
def sample():
    return render_template("sample2.html")

@app.route("/log_to_file/<data>")
def log_file(data):
    print data
    with open("sample2.log", "a") as myfile:
        myfile.write(data)
        myfile.write("\n")
    return "submitted"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7003, threaded=True,debug=True)
