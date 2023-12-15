from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error
import threading
import time
from adafruit_mpu6050 import MPU6050
import board
import busio

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': '192.168.8.161',  # MariaDB host
    'database': 'MCP',        # Database name
    'user': 'ned',            # Database username
    'password': 'ned'         # Database password
}
POST_INTERVAL = 60  # Interval in seconds
MACHINE_NAME = 'dusty'  # Machine name

# Initialize I2C bus and MPU6050
i2c = busio.I2C(board.SCL, board.SDA)
mpu = MPU6050(i2c)

def get_db_connection():
    """Create and return a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None

def write_to_database(measures):
    """Function to write each MPU6050 measure to the STATS_Machine table."""
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO STATS_Machine (timestamp, Major, Minor, Value, Machine, Notes)
                     VALUES (NOW(), %s, %s, %s, %s, %s)"""
            for key, value in measures.items():
                cursor.execute(sql, ('MPU', key, value, MACHINE_NAME, key))
            conn.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            conn.close()
    else:
        print("Failed to get database connection")

def get_mpu_stats():
    """Collect MPU6050 statistics."""
    return {
        "acceleration_x": mpu.acceleration[0],
        "acceleration_y": mpu.acceleration[1],
        "acceleration_z": mpu.acceleration[2],
        "gyro_x": mpu.gyro[0],
        "gyro_y": mpu.gyro[1],
        "gyro_z": mpu.gyro[2],
        "temperature": mpu.temperature
    }

def post_stats_periodically():
    """Function to post MPU6050 stats to the database periodically."""
    while True:
        measures = get_mpu_stats()
        write_to_database(measures)
        time.sleep(POST_INTERVAL)

@app.route('/', methods=['GET'])
def mpu_stats_endpoint():
    """Endpoint to manually get MPU6050 stats."""
    return jsonify(get_mpu_stats())

if __name__ == '__main__':
    threading.Thread(target=post_stats_periodically, daemon=True).start()
    app.run(host='0.0.0.0', port=5002)
