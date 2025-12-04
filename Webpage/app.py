from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
import paho.mqtt.client as mqtt
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="falldetectDatabase",
    user="postgres",
    password="123qwe"
)
cursor = conn.cursor()

def on_message(client, userdata, msg):
    cursor = userdata["cursor"]
    conn = userdata["conn"]
    topic = msg.topic
    payload = msg.payload.decode()
    cursor.execute(
        "INSERT INTO sensor_data (topic, payload) VALUES (%s, %s)",
        (topic, payload)
    )
    conn.commit()

def mqtt_runner(db_cursor, db_conn):
    client = mqtt.Client()
    client.on_message() = on_message
    client.connect("192.168.68.64")
    client.user_data_set({"cursor": db_cursor, "conn": db_conn})
    client.subscribe("fallband/battery")
    client.subscribe("fallband/pulse")
    client.subscribe("fallband/temp")
    client.subscribe("fallband/fall")
    client.loop_start()
mqtt_runner(cursor, conn)

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