from .db import *
class Questions():
    def __init__(self):
        self.database = Db()
        self.db_cursor = self.database.db_cursor
        # Creating a connection to the database when initialising the class

    def getSubjects(self):
        self.db_cursor.execute("SELECT * FROM subjects")
        result = self.db_cursor.fetchall()
        return result

    def getTopics(self):
        self.db_cursor.execute("SELECT * FROM topics")
        result = self.db_cursor.fetchall()
        return result

    def getQuestions(self):
        self.db_cursor.execute("SELECT question, choice_a, choice_b, choice_c, choice_d FROM questions")
        result = self.db_cursor.fetchall()
        return result