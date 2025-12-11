from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
import paho.mqtt.client as mqtt
import psycopg2
import json

conn = psycopg2.connect(
    host="localhost",
    database="falldetectDatabase",
    user="postgres",
    password="GGcakerocket87GG"
)
cursor = conn.cursor()

def create_test_database(cursor, conn):
    sql = """ 
        CREATE TABLE sensor_data (
            id SERIAL PRIMARY KEY,
            topic TEXT NOT NULL,
            payload TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """
    cursor.execute(sql)
    conn.commit()

def create_test_data(cursor, conn):
    cursor.execute(
        "INSERT INTO sensor_data (topic, payload) VALUES (%s, %s)",
        ("fallband/fall", "FALL")
    )
    cursor.execute(
        "INSERT INTO sensor_data (topic, payload) VALUES (%s, %s)",
        ("fallband/pulse", "23")
    )
    cursor.execute(
        "INSERT INTO sensor_data (topic, payload) VALUES (%s, %s)",
        ("fallband/battery", "46")
    )
    conn.commit()

create_test_data(cursor, conn)

def print_table(cursor, conn):
    sql1 = """
        SELECT payload
        FROM sensor_data
        WHERE topic = 'fallband/pulse'
        ORDER BY created_at DESC
        LIMIT 1;
    """
    cursor.execute(sql1)
    pulse_data = cursor.fetchone()
    print(pulse_data)

print_table(cursor, conn)


def on_message(client, userdata, msg):
    cursor = userdata["cursor"]
    conn = userdata["conn"]
    topic = msg.topic
    payload = msg.payload.decode()
    if "fallband/fall" in topic:
        client.publish(b"fallband/vibrator", "FALL")
    cursor.execute(
        "INSERT INTO sensor_data (topic, payload) VALUES (%s, %s)",
        (topic, payload)
    )
    conn.commit()

def mqtt_runner(db_cursor, db_conn):
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("192.168.68.64")
    client.user_data_set({"cursor": db_cursor, "conn": db_conn})
    client.subscribe("fallband/battery")
    client.subscribe("fallband/pulse")
    client.subscribe("fallband/fall")
    client.loop_start()
#mqtt_runner(cursor, conn)

app = Flask(__name__)
app.secret_key = "secret" #Skal ændres senere, just for developent/debugging

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

last_fall = None

class User(UserMixin):
    def __init__(self, id):
        self.id = id

TEMP_USERNAME = "123"
TEMP_PASSWORD = "123"

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def fetch_data_from_db():
    sql1 = """
        SELECT payload
        FROM sensor_data
        WHERE topic = 'fallband/pulse'
        ORDER BY created_at DESC
        LIMIT 1;
    """
    cursor.execute(sql1)
    pulse_data = cursor.fetchone()

    sql2 = """
        SELECT payload
        FROM sensor_data
        WHERE topic = 'fallband/battery'
        ORDER BY created_at DESC
        LIMIT 1;
    """
    cursor.execute(sql2)
    battery_data = cursor.fetchone()

    global last_fall
    sql3 = """
        SELECT created_at
        FROM sensor_data
        WHERE topic = 'fallband/fall'
        ORDER BY created_at DESC
        LIMIT 1;
    """
    cursor.execute(sql3)
    fall_registered = cursor.fetchone()

    if fall_registered != last_fall:
        print("!!!!!FALLLLLLL!!!!!!!")
        last_fall = fall_registered
        return (pulse_data[0], battery_data[0], fall_registered[0])

    return (pulse_data[0], battery_data[0], "no")


@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route('/data')
def api_data():
    """API endpoint to return the visualization data as JSON (for JS updates)."""
    data = fetch_data_from_db()
    print(data)
    return jsonify(data)

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