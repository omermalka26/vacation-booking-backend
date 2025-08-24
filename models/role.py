import sqlite3

class Role:
    @staticmethod
    def get_db_connection():
        return sqlite3.connect("projectdb.db")

    @staticmethod
    def create_table():
        with Role.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = '''create table if not exists roles
                    (role_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role_name TEXT not null unique)
                
                    
                    
                '''
            cursor.execute(sql)
            cursor.close()
    
    @staticmethod
    def insert(role_name):
        with Role.get_db_connection() as connection:
            cursor = connection.cursor()
            try:
                sql = '''insert into roles
                        (role_name)
                        values(?)'''
                cursor.execute(sql, (role_name,))
                connection.commit()
                cursor.close()
            except sqlite3.IntegrityError:
                cursor.close()
                return None
    
    @staticmethod
    def get_all():
        with Role.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = 'SELECT * FROM roles'
            cursor.execute(sql)
            roles = cursor.fetchall()
            cursor.close()
            return [dict(
                role_id=role[0],
                role_name=role[1]
            ) for role in roles]
    
    @staticmethod
    def get_by_id(role_id):
        with Role.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = 'SELECT * FROM roles WHERE role_id = ?'
            cursor.execute(sql, (role_id,))
            role = cursor.fetchone()
            cursor.close()
            if role:
                return dict(
                role_id=role[0],
                role_name=role[1]
                )
            return None
    
    @staticmethod
    def update(role_id, **kwargs):
        with Role.get_db_connection() as connection:
            cursor = connection.cursor()
            try:
               
                cursor.execute('SELECT * FROM roles WHERE role_id = ?', (role_id,))
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

                sql = f"UPDATE roles SET {', '.join(update_fields)} WHERE role_id = ?"
                values.append(role_id)
                cursor.execute(sql, values)
                connection.commit()
                cursor.close()
                return {'message': f"Role {role_id} updated successfully"}
            except sqlite3.IntegrityError:
                cursor.close()
                return None
    
    @staticmethod
    def delete(role_id):
        with Role.get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM roles WHERE role_id = ?', (role_id,))
            user = cursor.fetchone()
            if user is None:
                cursor.close()
                return None
            
            cursor.execute('DELETE FROM roles WHERE role_id = ?', (role_id,))
            connection.commit()
            cursor.close()
            return {'message': f"Role {role_id} deleted successfully"}