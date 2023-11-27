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
    
    def get_items(self):
        items = self.db.child("item").get().val()
        return items
    
    def get_item_by_key(self, item_key):
        item = self.db.child("item").child(item_key).get()
        if item.val():
            return item.val()
        return None
    
    def get_user_info_by_id(self, user_id): # id로 user 정보 접근
        users = self.db.child("users").get()
        for user in users.each():
            if user.val()['id'] == user_id:
                return user.val()
        return None
    
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
        my_oilist = self.db.child("oilist").child("uid").get().val()
        return my_oilist

    def update_oilist(self, uid, isOilist, item_key):
        item_info = self.db.child("item").child(item_key).get()
        oilist_info ={
            "interested": isOilist,
            "name":item_info['name'],
            "price": item_info['price'],
            "img_path": item_info['img_path']
        }
        self.db.child("oilist").child(uid).child(item_key).set(oilist_info)
        return True