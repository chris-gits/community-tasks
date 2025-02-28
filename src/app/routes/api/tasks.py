import flask as Flask
import flask_login as FlaskLogin
import datetime as DateTime
from ... import models as Models

# id = database.Column(database.Integer, primary_key = True)
# title = database.Column(database.String, nullable = False)
# description = database.Column(database.String, nullable = False)
# creator = database.Column(database.ForeignKey("users.id"), nullable = False)
# deadline = database.Column(database.DateTime, nullable = True)
# is_complete = database.Column(database.Boolean, nullable = False)
# claimed_by = database.Column(database.ForeignKey("users.id"), nullable = True)

from datetime import datetime, timedelta

def register_routes(app, database, bcrypt):
    @app.route("/api/create_task", methods=["POST"])
    def route_api_create_task():
        if not FlaskLogin.current_user.is_authenticated:
            return Flask.redirect('/signin')
        request = Flask.request
        form = request.form
        try:
            new_task = Models.tasks.Task(
                title = form.get("title"),
                description = form.get("description"),
                creator = FlaskLogin.current_user.id,
                deadline = DateTime.datetime.fromisoformat(form.get("deadline"))
            )
            
            database.session.add(new_task)
            database.session.commit()
            Flask.flash("Successfully created task.", category="Success")
            return Flask.redirect("/")
        except:
            Flask.flash("Could not create task.", category="Danger")
    
    @app.route("/api/claim_task", methods=["POST"])
    def route_api_claim_task():
        if not FlaskLogin.current_user.is_authenticated:
            return Flask.redirect('/signin')
        request = Flask.request
        form = request.form
        try:
            task = Models.tasks.Task.query.get(form.get("id"))
            if (task.deadline > DateTime.datetime.now()) and (task.claimed_by is None) and (not task.is_complete):
                task.claimed_by = FlaskLogin.current_user.id
                database.session.commit()
                Flask.flash("Successfully claimed task.", category="Success")
        except Exception as err:
            Flask.flash("Could not claim task." + str(err), category="Danger")
        return Flask.redirect("/")
            
    @app.route("/api/drop_task", methods=["POST"])
    def route_api_drop_task():
        if not FlaskLogin.current_user.is_authenticated:
            return Flask.redirect('/signin')
        request = Flask.request
        form = request.form
        try:
            task = Models.tasks.Task.query.get(form.get("id"))
            if (task.deadline > DateTime.datetime.now() and
                    task.claimed_by is FlaskLogin.current_user.id and
                    not task.is_complete):
                task.claimed_by = None
                database.session.commit()
                Flask.flash("Successfully dropped task.", category="Success")
        except Exception as err:
            Flask.flash("Could not drop task." + str(err), category="Danger")
        return Flask.redirect("/")
        
    @app.route("/api/complete_task", methods=["POST"])
    def route_api_complete_task():
        if not FlaskLogin.current_user.is_authenticated:
            return Flask.redirect('/signin')
        request = Flask.request
        form = request.form
        try:
            task = Models.tasks.Task.query.get(form.get("id"))
            if (task.deadline > DateTime.datetime.now() and
                    task.claimed_by is FlaskLogin.current_user.id and
                    not task.is_complete):
                task.is_complete = True
                task.completed_on = datetime.now()
                database.session.commit()
                Flask.flash("Successfully completed task.", category="Success")
        except Exception as err:
            Flask.flash("Could not complete task." + str(err), category="Danger")
        return Flask.redirect("/")