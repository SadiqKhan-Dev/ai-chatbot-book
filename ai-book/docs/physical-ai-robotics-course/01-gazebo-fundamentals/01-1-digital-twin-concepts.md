---
sidebar_position: 1
---

# 1.1 Digital Twin Concepts

Core concepts for simulation-only digital twin development.

## What is a Digital Twin?

A **digital twin** is a virtual representation of a physical robot that mirrors its geometry, physics, sensors, and behavior.

### Key Characteristics

| Characteristic | Description |
|---------------|-------------|
| Geometric fidelity | Accurate 3D model representation |
| Physics accuracy | Realistic mass, inertia, collision |
| Sensor simulation | Synthetic data matching real sensors |
| Bidirectional communication | State estimation and control |

## Benefits of Simulation-Only Development

### Safety
- Test dangerous scenarios without hardware risk
- Prototype risky behaviors safely

### Accessibility
- No physical robot required to learn
- Distributed learning across multiple users

### Reproducibility
- Identical conditions for every test run
- Deterministic execution with seed control

### Speed
- Accelerated time simulation possible
- Parallel scenario testing

## Platform Comparison: Gazebo vs. Unity

| Aspect | Gazebo | Unity |
|--------|--------|-------|
| Physics Engine | ODE, Bullet, DART | PhysX |
| ROS Integration | Native | ROS# library |
| Rendering | OGRE | Unity Renderer |
| Use Case | Research, Industrial | Visualization, Games |

### When to Use Gazebo

- Working with ROS-based systems
- Research publication or academic work
- Need deterministic physics for benchmarking
- Integrating with existing robotics pipeline

## Physics Simulation Fundamentals

### Rigid Body Dynamics

```
F = ma          (Linear motion)
τ = Iα          (Rotational motion)
```

Where:
- F = Force vector
- m = Mass
- a = Linear acceleration
- τ = Torque vector
- I = Inertia tensor
- α = Angular acceleration

### Coordinate Systems

```
World Frame (W)
    |
    +-- Robot Base Frame (B)
          |
          +-- Left Hip Frame (LH)
```

### Simulation Loop

```
Physics Step (1ms)          Rendering Step
+-----------+               +-----------+
| Apply     |-------------->| Update    |
| Forces    |               | Scene     |
+-----------+               +-----------+
         |                         |
         v                         v
    +--------+               +--------+
    | Solve  |               | Render  |
    | Physics|               | Frame   |
    +--------+               +---------+
```

## Model Representation Formats

### URDF Structure

```xml
<robot name="humanoid">
  <link name="base">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0"
               iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>
</robot>
```

### XACRO for Modular Descriptions

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://wiki.ros.org/xacro">
  <xacro:property name="leg_mass" value="5.0"/>

  <xacro:macro name="cylinder_link" params="name length radius mass">
    <link name="${name}">
      <visual>
        <geometry>
          <cylinder length="${length}" radius="${radius}"/>
        </geometry>
      </visual>
      <inertial>
        <mass value="${mass}"/>
      </inertial>
    </link>
  </xacro:macro>
</robot>
```

## Summary

Digital twins enable safe, accessible, and reproducible robotics development. Understanding physics fundamentals—rigid body dynamics, collision response, and joint constraints—is essential for accurate simulations.

## Next Section

Proceed to [Gazebo Tooling](./01-2-gazebo-tooling.md)
