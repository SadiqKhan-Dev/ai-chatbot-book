---
sidebar_position: 1
---

# 1. ROS 2 as a Robotic Nervous System

Understand ROS 2 architecture through the nervous system metaphor.

## Learning Objectives

1. Explain ROS 2's role in robot software
2. Understand DDS communication layer
3. Set up development environment

## Overview

Think of a robot's software architecture like the human nervous system:

```
Human Body              Robot
+---------+          +---------+
|  Brain  | <------> |  User   |
+---------+   Think  |  Code   |
     |                 |
  Spinal           ROS 2
  Cord             Middleware
     |                 |
+---------+          +---------+
| Sensors | <------> | Sensors |
+---------+   Input  +---------+
     |                 |
+---------+          +---------+
| Motors  | <------> | Motors  |
+---------+   Output +---------+
```

**ROS 2 = Spinal cord + peripheral nerves for robots**

## ROS 2 Architecture

```
+------------------+
|   Your Code      |  <-- rclpy (Python), rclcpp (C++)
+------------------+
         |
         v
+------------------+
|   rcl (client    |  <-- ROS client library
|   library)       |
+------------------+
         |
         v
+------------------+
|      DDS         |  <-- Data Distribution Service
|   Middleware     |     (CycloneDDS, FastDDS)
+------------------+
         |
         v
+------------------+
|   Network        |
+------------------+
```

## DDS: The Communication Layer

DDS (Data Distribution Service) handles all robot communication:

| DDS Feature | Nervous System Analogy |
|-------------|------------------------|
| Discovery | Reflex - automatic connection |
| Pub/Sub | Sensory broadcast |
| Services | Spinal reflex arc |
| QoS | Sensitivity settings |

## Why ROS 2 vs ROS 1?

| Aspect | ROS 1 | ROS 2 |
|--------|-------|-------|
| Middleware | Custom master | DDS (standard) |
| Real-time | Limited | Built-in support |
| Security | None | SROS2 |
| Cross-platform | Linux only | Linux, Windows, macOS |

## Workspace Setup

```bash
# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Build
colcon build

# Source environment
source install/setup.bash

# Add to .bashrc
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

## Package Creation

```bash
cd ~/ros2_ws/src
ros2 pkg create my_robot_pkg --build-type ament_python --dependencies rclpy
```

## Verify Installation

```bash
source /opt/ros/humble/setup.bash
ros2 node list              # List running nodes
ros2 topic list             # List active topics
ros2 service list           # List available services
ros2 doctor                 # Check system health
```

## Next Section

Proceed to [Communication Primitives](../02-communication-primitives/index.md)
