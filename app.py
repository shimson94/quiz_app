from crypt import methods
from readline import parse_and_bind
from flask import Flask, render_template, request, session, redirect, url_for
from models.questions import Questions
from models.quizzes import Quizzes
from models.user import *
from models.teachers import *
import re

app = Flask(__name__, template_folder = "templates")
app.secret_key = "Monkey" # Secret key required to store session data

@app.route("/") 
# Home page
def home():
    return render_template("home.html", title = "Quiz App Home")

def validate(formData):
    password = request.form.get("password") # Get password from registration form submission
    repeat_password = request.form.get("repeat_password") # Get repeat_password from registration form submission
    print(password)
    print(repeat_password)
    contains_number = bool(re.search('[0-9]',password))
    contains_lower = bool(re.search('[a-z]',password))
    contains_upper = bool(re.search('[A-Z]',password))
    contains_special_char = bool(re.search('[!$£@&#]',password))
    # Using regular expression for server side validation of password before registration is complete
    if len(password) < 6: 
    # Check if length of password is greater than 6
        return False
    else:
        if password == repeat_password and contains_number and contains_lower and contains_upper and contains_special_char: 
        # Check if password meets validation conditions
            return True
        else:
            return False

@app.route("/register", methods = ['POST', 'GET'])
# Webpage for registration
def register():
    if request.method == 'POST': 
    # If a post request has been made - i.e. form has been submitted
        if validate(request.form):
        # Check if password fulfills necessary requirements
            user = User()
            user.setUserData(request.form)
            # Calling setUserData method from user class to set registration details
            if user.register(): 
            # Register and insert details into database if possible (they haven't already registered before)
                return """<div class='alert alert-success'>Registered Successfully</div>
                <script>setTimeout(function(){window.location='/login';}, 2000);</script>"""
                # Alert to show successful registration and redirects user to login page
            else:
                return "<div class='alert alert-danger'>Email already exists</div>"
                # Alert to show unsuccessful registration as a user with the same email already exists
        else:
            return "<div class='alert alert-danger'>Password is not valid</div>"
            # Alert to show that the password didn't meet the validation requirements
    else:
        return render_template("register.html", title = "Register")

@app.route("/login", methods = ['POST','GET'])
# Webpage for login
def login():
    if request.method == 'POST':
        user = User() 
        user.setUserData(request.form)
        if user.login(): 
        # Login if details inputted are correct
            userdata = user.getUsers(request.form.get("email"))
            session['userdata'] = userdata 
            # Store user data in session to access user specific details later
            return """<div class='alert alert-success'>Successful login</div>
            <script>setTimeout(function(){window.location='/';}, 2000);</script>"""
            # Alert to show that login was successful and redirects you back to home page
        else:
            return "<div class='alert alert-danger'>Incorrect login details</div>"
            # Alert to show that incorrect login details were entered
    if 'userdata' in session: 
    # If user is already in session (didn't log out)
        return "<script>window.location='/';</script>"
        # Show home page instead of login page    
    return render_template("login.html", title = "Login")

@app.route("/create-class", methods = ['POST','GET'])
# Webpage for a teacher to create a class
def generateClass():
    class_obj = Classes()
    if request.method == 'POST':
        class_obj.setClassName(request.form.get('class_name')) 
        # Uses class name input from form to set class name
        class_obj.createClass() 
        # Creates a class
        token = class_obj.getClassToken() 
        # Creates a unique token for the class
        return ("<div class='alert alert-success'>You have created a class. The class token is: <strong>"+token+"""</strong></div>
        <script>setTimeout(function(){window.location='';}, 2000);</script>""")
        # Alert to show class has been successfully made and shows the token in bold.
    else:
        classes = class_obj.getClasses() 
        # Get classes that have already been made
        return render_template("createClass.html", title = "Create a Class", classes = classes)
        # Pass variable classes into createClass.html webpage

@app.route("/join-class", methods = ['POST','GET']) 
# Webpage for a student to join a class
def joinClass():
    if request.method == 'POST':
        class_obj = Classes()
        class_obj.setClassToken(request.form.get("class_token"))
        # Set class token to what has been inputted from join class form
        if class_obj.joinClass(): 
        # Join a student to a class if there token was correct
            return """<div class='alert alert-success'>You have joined the class.</div>
            <script>setTimeout(function(){window.location='';}, 2000);</script>"""
            # Alert to show class has been joined and refreshes current page
        else:
            return "<div class='alert alert-danger'>Invalid Token or you have already joined this class</div>"
            # Alert to show class has already been joined or invalid token was entered
    else:
        class_obj = Classes()
        classes = class_obj.getClasses()
        # Get all classes that the user is a part of
        return render_template("joinClass.html", title = "Join a Class", classes = classes)
        # Pass variable classes into joinClass.html webpage

@app.route('/generate-quiz', methods = ['POST','GET']) 
# Webpage for a student to create a quiz
def studentQuiz():
    questions = Questions()
    quiz = Quizzes()
    if request.method == 'POST':
        quiz_id = quiz.generateQuiz(request.form) 
        # Creates a quiz and returns the specific quiz id to access the quiz
        return f"<script>window.location='/take-quiz?quiz={quiz_id}';</script>" 
        # Redirects user to quiz
    else:
        listSubjects = questions.getSubjects() 
        # Call getSubjects() to show which subjects are available to select for a quiz
        return render_template("generateQuiz.html", title = "Create a Quiz", listSubjects = listSubjects) 
        # Pass listSubjects into generateQuiz.html webpage

@app.route('/take-quiz', methods = ['POST','GET']) 
# Webpage for a student to attempt the created quiz
def takeQuiz():
    questions = Quizzes()
    quiz_id = request.args.get("quiz")
    # quiz id taken from url
    if request.method == 'GET':
        listQuestions = questions.getQuizQuestions(quiz_id)
        # Pass quiz id get the questions to use in the quiz with that specific quiz id
        return render_template("takeQuiz.html", title = "Taking a quiz", listQuestions = listQuestions, quiz = quiz_id)
    else:
        if not questions.checkQuizMarked(request.form, quiz_id):
        # Check if quiz has already been attempted and marked
            total_score = questions.markQuiz(request.form, quiz_id)
            # markQuiz returns a message for a user's score
            score = str(total_score)
            id = str(quiz_id)
            # Cast total_score and quiz_id as strings so that they can be concatenated to the return message below
            # f string can't be used as javascript uses {} which interrupts f string
            return "<div class='alert alert-info'>"+score+"""</div>
            <script>setTimeout(function(){window.location='/quiz-result?quiz="""+id+"';}, 2000);</script>"
            # Alert to show user their score and redirects them to the quiz results page
        else:
            return f"<div class='alert alert-danger'>Quiz already attempted</div>"
            # Alert to show that the quiz can not be marked again as it has already been submitted

@app.route('/quiz-result', methods = ['GET'])
def quizResult():
    quiz_id = request.args.get("quiz")
    # quiz id taken from url
    quiz = Quizzes()
    results = quiz.quizResults(quiz_id)
    # Collects results from quiz to use in quiz results page
    return render_template("quizResult.html", title = "Quiz Results", results = results, q_map = {'a':6,'b':7,'c':8,'d':9})

@app.route('/logout')
# Allow user to logout
def logout():
   session.pop('userdata')
   # Removes user data from the session, logging the user out
   return redirect(url_for('home'))  
    
if __name__ == '__main__':
    app.run(debug = True, port = 8000)