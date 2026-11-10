import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ld250_tm12x_moveit_config'),
                'launch',
                'move_group.launch.py',
            )
        )
    )

    return LaunchDescription([
        moveit_launch,
    ])

    
