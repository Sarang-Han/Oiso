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

        for user_info in users.items():
            if user_info.get("id") == id_ and user_info.get("pw") == pw:  # 해당하는 id와 pw가 있는지 확인
                return True
        return False

    def write_to_db(self, name, id, pw_hash, email, phone):
        data = {
            "name": name,
            "id": id,  
            "pw": pw_hash,   
            "email": email,
            "phone": phone
        }
        self.db.child("users").push(data)