from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import sys
import hashlib
from datetime import datetime
import math

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
        pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

        if not id and not pw:  # 아이디나 비밀번호가 입력되지 않은 경우
            flash("아이디와 비밀번호를 입력해주세요.")
            return redirect(url_for('login'))
        
        elif not id: # 아이디가 입력되지 않은 경우
            flash("아이디를 입력해주세요.")
            return redirect(url_for('login'))
        
        elif not pw:  # 비밀번호가 입력되지 않은 경우
            flash("비밀번호를 입력해주세요.")
            return redirect(url_for('login'))

        elif DB.user_login(id, pw_hash):
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
        
        # 비밀번호 해싱
        pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
        
        if DB.user_duplicate_check(id):
            flash("아이디가 중복됩니다!")
            return redirect(url_for('signup'))  # 아이디가 중복된 경우 회원가입 페이지로 리다이렉트
        
        # db에 회원가입 데이터 저장
        DB.write_to_db(name, id, pw_hash, email, phone)
        session['username'] = name  # 세션에 사용자 이름 저장
        return redirect(url_for('welcome', username=name))  # 회원가입 성공 시 웰컴페이지로 리다이렉트

    return render_template("회원가입.html")

@application.route("/logout")
<<<<<<< HEAD
def logout():
    session.clear()
    return redirect(url_for('login'))

@application.route("/웰컴페이지/<username>")
def welcome(username):
    username = session.get('username')
    return render_template("웰컴페이지.html", username=username)
=======
def logout_user():
    session.clear()
    return redirect(url_for('main'))

@application.route("/웰컴페이지")
def welcome():
    return render_template("웰컴페이지.html")
>>>>>>> regi_item

@application.route("/메인화면")
def main():
    selected_category = request.args.get('category', 'all')
    page = request.args.get("page", 0, type=int) # 현 페이지 인덱스
    per_page = 12 # 페이지 상품 수
    start_idx = per_page * page
    end_idx = per_page * (page+1)
    data = DB.get_items()

    if data is None:
        data = {}
        item_counts = 0
    else:
        if selected_category != 'all':
            # 선택된 카테고리에 해당하는 상품만 필터링
            data = {k: v for k, v in data.items() if v['category'] == selected_category}
        item_counts = len(data)
    
    page_count = math.ceil(item_counts / per_page)
    data = dict(list(data.items())[start_idx:end_idx])
    return render_template("메인화면.html", datas=data.items(), limit=per_page, page=page,
                           page_count=page_count, total=item_counts, selected_category=selected_category)

@application.route("/view_detail/<item_key>/") # 상품 key로 동적 라우팅
def view_item_detail(item_key):
    print("### Item_key:",item_key)
    data = DB.get_item_by_key(str(item_key))
    print("#### Data:",data)
    return render_template("상품상세.html", item_key=item_key, data=data)

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

    return redirect(url_for('main'))

if __name__ == "__main__":
 application.run(host='0.0.0.0', debug=True)