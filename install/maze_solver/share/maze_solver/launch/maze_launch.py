import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('maze_solver')

    urdf_file = os.path.join(pkg, 'urdf', 'robot.urdf')
    world_file = os.path.join(pkg, 'worlds', 'maze.world')

    # Read the URDF as a string
    with open(urdf_file, 'r') as f:
        robot_desc = f.read()

    return LaunchDescription([

        # 1. Start Gazebo with our maze world
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world_file, '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),

        # 2. Publish the robot description (so ROS knows about our robot)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}]
        ),

        # 3. Spawn the robot into Gazebo (wait 3 seconds for Gazebo to start first)
        TimerAction(
            period=3.0,
            actions=[
                Node(
                    package='gazebo_ros',
                    executable='spawn_entity.py',
                    arguments=[
                        '-entity', 'maze_robot',
                        '-topic', 'robot_description',
                        '-x', '-2.5',
                        '-y', '-2.5',
                        '-z', '0.1'
                    ],
                    output='screen'
                )
            ]
        ),

        # 4. Start the maze solver (wait 6 seconds for robot to fully spawn)
        TimerAction(
            period=6.0,
            actions=[
                Node(
                    package='maze_solver',
                    executable='maze_solver_node',
                    name='maze_solver_node',
                    output='screen'
                )
            ]
        ),
    ])
