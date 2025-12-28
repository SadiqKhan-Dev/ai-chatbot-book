---
sidebar_position: 3
---

# 2.3 Exercises

Hands-on practice with Unity rendering and character controllers.

## Exercise 1: Import Humanoid Model and Configure Hierarchy

**Objective**: Import and configure humanoid physics hierarchy

### Task

1. Create new Unity 3D project
2. Import humanoid FBX model
3. Configure humanoid avatar
4. Add physics components

### Configuration

| Component | Placement | Configuration |
|-----------|-----------|---------------|
| Rigidbody | Every moving link | Mass based on link |
| Collider | Every link | Shape matching geometry |
| Joint | Connected links | Correct type and limits |

### Validation
- [ ] Model imports without errors
- [ ] Avatar configuration passes
- [ ] All links have Rigidbody
- [ ] All links have Collider

---

## Exercise 2: Set Up Physics Components

**Objective**: Configure physics properties for realistic behavior

### Task

Create physics materials:

```csharp
PhysicMaterial metal = new PhysicMaterial("Metal");
metal.dynamicFriction = 0.4f;
metal.staticFriction = 0.5f;
metal.bounciness = 0.0f;
```

### Validation
- [ ] Physics materials created
- [ ] Colliders detect collisions
- [ ] Robot doesn't slide excessively

---

## Exercise 3: Configure Joints for Humanoid Motion

**Objective**: Set up joints for realistic humanoid movement

### Task

```csharp
// Hip joint
ConfigurableJoint hip = thigh.gameObject.AddComponent<ConfigurableJoint>();
hip.connectedBody = pelvis;
hip.axis = Vector3.right;
hip.highAngularXLimit = 120f;  // Flexion
hip.lowAngularXLimit = -30f;    // Extension

// Knee joint (hinge)
HingeJoint knee = shin.gameObject.AddComponent<HingeJoint>();
knee.connectedBody = thigh;
knee.axis = Vector3.right;
knee.limits.min = -150f;
knee.limits.max = 0f;
knee.useLimits = true;
```

### Validation
- [ ] Joints connect correctly
- [ ] Limits prevent self-collision
- [ ] Movement feels natural

---

## Exercise 4: Create Interactive Simulation Scene

**Objective**: Build interactive simulation environment

### Task

1. Ground plane with physics
2. Obstacles to interact with
3. Keyboard input for control

```csharp
// Basic scene setup
GameObject ground = GameObject.CreatePrimitive(PrimitiveType.Plane);
ground.transform.position = Vector3.zero;
ground.AddComponent<MeshCollider>();

// Add obstacles
CreateObstacle(new Vector3(2, 0.25f, 2), new Vector3(0.5f, 0.5f, 0.5f));
CreateObstacle(new Vector3(-1.5f, 0.15f, 1), new Vector3(0.3f, 0.3f, 0.3f));
```

### Validation
- [ ] Scene loads without errors
- [ ] Ground has proper physics
- [ ] Robot responds to keyboard

---

## Quiz: Unity Fundamentals

### Question 1
What component is required for physics?

A) Collider
B) Rigidbody
C) MeshFilter
D) CharacterController

### Question 2
Which joint for robot knee?

A) ConfigurableJoint
B) FixedJoint
C) HingeJoint
D) SpringJoint

### Question 3
What is CCD?

A) Cyclic Coordinate Descent
B) Continuous Control Drive
C) Closed Chain Dynamics
D) Character Control Data

### Answer Key
1. B, 2. C, 3. A

---

## Summary

After completing these exercises, you can:
- Import and configure humanoid models
- Set up physics components
- Configure joint limits
- Create interactive scenes

Proceed to Chapter 3: Sensor Simulation
