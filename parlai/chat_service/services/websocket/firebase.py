
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("accountKey.json")
default_app = firebase_admin.initialize_app(
    cred,
    {
        'databaseURL': "https://misatobot-28b00-default-rtdb.europe-west1.firebasedatabase.app/"
    },
)

def get_history(id):
    user = db.reference('users').child(id).get()
    if (user):
            print(user['history'])
            return user['history']
    else:
        print("No user found, creating...")
        create_user(id)
        
def create_user(id):
    user = {
        'history': ""
    }
    db.reference('users').child(id).set(user)

def set_history(id, history):
    ref = db.reference('users').child(id)
    user = ref.get()
    ref.update({"history": history})