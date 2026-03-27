import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import numpy as np

class LidarPublisher(Node):
    def __init__(self):
        super().__init__('lidar_publisher_node')
        self.publisher_ = self.create_publisher(LaserScan, 'scan', 10)
        
        self.timer = self.create_timer(2.0, self.timer_callback)
        self.get_logger().info('Lidar Mock Publisher has started (2.0s interval)')

    def timer_callback(self):
        msg = LaserScan()
        
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'laser_frame'
        
        msg.angle_min = 0.0
        msg.angle_max = 2 * np.pi  
        msg.angle_increment = np.pi / 180.0  #
        msg.range_min = 0.12
        msg.range_max = 3.5
        
        msg.ranges = np.random.uniform(msg.range_min, msg.range_max, 360).tolist()
        
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
