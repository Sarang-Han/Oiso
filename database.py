import pyrebase
import json

class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f )
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def user_login(self, id, pw):
        users = self.db.child("users").get().val()

        for user_info in users.items():
            user_data = user_info[1]
            if user_data.get("id") == id and user_data.get("pw") == pw:  # 해당하는 id와 pw가 있는지 확인
                return True
        return False

    def write_to_db(self, profile, name, id, pw_hash, email, phone):
        user_info = {
            "profile": profile,
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
