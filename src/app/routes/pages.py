import flask as Flask
import flask_login as FlaskLogin
from .. import models as Models
import datetime as DateTime
from ..tools import beautify_datetime

def obtain_personalized_tasks(user) -> dict:
    tasks_query = Models.tasks.Task.query.all()
    dt_now = DateTime.datetime.now()
    tasks_list = list(map(lambda task: {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "creator": task.creator,
            "creator_display": Models.users.User.query.get(task.creator).name,
            "deadline": task.deadline,
            "deadline_display": beautify_datetime(task.deadline, dt_now),
            "is_complete": task.is_complete,
            "completed_on": task.completed_on,
            "completed_on_display": beautify_datetime(task.completed_on, dt_now),
            "claimed_by": task.claimed_by
        }, reversed(tasks_query)))
    return {
        "future_claimed": list(filter(lambda task: (
            task.get("deadline") > dt_now and
            task.get("claimed_by") is user.id and
            not task.get("is_complete")
            ), tasks_list)),
        "future_unclaimed": list(filter(lambda task: (
            task.get("deadline") > dt_now and
            task.get("claimed_by") is None and
            not task.get("is_complete")
            ), tasks_list)),
        "claimed_complete": list(filter(lambda task: (
            task.get("claimed_by") is user.id and
            task.get("is_complete")
            ), tasks_list)),
        "claimed_incomplete": list(filter(lambda task: (
            task.get("deadline") < dt_now and
            task.get("claimed_by") is user.id and
            not task.get("is_complete")
            ), tasks_list)),
    }

def register_routes(app, database, bcrypt):
    @app.route('/')
    def route_index():
        if not FlaskLogin.current_user.is_authenticated:
            return Flask.redirect('/signin')
        tasks = obtain_personalized_tasks(FlaskLogin.current_user)
        return Flask.render_template('pages/dashboard.html', tasks = tasks)

    @app.route('/history')
    def route_history():
        if not FlaskLogin.current_user.is_authenticated:
            return Flask.redirect('/signin')
        tasks = obtain_personalized_tasks(FlaskLogin.current_user)
        return Flask.render_template('pages/history.html', tasks = tasks)
    
    @app.route('/create')
    def route_create():
        if not FlaskLogin.current_user.is_authenticated:
            return Flask.redirect('/signin')
        return Flask.render_template('pages/createtask.html')

    @app.route('/signin')
    def route_signin():
        if FlaskLogin.current_user.is_authenticated:
            return Flask.redirect('/')
        return Flask.render_template('pages/signin.html')
    
    @app.route('/signup')
    def route_signup():
        if FlaskLogin.current_user.is_authenticated:
            return Flask.redirect('/')
        return Flask.render_template('pages/signup.html')

    @app.route('/signout')
    def route_signout():
        if not FlaskLogin.current_user.is_authenticated:
            return Flask.redirect('/signin')
        return Flask.redirect('/api/signout')