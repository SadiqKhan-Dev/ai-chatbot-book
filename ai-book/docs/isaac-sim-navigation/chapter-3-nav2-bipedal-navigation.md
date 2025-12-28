---
sidebar_position: 3
title: Chapter 3 - Nav2 Bipedal Navigation
description: Navigation configuration for humanoid robots
---

# Chapter 3: Nav2 Bipedal Navigation

Nav2 provides navigation capabilities for ROS 2 robots. This chapter covers Nav2 configuration specific to bipedal humanoid platforms.

---

## 3.1 Nav2 Architecture

### Server Architecture

Nav2 uses a server-based architecture with distinct behavior trees.

**Core Servers:**

| Server | Function |
|--------|----------|
| bt_navigator | Executes behavior tree navigation logic |
| planner_server | Generates global paths |
| controller_server | Executes local trajectory tracking |
| smoother_server | Refines path geometry |
| recovery_server | Executes recovery behaviors |
| map_server | Provides occupancy map data |

**Behavior Tree:**

```
NavigationGoal → bt_navigator
    ↓
    ├─→ Planner: Compute global path
    ├─→ Controller: Track path
    └─→ Recovery: Handle failures
```

### Navigation Stack

The navigation stack processes sensor data to generate motion commands.

```
Sensor Data → Costmap → Planner → Controller →cmd_vel→ Robot
    ↑                                            ↓
    └────────────── Recovery ←────────────────────┘
```

---

## 3.2 Humanoid Costmaps

### Costmap Structure

Costmaps represent the environment as a 2D grid with obstacle and inflation values.

**Grid Representation:**

```
Cell (i,j): {x = i * resolution, y = j * resolution}
Value: 0 = unknown, 0-252 = obstacle proximity, 253-254 = inflation, 255 = free
```

### Humanoid Footprint

The humanoid footprint differs from wheeled robots due to articulated limbs.

**Footprint Definition:**

```yaml
footprint: [[x0, y0], [x1, y1], [x2, y2], [x3, y3]]
```

**Humanoid Footprint Coordinates (meters):**

```
Front:    [ 0.30, ±0.20]  # Arms forward
Back:     [-0.35, ±0.20]  # Torso back
Width:    0.40 m
Length:   0.65 m
```

**Configuration:**

```yaml
footprint: [[0.30, 0.20], [0.30, -0.20], [-0.35, -0.20], [-0.35, 0.20]]
```

### Costmap Configuration

Configure costmaps for humanoid navigation.

**Global Costmap:**

```yaml
global_costmap:
  global_costmap:
    ros__parameters:
      footprint: [[0.30, 0.20], [0.30, -0.20], [-0.35, -0.20], [-0.35, 0.20]]
      footprint_padding: 0.05
      resolution: 0.05
      origin_x: 0.0
      origin_y: 0.0
      inflation_radius: 0.50  # Humanoid arm reach
      cost_scaling_factor: 1.0
```

**Local Costmap:**

```yaml
local_costmap:
  local_costmap:
    ros__parameters:
      footprint: [[0.30, 0.20], [0.30, -0.20], [-0.35, -0.20], [-0.35, 0.20]]
      footprint_padding: 0.05
      resolution: 0.05
      width: 3.0
      height: 3.0
      inflation_radius: 0.50
```

---

## 3.3 Planners and Controllers

### Humanoid-Safe Planner

Select planners appropriate for bipedal locomotion.

**Recommended Planners:**

| Planner | Use Case |
|---------|----------|
| NavFn | Simple grid-based planning |
| SmacPlanner 2D | Hybrid A* for complex environments |
| Theta* | Any-angle path planning |

**Configuration:**

```yaml
planner_server:
  ros__parameters:
    expected_planner_frequency: 5.0
    use_sim_time: True
    planner_plugins: ["grid_based"]
    grid_based:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: False
      allow_unknown: True
```

### Humanoid Controller

Controllers generate velocity commands for the robot base.

**Controller Types:**

| Controller | Description |
|------------|-------------|
| DWB | Dynamic Window Approach |
| MPPI | Model Predictive Path Integral control |
| Regulated Pure Pursuit | Waypoint following with regulation |

**DWB Configuration:**

```yaml
controller_server:
  ros__parameters:
    controller_plugins: ["FollowPath"]
    FollowPath:
      plugin: "dwb_core/DWBLocalPlanner"
      debug_trajectory_details: True
      min_vel_x: 0.0
      max_vel_x: 0.5
      min_vel_theta: -1.0
      max_vel_theta: 1.0
      max_linear_accel: 1.0
      max_angular_accel: 1.5
```

---

## 3.4 Humanoid-Specific Navigation

### Narrow Passage Navigation

Humanoids require specific handling for narrow passages.

**Challenges:**

- Width constraints from shoulder breadth
- Balance considerations during rotation
- Arm collision avoidance

**Configuration:**

```yaml
narrow_passage:
  ros__parameters:
    transform_tolerance: 0.5
    controller_frequency: 10.0
    min_turning_radius: 0.3
    max_linear_speed: 0.3  # Slower in confined spaces
```

### Stair Navigation

Nav2 supports multi-floor navigation with elevator or stair transitions.

**Stair Parameters:**

```yaml
stair_navigation:
  ros__parameters:
    stair_detection_enabled: True
    stair_costmap:
      footprint: [[0.25, 0.18], [0.25, -0.18], [-0.25, -0.18], [-0.25, 0.18]]
      inflation_radius: 0.0
    step_height_tolerance: 0.02
    max_vertical_step: 0.15  # Humanoid step height
```

---

## 3.5 Perception Integration

### Dynamic Obstacle Updates

Integrate perception output with costmap updates.

**Costmap Layer Configuration:**

```yaml
obstacle_layer:
  ros__parameters:
    observation_sources: pointcloud
    pointcloud:
      topic: /segmentation/obstacles
      observation_persistence: 0.5
      expected_update_rate: 5.0
      data_type: sensor_msgs/PointCloud2
      marking: True
      clearing: True
```

**Integration Flow:**

```
Isaac ROS Segmentation → Obstacle Layer → Costmap Update → Planner
         ↓                                              ↓
    Dynamic obstacles                           Path replanning
```

### Latency Considerations

Minimize latency between perception and navigation.

| Stage | Target Latency |
|-------|----------------|
| Sensor capture | < 10ms |
| ROS publish | < 5ms |
| Inference | < 50ms |
| Costmap update | < 20ms |
| Planning | < 50ms |
| **Total** | **< 135ms** |

---

## 3.6 Complete Configuration

### Full Parameter File

```yaml
amcl:
  ros__parameters:
    use_sim_time: True
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.1
    base_frame_id: humanoid_base
    global_frame_id: map
    laser_model_type: likelihood_field

bt_navigator:
  ros__parameters:
    use_sim_time: True
    plugin_lib_names:
      - nav2_behavior_tree_plugin
    goal_blackboard_id: goal
    path_blackboard_id: path

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 10.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.001
    min_theta_velocity_threshold: 0.001
    controller_plugins: ["FollowPath"]
    FollowPath:
      plugin: "dwb_core/DWBLocalPlanner"
      debug_trajectory_details: True
      default_tolerance: 0.2

local_costmap:
  local_costmap:
    ros__parameters:
      use_sim_time: True
      update_frequency: 5.0
      publish_frequency: 2.0
      global_frame: odom
      robot_base_frame: humanoid_base
      resolution: 0.05
      footprint: [[0.30, 0.20], [0.30, -0.20], [-0.35, -0.20], [-0.35, 0.20]]
      robot_radius: 0.0
      inflation_radius: 0.50
      cost_scaling_factor: 1.0

global_costmap:
  global_costmap:
    ros__parameters:
      use_sim_time: True
      update_frequency: 1.0
      publish_frequency: 1.0
      global_frame: map
      robot_base_frame: humanoid_base
      resolution: 0.05
      footprint: [[0.30, 0.20], [0.30, -0.20], [-0.35, -0.20], [-0.35, 0.20]]
      robot_radius: 0.0
      inflation_radius: 0.50
      cost_scaling_factor: 1.0
```

---

## 3.7 Summary

This chapter covered:

- Nav2 server architecture and behavior trees
- Humanoid-specific footprint and costmap configuration
- Planner and controller selection for bipedal robots
- Narrow passage and stair navigation
- Perception integration with costmap updates
- Complete Nav2 configuration file

---

## Exercise 3.1

**Objective**: Configure Nav2 for humanoid navigation in simulation.

**Steps**:
1. Create humanoid footprint configuration
2. Configure global and local costmaps
3. Set up planner and controller parameters
4. Launch Nav2 with Isaac Sim environment
5. Send navigation goal and verify path execution

**Verification**: Humanoid reaches goal while avoiding obstacles.
