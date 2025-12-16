from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
from lib.mqtt import MQTT
from lib.database import Database
import json
import atexit
import sys
import nmap

db = Database()
mqtt = MQTT(db.cursor, db.conn)

atexit.register(mqtt.cleanup_mqtt)

def scan_network_for_hosts(network_range):
    print(f"[*] Starting Nmap host discovery scan on {network_range}...")

    # Initialize the Nmap PortScanner object
    nm = nmap.PortScanner()

    # Run the scan with the -sn argument (ping sweep/host discovery)
    # The result is stored internally in the nm object
    nm.scan(hosts=network_range, arguments='-sn')

    active_hosts = []
    # Iterate over all hosts that Nmap scanned
    for host in nm.all_hosts():
        # Check if the host's status is 'up'
        if nm[host]['status']['state'] == 'up':
            active_hosts.append(host)
            # Optional: Get hostname if available
            # try:
            #     hostname = nm[host].hostname()
            #     print(f"Host: {host} ({hostname}) is UP")
            # except:
            #     print(f"Host: {host} is UP (Hostname not found)")

    return active_hosts

app = Flask(__name__)
app.secret_key = "secret" #Skal ændres senere, just for developent/debugging

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id):
        self.id = id

TEMP_USERNAME = "admin"
TEMP_PASSWORD = "1234"

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/hosts")
@login_required
def hosts():
    live_hosts_list = scan_network_for_hosts("192.168.1.0/24")
    return render_template("hosts.html", hosts_list=live_hosts_list)

@app.route('/data')
def api_data():
    """API endpoint to return the visualization data as JSON (for JS updates)."""
    data = db.fetch_data_from_db()
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
    app.run(host="0.0.0.0", debug=TrueActivate)