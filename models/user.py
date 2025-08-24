import sqlite3

class User:
    @staticmethod
    def get_db_connection():
        return sqlite3.connect("projectdb.db")

    @staticmethod
    def create_table():
        with User.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = '''create table if not exists users
                    (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT not null,
                    last_name TEXT not null,
                    email TEXT not null unique,
                    password text not null,
                    role_id INTEGER not null,
                    FOREIGN KEY (role_id) REFERENCES roles(role_id))
                '''
            cursor.execute(sql)
            cursor.close()
    
    @staticmethod
    def insert(first_name, last_name, email, password_hash, role_id):
        """
        Insert a new user with already hashed password
        """
        with User.get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            try:
                sql = '''insert into users 
                        (first_name, last_name, email, password, role_id)
                        values(?, ?, ?, ?, ?)'''
                cursor.execute(sql, (first_name, last_name, email, password_hash, role_id))
                user_id = cursor.lastrowid
                connection.commit()
                cursor.close()
                return {
                    'user_id': user_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'role_id': role_id
                }
            except sqlite3.IntegrityError:
                cursor.close()
                return None
    
    @staticmethod
    def get_all():
        with User.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = 'SELECT * FROM users'
            cursor.execute(sql)
            users = cursor.fetchall()
            cursor.close()
            return [dict(
                user_id=user[0],
                first_name=user[1],
                last_name=user[2],
                email=user[3],
                role_id=user[5]
            ) for user in users]
    
    @staticmethod
    def get_by_id(user_id):
        with User.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = 'SELECT * FROM users WHERE user_id = ?'
            cursor.execute(sql, (user_id,))
            user = cursor.fetchone()
            cursor.close()
            if user:
                return dict(
                    user_id=user[0],
                first_name=user[1],
                last_name=user[2],
                email=user[3],
                role_id=user[5]
                )
            return None
    
    @staticmethod
    def get_by_email(email):
        with User.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = 'SELECT * FROM users WHERE email = ?'
            cursor.execute(sql, (email,))
            user = cursor.fetchone()
            cursor.close()
            if user:
                return dict(
                    user_id=user[0],
                first_name=user[1],
                last_name=user[2],
                email=user[3],
                password_hash=user[4],
                role_id=user[5]
                )
            return None
    
    @staticmethod
    def update(user_id, **kwargs):
        with User.get_db_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
                if not cursor.fetchone():
                    cursor.close()
                    return None

               
                update_fields = []
                values = []
                for key, value in kwargs.items():
                    update_fields.append(f"{key} = ?")
                    values.append(value)
                
                if not update_fields:
                    cursor.close()
                    return None

                sql = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = ?"
                values.append(user_id)
                cursor.execute(sql, values)
                connection.commit()
                cursor.close()
                return {'message': f"User {user_id} updated successfully"}
            except sqlite3.IntegrityError:
                cursor.close()
                return None

    @staticmethod
    def delete(user_id):
        with User.get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
            if user is None:
                cursor.close()
                return None
            
            cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            connection.commit()
            cursor.close()
            return {'message': f"User {user_id} deleted successfully"}
