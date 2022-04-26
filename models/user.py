from models.db import *

class User:
    def __init__(self):
        self.database = Db()
        self.db_cursor = self.database.db_cursor
        # Creating a connection to the database when initialising the class

    def setUserData(self, userData):
    # Set user data from the details submitted in the registration form
        self.email = userData.get("email")
        self.password = userData.get("password")      
        if userData.get("form") == "registration":    
            self.first_name = userData.get("first_name")
            self.last_name = userData.get("last_name")  
            self.user_type = userData.get("user_type")  

    def getUsers(self, email=""):
    # Get necessary user information about a user when their email is inputted
        if email != "": # If inputted email is not blank
            self.db_cursor.execute(f"SELECT first_name, user_id, user_type FROM users WHERE email = '{email}'")
            result = self.db_cursor.fetchone()
            # Fetch information relating to that user
        else:
            self.db_cursor.execute("SELECT first_name, user_id, user_type FROM users")
            result = self.db_cursor.fetchall()
            # Fetch all relevant user information
        return result

    def register(self):
        self.db_cursor.execute(f"SELECT COUNT(*) FROM users WHERE email = '{self.email}'") 
        # Check how many users have registered with the same email
        result = self.db_cursor.fetchone()
        if result[0] == 0: 
        # If no other users have the same email
            self.db_cursor.execute(
                f"""INSERT INTO users (first_name, last_name, email, password, user_type)
                VALUES ('{self.first_name}', '{self.last_name}', '{self.email}', '{self.password}','{self.user_type}')""")
            # Insert registration details into the user table
            self.database.conn.commit()
            self.database.conn.close()
            return True
            # Successful registration
        else:
           return False
           # Unsuccessful registration

    def login(self):
        self.db_cursor.execute(f"SELECT COUNT(*) FROM users WHERE email = '{self.email}' AND password='{self.password}'")
        details = self.db_cursor.fetchone()
        # Select how many users exist with the same email and password as inputted in the login form
        if details[0] == 1: 
        # If there is a user
            return True
            # Login is successful
        else:
            return False
            # Login is unsuccessful