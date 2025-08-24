import sqlite3

class Country:
    @staticmethod
    def get_db_connection():
        return sqlite3.connect("projectdb.db")

    @staticmethod
    def create_table():
        with Country.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = '''create table if not exists countries
                    (country_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country_name TEXT not null unique)
                
                    
                    
                '''
            cursor.execute(sql)
            cursor.close()
    
    @staticmethod
    def insert(country_name):
        with Country.get_db_connection() as connection:
            cursor = connection.cursor()
            try:
                sql = '''insert into countries 
                        (country_name)
                        values(?)'''
                cursor.execute(sql, (country_name,))
                country_id = cursor.lastrowid
                connection.commit()
                cursor.close()
                return {
                    'country_id': country_id,
                    'country_name': country_name
                }
            except sqlite3.IntegrityError:
                cursor.close()
                return None
    
    @staticmethod
    def get_all():
        with Country.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = 'SELECT * FROM countries'
            cursor.execute(sql)
            countries = cursor.fetchall()
            cursor.close()
            return [dict(
                country_id=country[0],
                country_name=country[1]
            ) for country in countries]
    
    @staticmethod
    def get_by_id(country_id):
        with Country.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = 'SELECT * FROM countries WHERE country_id = ?'
            cursor.execute(sql, (country_id,))
            country = cursor.fetchone()
            cursor.close()
            if country:
                return dict(
                    country_id=country[0],
                    country_name=country[1]
                )
            return None
    
    @staticmethod
    def update(country_id, **kwargs):
        with Country.get_db_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute('SELECT * FROM countries WHERE country_id = ?', (country_id,))
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

                sql = f"UPDATE countries SET {', '.join(update_fields)} WHERE country_id = ?"
                values.append(country_id)
                cursor.execute(sql, values)
                connection.commit()
                cursor.close()
                return {'message': f"Country {country_id} updated successfully"}
            except sqlite3.IntegrityError:
                cursor.close()
                return None
    
    @staticmethod
    def delete(country_id):
        with Country.get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM countries WHERE country_id = ?', (country_id,))
            country = cursor.fetchone()
            if country is None:
                cursor.close()
                return None
            
            cursor.execute('DELETE FROM countries WHERE country_id = ?', (country_id,))
            connection.commit()
            cursor.close()
            return {'message': f"Country {country_id} deleted successfully"}