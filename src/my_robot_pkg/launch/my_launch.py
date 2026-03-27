from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        # turtlesim 실행
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),

        # lidar publisher 실행
        Node(
            package='my_robot_pkg',
            executable='lidar_publisher',
            name='lidar_publisher'
        ),

        # rosbridge websocket 실행
        Node(
            package='rosbridge_server',
            executable='rosbridge_websocket',
            name='rosbridge_websocket'
        ),
    ])