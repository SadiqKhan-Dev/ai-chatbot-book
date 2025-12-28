---
sidebar_position: 3
---

# 1.3 Exercises

Hands-on practice with Gazebo physics simulation.

## Exercise 1: Create Simple Arm in URDF

**Objective**: Create a 3-DOF arm using URDF

### Task

Create `arm.urdf` with:
- Base link (fixed)
- Shoulder joint + upper arm
- Elbow joint + forearm
- Wrist joint + hand

### Requirements

| Link | Geometry | Mass | Joint Type |
|------|----------|------|------------|
| base | box 0.1×0.1×0.1 | 1.0 kg | fixed |
| upper_arm | cylinder r=0.03, l=0.3 | 1.5 kg | revolute |
| forearm | cylinder r=0.025, l=0.25 | 0.8 kg | revolute |
| hand | box 0.05×0.05×0.05 | 0.2 kg | revolute |

### Validation

```bash
# Validate URDF
check_urdf arm.urdf

# Launch in Gazebo
roslaunch gazebo_ros spawn_model.launch -urdf -model arm -z 0.5
```

### Criteria
- [ ] `check_urdf` passes without errors
- [ ] Robot spawns successfully
- [ ] All joints visible in model hierarchy
- [ ] Robot holds position

---

## Exercise 2: Configure Joint Limits and Damping

**Objective**: Tune joint dynamics for stable motion

### Task

Modify arm URDF with:

| Joint | Effort (Nm) | Velocity (rad/s) | Damping (Nm·s/rad) |
|-------|-------------|------------------|-------------------|
| shoulder | 30 | 2.0 | 0.5 |
| elbow | 15 | 3.0 | 0.3 |
| wrist | 5 | 5.0 | 0.1 |

### Criteria
- [ ] Robot maintains stable equilibrium
- [ ] Joints return to position without excessive oscillation
- [ ] Motion limits prevent self-collision

---

## Exercise 3: Build Environment with Obstacles

**Objective**: Create simulation world with collision objects

### Task

Create world file with:
- Ground plane with friction
- 3 obstacles (cylinder, box, sphere)
- Appropriate lighting

### Criteria
- [ ] World loads without errors
- [ ] All obstacles visible
- [ ] Robot arm does not pass through obstacles

---

## Exercise 4: Launch and Control Simulation

**Objective**: Launch simulation and control robot via ROS

### Task

Create launch file and control via topics:

```bash
# Move to position (radians)
rostopic pub /arm_controller/command trajectory_msgs/JointTrajectoryPoint \
  "joint_names: ['shoulder_joint', 'elbow_joint', 'wrist_joint']" \
  "positions: [0.5, 0.3, 0.1]" -1

# Check joint states
rostopic echo /joint_states
```

### Criteria
- [ ] Simulation launches successfully
- [ ] Controller is active
- [ ] Joint commands result in motion
- [ ] Joint states update correctly

---

## Quiz: Gazebo Fundamentals

### Question 1
What is the purpose of the `<inertial>` element in URDF?

A) Visual appearance
B) Physical properties for simulation
C) Collision geometry
D) Joint connection

### Question 2
Which joint type allows unlimited rotation?

A) Revolute
B) Prismatic
C) Continuous
D) Fixed

### Question 3
What does XACRO provide?

A) Compile URDF to SDF
B) Macro-based URDF generation
C) Visualize models
D) Control physics

### Answer Key
1. B, 2. C, 3. B

---

## Summary

After completing these exercises, you can:
- Create URDF models for robot arms
- Configure joint limits and damping
- Build simulation worlds with obstacles
- Launch and control simulations via ROS

Proceed to Chapter 2: Unity Fundamentals
