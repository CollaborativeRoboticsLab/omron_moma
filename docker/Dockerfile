#---------------------------------------------------------------------------------------------------------------------------
#----
#----   Start image
#----
#---------------------------------------------------------------------------------------------------------------------------

# Use a ROS 2 Jazzy image for build and runtime
FROM ros:jazzy

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=jazzy
ENV WORKSPACE_ROOT=/omron_ws

## Parameters
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV ROS_DOMAIN_ID=0

ENV USE_RVIZ=true
ENV USE_MOVEIT=true
ENV USE_NAV2=true
ENV ARM_USE_SIMULATION=false

#############################################################################################################################
#####
#####   Install Dependencies
#####
#############################################################################################################################

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-dev \
    build-essential \
    curl \
    qtdeclarative5-dev \
    ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
    ros-${ROS_DISTRO}-navigation2 \
    ros-${ROS_DISTRO}-nav2-bringup \
    ros-${ROS_DISTRO}-slam-toolbox \
    ros-${ROS_DISTRO}-moveit \
    ros-${ROS_DISTRO}-rviz2 \
    ros-${ROS_DISTRO}-controller-manager \
    ros-${ROS_DISTRO}-joint-trajectory-controller \
    ros-${ROS_DISTRO}-joint-state-broadcaster \
    ros-${ROS_DISTRO}-joint-state-publisher \
    ros-${ROS_DISTRO}-vision-opencv \
    ros-${ROS_DISTRO}-teleop-twist-joy \
    ros-${ROS_DISTRO}-joy \
 && rm -rf /var/lib/apt/lists/*

# Install python packages
RUN pip3 install --break-system-packages --no-cache-dir pymodbus

#############################################################################################################################
#####
#####   Clone and build the workspace
#####
#############################################################################################################################

# Create and clone workspace
WORKDIR ${WORKSPACE_ROOT}/src

RUN git clone https://github.com/CollaborativeRoboticsLab/omron_moma.git
RUN git clone https://github.com/CollaborativeRoboticsLab/tmr_ros2.git 
RUN git clone --recurse-submodules https://github.com/CollaborativeRoboticsLab/omron_amr.git
RUN git clone https://github.com/CollaborativeRoboticsLab/omron_gripper.git

WORKDIR ${WORKSPACE_ROOT}

# Build the workspace
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && colcon build

WORKDIR /

# Copy the container entrypoint
COPY docker/ros_entrypoint.sh ros_entrypoint.sh

RUN chmod +x /ros_entrypoint.sh

ENTRYPOINT [ "/ros_entrypoint.sh" ]