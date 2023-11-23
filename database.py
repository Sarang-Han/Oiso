import pyrebase
import json

class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f )
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def user_login(self, id_, pw):
        users = self.db.child("users").get().val()

        for user_id, user_info in users.items():
            if user_info["id"] == id_ and user_info["pw"] == pw:
                return True

        return False
    
    def write_to_db(self, name, id_, pw, email, phone):
        data = {
            "name": name,
            "id": id_,  
            "pw": pw,   
            "email": email,
            "phone": phone
        }
        self.db.child("users").push(data)

    def insert_item(self, data, img_paths, current_time):
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
        selllist = self.db.child("item").get().val()
        return selllist