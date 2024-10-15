import os
from typing import List, Dict, Any, Optional, Union
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'library_user'),
            password=os.getenv('DB_PASSWORD', 'password123'),
            database=os.getenv('DB_NAME', 'library_management_system'),
            port=int(os.getenv('DB_PORT', '3306'))
        )
        self.cursor = self.connection.cursor(dictionary=True)  # type: mysql.connector.cursor.MySQLCursor

    def execute_query(self, query: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> Union[List[Dict[str, Any]], bool]:
        try:
            self.cursor.execute(query, params or ())
            
            if query.strip().upper().startswith(('SELECT', 'SHOW')):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return True
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            self.connection.rollback()
            return False

    def close(self) -> None:
        try:
            self.cursor.close()
            self.connection.close()
        except mysql.connector.Error as err:
            print(f"Error closing database connection: {err}")

    def __enter__(self) -> 'Database':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

def test_connection():
    try:
        with Database() as db:
            result = db.execute_query("SHOW TABLES")
            if isinstance(result, list):
                print("Tables in the database:")
                for table in result:
                    print(table['Tables_in_' + os.getenv('DB_NAME', 'library_management_system')])
            else:
                print("Failed to retrieve tables.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    test_connection()