import pyrebase
import json

class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f )
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def user_login(self, id, pw): # db에서 유저 로그인 정보 확인
        users = self.db.child("users").get().val()

        for user_info in users.items():
            user_data = user_info[1]
            if user_data.get("id") == id and user_data.get("pw") == pw:  # 해당하는 id와 pw가 있는지 확인
                return True
        return False

    def write_to_db(self, profile, name, id, pw_hash, email, phone): # 회원가입 정보 받아서 db에 쓰는 함수
        user_info = {
            "profile": profile, # 프로필 사진
            "name": name,       # 이름
            "id": id,           # ID
            "pw": pw_hash,      # PW
            "email": email,     # 이메일
            "phone": phone      # 전화번호
        }
        self.db.child("users").push(user_info)

    def user_duplicate_check(self, id_string): # 아이디 중복체크 함수
        users = self.db.child("users").get()
        
        if str(users.val()) == "None":  # 첫 번째 등록인 경우
            return False
        else: #아이디가 중복된 경우
            for res in users.each():
                value = res.val()
                if value['id'] == id_string:
                    return True
            return False

    def insert_item(self, data, img_paths, current_time): # 상품 등록
        item_info ={
            "seller": data['seller'],           # 판매자 ID
            "name": data['name'],               # 상품명
            "category": data['category'],       # 카테고리
            "price": data['price'],             # 가격
            "place": data['place'],             # 거래 지역
            "status": data['status'],           # 상품 상태
            "description": data['description'], # 상품 설명
            "img_path": img_paths,              # 이미지 경로
            "date": current_time                # 등록 날짜
        }
        self.db.child("item").push(item_info)
        print(data, img_paths)
        return True
    
    def get_user_info_by_id(self, user_id): # id로 user 정보 접근
        users = self.db.child("users").get()
        for user in users.each():
            if user.val()['id'] == user_id:
                return user.val()
        return None
    
    def get_items(self):
        items = self.db.child("item").get().val()
        return items
    
    def get_item_key(self, item_key):
        return item_key
    
    def get_item_by_key(self, item_key):
        item = self.db.child("item").child(item_key).get()
        if item.val():
            return item.val()
        return None
    
        #session id 별로 등록한 상품 정보 저장
    def insert_selllist(self, id_, data, img_paths):
        item_info ={
            "name": data['name'],               # 상품명
            "price": data['price'],             # 가격
            "img_path": img_paths               # 이미지 경로
        }
        self.db.child("selllist").child(id_).push(item_info)
        print(data, img_paths)
        return True

    def get_sellitems(self, id_):
        selllist = self.db.child("selllist").child(id_).get().val()
        return selllist
    
    def get_sellitems_by_seller(self, seller_id):
        items = self.db.child("item").get().val()
        seller_items = {}
        if items:
            for item_key, item_info in items.items():
                if 'seller' in item_info and item_info['seller'] == seller_id:
                    seller_items[item_key] = {
                        'name': item_info['name'],  # 상품명
                        'img_path': item_info['img_path'][0] if 'img_path' in item_info else None  # 이미지 경로 (첫 번째 이미지만 가져오기)
                    }
        return seller_items

    def get_oilist_bykey(self, uid, item_key):
        ois = self.db.child("oilist").child(uid).get()
        target_value=""
        if ois.val() == None:
            return target_value
        
        for res in ois.each():
            key_value = res.key()
            
            if key_value == item_key:
                target_value=res.val()
                
        return target_value

    def get_oilist_byuid(self, uid):
        my_oilist = self.db.child("oilist").child(uid).get().val()
        return my_oilist

    def update_oilist(self, uid, isOilist, item_key):
        item_info = self.db.child("item").child(item_key).get().val()
        imgpath = item_info["img_path"]
        oilist_info ={
            "interested": isOilist,
            "name": item_info['name'],
            "price": item_info['price'],
            "img_path": imgpath[0]
        }
        self.db.child("oilist").child(uid).child(item_key).set(oilist_info)
        return True
    
    def get_chat_messages(self, item_key):
        chat_ref = self.db.child("chatlist").child(item_key).get().val()
        if chat_ref:
            return list(chat_ref.values())  # 딕셔너리를 리스트로 변환하여 반환합니다.
        return None
    
    def insert_chatlist(self, uid, item_key):
        item_info=self.db.child("item").child(item_key).get().val()
        imgpath = item_info['img_path']
        chat_info={
            "img_path": imgpath[0],
            "name": item_info['name'],
            "price": item_info['price'],
            "item_key": item_key
        }
        self.db.child("buyer_chatlist").child(uid).child(item_key).push(chat_info)
        return True
    
    def get_chatlist_by_itemkey(self, uid, item_key):
        item = self.db.child("buyer_chatlist").child(uid).child(item_key).get().val()
        return item

    def get_chatitems(self, uid):
        items = self.db.child("buyer_chatlist").child(uid).get().val()
        chatitems = {}
        if items:
            for item in items.items():
                item_key = item[0]
                for value in item[1]:
                    chatitems[item_key] = {
                        'name': item[1][value]['name'],
                        'price': item[1][value]['price'],
                        'item_key': item_key,
                        'img_path': item[1][value]['img_path'] if 'img_path' in item[1][value] else None  # 이미지 경로 (첫 번째 이미지만 가져오기)
                    }
        return chatitems

    def get_chatlist_byuid(self, uid):
        chatlist = self.db.child("buyer_chatlist").child(uid).get().val()
        return chatlist

    def insert_message(self, item_key, user_id, message, timestamp):
    # 채팅 메시지 추가
        chat_ref = self.db.child("chatlist").child(item_key)

        # 새로운 메시지 정보
        new_message = {
            'id': user_id,
            'msg': message,
            'timestamp': timestamp
        }

        # 채팅방에 새로운 메시지 추가
        chat_ref.push(new_message)

    def insert_buylist(self, uid, data):
        item_info={
            'name': data['name'],
            'price': data['price'],
            'img_path': data['img_path'],
            'item_key': data['item_key']
        }
        self.db.child("buylist").child(uid).push(item_info)
        return True
    
    def get_buyitems(self, uid):
        buylist = self.db.child("buylist").child(uid).get().val()
        return buylist
    
    def get_user_key_by_id(self, user_id): # id로 user key
        users = self.db.child("users").get()
        for user in users.each():
            if user.val()['id'] == user_id:
                return user.key()
        return None


    def reg_review(self, data, img_paths): # 리뷰 작성 DB 저장
        seller_key = self.get_user_key_by_id(data['seller_id'])
        buyer_key = self.get_user_key_by_id(data['buyer_id'])
        seller_name = self.db.child("users").child(seller_key).val()['name']
        buyer_name = self.db.child("users").child(buyer_key).val()['name']
        review_info ={
            "seller_id": data['seller_id'], # 판매자(리뷰받음)ID
            "seller_name": seller_name,
            "buyer_id": data['buyer_id'],   # 구매자(리뷰작성)ID
            "buyer_name": buyer_name,
            "name": data['name'],           # 상품명
            "price": data['price'],         # 가격
            "title": data['title'],         # 리뷰 제목
            "content": data['content'],     # 리뷰 내용
            "rate": data['reviewStar'],     # 별점
            "img_path": img_paths,          # 리뷰 이미지
        }
        self.db.child("review").push(review_info)
        result = self.db.child("review").push(review_info)
        review_key = result['name'] # 리뷰 key

        self.db.child("users").child(seller_key).child("received_reviews").update({review_key: True}) # 판매자의 받은 리뷰에 리뷰key 저장
        self.db.child("users").child(buyer_key).child("written_reviews").update({review_key: True}) # 구매자의 작성한 리뷰에 리뷰key 저장

        self.db.child("received_reviews").child(data['seller_id']).push(review_info)
        self.db.child("written_reviews").child(data['buyer_id']).push(review_info)
        return True

    def get_received_reviews(self, uid):
        reviews = self.db.child("received_reviews").child(uid).get().val()
        return reviews

    def get_written_reviews(self, uid):
        reviews = self.db.child("written_reviews").child(uid).get().val()
        return reviews