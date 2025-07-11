#!/usr/bin/env python3
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import os

'''
Parameter Description:
---
- Set laser scan directon:
  1. Set counterclockwise, example: {'laser_scan_dir': True}
  2. Set clockwise,        example: {'laser_scan_dir': False}
- Angle crop setting, Mask data within the set angle range:
  1. Enable angle crop fuction:
    1.1. enable angle crop,  example: {'enable_angle_crop_func': True}
    1.2. disable angle crop, example: {'enable_angle_crop_func': False}
  2. Angle cropping interval setting:
  - The distance and intensity data within the set angle range will be set to 0.
  - angle >= 'angle_crop_min' and angle <= 'angle_crop_max' which is [angle_crop_min, angle_crop_max], unit is degress.
    example:
      {'angle_crop_min': 135.0}
      {'angle_crop_max': 225.0}
      which is [135.0, 225.0], angle unit is degress.
'''

def generate_launch_description():
  # LDROBOT LiDAR publisher node
  ldlidar_node = Node(
      package='ldlidar_stl_ros2',
      executable='ldlidar_stl_ros2_node',
      name='STL27L',
      output='screen',
      parameters=[
        {'product_name': 'LDLiDAR_STL27L'},
        {'topic_name': 'scan_raw'},
        {'frame_id': 'base_laser'},
        {'port_name': '/dev/ldlidar'},
        {'port_baudrate': 921600},
        {'laser_scan_dir': True},
        {'enable_angle_crop_func': False},
        {'angle_crop_min': 0.0},
        {'angle_crop_max': 0.0}
      ]
  )

  scan_filter_config = os.path.join(
      get_package_share_directory('ldlidar_stl_ros2'),
      'config',
      'laser_filter_config.yaml'
  )

  scan_filter_node = Node(
      package='laser_filters',
      executable="scan_to_scan_filter_chain",
      # name='scan_filter_node',
      output='screen',
      parameters=[scan_filter_config],
      remappings=[
          ('/scan', '/scan_raw'),
          ('/scan_filtered', '/scan'),
      ]
  )

  # base_link to base_laser tf node
  base_link_to_laser_tf_node = Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    name='base_link_to_base_laser_stl27l',
    arguments=['0','0','0.18','0','0','0','base_link','base_laser']
  )


  # Define LaunchDescription variable
  ld = LaunchDescription()

  ld.add_action(ldlidar_node)
  ld.add_action(scan_filter_node)
  ld.add_action(base_link_to_laser_tf_node)

  return ld
