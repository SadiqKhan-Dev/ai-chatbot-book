---
sidebar_position: 0
---

# 3. Sensor Simulation

Implement realistic sensor models (camera, LiDAR, IMU) in Gazebo and Unity.

## Learning Objectives

By completing this section, you will be able to:

1. **Implement** camera sensors with realistic noise models in both Gazebo and Unity
2. **Configure** LiDAR sensors with appropriate beam patterns and range limitations
3. **Add** IMU sensors with drift and bias modeling
4. **Compare** sensor modeling approaches between simulation platforms
5. **Integrate** sensor data with robot control systems

## Estimated Time

**6 hours** (2 hours concepts, 4 hours tooling)

## Prerequisites

- Completion of Chapters 1 and 2
- Basic understanding of computer vision concepts

## Sub-pages

- [Sensor Concepts](./03-1-sensor-concepts.md) — Platform-agnostic sensor modeling fundamentals
- [Gazebo Sensors](./03-2-gazebo-sensors.md) — Camera, LiDAR, IMU in Gazebo
- [Unity Sensors](./03-3-unity-sensors.md) — Camera, LiDAR, IMU in Unity
- [Exercises](./03-4-exercises.md) — Hands-on practice with validation criteria

## Chapter Assessment

Complete the [Exercises](./03-4-exercises.md) section and quiz to verify understanding.

---

## Key Concepts

### Sensor Modeling Architecture

```
+------------------+     +------------------+     +------------------+
|   Physical       |     |   Sensor Model   |     |   Sensor Data    |
|   Phenomenon     | --> |   (Simulation)   | --> |   Output         |
+------------------+     +------------------+     +------------------+
                                |
                    +-----------+-----------+
                    |           |           |
              Noise Model   Failure Model   Delay Model
```

### Sensor Types Coverage

| Sensor Type | Gazebo Plugin | Unity Component | Output |
|-------------|---------------|-----------------|--------|
| Camera | `libgazebo_ros_camera.so` | `Camera` | Image (RGB/Depth) |
| LiDAR | `libgazebo_ros_laser.so` | Raycast | Point Cloud |
| IMU | `libgazebo_ros_imu.so` | `IMU` | Linear/Angular Accel |

## Next Section

Proceed to [Sensor Concepts](./03-1-sensor-concepts.md) to understand sensor modeling fundamentals.
