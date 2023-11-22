from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import sys
import hashlib


application = Flask(__name__, static_url_path='/static', static_folder='static')
DB = DBhandler()
application.config["SECRET_KEY"] = "Oisobaki"

@application.route("/")
def main():
    return render_template("/메인화면.html")

if __name__ == "__main__":
 application.run(host='0.0.0.0', debug=True)