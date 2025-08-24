import sqlite3

class Like:
    @staticmethod
    def get_db_connection():
        return sqlite3.connect("projectdb.db")

    @staticmethod
    def create_table():
        """
        Creates the 'likes' table in the database if it doesn't already exist.
        Includes foreign key constraints with ON DELETE CASCADE.
        """
        with Like.get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS likes (
                    user_id INTEGER NOT NULL,
                    vacation_id INTEGER NOT NULL,
                    PRIMARY KEY (user_id, vacation_id), -- Composite primary key to ensure uniqueness
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (vacation_id) REFERENCES vacations(vacation_id) ON DELETE CASCADE
                )
            ''')
            connection.commit()
            cursor.close()
            print("Likes table ensured.")


    @staticmethod
    def insert(user_id: int, vacation_id: int) -> dict | None:
        """
        Records a new 'like' for a vacation by a user.

        Args:
            user_id (int): The ID of the user who liked the vacation.
            vacation_id (int): The ID of the vacation that was liked.

        Returns:
            dict: A success message if the like was recorded.
            None: If the like already exists or a foreign key constraint is violated.
        """
        with Like.get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            try:
                sql = "INSERT INTO likes (user_id, vacation_id) VALUES (?, ?)"
                cursor.execute(sql, (user_id, vacation_id))
                connection.commit()
                cursor.close()
                return {'message': f"User {user_id} liked Vacation {vacation_id} successfully."}
            except sqlite3.IntegrityError as e:
                cursor.close()
                if "UNIQUE constraint failed" in str(e):
                    return {'error': 'User has already liked this vacation.'}
                elif "FOREIGN KEY constraint failed" in str(e):
                    return {'error': 'Invalid User ID or Vacation ID.'}
                else:
                    return {'error': f"Database error: {e}"}
            except Exception as e:
                cursor.close()
                return {'error': f"An unexpected error occurred: {e}"}

    @staticmethod
    def delete(user_id: int, vacation_id: int) -> dict | None:
        """
        Removes a 'like' (unlikes) for a vacation by a user.

        Args:
            user_id (int): The ID of the user.
            vacation_id (int): The ID of the vacation.

        Returns:
            dict: A success message if the like was removed.
            None: If the like was not found.
        """
        with Like.get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            sql = "DELETE FROM likes WHERE user_id = ? AND vacation_id = ?"
            cursor.execute(sql, (user_id, vacation_id))
            connection.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            if rows_affected > 0:
                return {'message': f"User {user_id} unliked Vacation {vacation_id} successfully."}
            return {'error': 'Like not found.'}
    