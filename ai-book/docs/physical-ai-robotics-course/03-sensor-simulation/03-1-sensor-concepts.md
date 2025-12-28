---
sidebar_position: 1
---

# 3.1 Sensor Concepts

Platform-agnostic fundamentals of sensor modeling for robotics simulation.

## Sensor Modeling Fundamentals

### Ideal vs. Realistic Sensors

| Aspect | Ideal Sensor | Realistic Sensor |
|--------|--------------|------------------|
| Noise | None | Present (thermal, shot, etc.) |
| Range | Infinite | Limited (hardware specs) |
| Latency | Zero | Non-zero (processing time) |
| Accuracy | Perfect | Error bounds (specs) |
| Failure Modes | None | Possible (occlusion, saturation) |

### Sensor Error Categories

```
Sensor Error Sources
├── Systematic Errors (calibratable)
│   ├── Offset/bias
│   ├── Scale factor error
│   └── Non-orthogonality
│
├── Random Errors (stochastic)
│   ├── White noise
│   ├── 1/f noise (flicker)
│   └── Random walk
│
└── Failure Modes
    ├── Dropout
    ├── Saturation
    └── Outlier/spike
```

## Camera Models

### Pinhole Camera Model

```
World Point (X, Y, Z)
       \
        \  Perspective projection
         \
          +-----> Image Plane (u, v)
          |
    Camera Center (Cx, Cy)
```

### Camera Intrinsics

The camera projection equation:

```
u = fx * (X/Z) + cx
v = fy * (Y/Z) + cy
```

Where:
- fx, fy = focal lengths (pixels)
- cx, cy = principal point (pixels)

### Distortion Models

#### Radial Distortion

```
r² = u² + v²
u_distorted = u * (1 + k1*r² + k2*r⁴ + k3*r⁶)
v_distorted = v * (1 + k1*r² + k2*r⁴ + k3*r⁶)
```

#### Tangential Distortion

```
u_distorted = u + 2*p1*u*v + p2*(r² + 2*u²)
v_distorted = v + p1*(r² + 2*v²) + 2*p2*u*v
```

### Camera Noise Models

```python
# Gaussian noise model for camera
class CameraNoiseModel:
    def __init__(self, sigma_read=0.01, sigma_shot=0.01):
        self.sigma_read = sigma_read   # Read noise (electrons)
        self.sigma_shot = sigma_shot   # Shot noise (photon)

    def apply(self, image):
        """Apply noise to image."""
        # Read noise (Gaussian, independent of signal)
        read_noise = np.random.normal(0, self.sigma_read, image.shape)

        # Shot noise (Poisson, signal-dependent)
        shot_noise = np.random.poisson(image) - image

        # Combine
        noisy_image = image + read_noise + shot_noise * self.sigma_shot

        return np.clip(noisy_image, 0, 255)
```

## Depth Sensing Principles

### Stereo Depth Estimation

```
Left Camera          Right Camera
    O----------------------O  Baseline: b
    | \                  / |
    |   \              /   |
    |     \          /     |
    |       \      /       |
    |         \  /         |
    +----------X-----------+  Depth: Z = f * b / disp
         Disparity: d
```

### Time-of-Flight (ToF)

```
光源 ----> 物体 ----> 传感器
 |                    |
 |----t--------------|  飞行时间 t = 2D/c
 |                   |
 测量相位偏移Δφ       c = 3×10⁸ m/s

距离 D = c * Δφ / (4πf)
```

## LiDAR Principles

### Scanning Patterns

#### 2D LiDAR (Planar)

```
        ^ Y (forward)
        |
        |
        +----> X (right)
   Scan line at height h
```

#### 3D LiDAR (Multi-beam)

```
      Top view              Side view
    +-------+            +-------+
    |       |            |   o   |
    |   o   |            |   |   |
    | ||||| |            |   |   |
    | ||||| |            |   o   |
    +-------+            +-------+
    (beams)              (fov)
```

### LiDAR Specifications

| Parameter | Typical Value | Description |
|-----------|---------------|-------------|
| Range | 0.1 - 200m | Maximum detection range |
| FOV (horizontal) | 360° / 120° | Horizontal coverage |
| FOV (vertical) | 30° / 40° | Vertical coverage |
| Points/second | 100k - 2M | Scan density |
| Accuracy | ±2-5cm | Range measurement error |

### LiDAR Noise Model

```python
class LidarNoiseModel:
    def __init__(self, range_std=0.02, angular_std=0.001, dropout_rate=0.001):
        self.range_std = range_std      # Range measurement std (m)
        self.angular_std = angular_std  # Angular noise (rad)
        self.dropout_rate = dropout_rate  # Missed detection rate

    def apply(self, ranges, angles):
        """Apply noise to LiDAR measurements."""
        n = len(ranges)

        # Range noise (Gaussian)
        range_noise = np.random.normal(0, self.range_std, n)

        # Angular noise
        angle_noise = np.random.normal(0, self.angular_std, n)

        # Dropout (false negatives)
        dropout_mask = np.random.random(n) < self.dropout_rate

        # Apply noise
        noisy_ranges = np.where(dropout_mask, np.inf, ranges + range_noise)

        return noisy_ranges, angles + angle_noise
```

## IMU Fundamentals

### IMU Composition

```
IMU Chip
+-------+-------+
|  Gyro |  Accel|
|  (3)  |  (3)  |
+-------+-------+
    |
    +-- Temperature sensor
    +-- Magnetometer (optional)
```

### Accelerometer Model

```
measured_accel = true_accel + bias_accel + noise_accel + gravity_error

Where:
- bias_accel = bias + bias_drift
- noise_accel = white_noise * sqrt(dt)
- gravity_error = misalignment * g
```

### Gyroscope Model

```
measured_omega = true_omega + bias_gyro + noise_gyro

Where:
- bias_gyro = bias + bias_random_walk
- noise_gyro = white_noise * sqrt(dt)
```

### IMU Noise Parameters (Allan Variance)

| Noise Source | Symbol | Units |
|--------------|--------|-------|
| Quantization | Q | LSB |
| White Noise | N | °/√h or mg/√Hz |
| Bias Instability | B | °/h or mg |
| Rate Random Walk | K | °/√h² |
| Angular Random Walk | K | °/√h |

### IMU Simulation Model

```python
class IMUModel:
    def __init__(self, accel_noise_density=0.002,
                 gyro_noise_density=0.001,
                 accel_bias_stability=0.001,
                 gyro_bias_stability=0.001):
        # Noise densities (white noise)
        self.accel_nsd = accel_noise_density  # m/s²/√Hz
        self.gyro_nsd = gyro_noise_density    # rad/s/√Hz

        # Bias stability (random walk)
        self.accel_bs = accel_bias_stability  # m/s²/√Hz
        self.gyro_bs = gyro_bias_stability    # rad/s/√Hz

    def measure(self, true_accel, true_omega, dt):
        """Generate IMU measurement."""
        # White noise
        accel_noise = np.random.normal(0, self.accel_nsd * np.sqrt(1/dt))
        gyro_noise = np.random.normal(0, self.gyro_nsd * np.sqrt(1/dt))

        # Bias random walk (simplified)
        accel_bias = np.random.normal(0, self.accel_bs * np.sqrt(dt))
        gyro_bias = np.random.normal(0, self.gyro_bs * np.sqrt(dt))

        # Add gravity (simplified, assumes z-up)
        gravity = np.array([0, 0, 9.81])

        measured_accel = true_accel + accel_bias + accel_noise + gravity
        measured_omega = true_omega + gyro_bias + gyro_noise

        return measured_accel, measured_omega
```

## Sensor Data Formats

### Image Data

| Format | Channels | Data Type | Range |
|--------|----------|-----------|-------|
| RGB | 3 | uint8 | 0-255 |
| RGBA | 4 | uint8 | 0-255 |
| Grayscale | 1 | uint8 | 0-255 |
| Depth | 1 | float32 | meters |

### Point Cloud Data

```python
# PCL PointXYZ format
point = {
    'x': float32,  # meters
    'y': float32,
    'z': float32,
    'intensity': float32,  # optional
    'ring': int16,         # LiDAR ring index
    'time': float32        # timestamp
}
```

### IMU Data

```python
# ROS IMU message format
imu_message = {
    'header': {
        'frame_id': 'imu_link',
        'stamp': timestamp
    },
    'orientation': quaternion,     # optional
    'orientation_covariance': [9],  # 3x3, -1 if unknown
    'angular_velocity': vector3,   # rad/s
    'angular_velocity_covariance': [9],
    'linear_acceleration': vector3, # m/s²
    'linear_acceleration_covariance': [9]
}
```

## Cross-Platform Sensor Comparison

| Aspect | Gazebo | Unity |
|--------|--------|-------|
| Camera Plugin | `libgazebo_ros_camera.so` | Unity Camera + post-processing |
| Depth Sensing | Plugin with noise models | Depth Buffer + Shader |
| LiDAR Plugin | `libgazebo_ros_laser.so` | Raycast + custom script |
| IMU Plugin | `libgazebo_ros_imu.so` | `UnityEngine.Device.Sensors` |
| Noise Modeling | Plugin parameters | C# scripts |
| Data Output | ROS topics | C# events, ROS# bridge |

## Summary

Sensor simulation requires understanding:
- Ideal vs. realistic sensor characteristics
- Camera models (intrinsics, distortion, noise)
- LiDAR scanning patterns and error sources
- IMU noise parameters (bias, random walk)
- Cross-platform implementation differences

## Next Sections

- [Gazebo Sensors](./03-2-gazebo-sensors.md) — Platform-specific implementation
- [Unity Sensors](./03-3-unity-sensors.md) — Unity-specific implementation
