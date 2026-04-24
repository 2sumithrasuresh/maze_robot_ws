#!/usr/bin/env python3
"""
Maze Solver Node - Right-Hand Wall Following Algorithm
======================================================
Robot keeps the right wall at a target distance.
If right wall is too far  -> turn right
If right wall is too close -> turn left
If wall ahead             -> turn left
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math


class MazeSolverNode(Node):

    def __init__(self):
        super().__init__('maze_solver_node')

        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.scan_sub = self.create_subscription(
            LaserScan, 'scan', self.scan_callback, 10)
        self.odom_sub = self.create_subscription(
            Odometry, 'odom', self.odom_callback, 10)

        # --- Goal ---
        self.goal_x = 2.5
        self.goal_y = 2.5
        self.goal_radius = 0.4
        self.goal_reached = False

        # --- Robot position ---
        self.current_x = -2.5
        self.current_y = -2.5

        # --- Tuning ---
        self.forward_speed   = 0.35
        self.turn_speed      = 0.8
        self.wall_target_dist = 0.4
        self.front_threshold  = 0.45

        self.get_logger().info('Right-Hand Wall Follower Started')
        self.get_logger().info(f'START: (-2.5, -2.5)  |  GOAL: ({self.goal_x}, {self.goal_y})')

    def odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

    def distance_to_goal(self):
        dx = self.goal_x - self.current_x
        dy = self.goal_y - self.current_y
        return math.sqrt(dx*dx + dy*dy)

    def get_range(self, scan, angle_deg):
        angle_rad = math.radians(angle_deg)
        index = int((angle_rad - scan.angle_min) / scan.angle_increment)
        index = max(0, min(index, len(scan.ranges) - 1))
        d = scan.ranges[index]
        return scan.range_max if (math.isnan(d) or math.isinf(d)) else d

    def stop_robot(self):
        self.cmd_pub.publish(Twist())

    def scan_callback(self, scan):

        # --- Check goal ---
        dist = self.distance_to_goal()

        if self.goal_reached:
            self.stop_robot()
            return

        if dist < self.goal_radius:
            self.goal_reached = True
            self.stop_robot()
            self.get_logger().info('=' * 50)
            self.get_logger().info('*** GOAL REACHED — MAZE SOLVED! ***')
            self.get_logger().info(f'Final position: ({self.current_x:.2f}, {self.current_y:.2f})')
            self.get_logger().info('=' * 50)
            return

        # --- Laser readings ---
        front = self.get_range(scan, 0)
        right = self.get_range(scan, -90)

        cmd = Twist()

        if front < self.front_threshold:
            # Wall ahead — turn left
            self.get_logger().info(f'Wall ahead ({front:.2f}m) — turning LEFT')
            cmd.linear.x  = 0.0
            cmd.angular.z = self.turn_speed

        elif right > self.wall_target_dist + 0.15:
            # Right wall too far — turn right to find it
            self.get_logger().info(f'Right wall far ({right:.2f}m) — turning RIGHT')
            cmd.linear.x  = self.forward_speed * 0.8
            cmd.angular.z = -self.turn_speed * 0.5

        elif right < self.wall_target_dist - 0.1:
            # Right wall too close — turn left
            self.get_logger().info(f'Right wall close ({right:.2f}m) — turning LEFT')
            cmd.linear.x  = self.forward_speed * 0.8
            cmd.angular.z = self.turn_speed * 0.5

        else:
            # Good distance — go straight
            self.get_logger().info(f'Following wall ({right:.2f}m) — STRAIGHT | goal dist: {dist:.2f}m')
            cmd.linear.x  = self.forward_speed
            cmd.angular.z = 0.0

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = MazeSolverNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
