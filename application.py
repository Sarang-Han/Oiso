from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import sys
import hashlib
from datetime import datetime


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
    seller_id = session.get('id', '')  # 세션에서 id 가져오기, 없으면 빈 문자열
    return render_template("상품등록.html", seller_id=seller_id)

@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    
    image_files = request.files.getlist("image[]")
    img_paths = []

    for image_file in image_files:
        try:
            if image_file.filename != '':
                image_file.save("static/image/{}".format(image_file.filename))
                img_paths.append("static/image/{}".format(image_file.filename))
        except Exception as e:
            print("파일 저장 오류: ", e)
    
    data=request.form
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    DB.insert_item(data, img_paths, current_time)

    #session id 별로 상품 저장
    seller_id = session.get('id', '')
    DB.insert_selllist(seller_id, data, img_paths)

    return render_template("메인화면.html")

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
    #세션 정보 활용하여 로그인 한 사람이 등록한 상품 정보 가져오기
    seller_id = session.get('id', '')
    my_selllist = DB.get_sellitems(seller_id)
    tot_count = len(my_selllist)
    
    return render_template(
        "판매내역.html",
        lists = my_selllist.items(),
        total = tot_count
    )

@application.route("/오이목록")
def oilist():
    return render_template("오이목록.html")

if __name__ == "__main__":
 application.run(host='0.0.0.0', debug=True)