import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Top-level launch args
    tm_use_simulation = LaunchConfiguration('tm_use_simulation')
    tm_robot_ip = LaunchConfiguration('tm_robot_ip')

    declare_tm_use_simulation = DeclareLaunchArgument(
        'tm_use_simulation',
        default_value='false',
        description='Forwarded to hardware bringup to run TM robot in simulation (true/false)'
    )

    declare_tm_robot_ip = DeclareLaunchArgument(
        'tm_robot_ip',
        default_value='192.168.1.2',
        description='Target robot IP address'
    )

    moma_ros_share = get_package_share_directory('moma_ros')
    amr_teleop_share = get_package_share_directory('amr_teleop')
    
    include_hardware = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(moma_ros_share, 'launch', 'ld250_tm12x', 'ld250_tm12x.hardware.launch.py')
        ),
        launch_arguments={
            'tm_use_simulation': tm_use_simulation,
            'tm_robot_ip': tm_robot_ip,
        }.items(),
    )

    include_teleop = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(amr_teleop_share, 'launch', 'amr_joyop.launch.py')
        ),
        launch_arguments={'joy_vel': 'cmd_vel'}.items(),
    )

    return LaunchDescription([
        declare_tm_use_simulation,
        declare_tm_robot_ip,
        include_hardware,
        include_teleop
    ])
