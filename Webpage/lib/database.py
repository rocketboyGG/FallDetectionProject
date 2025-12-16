import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="falldetectdatabase",
            user="adminuser",
            password="qwe123"
        )
        self.cursor = self.conn.cursor()
        self.last_fall = None

    def create_database(self):
        sql = """ 
            CREATE TABLE sensor_data (
                id SERIAL PRIMARY KEY,
                topic TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """
        self.cursor.execute(sql)
        self.conn.commit()

    def fetch_data_from_db(self):
        sql1 = """
            SELECT payload
            FROM sensor_data
            WHERE topic = 'fallband/pulse'
            ORDER BY created_at DESC
            LIMIT 1;
        """
        self.cursor.execute(sql1)
        pulse_data = self.cursor.fetchone()
        pulse = "0"
        if pulse_data is not None:
            pulse = pulse_data[0]

        sql2 = """
            SELECT payload
            FROM sensor_data
            WHERE topic = 'fallband/battery'
            ORDER BY created_at DESC
            LIMIT 1;
        """
        self.cursor.execute(sql2)
        battery_data_fallband = self.cursor.fetchone()
        battery_fallband = "0"
        if battery_data_fallband is not None:
            battery_fallband = battery_data_fallband[0]

        sql3 = """
            SELECT created_at
            FROM sensor_data
            WHERE topic = 'fallband/fall'
            ORDER BY created_at DESC
            LIMIT 1;
        """
        self.cursor.execute(sql3)
        fall_registered = self.cursor.fetchone()
        fall = "no"
        if fall_registered is not None:
            fall = fall_registered[0]

        sql4 = """
            SELECT payload
            FROM sensor_data
            WHERE topic = 'vibration/battery'
            ORDER BY created_at DESC
            LIMIT 1;
        """
        self.cursor.execute(sql4)
        battery_data_vibration = self.cursor.fetchone()
        battery_vibration = "0"
        if battery_data_vibration is not None:
            battery_vibration = battery_data_vibration[0]

        if fall_registered != self.last_fall:
            print("!!!!!FALLLLLLL!!!!!!!")
            self.last_fall = fall_registered
            return (pulse, battery_fallband, fall, battery_vibration)

        return (pulse, battery_fallband, "no", battery_vibration)
