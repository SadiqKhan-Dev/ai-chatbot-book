---
sidebar_position: 2
---

# 2.2 Character Controllers

Humanoid motion configuration and interactive control systems.

## CharacterController vs. Rigidbody

| Aspect | CharacterController | Rigidbody |
|--------|---------------------|-----------|
| Movement | Direct transform | Physics forces |
| Collision | Capsule-based | Collider-based |
| Gravity | Manual | Automatic |
| Stairs | Built-in | Custom logic |

For robotics, use **Rigidbody-based movement**.

## Humanoid Animation System

```csharp
using UnityEngine;

public class RobotAnimator : MonoBehaviour
{
    public Animator animator;
    public float velocityFactor = 1.0f;

    private readonly string speedParam = "Speed";
    private readonly string isWalkingParam = "IsWalking";

    private Rigidbody rb;
    private Transform mainCamera;

    private void Awake()
    {
        rb = GetComponent<Rigidbody>();
        animator = GetComponent<Animator>();
        if (Camera.main != null) mainCamera = Camera.main.transform;
    }

    private void Update()
    {
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        Vector3 direction = new Vector3(horizontal, 0, vertical);

        float currentSpeed = direction.magnitude * velocityFactor;
        animator.SetFloat(speedParam, currentSpeed);
        animator.SetBool(isWalkingParam, currentSpeed > 0.1f);

        if (direction.magnitude > 0.1f)
        {
            float targetAngle = Mathf.Atan2(direction.x, direction.z) * Mathf.Rad2Deg +
                              mainCamera.eulerAngles.y;
            transform.rotation = Quaternion.Euler(0, targetAngle, 0);

            Vector3 moveDir = Quaternion.Euler(0, targetAngle, 0) * Vector3.forward;
            rb.MovePosition(rb.position + moveDir.normalized * currentSpeed * Time.deltaTime);
        }
    }
}
```

## Inverse Kinematics (CCD)

```csharp
using UnityEngine;

public class SimpleIK : MonoBehaviour
{
    public Transform target;
    public Transform[] joints;
    public Transform endEffector;

    public int iterations = 10;
    public float learningRate = 10f;
    public float distanceThreshold = 0.01f;

    private void LateUpdate()
    {
        if (target == null || joints.Length == 0) return;

        for (int i = 0; i < iterations; i++)
        {
            SolveIK();
            if (Vector3.Distance(endEffector.position, target.position) < distanceThreshold) break;
        }
    }

    private void SolveIK()
    {
        for (int i = joints.Length - 1; i >= 0; i--)
        {
            Vector3 endPos = endEffector.position;
            Vector3 toTarget = target.position - joints[i].position;
            Quaternion rotation = Quaternion.FromToRotation(endPos - joints[i].position, toTarget);
            joints[i].rotation = rotation * joints[i].rotation;
        }
    }
}
```

## Joint Position Controller

```csharp
using UnityEngine;

public class JointPositionController : MonoBehaviour
{
    public ConfigurableJoint joint;
    public Transform targetTransform;

    public float proportionalGain = 100f;
    public float derivativeGain = 10f;
    public float maximumVelocity = 10f;

    private Rigidbody rb;

    private void Awake()
    {
        rb = GetComponent<Rigidbody>();
    }

    private void FixedUpdate()
    {
        if (joint == null || targetTransform == null) return;

        Vector3 positionError = transform.InverseTransformDirection(
            targetTransform.position - transform.position);

        Vector3 velocityError = transform.InverseTransformDirection(rb.linearVelocity);

        Vector3 force = (positionError * proportionalGain) - (velocityError * derivativeGain);

        rb.AddRelativeForce(Vector3.ClampMagnitude(force, maximumVelocity));
    }
}
```

## Interactive Control

```csharp
using UnityEngine;

public class RobotManipulator : MonoBehaviour
{
    public ConfigurableJoint leftGripper;
    public ConfigurableJoint rightGripper;
    public float gripSpeed = 5f;

    private float currentGripPosition = 0f;

    private void Update()
    {
        if (Input.GetKey(KeyCode.Space))
        {
            currentGripPosition = Mathf.MoveTowards(currentGripPosition, 1f, gripSpeed * Time.deltaTime);
            CloseGrip();
        }
        else
        {
            currentGripPosition = Mathf.MoveTowards(currentGripPosition, 0f, gripSpeed * Time.deltaTime);
            OpenGrip();
        }
    }

    private void CloseGrip()
    {
        // Gripper closing logic
    }

    private void OpenGrip()
    {
        // Gripper opening logic
    }
}
```

## Summary

Character controllers enable humanoid motion with Animator state machines, IK for end effectors, and joint PID controllers.

## Next Section

Proceed to [Exercises](./02-3-exercises.md)
