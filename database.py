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