import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import numpy as np

class LidarPublisher(Node):
    def __init__(self):
        super().__init__('lidar_publisher_node')
        # 'scan' 이라는 이름의 토픽으로 데이터를 보냅니다.
        self.publisher_ = self.create_publisher(LaserScan, 'scan', 10)
        
        # 2초(2.0)마다 timer_callback 함수를 실행합니다.
        self.timer = self.create_timer(2.0, self.timer_callback)
        self.get_logger().info('Lidar Mock Publisher has started (2.0s interval)')

    def timer_callback(self):
        msg = LaserScan()
        
        # 헤더 설정
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'laser_frame'
        
        # LDS-02 센서 사양 시뮬레이션
        msg.angle_min = 0.0
        msg.angle_max = 2 * np.pi  # 360도
        msg.angle_increment = np.pi / 180.0  # 1도 간격
        msg.range_min = 0.12
        msg.range_max = 3.5
        
        # 360개의 랜덤 거리 데이터 생성 (0.12m ~ 3.5m 사이)
        msg.ranges = np.random.uniform(msg.range_min, msg.range_max, 360).tolist()
        
        # 토픽 발행
        self.publisher_.publish(msg)
        self.get_logger().info('Published random scan data to /scan')

def main(args=None):
    rclpy.init(args=args)
    node = LidarPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()