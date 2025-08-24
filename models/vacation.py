import sqlite3
from datetime import datetime, date


class Vacation:
    @staticmethod
    def get_db_connection():
        return sqlite3.connect("projectdb.db")

    @staticmethod
    def create_table():
        with Vacation.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = '''create table if not exists vacations
                    (vacation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country_id INTEGER not null,
                    vacation_description TEXT not null,
                    vacation_start TEXT not null,
                    vacation_end TEXT not null,
                    price NUMERIC not null,
                    picture_file_name TEXT not null,
                    FOREIGN KEY (country_id) REFERENCES countries(country_id))
                
                    
                    
                '''
            cursor.execute(sql)
            cursor.close()
    
    @staticmethod
    def insert(country_id, vacation_description, vacation_start,
                                 vacation_end, price, picture_file_name):
        """
        Inserts a new vacation record into the database.
        Assumes all input data has been validated by the controller.
        """
        with Vacation.get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            try:
                sql = '''INSERT INTO vacations
                             (country_id, vacation_description, vacation_start,
                                vacation_end, price, picture_file_name)
                             VALUES(?, ?, ?, ?, ?, ?)'''
                cursor.execute(sql, (country_id, vacation_description, vacation_start,
                                   vacation_end, price, picture_file_name))
                vacation_id = cursor.lastrowid
                connection.commit()
                cursor.close()
                return {'message': f"Vacation '{vacation_id}' inserted successfully", 'id': vacation_id}
            except sqlite3.IntegrityError as e:
                cursor.close()
                return {'error': f"Database error: Could not insert vacation due to a constraint violation. Details: {e}"}
            except Exception as e:
                cursor.close()
                return {'error': f"An unexpected database error occurred during insertion: {e}"}
    @staticmethod
    def get_all():
        with Vacation.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = '''
                SELECT v.*, COALESCE(l.likes_count, 0) as likes_count 
                FROM vacations v 
                LEFT JOIN (
                    SELECT vacation_id, COUNT(*) as likes_count 
                    FROM likes 
                    GROUP BY vacation_id
                ) l ON v.vacation_id = l.vacation_id 
                ORDER BY v.vacation_start ASC
            '''
            cursor.execute(sql)
            vacations = cursor.fetchall()
            cursor.close()
            return [dict(
                vacation_id=vacation[0],
                country_id=vacation[1],
                vacation_description=vacation[2],
                vacation_start=vacation[3],
                vacation_end=vacation[4],
                price=vacation[5],
                picture_file_name=vacation[6],
                likes_count=vacation[7]
            ) for vacation in vacations]
    
    @staticmethod
    def get_by_id(vacation_id):
        with Vacation.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = '''
                SELECT v.*, COALESCE(l.likes_count, 0) as likes_count 
                FROM vacations v 
                LEFT JOIN (
                    SELECT vacation_id, COUNT(*) as likes_count 
                    FROM likes 
                    GROUP BY vacation_id
                ) l ON v.vacation_id = l.vacation_id 
                WHERE v.vacation_id = ?
            '''
            cursor.execute(sql, (vacation_id,))
            vacation = cursor.fetchone()
            cursor.close()
            if vacation:
                return dict(
                    vacation_id=vacation[0],
                    country_id=vacation[1],
                    vacation_description=vacation[2],
                    vacation_start=vacation[3],
                    vacation_end=vacation[4],
                    price=vacation[5],
                    picture_file_name=vacation[6],
                    likes_count=vacation[7]
                )
            return None
    
    @staticmethod
    def update(vacation_id, **kwargs):
        with Vacation.get_db_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute('SELECT * FROM vacations WHERE vacation_id = ?', (vacation_id,))
                if not cursor.fetchone():
                    cursor.close()
                    return {'error': 'Vacation not found'}

                update_fields = []
                values = []
                for key, value in kwargs.items():
                    update_fields.append(f"{key} = ?")
                    values.append(value)
                
                if not update_fields:
                    cursor.close()
                    return {'error': 'No fields to update'}

                sql = f"UPDATE vacations SET {', '.join(update_fields)} WHERE vacation_id = ?"
                values.append(vacation_id)
                cursor.execute(sql, values)
                connection.commit()
                cursor.close()
                return {'message': f"Vacation {vacation_id} updated successfully"}
            except sqlite3.IntegrityError as e:
                cursor.close()
                return {'error': f"Database error: Could not update vacation due to a constraint violation. Details: {e}"}
            except Exception as e:
                cursor.close()
                return {'error': f"An unexpected database error occurred during update: {e}"}
    
    @staticmethod
    def delete(vacation_id):
        with Vacation.get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute('SELECT * FROM vacations WHERE vacation_id = ?', (vacation_id,))
            vacation = cursor.fetchone()
            if vacation is None:
                cursor.close()
                return None
            
            cursor.execute('DELETE FROM vacations WHERE vacation_id = ?', (vacation_id,))
            connection.commit()
            cursor.close()
            return {'message': f"Vacation {vacation_id} deleted successfully"}

    @staticmethod
    def get_user_liked_vacations(user_id):
        """Get list of vacation IDs that a user has liked"""
        with Vacation.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = 'SELECT vacation_id FROM likes WHERE user_id = ?'
            cursor.execute(sql, (user_id,))
            liked_vacations = cursor.fetchall()
            cursor.close()
            return [row[0] for row in liked_vacations]

    