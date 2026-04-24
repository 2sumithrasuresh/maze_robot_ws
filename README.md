# Maze-Solving Robot

A ROS2/Gazebo simulation of an autonomous maze-solving robot using Right-Hand Wall Following.

The robot navigates from a start position (-2.5, -2.5) to a goal position (2.5, 2.5)
using only laser scan data — no map, no prior knowledge of the maze.

---

## Demo

[Add screenshot or GIF here]

---

## Requirements

- Ubuntu 22.04 LTS
- ROS2 Humble Hawksbill
- Gazebo Classic v11
- Python 3.10+

---

## Installation

### 1. Install ROS2 Humble
Follow the official guide: https://docs.ros.org/en/humble/Installation.html

### 2. Install Gazebo and ROS-Gazebo bridge
```bash
sudo apt install gazebo ros-humble-gazebo-ros-pkgs -y
```

### 3. Clone this repository
```bash
cd ~
git clone <your-repo-url> maze_robot_ws
cd maze_robot_ws
```

### 4. Install dependencies
```bash
sudo apt install ros-humble-robot-state-publisher ros-humble-xacro python3-colcon-common-extensions -y
```

### 5. Build the package
```bash
source /opt/ros/humble/setup.bash
colcon build --packages-select maze_solver
source install/setup.bash
```

---

## Running the Simulation

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch maze_solver maze_launch.py
```

Gazebo will open with the maze. The robot spawns after ~3 seconds and
starts navigating after ~6 seconds.

---

## Project Structure
```bash
maze_robot_ws/
└── src/
└── maze_solver/
├── maze_solver/
│   └── maze_solver_node.py   # Wall following algorithm
├── urdf/
│   └── robot.urdf            # Robot description
├── worlds/
│   └── maze.world            # Gazebo maze environment
├── launch/
│   └── maze_launch.py        # Launch file
├── package.xml
└── setup.py
```
---

## How It Works

**Robot:** Circular differential-drive robot with a 360° laser scanner.

**Algorithm — Right-Hand Wall Following:**

The robot reads two laser distances on every scan cycle:
- `front` — distance directly ahead
- `right` — distance directly to the right

Decision logic:

| Condition              | Action           |
|------------------------|------------------|
| front < 0.45m          | Turn left        |
| right > 0.55m          | Curve right      |
| right < 0.30m          | Curve left       |
| right at good distance | Go straight      |

The robot stops automatically when odometry detects it is within 0.4m of the goal.

---

## Configuration

Key parameters in `maze_solver_node.py`:

| Parameter          | Default | Description                        |
|--------------------|---------|------------------------------------|
| forward_speed      | 0.35    | Linear speed (m/s)                 |
| turn_speed         | 0.8     | Angular speed (rad/s)              |
| wall_target_dist   | 0.4     | Target distance from right wall    |
| front_threshold    | 0.45    | Distance to trigger turn           |
| goal_radius        | 0.4     | Distance to trigger goal detection |

---

## Topics

| Topic     | Type                        | Description              |
|-----------|-----------------------------|--------------------------|
| /scan     | sensor_msgs/LaserScan       | Laser scan input         |
| /cmd_vel  | geometry_msgs/Twist         | Velocity commands output |
| /odom     | nav_msgs/Odometry           | Robot position input     |

---

## Authors

<a href="https://github.com/2sumithrasuresh">
  <img src="https://github.com/2sumithrasuresh.png" width="20px;" />
  Sumithra Suresh
</a>
<br/>
<a href="https://github.com/quack101">
  <img src="https://github.com/quack101.png" width="20px;" />
   Sriharshita Vayyasi
</a>
<br/>
<a href="https://github.com/Suhaniverma2004">
  <img src="https://github.com/Suhaniverma2004.png" width="20px;" />
  Suhani Verma
</a>


---

## License

MIT License
