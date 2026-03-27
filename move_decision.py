import json
import time
from datetime import datetime

import mysql.connector
import roslibpy



ROSBRIDGE_HOST = 'localhost'   
ROSBRIDGE_PORT = 9090


DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '0000',   
    'database': 'lidar_db'
}

INSERT_INTERVAL_SEC = 2.0


class MoveDecisionWithDB:
    def __init__(self):
        self.client = roslibpy.Ros(host=ROSBRIDGE_HOST, port=ROSBRIDGE_PORT)
        self.client.run()

        if not self.client.is_connected:
            raise RuntimeError('ROS bridge 연결 실패')

        print('Connected to ROS bridge.')

        self.cmd_vel_pub = roslibpy.Topic(
            self.client,
            '/turtle1/cmd_vel',
            'geometry_msgs/Twist'
        )

        self.scan_sub = roslibpy.Topic(
            self.client,
            '/scan',
            'sensor_msgs/LaserScan'
        )

        self.db_conn = mysql.connector.connect(**DB_CONFIG)
        self.db_cursor = self.db_conn.cursor()
        print('Connected to MySQL.')

        self.last_insert_time = 0.0

    def decide_action(self, front_dist):
        if front_dist < 1.0:
            return 0.0, 1.0, 'TURN LEFT'
        elif front_dist < 2.0:
            return 0.5, -0.5, 'TURN RIGHT'
        else:
            return 1.0, 0.0, 'FORWARD'

    def publish_cmd(self, linear_x, angular_z):
        msg = roslibpy.Message({
            'linear': {
                'x': linear_x,
                'y': 0.0,
                'z': 0.0
            },
            'angular': {
                'x': 0.0,
                'y': 0.0,
                'z': angular_z
            }
        })
        self.cmd_vel_pub.publish(msg)

    def save_to_db(self, ranges, action):
        now = datetime.now()

        sql = """
        INSERT INTO lidardata (ranges, `when`, action)
        VALUES (%s, %s, %s)
        """

        values = (
            json.dumps(ranges),
            now.strftime('%Y-%m-%d %H:%M:%S'),
            action
        )

        self.db_cursor.execute(sql, values)
        self.db_conn.commit()

        print(f'[DB] saved at {now.strftime("%H:%M:%S")} / action={action}')

    def callback(self, message):
        ranges = message.get('ranges', [])

        if not ranges:
            print('ranges is empty')
            return

        front_dist = ranges[0]

        linear_x, angular_z, action = self.decide_action(front_dist)
        self.publish_cmd(linear_x, angular_z)

        print(f'front={front_dist:.2f} -> {action}')

        current_time = time.time()
        if current_time - self.last_insert_time >= INSERT_INTERVAL_SEC:
            self.save_to_db(ranges, action)
            self.last_insert_time = current_time

    def start(self):
        self.scan_sub.subscribe(self.callback)
        print('Subscribed to /scan')

        try:
            while self.client.is_connected:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print('\nShutting down...')
        finally:
            self.cleanup()

    def cleanup(self):
        try:
            self.scan_sub.unsubscribe()
        except Exception:
            pass

        try:
            self.cmd_vel_pub.unadvertise()
        except Exception:
            pass

        try:
            self.db_cursor.close()
            self.db_conn.close()
        except Exception:
            pass

        try:
            self.client.terminate()
        except Exception:
            pass

        print('Cleaned up.')


if __name__ == '__main__':
    app = MoveDecisionWithDB()
    app.start()