---
sidebar_position: 1
---

# 2.1 Unity Physics System

Unity physics components and model configuration.

## Unity Physics System (PhysX)

### Key Components

| Component | Purpose | Key Properties |
|-----------|---------|----------------|
| Rigidbody | Physics body | Mass, Drag, Constraints |
| Collider | Collision shape | Type, Size, Center |
| Joint | Link constraints | Type, Limits, Connected Body |
| PhysicMaterial | Surface properties | Friction, Bounciness |

## Project Configuration

```csharp
// Physics settings
Physics.defaultSolverIterations = 50;
Physics.defaultSolverVelocityIterations = 10;
```

## Model Import Settings

```
Import Settings -> Model:
├── Mesh Compression: Off
├── Normals: Import
└-- Smoothing Angle: 60

Import Settings -> Rig:
├── Animation Type: Humanoid
└-- Avatar Definition: Create From This Model
```

## Physics Component Configuration

### Rigidbody Setup

```csharp
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
[RequireComponent(typeof(Collider))]
public class RobotLink : MonoBehaviour
{
    [SerializeField] private float mass = 1.0f;
    [SerializeField] private float drag = 0.5f;

    private Rigidbody rb;

    private void Reset()
    {
        rb = GetComponent<Rigidbody>();
        if (rb == null) rb = gameObject.AddComponent<Rigidbody>();
        rb.mass = mass;
        rb.drag = drag;
    }
}
```

### Collider Types

```csharp
// Box Collider for rectangular parts
var boxCollider = gameObject.AddComponent<BoxCollider>();
boxCollider.center = Vector3.zero;
boxCollider.size = new Vector3(0.1f, 0.1f, 0.1f);

// Capsule Collider for limbs
var capsuleCollider = gameObject.AddComponent<CapsuleCollider>();
capsuleCollider.center = Vector3.zero;
capsuleCollider.radius = 0.05f;
capsuleCollider.height = 0.3f;
```

### PhysicMaterial

```csharp
using UnityEngine;

public class RobotPhysics : MonoBehaviour
{
    public PhysicMaterial CreateMaterial()
    {
        PhysicMaterial mat = new PhysicMaterial("RobotMaterial");
        mat.dynamicFriction = 0.6f;
        mat.staticFriction = 0.6f;
        mat.frictionCombine = PhysicMaterialCombine.Average;
        mat.bounciness = 0.0f;
        return mat;
    }
}
```

## Joint Configuration

### Configurable Joint

```csharp
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class ConfigurableJointController : MonoBehaviour
{
    public Rigidbody connectedBody;
    public float linearLimit = 0.5f;
    public float angularLimitMin = -45f;
    public float angularLimitMax = 45f;

    private ConfigurableJoint joint;

    private void Reset()
    {
        joint = GetComponent<ConfigurableJoint>();
        if (joint == null) joint = gameObject.AddComponent<ConfigurableJoint>();
    }

    private void Awake()
    {
        if (connectedBody != null) joint.connectedBody = connectedBody;
        joint.linearLimit = linearLimit;
        joint.lowAngularXLimit = angularLimitMin;
        joint.highAngularXLimit = angularLimitMax;
    }
}
```

### Hinge Joint

```csharp
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class HingeJointController : MonoBehaviour
{
    public Rigidbody connectedBody;
    public Vector3 axis = Vector3.right;
    public float minLimit = -150f;
    public float maxLimit = 0f;

    private HingeJoint joint;

    private void Reset()
    {
        joint = GetComponent<HingeJoint>();
        if (joint == null) joint = gameObject.AddComponent<HingeJoint>();
    }

    private void Awake()
    {
        if (connectedBody != null) joint.connectedBody = connectedBody;
        joint.axis = axis;

        JointLimits limits = new JointLimits();
        limits.min = minLimit;
        limits.max = maxLimit;
        joint.limits = limits;
        joint.useLimits = true;
    }
}
```

## Scene Setup

```csharp
using UnityEngine;

public class RobotSceneSetup : MonoBehaviour
{
    public Material groundMaterial;
    public Vector3 spawnPosition = Vector3.zero;

    private void Start()
    {
        SetupEnvironment();
        SpawnRobot();
    }

    private void SetupEnvironment()
    {
        // Ground
        GameObject ground = GameObject.CreatePrimitive(PrimitiveType.Plane);
        ground.name = "Ground";
        ground.transform.position = Vector3.zero;
        ground.transform.localScale = new Vector3(10, 1, 10);

        // Lighting
        GameObject lightObj = new GameObject("Directional Light");
        Light light = lightObj.AddComponent<Light>();
        light.type = LightType.Directional;
        light.intensity = 1f;
        lightObj.transform.rotation = Quaternion.Euler(50f, -30f, 0f);
    }

    private void SpawnRobot()
    {
        // Robot creation handled by RobotBuilder
    }
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Robot falls through ground | Add Rigidbody + Collider |
| Joints unstable | Increase solver iterations |
| Robot collapses | Check joint connections |

## Summary

Unity physics requires Rigidbody and Collider components on each link, and Joint components for connections.

## Next Section

Proceed to [Character Controllers](./02-2-character-controllers.md)
