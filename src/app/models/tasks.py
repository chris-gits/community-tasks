from .. import database
from . import users

class Task(database.Model):
    __tablename__ = "tasks"
    
    id = database.Column(database.Integer, primary_key = True)
    title = database.Column(database.String, nullable = False, default = 'Untitled Task')
    description = database.Column(database.String, nullable = False, default = 'Incomplete description.')
    creator = database.Column(database.ForeignKey('users.id'), nullable = False)
    deadline = database.Column(database.DateTime, nullable = True)
    is_complete = database.Column(database.Boolean, nullable = False, default = False)
    completed_on = database.Column(database.DateTime, nullable = True, default = None)
    claimed_by = database.Column(database.ForeignKey('users.id'), nullable = True, default = None)