from setuptools import setup
import os
from glob import glob

package_name = 'maze_solver'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='student@example.com',
    description='Maze solving robot using ROS2 and Gazebo',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'maze_solver_node = maze_solver.maze_solver_node:main',
        ],
    },
)
