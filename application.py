from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import sys
import hashlib


application = Flask(__name__, static_url_path='/static', static_folder='static')
DB = DBhandler()
application.config["SECRET_KEY"] = "Oisobaki"

@application.route("/")
def login():
    return render_template("로그인.html")

@application.route("/login_", methods=['GET', 'POST'])
def login_():
    if request.method == 'POST':
        id_ = request.form['id']
        pw = request.form['pw']
        if DB.user_login(id_, pw):
            session['logged_in'] = True
            session['id'] = id_
            return redirect(url_for('main'))  # 로그인 성공 시 main 페이지로 리다이렉트
        else:
            flash("아이디나 비밀번호를 잘못 입력하셨습니다!")
            return redirect(url_for('login'))
    return render_template("로그인.html")

@application.route("/회원가입", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        id_ = request.form['id']
        pw = request.form['pw']
        email = request.form['email']
        phone = request.form['phone']
        
        # Firebase에 회원가입 데이터 저장
        DB.write_to_db(name, id_, pw, email, phone)
        return redirect(url_for('welcome'))  # 웰컴페이지로 리다이렉트
    return render_template("회원가입.html")

@application.route("/웰컴페이지")
def welcome():
    return render_template("웰컴페이지.html")

@application.route("/메인화면")
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
def mypage1():
    return render_template("마이페이지1.html")
@application.route("/마이페이지2")
def mypage2():
    return render_template("마이페이지2.html")

@application.route("/구매내역")
def buylist():
    return render_template("구매내역.html")

@application.route("/판매내역")
def selllist():
    return render_template("판매내역.html")

@application.route("/오이목록")
def oilist():
    return render_template("오이목록.html")

if __name__ == "__main__":
 application.run(host='0.0.0.0', debug=True)