---
sidebar_position: 4
---

# 3.4 Exercises

Hands-on practice with sensor simulation in both Gazebo and Unity.

## Exercise 1: Configure Camera Sensors in Gazebo

**Objective**: Add and configure RGB and depth cameras on a humanoid robot

### Task

Add a head-mounted camera to the humanoid URDF:

1. Add camera sensor to head link
2. Configure image parameters (resolution, FOV)
3. Add noise model
4. Set up ROS topic publishing

### Camera Configuration

```xml
<!-- Add to head_link -->
<sensor name="head_camera" type="camera">
  <pose>0.05 0 0.1 0 0 0</pose>
  <camera>
    <horizontal_fov>1.047</horizontal_fov>  <!-- 60 degrees -->
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>50</far>
    </clip>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.01</stddev>
    </noise>
  </camera>
  <plugin name="camera_plugin" filename="libgazebo_ros_camera.so">
    <ros>
      <namespace>/humanoid</namespace>
      <argument>~image_raw:=camera/image</argument>
      <argument>~camera_info:=camera/camera_info</argument>
    </ros>
    <camera_name>head</camera_name>
  </plugin>
</sensor>
```

### Validation Criteria

- [ ] Camera sensor appears in Gazebo model
- [ ] `/humanoid/camera/image` topic publishes image data
- [ ] Image resolution matches configuration
- [ ] Camera info topic publishes intrinsics
- [ ] Rviz can display camera image overlay

---

## Exercise 2: Set Up LiDAR with Realistic Beam Patterns

**Objective**: Configure a multi-beam LiDAR sensor

### Task

Add a 2D scanning LiDAR to the robot:

1. Configure horizontal scan parameters
2. Set range limits and resolution
3. Add beam noise model
4. Verify point cloud output

### LiDAR Configuration

```xml
<sensor name="hokuyo_lidar" type="ray">
  <pose>0 0 1.3 0 0 0</pose>
  <ray>
    <scan>
      <horizontal>
        <samples>1080</samples>
        <resolution>1</resolution>
        <min_angle>-2.356</min_angle>  <!-- -135 deg -->
        <max_angle>2.356</max_angle>   <!-- +135 deg -->
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>30.0</max>
      <resolution>0.01</resolution>
    </range>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.02</stddev>
    </noise>
  </ray>
  <plugin name="laser_plugin" filename="libgazebo_ros_laser.so">
    <ros>
      <namespace>/humanoid</namespace>
      <argument>~scan:=lidar/scan</argument>
    </ros>
  </plugin>
</sensor>
```

### Validation Commands

```bash
# Check topic is publishing
rostopic hz /humanoid/lidar/scan

# View laser scan data
rosrun rviz rviz
# Add LaserScan display with topic /humanoid/lidar/scan

# Record data
rosbag record /humanoid/lidar/scan
```

### Validation Criteria

- [ ] LiDAR topic publishes at expected rate
- [ ] Scan covers expected horizontal range
- [ ] Range measurements are accurate
- [ ] RViz displays point cloud correctly

---

## Exercise 3: Implement IMU with Noise Modeling

**Objective**: Add and configure an IMU sensor

### Task

Add an IMU sensor to the torso link:

1. Configure gyroscope parameters
2. Configure accelerometer parameters
3. Add noise models
4. Verify IMU data output

### IMU Configuration

```xml
<sensor name="torso_imu" type="imu">
  <pose>0 0 0.2 0 0 0</pose>
  <imu>
    <noise>
      <type>gaussian</type>
      <rate>
        <mean>0.0</mean>
        <stddev>0.0002</stddev>
      </rate>
      <accel>
        <mean>0.0</mean>
        <stddev>0.03</stddev>
      </accel>
    </noise>
  </imu>
  <plugin name="imu_plugin" filename="libgazebo_ros_imu.so">
    <ros>
      <namespace>/humanoid</namespace>
      <argument>~data:=imu/data</argument>
    </ros>
    <bodyName>torso_link</bodyName>
    <gaussian_noise>0.0</gaussian_noise>
  </plugin>
</sensor>
```

### Validation Commands

```bash
# View IMU data
rostopic echo /humanoid/imu/data

# Check TF transforms
rosrun rqt_tf_tree rqt_tf_tree

# Visualize orientation
rosrun rviz rviz
# Add IMU display
```

### Validation Criteria

- [ ] IMU topic publishes at expected rate
- [ ] Accelerometer reads ~9.81 m/s² when stationary
- [ ] Gyroscope reads near zero when stationary
- [ ] Orientation changes with robot movement

---

## Exercise 4: Add Sensors to Unity Humanoid

**Objective**: Implement camera, LiDAR, and IMU in Unity

### Task

Create a sensor package for Unity:

1. Add CameraSensor component
2. Add LidarSensor component
3. Add IMUSensor component
4. Configure output for each sensor

### Unity Scene Setup

```csharp
using UnityEngine;

public class RobotSensorSetup : MonoBehaviour
{
    [Header("Sensors")]
    public bool enableCamera = true;
    public bool enableLidar = true;
    public bool enableIMU = true;

    [Header("Camera Settings")]
    public int cameraWidth = 640;
    public int cameraHeight = 480;
    public float cameraFOV = 60f;

    [Header("LiDAR Settings")]
    public int lidarSamples = 720;
    public float lidarRange = 30f;
    public int lidarVerticalSamples = 1;

    [Header("IMU Settings")]
    public float imuRate = 100f;
    public Vector3 accelNoise = new Vector3(0.02f, 0.02f, 0.02f);
    public Vector3 gyroNoise = new Vector3(0.0001f, 0.0001f, 0.0001f);

    private void Start()
    {
        if (enableCamera) SetupCamera();
        if (enableLidar) SetupLidar();
        if (enableIMU) SetupIMU();
    }

    private void SetupCamera()
    {
        GameObject cameraObj = new GameObject("HeadCamera");
        cameraObj.transform.parent = transform;
        cameraObj.transform.localPosition = new Vector3(0.05f, 0.1f, 0);

        CameraSensor cam = cameraObj.AddComponent<CameraSensor>();
        cam.width = cameraWidth;
        cam.height = cameraHeight;
        cam.fieldOfView = cameraFOV;
    }

    private void SetupLidar()
    {
        GameObject lidarObj = new GameObject("HeadLiDAR");
        lidarObj.transform.parent = transform;
        lidarObj.transform.localPosition = new Vector3(0.05f, 0.15f, 0);

        LidarSensor lidar = lidarObj.AddComponent<LidarSensor>();
        lidar.horizontalSamples = lidarSamples;
        lidar.maxRange = lidarRange;
        lidar.verticalSamples = lidarVerticalSamples;
    }

    private void SetupIMU()
    {
        GameObject imuObj = new GameObject("TorsoIMU");
        imuObj.transform.parent = transform;
        imuObj.transform.localPosition = new Vector3(0, 0.2f, 0);

        IMUSensor imu = imuObj.AddComponent<IMUSensor>();
        imu.updateRate = imuRate;
        imu.accelerometerNoise = accelNoise;
        imu.gyroscopeNoise = gyroNoise;
    }
}
```

### Validation Criteria

- [ ] Camera captures and displays image
- [ ] LiDAR shows raycast visualization
- [ ] IMU outputs data in OnIMUData callback
- [ ] All sensors update at configured rates

---

## Exercise 5: Compare Sensor Outputs Between Platforms

**Objective**: Run same scenario in Gazebo and Unity, compare outputs

### Task

1. Create identical test scenario in both platforms
2. Place robot in same environment
3. Record sensor outputs from both
4. Compare accuracy and noise characteristics

### Comparison Framework

```csharp
using UnityEngine;
using System.Collections.Generic;
using System.IO;

public class SensorComparison : MonoBehaviour
{
    [Header("Reference Data (Gazebo)")]
    public TextAsset gazeboLidarCSV;
    public TextAsset gazeboCameraPNG;

    [Header("Unity Data")]
    public LidarSensor unityLidar;
    public CameraSensor unityCamera;

    [Header("Comparison Settings")]
    public float maxRangeError = 0.05f;
    public float maxAngleError = 0.01f;

    [Output]
    private List<float> rangeErrors = new List<float>();
    private StreamWriter reportFile;

    private void Start()
    {
        // Create comparison report
        reportFile = new StreamWriter("sensor_comparison_report.txt");
        reportFile.WriteLine("Sensor Comparison Report");
        reportFile.WriteLine("========================");
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.C))
        {
            CompareLidar();
        }
    }

    private void CompareLidar()
    {
        // Load Gazebo reference data
        string[] gazeboLines = gazeboLidarCSV.text.Split('\n');

        // Get Unity LiDAR data
        float[] unityRanges = unityLidar.GetLatestRanges();

        // Compare point by point
        int matchCount = 0;
        for (int i = 0; i < Mathf.Min(gazeboLines.Length, unityRanges.Length); i++)
        {
            float gazeboRange = float.Parse(gazeboLines[i]);
            float error = Mathf.Abs(gazeboRange - unityRanges[i]);

            rangeErrors.Add(error);

            if (error < maxRangeError)
            {
                matchCount++;
            }
        }

        // Generate report
        float accuracy = (float)matchCount / rangeErrors.Count * 100;

        reportFile.WriteLine($"LiDAR Comparison:");
        reportFile.WriteLine($"- Samples compared: {rangeErrors.Count}");
        reportFile.WriteLine($"- Within tolerance: {matchCount}");
        reportFile.WriteLine($"- Accuracy: {accuracy:F1}%");
        reportFile.WriteLine($"- Mean error: {GetMeanError():F4}m");
        reportFile.WriteLine($"- Max error: {GetMaxError():F4}m");

        Debug.Log($"Comparison complete. Accuracy: {accuracy:F1}%");
    }

    private float GetMeanError()
    {
        if (rangeErrors.Count == 0) return 0;
        float sum = 0;
        foreach (float e in rangeErrors) sum += e;
        return sum / rangeErrors.Count;
    }

    private float GetMaxError()
    {
        if (rangeErrors.Count == 0) return 0;
        float max = 0;
        foreach (float e in rangeErrors) if (e > max) max = e;
        return max;
    }

    private void OnDestroy()
    {
        if (reportFile != null)
        {
            reportFile.Close();
        }
    }
}
```

### Validation Criteria

- [ ] Test scenarios are identical in both platforms
- [ ] Sensor outputs are recorded and saved
- [ ] Comparison report is generated
- [ ] Differences are documented and explained

---

## Quiz: Sensor Simulation

### Question 1
What is the primary noise source in camera images?

A) Quantization noise
B) Shot noise (photon noise)
C) Read noise
D) All of the above

### Question 2
Which Gazebo plugin is used for LiDAR simulation?

A) libgazebo_ros_camera.so
B) libgazebo_ros_laser.so
C) libgazebo_ros_imu.so
D) libgazebo_ros_openni.so

### Question 3
What parameters define a LiDAR's vertical field of view?

A) Number of horizontal samples
B) Min and max vertical angles
C) Range resolution
D) Scan rate

### Question 4
In Unity, what component is used for depth sensing?

A) DepthBufferMode
B) DepthTextureMode
C) DepthCameraComponent
D) DepthSensorScript

### Question 5
What does IMU bias drift cause over time?

A) Increasing measurement noise
B) Slowly changing offset
C) Random spikes in data
D) Signal dropout

### Answer Key
1. D, 2. B, 3. B, 4. B, 5. B

---

## Summary

After completing these exercises, you should be able to:
- Configure camera sensors in Gazebo with proper parameters
- Set up LiDAR sensors with realistic beam patterns
- Implement IMU sensors with noise modeling
- Add sensor components to Unity robots
- Compare sensor outputs between platforms

## Next Section

Return to [Module Overview](../index.md) to continue with other modules.
