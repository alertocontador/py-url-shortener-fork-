import os
import pymysql
from pymysql.cursors import DictCursor

# MySQL database configuration
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', '3306')),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'mysql'),
    'database': os.getenv('MYSQL_DATABASE', 'mysql'),
    'charset': 'utf8mb4',
    'cursorclass': DictCursor,
    'autocommit': False,
}

print(MYSQL_CONFIG)

def get_mysql_connection():
    """Get MySQL database connection"""
    try:
        connection = pymysql.connect(**MYSQL_CONFIG)
        return connection
    except Exception as error:
        print(f"Error connecting to MySQL: {error}")
        return None

async def connect_mysql():
    """Test MySQL connection"""
    try:
        connection = get_mysql_connection()
        if connection:
            connection.close()
            print("Connected to MySQL database")
            return True
        return False
    except Exception as error:
        print(f"MySQL connection failed: {error}")
        return False

