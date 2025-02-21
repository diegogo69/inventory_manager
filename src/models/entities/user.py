from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    
    def __init__(self, id, username, password, theme=None) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.theme = theme
        
    @classmethod
    def check_password(self, hashed, password):
        return check_password_hash(hashed, password)