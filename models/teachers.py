from models.user import *
from models.classes import *
from models.db import *

class Teacher(User): 
# Teacher inherits from user
    def __init__(self):
        super().__init__()