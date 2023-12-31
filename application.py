from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler
import hashlib
from datetime import datetime
import math
from functools import wraps

application = Flask(__name__, static_url_path='/static', static_folder='static')
DB = DBhandler()
application.config["SECRET_KEY"] = "Oisobaki"

# 로그인 확인하는 데코레이터 함수
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@application.route("/")
def login():
    return render_template("로그인.html")


@application.route("/login_", methods=['GET', 'POST']) # 로그인 확인 함수
def login_():
    if request.method == 'POST':
        id = request.form.get('id')
        pw = request.form.get('pw')
        pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest() # 비밀번호 해싱

        if not DB.check_if_users_exist():
            flash("등록된 사용자가 없습니다. 회원가입을 진행해주세요.")
            return redirect(url_for('login'))
        
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
        if 'profile' in request.files and request.files['profile'].filename != '':
            img_file = request.files['profile']
            img_file.save("static/image/{}".format(img_file.filename)) # static/image 경로에 이미지 저장
            profile = "{}".format(img_file.filename) # profile에 이미지 이름으로 저장
        else:
            profile = "_"  # 이미지가 업로드되지 않은 경우 "_" 문자열로 처리
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
        DB.write_to_db(profile, name, id, pw_hash, email, phone)
        session['username'] = name  # 세션에 사용자 이름 저장
        session['profile'] = profile
        return redirect(url_for('welcome', username=name, profile=profile))  # 회원가입 성공 시 웰컴페이지로 리다이렉트
    return render_template("회원가입.html")

@application.route("/logout") # 로그아웃 함수
def logout():
    session.clear()
    return redirect(url_for('login'))

@application.route("/웰컴페이지/<username>/<profile>") # 웰컴페이지 동적 라우팅 함수
def welcome(username, profile):
    username = session.get('username')
    profile = session.get('profile')
    return render_template("웰컴페이지.html", username=username, profile=profile) # 회원가입 정보로 임시 로그인하여 이름, 프사 띄우기

@application.route("/메인화면")
def main():
    selected_category = request.args.get('category', 'all')
    page = request.args.get("page", 0, type=int) # 현 페이지 인덱스
    per_page = 15 # 페이지 상품 수
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

@application.route("/상품등록")
@login_required
def reg_items():
    seller_id = session.get('id', '')  # 세션에서 id 가져와 판매자 id 자동완성, 없으면 빈 문자열
    return render_template("상품등록.html", seller_id=seller_id)

@application.route("/submit_item_post", methods=['POST']) # 상품 등록 함수
def reg_item_submit_post():
    
    image_files = request.files.getlist("image[]")
    img_paths = []

    for image_file in image_files:
        try:
            if image_file.filename != '': # 이미지 파일이 비어있지 않으면 저장 후 경로를 리스트에 추가.
                image_file.save("static/image/{}".format(image_file.filename))
                img_paths.append("static/image/{}".format(image_file.filename))
        except Exception as e:
            print("파일 저장 오류: ", e)
    
    data=request.form
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    DB.insert_item(data, img_paths, current_time) # 상품 정보와 이미지 경로, 현재 시간 저장
    seller_id = session.get('id', '')
    img_paths = str(img_paths[0])
    DB.insert_selllist(seller_id, data, img_paths)
    return redirect(url_for('main'))

@application.route("/상품상세/<item_key>/") # 상품 key로 동적 라우팅
def view_item_detail(item_key):
    data = DB.get_item_by_key(str(item_key))
    seller_info = DB.get_user_info_by_id(data['seller'])  # 판매자 정보 가져옴
    seller_name = seller_info['name'] if seller_info else None
    seller_id = seller_info['id']
    my_id = session.get('id', '')
    product_key = None
    
    # 상품 키 가져오기
    seller_items = DB.get_sellitems(seller_id)
    if seller_items:
        for key, value in seller_items.items():
            if value.get('name') == data.get('name') and value.get('price') == data.get('price'):
                product_key = key
                break

    if seller_info and 'profile' in seller_info and seller_info['profile'] != "_":
        seller_profile = seller_info['profile']
    else:
        seller_profile = 'prof1.png'  # 기본 프로필 이미지

    return render_template("상품상세.html", item_key=item_key, data=data, seller_name=seller_name, seller_profile=seller_profile,
                           seller_id=seller_id, my_id=my_id, product_key=product_key)

@application.route("/판매자프로필1/<seller_id>") # 판매자 프로필1(받은 리뷰)
def view_seller_detail1(seller_id):
    seller_info = DB.get_user_info_by_id(seller_id)

    # 받은 리뷰 데이터 가져오기
    reviews = DB.get_received_reviews(seller_id)
    if (reviews == None):
        lists = []
        tot_count = 0
    else:
        lists = reviews.items()
        tot_count = len(reviews)
    
    return render_template("판매자프로필1.html", seller_info=seller_info, received_reviews=lists, total=tot_count)

@application.route("/판매자프로필2/<seller_id>") # 판매자 프로필2(작성한 리뷰)
def view_seller_detail2(seller_id):
    seller_info = DB.get_user_info_by_id(seller_id)

    # 작성한 리뷰 데이터 가져오기
    reviews = DB.get_written_reviews(seller_id)
    if (reviews == None):
        lists = []
        tot_count = 0
    else:
        lists = reviews.items()
        tot_count = len(reviews)
    
    return render_template("판매자프로필2.html", seller_info=seller_info, written_reviews=lists, total=tot_count)

@application.route("/리뷰전체보기")
def all_review():
    page = request.args.get("page", 0, type=int) # 현 페이지 인덱스
    per_page = 18 # 페이지 상품 수
    start_idx = per_page * page
    end_idx = per_page * (page+1)
    data = DB.get_reviews()

    if not data or len(data) == 0:
        return render_template("리뷰전체보기.html", total=0)  # 리뷰 예외처리

    item_counts = len(data)
    page_count = math.ceil(item_counts / per_page)
    data = dict(list(data.items())[start_idx:end_idx])
    item_counts = len(data)
    page_count = math.ceil(item_counts / per_page)
    data = dict(list(data.items())[start_idx:end_idx])

    return render_template("리뷰전체보기.html", datas=data.items(), limit=per_page, page=page,
                           page_count=page_count, total=item_counts)

@application.route("/리뷰작성하기/<item_key>/") # 상품 key로 리뷰작성 동적라우팅
def reg_review_route(item_key):
    buyer_id = session.get('id', '')
    data = DB.get_item_by_key(str(item_key))
    return render_template("리뷰작성하기.html",item_key=item_key, data=data, buyer_id=buyer_id)

@application.route("/reg_review", methods=['POST']) # 리뷰작성 DB 넘기고 리뷰전체보기 이동
def regi_review():
    image_files = request.files.getlist("image[]")
    img_paths = []

    for image_file in image_files:
        try:
            if image_file.filename != '': # 이미지 파일이 비어있지 않으면 저장 후 경로를 리스트에 추가.
                image_file.save("static/image/{}".format(image_file.filename))
                img_paths.append("static/image/{}".format(image_file.filename))
        except Exception as e:
            print("파일 저장 오류: ", e)

    data = request.form
    DB.reg_review(data, img_paths)
    return redirect(url_for('all_review'))

@application.route("/리뷰상세/<review_key>/") # 리뷰 key로 동적 라우팅
def view_review_detail(review_key):
    data = DB.get_review_by_key(str(review_key))
    buyer = DB.get_user_info_by_id(data['buyer_id'])
    buyer_name = buyer['name']
    data['rate'] = int(data['rate']) # rate 정수로 변환

    return render_template("리뷰상세.html", review_key=review_key, data=data, buyer_name=buyer_name)

@application.route("/채팅목록")
@login_required
def chatlist():
    user_id = session.get('id', '')  # 세션에서 사용자 ID 가져오기
    if user_id:
        item_info_list = DB.get_sellitems_by_seller(user_id)
        if (item_info_list == None):
            sell_total = 0
        else:
            sell_total = len(item_info_list)

        buyer_chatlist = DB.get_chatitems(user_id)
        if (buyer_chatlist == None):
            buy_total = 0
        else:
            buy_total = len(buyer_chatlist)

        buylist = DB.get_buyitems_key(user_id)
        return render_template("채팅목록.html", item_info_list=item_info_list, sell_total=sell_total,
                               buyer_chatlist=buyer_chatlist, buy_total=buy_total, buylist=buylist)
    else:
        # 세션에 사용자 ID가 없는 경우 로그인 페이지로 리다이렉트 또는 다른 처리 수행
        return redirect(url_for('login'))  # login 함수명에 맞게 수정해야 합니다.

@application.route("/buying_complete/") # 구매 완료 함수
def buying_complete():
    name = request.args.get('name')
    price = request.args.get('price')
    img_path = request.args.get('img_path')
    item_key = request.args.get('item_key')

    data = {
    'name': name,
    'price': price,
    'img_path': img_path,
    'item_key': item_key
    }

    user_id = session.get('id', '')

    buylist = DB.get_buyitems_key(user_id)
    count = 0
    for item in buylist:
        if item == item_key:
            count += 1
            break
    if count == 0:
        DB.insert_buylist(user_id, data)
    return redirect(url_for('chatlist'))

@application.route("/채팅상세/<item_key>/")
@login_required
def chat_detail(item_key):
    user_id = session.get('id', '')
    chat_messages = DB.get_chat_messages(item_key)  # item_key에 해당하는 채팅 메시지 가져오기
    return render_template("채팅상세.html", user_id=user_id, item_key=item_key, chat_messages=chat_messages)

@application.route("/send_message", methods=["POST"])
def send_message():
    if request.method == "POST":
        data = request.json
        item_key = data.get("item_key")
        user_id = session.get('id', '')
        message = data.get("msg")
        timestamp = data.get("timestamp")

        item_info = DB.get_item_by_key(item_key)
        seller_id = item_info['seller']
        # 여기서 DB에 메시지를 저장하는 함수 호출
        DB.insert_message(item_key, user_id, message, timestamp)

        if (seller_id != user_id):
            item = DB.get_chatlist_by_itemkey(user_id, item_key)
            if (item == None):
                DB.insert_chatlist(user_id, item_key)

        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 400


@application.route("/마이페이지1")
@login_required
def mypage1():
    my_id = session.get('id', '')
    user_info = DB.get_user_info_by_id(my_id)
    name = user_info['name']
    profile = user_info['profile']

    #리뷰 부분
    reviews = DB.get_received_reviews(my_id)
    if (reviews == None):
        lists = []
        tot_count = 0
    else:
        lists = reviews.items()
        tot_count = len(reviews)
    return render_template("마이페이지1.html", my_id=my_id, name=name, profile=profile, lists=lists, total=tot_count)

@application.route("/마이페이지2")
def mypage2():
    my_id = session.get('id', '')
    user_info = DB.get_user_info_by_id(my_id)
    name = user_info['name']
    profile = user_info['profile']

    #리뷰 부분
    reviews = DB.get_written_reviews(my_id)
    if (reviews == None):
        lists = []
        tot_count = 0
    else:
        lists = reviews.items()
        tot_count = len(reviews)
    return render_template("마이페이지2.html", my_id=my_id, name=name, profile=profile, lists=lists, total=tot_count)

@application.route("/구매내역")
def buylist():
    my_id = session.get('id', '')
    my_buylist = DB.get_buyitems(my_id)
    if (my_buylist == None):
        lists = []
        tot_count = 0
    else:
        lists = my_buylist.items()
        tot_count = len(my_buylist)
    
    return render_template(
        "구매내역.html",
        lists = lists,
        total = tot_count
    )

@application.route("/판매내역")
def selllist():
    #세션 정보 활용하여 로그인 한 사람이 등록한 상품 정보 가져오기
    seller_id = session.get('id', '')
    my_selllist = DB.get_sellitems(seller_id)
    if (my_selllist == None):
        lists = []
        tot_count = 0
    else:
        lists = my_selllist.items()
        tot_count = len(my_selllist)
    
    return render_template(
        "판매내역.html",
        lists = lists,
        total = tot_count
    )

@application.route("/오이목록")
def oilist():
    my_id = session.get('id', '')
    my_oilist = DB.get_oilist_byuid(my_id)
    if (my_oilist == None):
        lists = []
        tot_count = 0
    else:
        lists = my_oilist.items()
        tot_count = len(my_oilist)
        
    return render_template(
        "오이목록.html",
        lists = lists,
        total = tot_count
    )

@application.route('/show_Oi/<item_key>/', methods=['GET'])
def show_Oi(item_key):
    my_oi = DB.get_oilist_bykey(session['id'],item_key)
    data = DB.get_item_by_key(str(item_key))
    seller_info = DB.get_user_info_by_id(data['seller'])  # 판매자 정보 가져옴
    seller_id = seller_info['id']
    my_id = session.get('id', '')
    return jsonify({'my_oi': my_oi, 'seller_id': seller_id, 'my_id': my_id})

@application.route('/like/<item_key>/', methods=['POST'])
def like(item_key):
    my_oilist = DB.update_oilist(session['id'],'Y',item_key)
    return jsonify({'msg': '오이목록에 추가!'})

@application.route('/unlike/<item_key>/', methods=['POST'])
def unlike(item_key):
    my_oilist = DB.update_oilist(session['id'],'N',item_key)
    return jsonify({'msg': '오이목록에서 삭제!'})



if __name__ == "__main__":
 application.run(host='0.0.0.0', debug=True)