import mysql.connector, atexit

try:
    mysql_connector = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        database='ticketing'
    )
    print(mysql_connector.is_connected())
except:
    print("MySQL connection failed.")

mysql_cursor = mysql_connector.cursor()
atexit.register(mysql_cursor.close)
atexit.register(mysql_connector.close)
