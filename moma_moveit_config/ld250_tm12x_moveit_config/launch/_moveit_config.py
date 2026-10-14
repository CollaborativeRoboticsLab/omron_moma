import os

import yaml
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder


def _load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def load_moveit_config():
    combined_package_path = get_package_share_directory("ld250_tm12x_moveit_config")
    tm12x_package_path = get_package_share_directory("tm12x_moveit_config")

    moveit_config = (
        MoveItConfigsBuilder("ld250_tm12x", package_name="ld250_tm12x_moveit_config")
        .robot_description(
            file_path=os.path.join(combined_package_path, "config", "ld250_tm12x.urdf.xacro")
        )
        .robot_description_semantic(
            file_path=os.path.join(combined_package_path, "config", "ld250_tm12x.srdf")
        )
        .robot_description_kinematics(
            file_path=os.path.join(tm12x_package_path, "config", "kinematics.yaml")
        )
        .planning_pipelines(
            default_planning_pipeline="ompl",
            pipelines=["ompl", "pilz_industrial_motion_planner", "chomp"],
            load_all=False,
        )
        .trajectory_execution(
            file_path=os.path.join(tm12x_package_path, "config", "moveit_controllers.yaml")
        )
        .sensors_3d(file_path=os.path.join(tm12x_package_path, "config", "sensors_3d.yaml"))
        .joint_limits(file_path=os.path.join(tm12x_package_path, "config", "joint_limits.yaml"))
        .pilz_cartesian_limits(
            file_path=os.path.join(tm12x_package_path, "config", "pilz_cartesian_limits.yaml")
        )
        .to_moveit_configs()
    )

    moveit_config.planning_pipelines["ompl"] = _load_yaml(
        os.path.join(tm12x_package_path, "config", "ompl_planning.yaml")
    )
    moveit_config.planning_pipelines["pilz_industrial_motion_planner"] = _load_yaml(
        os.path.join(tm12x_package_path, "config", "pilz_industrial_motion_planner_planning.yaml")
    )
    moveit_config.planning_pipelines["chomp"] = _load_yaml(
        os.path.join(tm12x_package_path, "config", "chomp_planning.yaml")
    )

    return moveit_config