from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin

app = Flask(__name__)
app.secret_key = "secret" #Skal ændres senere, just for developent/debugging

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id):
        self.id = id

TEMP_USERNAME = "123"
TEMP_PASSWORD = "123"

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/home")
@login_required
def home():
    temp_list = [
        {"navn": "Navn 1", "t": "31", "p": "1", "status": "Good"},
        {"navn": "Rigtig langt navn !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", "t": "32", "p": "2", "status": "uhh"},
        {"navn": "Navn 3", "t": "33", "p": "3", "status": "Bad"},
    ]
    return render_template("home.html", temp_list=temp_list)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == TEMP_USERNAME and password == TEMP_PASSWORD:
            user = User(id=username)
            login_user(user)
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == ('__main__'):
    app.run(host="0.0.0.0", debug=True)