# Omron Mobile Manipulator

Original packages are from [OmronAPAC](https://github.com/OmronAPAC) 

This repository allows controlling the Base, Arm and Gripper of the Omron Mobile Manipulator using packages,

- [tmr_ros2](https://github.com/CollaborativeRoboticsLab/tmr_ros2) package 
- [omron_amr](https://github.com/CollaborativeRoboticsLab/omron_amr) package
- [omron_gripper](https://github.com/CollaborativeRoboticsLab/omron_gripper.git) package

For supported features and limitations, see the individual repositories on the features supported by the MoMa.

| Branch | ROS2 Version | Compile |
|--------|--------------|---------|
| main | Jazzy | [![main](https://github.com/CollaborativeRoboticsLab/omron_moma/actions/workflows/compile.yml/badge.svg?branch=main)](https://github.com/CollaborativeRoboticsLab/omron_moma/actions/workflows/compile.yml?query=branch%3Amain) |
| develop | Jazzy | [![develop](https://github.com/CollaborativeRoboticsLab/omron_moma/actions/workflows/compile.yml/badge.svg?branch=develop)](https://github.com/CollaborativeRoboticsLab/omron_moma/actions/workflows/compile.yml?query=branch%3Adevelop) |
| humble | Humble | [![humble](https://github.com/CollaborativeRoboticsLab/omron_moma/actions/workflows/compile.yml/badge.svg?branch=humble)](https://github.com/CollaborativeRoboticsLab/omron_moma/actions/workflows/compile.yml?query=branch%3Ahumble) |

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
sudo apt install ros-humble-moveit ros-humble-controller-manager ros-humble-joint-trajectory-controller ros-humble-joint-state-broadcaster ros-humble-rmw-cyclonedds-cpp ros-humble-joint-state-publisher ros-humble-joint-state-publisher-gui ros-humble-vision-opencv ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-slam-toolbox
```
```sh
pip install pymodbus
```

Clone the repositories into the `src` folder by

```sh
git clone https://github.com/CollaborativeRoboticsLab/tmr_ros2.git
git clone https://github.com/CollaborativeRoboticsLab/omron_amr.git
git clone https://github.com/CollaborativeRoboticsLab/omron_gripper.git
git clone https://github.com/CollaborativeRoboticsLab/omron_moma.git
```

finally build by

```sh
cd ..
colcon build
```

**or save time and use devcontainer** 

## Launch Parameters

The top-level launch entry point is `ros2 launch moma_ros ld250_tm12x.launch.py`.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `tm_use_simulation` | `false` | Runs the TM arm bringup in simulation mode instead of connecting to the physical arm. |
| `tm_robot_ip` | `192.168.1.2` | IP address of the TM arm controller. |
| `use_arm` | `true` | Starts the TM arm hardware stack. If `false`, the arm hardware and MoveIt are not started. |
| `use_base` | `true` | Starts the AMR base hardware stack. If `false`, the base hardware and Nav2 are not started. |
| `use_rviz` | `false` | Starts RViz. When enabled, the launch automatically chooses the MoveIt RViz layout if the arm and MoveIt are active, otherwise it uses the Nav2 RViz layout. |
| `use_moveit` | `true` | Starts MoveIt for the arm. This is only effective when `use_arm:=true`. |
| `use_nav2` | `true` | Starts Nav2 for the mobile base. This is only effective when `use_base:=true`. |

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

### Start the full system headless

```bash
source install/setup.bash
ros2 launch moma_ros ld250_tm12x.launch.py
```

### Start the full system with RVIZ

```bash
source install/setup.bash
ros2 launch moma_ros ld250_tm12x.launch.py use_rviz:=true
```

### Start the full system without Nav2 or Moveit to evaluate the Hardware connection

```bash
source install/setup.bash
ros2 launch moma_ros ld250_tm12x.launch.py use_nav2:=false use_moveit:=false
```

### Start the ARM only to control Arm and Gripper using RVIZ

```bash
source install/setup.bash
ros2 launch moma_ros ld250_tm12x.launch.py use_base:=false use_rviz:=true
```

### Start the base only to control just the base using RVIZ

```bash
source install/setup.bash
ros2 launch moma_ros ld250_tm12x.launch.py use_arm:=false use_rviz:=true
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

## To generate a new urdf file,

1. Define a xacro file within `moma_description/xacro` that imports and customises parts and joints as reqired.
2. Run the following command to generate the urdf file. replace the `<filename>` with required name.
```bash
ros2 run xacro xacro src/omron_moma/moma_description/xacro/<filename>.urdf.xacro -o <filename>.urdf
```
eg
```bash
ros2 run xacro xacro src/omron_moma/moma_description/xacro/ld250_tm12x.urdf.xacro -o ld250_tm12x.urdf
```
3. This would generate the file in the root of the workspace. Move the file into `moma_description/urdf` folder


## To Do List

- [x] Update launch files to use standard parameters and remove non-launch related python code
- [x] Create cascadeing launch files for TMDriver, Moveit and RVIZ, AMR base and RVIZ

