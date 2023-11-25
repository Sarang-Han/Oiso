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
        id = request.form.get('id')  # 입력값 받기
        pw = request.form.get('pw')

        if not id and not pw:  # 아이디나 비밀번호가 입력되지 않은 경우
            flash("아이디와 비밀번호를 입력해주세요.")
            return redirect(url_for('login'))
        
        elif not id: # 아이디가 입력되지 않은 경우
            flash("아이디를 입력해주세요.")
            return redirect(url_for('login'))
        
        elif not pw:  # 비밀번호가 입력되지 않은 경우
            flash("비밀번호를 입력해주세요.")
            return redirect(url_for('login'))

        elif DB.user_login(id, pw):
            session['logged_in'] = True
            session['id'] = id
            return redirect(url_for('main'))  # 로그인 성공 시 main 페이지로 리다이렉트
        else:
            flash("아이디나 비밀번호를 잘못 입력하셨습니다.")
        return redirect(url_for('login'))
    return render_template("로그인.html")


@application.route("/회원가입", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        pw = request.form['pw']
        email = request.form['email']
        phone = request.form['phone']

        # 필수 정보가 모두 입력되었는지 확인
        if not all([name, id, pw, email]):
            flash("필수 정보를 모두 기입해주세요!")
            return redirect(url_for('signup'))  # 필수 정보가 누락된 경우 회원가입 페이지로 리다이렉트
        
        # 비밀번호 해실
        pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
        
        if DB.user_duplicate_check(id):
            flash("아이디가 중복됩니다!")
            return redirect(url_for('signup'))  # 아이디가 중복된 경우 회원가입 페이지로 리다이렉트
        
        # db에 회원가입 데이터 저장
        DB.write_to_db(name, id, pw_hash, email, phone)
        return redirect(url_for('welcome'))  # 회원가입 성공 시 웰컴페이지로 리다이렉트

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

@application.route('/오이목록/<data>/', methods=['GET'])
def oilist(data):
    me = session.get('id', '')
    my_oilist = DB.get_oilist(me)
    tot_count = len(my_oilist)

    return render_template(
        "오이목록.html",
        lists=my_oilist.items(),
        total = tot_count
    )

@application.route('/상품상세/<data>/', methods=['POST'])
def like(data):
    my_oilist = DB.update_oilist(session['id'],'Y',data)
    return jsonify({'msg': '오이목록에 추가!'})

@application.route('/상품상세/<data>/', methods=['POST'])
def unlike(data):
    my_oilist = DB.update_oilist(session['id'],'N',data)
    return jsonify({'msg': '오이목록에서 삭제!'})

if __name__ == "__main__":
 application.run(host='0.0.0.0', debug=True)