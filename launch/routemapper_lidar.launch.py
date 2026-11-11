#!/usr/bin/env python3
# STL-27L on the routemapper backpack: unfiltered scan published on /scan.
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ldlidar_node = Node(
        package='ldlidar_stl_ros2',
        executable='ldlidar_stl_ros2_node',
        name='STL27L',
        output='screen',
        parameters=[
            {'product_name': 'LDLiDAR_STL27L'},
            {'topic_name': 'scan'},
            {'frame_id': 'base_laser'},
            {'port_name': '/dev/ldlidar'},
            {'port_baudrate': 921600},
            {'laser_scan_dir': True},
            {'enable_angle_crop_func': False},
            {'angle_crop_min': 0.0},
            {'angle_crop_max': 0.0},
        ],
    )

    base_link_to_laser_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_base_laser_stl27l',
        arguments=['0', '0', '0.18', '0', '0', '0', 'base_link', 'base_laser'],
    )

    return LaunchDescription([
        ldlidar_node,
        base_link_to_laser_tf_node,
    ])
