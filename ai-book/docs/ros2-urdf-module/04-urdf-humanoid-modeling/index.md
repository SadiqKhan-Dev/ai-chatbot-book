---
sidebar_position: 4
---

# 4. URDF Humanoid Modeling

Create robot descriptions using Unified Robot Description Format.

## Learning Objectives

1. Understand URDF structure for robot modeling
2. Create humanoid robot descriptions
3. Use XACRO for modular robot definitions

## URDF Basics

URDF (Unified Robot Description Format) is XML for robot structure:

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <!-- Links: Rigid bodies -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.2 0.2 0.1"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.2 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0"
               iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Joints: Connections between links -->
  <joint name="base_to_wheel" type="fixed">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <origin xyz="0 0 -0.05"/>
  </joint>
</robot>
```

## Humanoid Robot Structure

```
                    head
                     |
        arm -- torso -- arm
          |     |     |
        leg   leg   leg
```

### Complete Humanoid URDF

```xml
<?xml version="1.0"?>
<robot name="humanoid_robot">

  <!-- ============= LINKS ============= -->

  <!-- Torso -->
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.2 0.3 0.4"/>
      </geometry>
      <material name="blue">
        <color rgba="0.2 0.2 0.8 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.3 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="15.0"/>
      <inertia ixx="0.3" ixy="0" ixz="0"
               iyy="0.3" iyz="0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Head -->
  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.12"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.12"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0"
               iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Left Upper Arm -->
  <link name="left_upper_arm">
    <visual>
      <geometry>
        <cylinder length="0.25" radius="0.04"/>
      </geometry>
      <material name="gray"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.25" radius="0.04"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <inertia ixx="0.01" ixy="0" ixz="0"
               iyy="0.01" iyz="0" izz="0.002"/>
    </inertial>
  </link>

  <!-- Left Lower Arm -->
  <link name="left_lower_arm">
    <visual>
      <geometry>
        <cylinder length="0.22" radius="0.03"/>
      </geometry>
      <material name="gray"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.22" radius="0.03"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.005" ixy="0" ixz="0"
               iyy="0.005" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Right arm mirrors left... -->

  <!-- Left Upper Leg -->
  <link name="left_upper_leg">
    <visual>
      <geometry>
        <cylinder length="0.35" radius="0.07"/>
      </geometry>
      <material name="dark_gray"/>
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

  <!-- Left Lower Leg -->
  <link name="left_lower_leg">
    <visual>
      <geometry>
        <cylinder length="0.35" radius="0.05"/>
      </geometry>
      <material name="dark_gray"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.35" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="3.0"/>
      <inertia ixx="0.03" ixy="0" ixz="0"
               iyy="0.03" iyz="0" izz="0.005"/>
    </inertial>
  </link>

  <!-- Right leg mirrors left... -->

  <!-- ============= JOINTS ============= -->

  <!-- Neck Joint -->
  <joint name="neck_joint" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0.15 0"/>
    <axis xyz="0 1 0"/>  <!-- Y-axis rotation -->
    <limit lower="-0.5" upper="0.5"
           effort="10" velocity="2.0"/>
    <dynamics damping="0.5"/>
  </joint>

  <!-- Left Shoulder Joint -->
  <joint name="left_shoulder_joint" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_arm"/>
    <origin xyz="-0.15 0.1 0"/>
    <axis xyz="0 0 1"/>  <!-- Z-axis rotation -->
    <limit lower="-3.0" upper="0"
           effort="20" velocity="5.0"/>
  </joint>

  <!-- Left Elbow Joint -->
  <joint name="left_elbow_joint" type="revolute">
    <parent link="left_upper_arm"/>
    <child link="left_lower_arm"/>
    <origin xyz="0 -0.15 0"/>
    <axis xyz="1 0 0"/>  <!-- X-axis rotation -->
    <limit lower="-2.5" upper="0"
           effort="10" velocity="5.0"/>
  </joint>

  <!-- Right shoulder and elbow mirror left... -->

  <!-- Left Hip Joint -->
  <joint name="left_hip_joint" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_leg"/>
    <origin xyz="-0.08 0 0"/>
    <axis xyz="1 0 0"/>  <!-- X-axis rotation -->
    <limit lower="-1.5" upper="0.5"
           effort="50" velocity="10.0"/>
    <dynamics damping="1.0"/>
  </joint>

  <!-- Left Knee Joint -->
  <joint name="left_knee_joint" type="revolute">
    <parent link="left_upper_leg"/>
    <child link="left_lower_leg"/>
    <origin xyz="0 -0.35 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="-2.5" upper="0"
           effort="40" velocity="10.0"/>
    <dynamics damping="0.5"/>
  </joint>

  <!-- Right hip and knee mirror left... -->

</robot>
```

## XACRO Modularization

XACRO allows parameterized, reusable robot definitions:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://wiki.ros.org/xacro">

  <!-- ============= MACROS ============= -->

  <!-- Cylinder Link -->
  <xacro:macro name="cylinder_link" params="name length radius mass color">
    <link name="${name}">
      <visual>
        <geometry>
          <cylinder length="${length}" radius="${radius}"/>
        </geometry>
        <material name="${color}"/>
      </visual>
      <collision>
        <geometry>
          <cylinder length="${length}" radius="${radius}"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="${mass}"/>
        <inertia ixx="${mass*(3*radius*radius + length*length)/12}"
                 iyy="${mass*(3*radius*radius + length*length)/12}"
                 izz="${mass*radius*radius/2}"/>
      </inertial>
    </link>
  </xacro:macro>

  <!-- Revolute Joint -->
  <xacro:macro name="revolute_joint" params="name parent child axis lower upper effort velocity color">
    <joint name="${name}" type="revolute">
      <parent link="${parent}"/>
      <child link="${child}"/>
      <axis xyz="${axis}"/>
      <limit lower="${lower}" upper="${upper}"
             effort="${effort}" velocity="${velocity}"/>
      <dynamics damping="0.5"/>
    </joint>
  </xacro:macro>

  <!-- ============= USAGE ============= -->

  <!-- Torso -->
  <link name="torso">
    <visual>
      <box size="0.2 0.3 0.4"/>
      <material name="blue"/>
    </visual>
    <inertial>
      <mass value="15.0"/>
      <inertia ixx="0.3" iyy="0.3" izz="0.1"/>
    </inertial>
  </link>

  <!-- Left Arm using macros -->
  <xacro:cylinder_link name="left_upper_arm" length="0.25" radius="0.04"
                        mass="1.5" color="gray"/>
  <xacro:cylinder_link name="left_lower_arm" length="0.22" radius="0.03"
                        mass="1.0" color="gray"/>

  <xacro:revolute_joint name="left_shoulder" parent="torso" child="left_upper_arm"
                        axis="0 0 1" lower="-3.0" upper="0"
                        effort="20" velocity="5.0" color="gray"/>
  <xacro:revolute_joint name="left_elbow" parent="left_upper_arm" child="left_lower_arm"
                        axis="1 0 0" lower="-2.5" upper="0"
                        effort="10" velocity="5.0" color="gray"/>

</robot>
```

## Launch and Visualize

```bash
# Convert XACRO to URDF
xacro model.xacro > model.urdf

# Check URDF
check_urdf model.urdf

# Launch in RViz
ros2 launch urdf_tutorial display.launch.py model:=model.urdf
```

## Joint Types

| Type | DOF | Motion | Human Analog |
|------|-----|--------|--------------|
| fixed | 0 | None | Bones fused |
| revolute | 1 | Rotation | Knee, elbow |
| continuous | 1 | Unlimited rotation | Neck |
| prismatic | 1 | Translation | Linear actuator |
| floating | 6 | Free motion | Hand in air |

## Inertial Properties

Inertia tensor calculation for common shapes:

```python
# Box: Ix = m*(h² + d²)/12
# Cylinder (about z): Ix = m*(3r² + h²)/12
# Sphere: I = 2mr²/5
```

## Next Steps

You have completed Module 1! You can now:

1. Create ROS 2 nodes with rclpy
2. Implement topic and service communication
3. Build Python agents for robot control
4. Define humanoid robots with URDF

Proceed to Module 2 for simulation integration.
