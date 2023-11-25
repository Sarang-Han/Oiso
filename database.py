import pyrebase
import json
import hashlib

class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f )
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def user_login(self, id_, pw):
        users = self.db.child("users").get().val()
        hashed_pw = hashlib.sha256(pw.encode('utf-8')).hexdigest()

        for user_info in users.items():
            user_data = user_info[1]
            if user_data.get("id") == id_ and user_data.get("pw") == hashed_pw:  # 해당하는 id와 pw가 있는지 확인
                return True
        return False

    def write_to_db(self, name, id, pw_hash, email, phone):
        user_info = {
            "name": name,
            "id": id,  
            "pw": pw_hash,   
            "email": email,
            "phone": phone
        }
        self.db.child("users").push(user_info)

    def user_duplicate_check(self, id_string):
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
            "description": data['description'], # 상품 상태/설명
            "img_path": img_paths,              # 이미지 경로
            "date": current_time                # 등록 날짜
        }
        self.db.child("item").push(item_info)
        print(data, img_paths)
        return True
    
    def get_items(self):
        items = self.db.child("item").get().val()
        return items