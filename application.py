from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import sys
import hashlib


application = Flask(__name__, static_url_path='/static', static_folder='static')
DB = DBhandler()
application.config["SECRET_KEY"] = "Oisobaki"

@application.route("/")
def main():
    return render_template("메인화면.html")

@application.route("/리뷰전체보기")
def all_review():
    return render_template("리뷰전체보기.html")

@application.route("/채팅목록")
def chatlist():
    return render_template("채팅목록.html")

@application.route("/상품등록")
def reg_items():
    return render_template("상품등록.html")

@application.route("/마이페이지1")
def mypage():
    return render_template("마이페이지1.html")

if __name__ == "__main__":
 application.run(host='0.0.0.0', debug=True)