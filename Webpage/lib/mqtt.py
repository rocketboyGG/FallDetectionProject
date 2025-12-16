import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    cursor = userdata["cursor"]
    conn = userdata["conn"]
    topic = msg.topic
    payload = msg.payload.decode()
    if "fallband/fall" in topic:
        client.publish("vibration/activate", "Activate")
    cursor.execute(
        "INSERT INTO sensor_data (topic, payload) VALUES (%s, %s)",
        (topic, payload)
    )
    conn.commit()

class MQTT:
    def __init__(self, db_cursor, db_conn):
        self.db_cursor = db_cursor
        self.db_conn = db_conn
        self.client = mqtt.Client()
        self.client.on_message = on_message
        self.client.connect("192.168.1.2")
        self.client.user_data_set({"cursor": self.db_cursor, "conn": self.db_conn})
        self.client.subscribe("fallband/battery")
        self.client.subscribe("fallband/pulse")
        self.client.subscribe("fallband/fall")
        self.client.subscribe("vibration/battery")
        self.client.loop_start()
    
    def cleanup_mqtt(self):
        """Stops the MQTT loop and disconnects on exit."""
        if self.client:
            print("Stopping MQTT client...")
            self.client.loop_stop()
            self.client.disconnect()



