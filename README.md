# Omron Mobile Manipulator

Original packages are from [OmronAPAC](https://github.com/OmronAPAC)

This repository allows controlling the Base, Arm and Gripper of the Omron Mobile Manipulator using packages,

- [tmr_ros2](https://github.com/CollaborativeRoboticsLab/tmr_ros2) package
- [omron_amr](https://github.com/CollaborativeRoboticsLab/omron_amr) package
- [omron_gripper](https://github.com/CollaborativeRoboticsLab/omron_gripper.git) package

For supported features and limitations, see the individual repositories on the features supported by the MoMa.

## Device Configuration

The robot expects the remote PC to be configured with the following IP address to connect to the robot,

IP Address : 192.168.1.50
Subnet Mask : 255.255.255.0

## Setup

Create a workspace

```sh
mkdir -p omron_ws/src
cd omron_ws/src
```

Install dependencies
```sh
sudo apt install ros-jazzy-moveit ros-jazzy-controller-manager ros-jazzy-joint-trajectory-controller ros-jazzy-joint-state-broadcaster ros-jazzy-rmw-cyclonedds-cpp ros-jazzy-joint-state-publisher ros-jazzy-vision-opencv ros-jazzy-navigation2 ros-jazzy-nav2-bringup ros-jazzy-slam-toolbox ros-jazzy-rviz2 ros-jazzy-teleop-twist-joy ros-jazzy-joy
```
```sh
pip install --break-system-packages pymodbus
```

Clone the repositories into the `src` folder by

```sh
git clone https://github.com/CollaborativeRoboticsLab/tmr_ros2.git
git clone --recurse-submodules https://github.com/CollaborativeRoboticsLab/omron_amr.git
git clone https://github.com/CollaborativeRoboticsLab/omron_moma.git
```

finally build by

```sh
cd ..
colcon build
```

**or save time and use devcontainer** 

## MoveIt Configuration

The combined MoveIt package for the mobile manipulators lives in `moma_moveit_config/`.

The combined package owns only the combined-model-specific assets:

- combined URDF wrapper
- combined SRDF
- combined launch files

The TM arm tuning remains in the upstream `tmXXX_moveit_config` packages and is reused by the combined package:

- kinematics
- joint limits
- controllers
- OMPL, CHOMP, and Pilz planner settings

When updating the mounted robot model, keep the arm-specific tuning in `tmXXX_moveit_config` as the source of truth and only change the combined package where the mobile base integration actually differs.

## Usage

`ld250_tm12x.launch.py` now treats `use_rviz:=true` as the default behavior. In practice that means RViz starts automatically when MoveIt is enabled, and you only need to set `use_rviz:=false` for headless runs.

### Start the system headless

```bash
source install/setup.bash
ros2 launch moma_ros ld250_tm12x.launch.py use_rviz:=false
```

### Start the system with RVIZ

```bash
source install/setup.bash
ros2 launch moma_ros ld250_tm12x.launch.py
```

### Start the system without Nav2 or Moveit to evaluate the Hardware connection

```bash
source install/setup.bash
ros2 launch moma_ros ld250_tm12x.launch.py use_nav2:=false use_moveit:=false
```

### Start the system without Nav2 to control just the Arm and Gripper using RVIZ

```bash
source install/setup.bash
ros2 launch moma_ros ld250_tm12x.launch.py use_nav2:=false
```

## Docker

Clone this reposiotory

```bash
git clone https://github.com/CollaborativeRoboticsLab/omron_moma.git 
cd omron_moma/docker
```

Pull the Docker image and start compose (No need to run `docker compose build`)
```bash
docker compose pull
docker compose up
```

To clean the system,
```bash
docker compose down
```
