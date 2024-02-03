from dataclasses import dataclass
import mysql.connector

try:
    mysql_connector = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        database='ticketing'
    )
    print("Database connection roles: ", mysql_connector.is_connected())
except:
    print("Roles MySQL connection failed")

@dataclass
class Role:
    role_name: str
    role_desc: str
    role_id: str = None

    def __post_init__(self):
        if self.role_id is None:
           pass 

    def create_role(self):
        cursor = mysql_connector.cursor()
        new_role_name = self.role_name
        new_role_desc = self.role_desc
        query = "INSERT INTO role (roleID, name, description) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query)
        except:
            print("could not create role")


    def get_roles(self):
        cursor = mysql_connector.cursor()
        query = "SELECT * FROM ROLE"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result