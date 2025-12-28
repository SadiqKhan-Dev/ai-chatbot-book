---
sidebar_position: 2
---

# 1.2 Gazebo Tooling

URDF/XACRO, physics plugin configuration, and world creation.

## Gazebo Architecture

```
+------------------+     +------------------+
|   Gazebo GUI     |     |   libsdformat    |
|   (Qt/Ogre)      |---->|   (World Parser) |
+------------------+     +------------------+
                              |
                              v
                       +------------------+
                       |   Physics Engine  |
                       |   (ODE/Bullet)    |
                       +------------------+
```

### Key Executables

| Executable | Purpose |
|------------|---------|
| `gzserver` | Physics simulation server |
| `gzclient` | Visualization GUI |
| `gz` | Unified command-line tool |

## Complete Humanoid URDF Example

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">

  <!-- Materials -->
  <material name="white">
    <color rgba="0.9 0.9 0.9 1.0"/>
  </material>
  <material name="metal">
    <color rgba="0.5 0.5 0.6 1.0"/>
  </material>

  <!-- Torso -->
  <link name="torso_link">
    <visual>
      <geometry>
        <box size="0.2 0.3 0.4"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.3 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="20.0"/>
      <inertia ixx="0.5" ixy="0" ixz="0"
               iyy="0.5" iyz="0" izz="0.2"/>
    </inertial>
  </link>

  <!-- Head -->
  <link name="head_link">
    <visual>
      <geometry>
        <sphere radius="0.12"/>
      </geometry>
      <material name="white"/>
    </visual>
    <inertial>
      <mass value="1.5"/>
      <inertia ixx="0.01" ixy="0" ixz="0"
               iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <joint name="torso_to_head" type="revolute">
    <parent link="torso_link"/>
    <child link="head_link"/>
    <origin xyz="0 0.15 0.2"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.0" upper="1.0" effort="10" velocity="5"/>
  </joint>

  <!-- Left Hip -->
  <link name="left_hip_link">
    <visual>
      <geometry>
        <cylinder length="0.08" radius="0.06"/>
      </geometry>
      <material name="metal"/>
    </visual>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0"
               iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <joint name="torso_to_left_hip" type="revolute">
    <parent link="torso_link"/>
    <child link="left_hip_link"/>
    <origin xyz="-0.08 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="-1.5" upper="1.5" effort="50" velocity="10"/>
    <dynamics damping="0.5"/>
  </joint>

  <!-- Left Upper Leg -->
  <link name="left_upper_leg_link">
    <visual>
      <geometry>
        <cylinder length="0.35" radius="0.07"/>
      </geometry>
      <material name="black"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.35" radius="0.07"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.05" ixy="0" ixz="0"
               iyy="0.05" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <joint name="left_hip_to_upper_leg" type="revolute">
    <parent link="left_hip_link"/>
    <child link="left_upper_leg_link"/>
    <origin xyz="0 0 -0.08"/>
    <axis xyz="1 0 0"/>
    <limit lower="-1.5" upper="0.5" effort="50" velocity="10"/>
    <dynamics damping="0.5"/>
  </joint>

  <!-- Right leg (same pattern) -->
  <link name="right_hip_link">
    <visual>
      <geometry>
        <cylinder length="0.08" radius="0.06"/>
      </geometry>
      <material name="metal"/>
    </visual>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0"
               iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <joint name="torso_to_right_hip" type="revolute">
    <parent link="torso_link"/>
    <child link="right_hip_link"/>
    <origin xyz="0.08 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="-1.5" upper="1.5" effort="50" velocity="10"/>
    <dynamics damping="0.5"/>
  </joint>

</robot>
```

## Physics Plugin Configuration

```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1.0</real_time_factor>
  <gravity>0 0 -9.8</gravity>
</physics>
```

## World File Creation

```xml
<?xml version="1.0"?>
<sdf version="1.7">
  <world name="humanoid_lab">
    <physics type="ode">
      <gravity>0 0 -9.81</gravity>
    </physics>

    <!-- Ground plane -->
    <model name="ground">
      <static>true</static>
      <link name="surface">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>20 20</size>
            </plane>
          </geometry>
        </collision>
      </link>
    </model>

    <!-- Lighting -->
    <light type="directional" name="main_light">
      <pose>2 2 5 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
    </light>

  </world>
</sdf>
```

## Running Simulations

```bash
# Check URDF for errors
check_urdf humanoid.urdf

# Convert XACRO to URDF
xacro humanoid.xacro > humanoid.urdf

# Run Gazebo
roslaunch gazebo_ros empty_world.launch

# Spawn robot
rosrun gazebo_ros spawn_model -urdf -model humanoid -param robot_description -z 0.7
```

## Summary

Gazebo simulation requires URDF/XACRO for model definition, physics plugins for realistic behavior, and world files for environment setup.

## Next Section

Proceed to [Exercises](./01-3-exercises.md)
