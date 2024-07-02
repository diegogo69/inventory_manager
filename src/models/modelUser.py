from .entities.user import User

class ModelUser():

    @classmethod
    def login(self, db, user):

        try:
            cursor = db.connection.cursor()
            cursor.execute('''SELECT id_user, username, hash, theme FROM users 
                                WHERE username = %s''', (user.username,))
            row = cursor.fetchone()

            if row != None:
                user = User(row['id_user'], row['username'], 
                            User.check_password(row['hash'], user.password), 
                            row['theme'])
                return user

            else:
                return None
            
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def get_by_id(self, db, id):

        try:
            cursor = db.connection.cursor()
            cursor.execute('''SELECT id_user, username FROM users 
                                WHERE id_user = %s''', (id,))
            row = cursor.fetchone()

            if row != None:
                return User(row['id_user'], row['username'], None)

            else:
                return None
        except Exception as ex:
            raise Exception(ex)