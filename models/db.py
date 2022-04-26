import sqlite3
class Db:

    db_name = "quiz.db"
    # Create a database named quiz.db

    def __init__(self):
        self.conn = sqlite3.connect(self.db_name) 
        # Connection to database
        self.db_cursor = self.conn.cursor() 
        # Create a database cursor
        # Call the methods to create the tables in the database
        self.createUserTable()
        self.createClassTable()
        self.createUsersInClassTable()
        self.createSubjectsTable()
        self.createTopicsTable()
        self.createQuestionsTable()
        self.createQuizTable()
        self.createQuizQuestionsTable()
        self.createQuizAnswerTable()

    def createUserTable(self):
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS users
        (user_id integer PRIMARY KEY AUTOINCREMENT,
        email text,
        first_name text,
        last_name text,
        password text,
        user_type text)
        """)
    
    def createClassTable(self):
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS classes
        (class_id integer PRIMARY KEY AUTOINCREMENT,
        class_name text,
        class_token text,
        teacher text,
        FOREIGN KEY (teacher) REFERENCES users(user_id))
        """)
    
    def createUsersInClassTable(self):
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS usersInClass
        (user_in_class_id integer PRIMARY KEY AUTOINCREMENT,
        student text,
        class_id integer,
        FOREIGN KEY (student) REFERENCES users(user_id)
        FOREIGN KEY (class_id) REFERENCES classes(class_id)
        )"""
        )
    
    def createSubjectsTable(self):
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS subjects
        (subject_id integer PRIMARY KEY AUTOINCREMENT,
        subject_name text
        )""")

    def createTopicsTable(self):
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS topics
        (topic_id integer PRIMARY KEY AUTOINCREMENT,
        topic_name text,
        subject_id integer,
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )""")

    def createQuestionsTable(self):
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS questions
        (question_id integer PRIMARY KEY AUTOINCREMENT,
        topic_id text,
        question text,
        choice_a text,
        choice_b text,
        choice_c text,
        choice_d text,
        answer text,
        class_id integer,
        score integer,
        difficulty text,
        FOREIGN KEY (class_id) REFERENCES classes(class_id)
        FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
        )""")

    def createQuizTable(self):
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS quizzes
        (quiz_id integer PRIMARY KEY AUTOINCREMENT,
        user_id integer,
        class_id integer,
        type text,
        total_marks integer,
        score integer,
        FOREIGN KEY (class_id) REFERENCES classes(class_id)
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        )""")

    def createQuizQuestionsTable(self):
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS quizQuestions
        (quiz_question_id integer PRIMARY KEY AUTOINCREMENT,
        question_id integer,
        quiz_id integer,
        FOREIGN KEY (question_id) REFERENCES questions(question_id)
        FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id)
        )""")

    def createQuizAnswerTable(self):
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS quizAnswers
        (quiz_answer_id integer PRIMARY KEY AUTOINCREMENT,
        quiz_question_id integer,
        user_answer text,
        correct bool,
        score integer,
        user_id integer,
        FOREIGN KEY (quiz_question_id) REFERENCES quizQuestions(quiz_question_id)
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        )""")