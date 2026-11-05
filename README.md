# LDLidar ROS 2 Driver

ROS 2 driver and RViz layouts for these LDROBOT 2D lidars:

- LD06
- LD19
- STL-27L

This workspace uses the stable serial name `/dev/ldlidar`. Choose the launch
file that matches the physical model; LD06 and LD19 use 230400 baud, while
STL-27L uses 921600 baud.

## Install dependencies

For ROS 2 Jazzy:

```bash
source /opt/ros/jazzy/setup.bash
sudo apt update
sudo apt install ros-jazzy-laser-filters ros-jazzy-rviz2
```

`laser_filters` is required by the STL-27L launch. It filters `/scan_raw` and
publishes the RViz-facing `/scan` topic.

## Create the stable serial-device name

Install the included udev rule once:

```bash
sudo install -m 0644 \
  ~/ros2_ws/src/ldlidar_stl_ros2/scripts/ldlidar.rules \
  /etc/udev/rules.d/99-ldlidar.rules

sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=tty
udevadm settle
```

Unplug and reconnect the USB serial adapter, then verify the link:

```bash
ls -l /dev/ldlidar
readlink -f /dev/ldlidar
```

It should resolve to a device such as `/dev/ttyUSB0`.

## Build with symbolic links

Build this package from the workspace root using Colcon's symlink-install
mode:

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash

colcon build --symlink-install \
  --packages-select ldlidar_stl_ros2

source install/setup.bash
```

Source both ROS and the workspace in every new terminal:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

## Launch with RViz

Use only the command matching the lidar model.

LD06:

```bash
ros2 launch ldlidar_stl_ros2 viewer_ld06.launch.py
```

LD19:

```bash
ros2 launch ldlidar_stl_ros2 viewer_ld19.launch.py
```

STL-27L:

```bash
ros2 launch ldlidar_stl_ros2 viewer_stl27l.launch.py
```

The STL-27L configuration was verified on this host at 921600 baud with
`/scan` publishing at approximately 10 Hz.

## Check the data

```bash
ros2 topic list | grep scan
ros2 topic hz /scan
ros2 topic echo /scan --once
```

RViz uses `base_laser` as the fixed frame and displays `/scan`.

## Troubleshooting

- `ldlidar communication is abnormal`: confirm that the launch file matches
  the physical model, `/dev/ldlidar` exists, the lidar is powered, and serial
  RX/TX wiring is correct. Using an LD06 launch for a 921600-baud STL-27L
  produces this error.
- `package 'laser_filters' not found`: install
  `ros-jazzy-laser-filters`, then source `/opt/ros/jazzy/setup.bash` again.
- `Stereo is NOT SUPPORTED`: this RViz/OpenGL message is harmless and is not a
  lidar or camera-stereo error.
- No `/dev/ldlidar`: reload the udev rule and reconnect the USB adapter.
- Permission denied: add the user to `dialout`, then log out and back in:

  ```bash
  sudo usermod -aG dialout "$USER"
  ```
