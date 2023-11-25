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
