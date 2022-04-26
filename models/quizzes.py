from flask import session
from .db import *
class Quizzes():
    def __init__(self):
        self.database = Db()
        self.db_cursor = self.database.db_cursor
        # Creating a connection to the database when initialising the class

    def generateQuiz(self, data):
        # Create a quiz in DB
        user_id = session['userdata'][1]
        quiz_type = "student quiz"
        # Teacher quiz hasn't been developed yet so quiz_type is hard coded as 'student quiz'
        self.db_cursor.execute(f"INSERT INTO quizzes (user_id, type) VALUES ('{user_id}','{quiz_type}')")
        # Add a quiz to quizzes table in database
        quiz_id = self.db_cursor.lastrowid 
        # Quiz ID for the last quiz generated
        
        self.db_cursor.execute(
            f"""SELECT questions.question_id FROM questions
            JOIN
            topics ON topics.topic_id = questions.topic_id
            JOIN
            subjects ON topics.subject_id = subjects.subject_id
            WHERE subjects.subject_id = {data.get('subject')} LIMIT {data.get('questions')}""")
        results = self.db_cursor.fetchall()
        # Get the question as per the subject and number of questions
        
        for eachQuestion in results:
            self.db_cursor.execute(f"INSERT INTO quizQuestions (question_id, quiz_id) VALUES ('{eachQuestion[0]}','{quiz_id}')")
        # Combine Question ID with Quiz ID, insert into QuizQuestion
        
        self.database.conn.commit()
        self.database.conn.close()

        return quiz_id

    def getQuizQuestions(self, quiz_id):
        self.db_cursor.execute(f"""SELECT quizzes.quiz_id, quizQuestions.question_id, quizQuestions.quiz_question_id,
        questions.question, questions.choice_a, questions.choice_b, questions.choice_c, questions.choice_d
        FROM quizzes
        JOIN
        quizQuestions ON quizQuestions.quiz_id = quizzes.quiz_id
        JOIN
        questions ON questions.question_id = quizQuestions.question_id
        WHERE quizzes.quiz_id = {quiz_id} AND (quizzes.user_id = {session['userdata'][1]} OR quizzes.type = 'teacher quiz')""")
        results = self.db_cursor.fetchall()
        # Gets all necessary information required to generate a quiz (question and the 4 choices) used in takeQuiz.html
        return results

    def checkQuizMarked(self, formData, quiz_id):
        noQuestions = len(formData.getlist("questions"))
        # Check how many questions there are in the quiz
        self.db_cursor.execute(
            f"""SELECT COUNT(*) FROM quizQuestions
            JOIN quizAnswers ON quizQuestions.quiz_question_id = quizAnswers.quiz_question_id
            WHERE quizQuestions.quiz_id = {quiz_id} AND quizAnswers.user_id = {session['userdata'][1]}""")
        result = self.db_cursor.fetchone()
        # Find how many questions were added to the quiz with the same quiz id that only the user who created the quiz can access
        if result[0] == noQuestions:
        # If the number of questions in the quiz form is the same as questions stored in quizQuestions table
            return True
            # Quiz already marked
        else:
            return False
            # Quiz has not been marked yet

    def markQuiz(self, formData, quiz_id):
        for question_id in formData.getlist("questions"):
        # For each question
            userAnswer = formData.get("answer["+question_id+"]")
            quiz_question_id = formData.get("quiz_question_id["+question_id+"]")
            # User's answer and quiz_question_id is taken from takeQuiz.html form 
            self.db_cursor.execute(f"SELECT answer, score FROM questions WHERE question_id = {question_id}")
            results = self.db_cursor.fetchone()
            # Select the answer and how many marks each question is worth from questions table
            correct_answer = False
            if userAnswer == results[0]:
            # If user answer is same as actual answer
                correct_answer = True
                # User scores a mark
            else:
                correct_answer = False
                # User's mark is unchanged
            question_score = results[1]
            # How many marks question is worth
            
            self.db_cursor.execute(
                f"""INSERT INTO quizAnswers (quiz_question_id, user_answer, correct, score, user_id)
                VALUES ({quiz_question_id},'{userAnswer}',{correct_answer},{question_score},{session['userdata'][1]})""")
            # Insert relevant information into quizAnswers table 
            
            self.db_cursor.execute(
                f"""SELECT SUM(quizAnswers.correct) AS total_correct FROM quizQuestions
                JOIN quizAnswers ON quizQuestions.quiz_question_id = quizAnswers.quiz_question_id
                WHERE quizQuestions.quiz_id = {quiz_id} AND quizAnswers.user_id = {session['userdata'][1]}""")
            marks = self.db_cursor.fetchone()
            # Stores total marks user scores on quiz
            
            self.db_cursor.execute(
                f"""SELECT SUM(quizAnswers.score) AS total_questions FROM quizQuestions
                JOIN quizAnswers ON quizQuestions.quiz_question_id = quizAnswers.quiz_question_id
                WHERE quizQuestions.quiz_id = {quiz_id} AND quizAnswers.user_id = {session['userdata'][1]}""")
            total_marks = self.db_cursor.fetchone()
            # Stores total marks the quiz was out of
            
        self.db_cursor.execute(f"UPDATE quizzes SET score = {marks[0]}, total_marks = {total_marks[0]} WHERE quiz_id = {quiz_id}")
        # When quizzes table was initialised, user score and total_marks were empty. This is now updated using the above information
        self.database.conn.commit()
        self.database.conn.close()
        
        return "You scored " + str(marks[0])+ " marks out of " + str(total_marks[0])

    def quizResults(self, quiz_id):
        self.db_cursor.execute(
            f"""SELECT quizzes.quiz_id, quizzes.total_marks, quizzes.score, quizQuestions.question_id, questions.question, questions.answer,
            questions.choice_a, questions.choice_b, questions.choice_c, questions.choice_d, quizAnswers.user_answer, quizAnswers.score
            FROM quizzes
            JOIN
            quizQuestions ON quizzes.quiz_id = quizQuestions.quiz_id
            JOIN
            questions ON quizQuestions.question_id = questions.question_id
            JOIN
            quizAnswers ON quizQuestions.quiz_question_id = quizAnswers.quiz_question_id
            WHERE quizQuestions.quiz_id = {quiz_id} AND quizAnswers.user_id = {session['userdata'][1]}""")

        result = self.db_cursor.fetchall()
        # All necessary information taken to display quiz results
        return result