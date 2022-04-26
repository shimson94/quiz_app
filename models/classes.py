from flask import session
import string, random
from models.db import *

class Classes():
    
    def __init__(self):
        self.database = Db()
        self.db_cursor = self.database.db_cursor
        # Creating a connection to the database when initialising the class

    def setClassName(self, class_name): 
        self.class_name = class_name

    def setClassToken(self, class_token): 
        self.class_token = class_token

    def getClassName(self):
        return self.class_name

    def getClassToken(self):
        return self.class_token

    def generateClassToken(self):
        characters = list(string.ascii_letters + string.digits + "!@#$%^&*()") 
        # List of all possible characters available for token
        token = [] 
        # Create an empty array to add characters into
        for i in range(5):
            token.append(random.choice(characters)) 
            # Append 5 random characters 1 at a time to token
        random.shuffle(token) 
        # Randomly shuffle the order of the 5 characters
        self.setClassToken(''.join(token)) 
        # Use join to make array into one easily readable string

    def createClass(self):
        self.generateClassToken() 
        # Class token must be generated for the new class being created
        self.db_cursor.execute(f"INSERT INTO classes (class_name, class_token, teacher) VALUES ('{self.class_name}', '{self.class_token}', '{session['userdata'][1]}' )")
        # Insert class name, token and teacher name into classes table in database
        self.database.conn.commit()
        self.database.conn.close()
        # Commit and close database after every insert
    
    def joinClass(self):
        self.db_cursor.execute(f"SELECT class_id, class_token FROM classes WHERE class_token = '{self.class_token}'")
        #  Find the class corresponding to user input of class token
        result = self.db_cursor.fetchone()
        if result:
        # If there is a class with the same class token as the user entered
            self.db_cursor.execute(f"SELECT COUNT(*) FROM usersInClass WHERE student = {session['userdata'][1]} AND class_id = {result[0]}")
            student_exists = self.db_cursor.fetchone()
            if bool(student_exists[0]):
                # Check if they have already joined the class
                return False
                # Student can not join class
            else:
                self.db_cursor.execute(f"INSERT INTO usersInClass (student, class_id) VALUES ('{session['userdata'][1]}','{result[0]}')")
                # Insert student name and the id of the class they joined into usersInClass table in database
                self.database.conn.commit()
                self.database.conn.close()
                # Commit and close database after every insert
                return True
                # Student has joined class
        else:
            return False
            # Student can not join class

    def getClasses(self):
        if session['userdata'][2] == "Teacher": 
        # If user in session is a teacher
            self.db_cursor.execute(f"SELECT * FROM classes WHERE teacher = '{session['userdata'][1]}' ORDER BY class_name")
            # Able to see only classes that they have made
        elif session['userdata'][2] == "Admin": 
        # If user in session is the admin (me)
            self.db_cursor.execute(f"SELECT * FROM classes ORDER BY class_name") 
            # Able to see all information for classes table
        else: 
        # If user in session is a student
            self.db_cursor.execute(
            f"""SELECT usersInClass.class_id, classes.class_name, users.last_name, classes.class_token FROM usersInClass
            JOIN
            classes ON usersInClass.class_id = classes.class_id
            JOIN
            users ON classes.teacher = users.user_id
            WHERE usersInClass.student = '{session['userdata'][1]}'""")
            # Only able to see certain information from classes that they have joined

        result = self.db_cursor.fetchall()
        self.database.conn.commit()
        self.database.conn.close()
        return result