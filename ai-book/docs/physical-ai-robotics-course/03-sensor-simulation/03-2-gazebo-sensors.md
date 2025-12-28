---
sidebar_position: 2
---

# 3.2 Gazebo Sensors

Camera, LiDAR, and IMU sensor configuration in Gazebo.

## Gazebo Sensor Plugin Architecture

### Plugin Types

```
Gazebo Sensor Plugins
├── Camera Plugins
│   ├── libgazebo_ros_camera.so
│   ├── libgazebo_ros_multicamera.so
│   └── libgazebo_ros_openni_kinect.so
│
├── Laser Plugins
│   ├── libgazebo_ros_laser.so (2D)
│   ├── libgazebo_ros_ray_sensor.so (3D)
│   └── libgazebo_ros_gpu_laser.so
│
├── IMU Plugins
│   └── libgazebo_ros_imu.so
│
└── Contact Plugins
    └── libgazebo_ros_bumper.so
```

### Plugin Configuration Pattern

```xml
<sensor name="sensor_name" type="sensor_type">
  <plugin name="plugin_name" filename="libgazebo_ros_sensor.so">
    <!-- ROS parameters -->
    <ros>
      <namespace>/robot</namespace>
      <argument>~topic:=sensor_data</argument>
    </ros>
    <!-- Update rate -->
    <update_rate>30</update_rate>
    <!-- Sensor-specific parameters -->
    <parameter1>value1</parameter1>
  </plugin>
</sensor>
```

## Camera Sensor Configuration

### Basic RGB Camera

```xml
<sensor name="camera" type="camera">
  <pose>0 0 1.5 0 0 0</pose>
  <camera>
    <horizontal_fov>1.047</horizontal_fov>  <!-- ~60 degrees -->
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>100</far>
    </clip>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.007</stddev>
    </noise>
  </camera>
  <plugin name="camera_plugin" filename="libgazebo_ros_camera.so">
    <ros>
      <namespace>/humanoid</namespace>
      <argument>~image_raw:=camera/image_raw</argument>
      <argument>~camera_info:=camera/camera_info</argument>
    </ros>
    <camera_name>head_camera</camera_name>
  </plugin>
</sensor>
```

### Depth Camera with Point Cloud

```xml
<sensor name="depth_camera" type="depth">
  <pose>0 0 1.5 0 0 0</pose>
  <camera>
    <horizontal_fov>1.047</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.5</near>
      <far>10</far>
    </clip>
  </camera>
  <plugin name="depth_camera_plugin" filename="libgazebo_ros_openni_kinect.so">
    <ros>
      <namespace>/humanoid</namespace>
      <argument>~depth/image_raw:=depth/image</argument>
      <argument>~depth/camera_info:=depth/camera_info</argument>
      <argument>~depth/points:=depth/points</argument>
    </ros>
    <camera_name>head_depth</camera_name>
    <depth_registration>true</depth_registration>
  </plugin>
</sensor>
```

### Stereo Camera Setup

```xml
<sensor name="left_camera" type="camera">
  <pose>0 0.06 1.5 0 0 0</pose>
  <camera>
    <horizontal_fov>1.047</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
    </image>
    <clip>
      <near>0.1</near>
      <far>50</far>
    </clip>
  </camera>
  <plugin name="left_camera_plugin" filename="libgazebo_ros_camera.so">
    <ros>
      <namespace>/humanoid</namespace>
      <argument>~left/image_raw:=stereo/left/image</argument>
    </ros>
    <camera_name>stereo_left</camera_name>
  </plugin>
</sensor>

<sensor name="right_camera" type="camera">
  <pose>0 -0.06 1.5 0 0 0</pose>
  <camera>
    <horizontal_fov>1.047</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
    </image>
    <clip>
      <near>0.1</near>
      <far>50</far>
    </clip>
  </camera>
  <plugin name="right_camera_plugin" filename="libgazebo_ros_camera.so">
    <ros>
      <namespace>/humanoid</namespace>
      <argument>~right/image_raw:=stereo/right/image</argument>
    </ros>
    <camera_name>stereo_right</camera_name>
  </plugin>
</sensor>
```

### Camera with Distortion

```xml
<sensor name="camera_with_distortion" type="camera">
  <pose>0 0 1.5 0 0 0</pose>
  <camera>
    <horizontal_fov>1.2</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
    </image>
    <clip>
      <near>0.1</near>
      <far>100</far>
    </clip>
    <distortion>
      <k1>-0.15</k1>
      <k2>0.03</k2>
      <k3>0.0</k3>
      <p1>0.0</p1>
      <p2>0.0</p2>
      <center>0.5 0.5</center>
    </distortion>
  </camera>
  <plugin name="distorted_camera_plugin" filename="libgazebo_ros_camera.so">
    <ros>
      <namespace>/humanoid</namespace>
    </ros>
    <camera_name>distorted</camera_name>
  </plugin>
</sensor>
```

## LiDAR Sensor Configuration

### 2D LiDAR (Hokuyo-style)

```xml
<sensor name="hokuyo" type="ray">
  <pose>0 0 1.3 0 0 0</pose>
  <ray>
    <scan>
      <horizontal>
        <samples>1080</samples>
        <resolution>1</resolution>
        <min_angle>-2.356</min_angle>  <!-- -135 degrees -->
        <max_angle>2.356</max_angle>   <!-- +135 degrees -->
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>10.0</max>
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
    <output_type>sensor_msgs/LaserScan</output_type>
  </plugin>
</sensor>
```

### 3D LiDAR (Velodyne-style)

```xml
<sensor name="velodyne" type="ray">
  <pose>0 0 1.5 0 0 0</pose>
  <ray>
    <scan>
      <horizontal>
        <samples>360</samples>
        <resolution>1</resolution>
        <min_angle>0</min_angle>
        <max_angle>6.283</max_angle>  <!-- 360 degrees -->
      </horizontal>
      <vertical>
        <samples>16</samples>
        <resolution>1</resolution>
        <min_angle>-0.261</min_angle>  <!-- -15 degrees -->
        <max_angle>0.261</max_angle>    <!-- +15 degrees -->
      </vertical>
    </scan>
    <range>
      <min>0.5</min>
      <max>100</max>
      <resolution>0.01</resolution>
    </range>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.03</stddev>
    </noise>
  </ray>
  <plugin name="gpu_laser_plugin" filename="libgazebo_ros_gpu_laser.so">
    <ros>
      <namespace>/humanoid</namespace>
      <argument>~scan:=lidar/points</argument>
    </ros>
    <output_type>sensor_msgs/PointCloud2</output_type>
    <organize_cloud>true</organize_cloud>
  </plugin>
</sensor>
```

### LiDAR with Ring Configuration

```xml
<!-- Custom 32-beam LiDAR configuration -->
<sensor name="custom_lidar" type="ray">
  <pose>0 0 1.5 0 0 0</pose>
  <ray>
    <scan>
      <horizontal>
        <samples>2000</samples>
        <resolution>1</resolution>
        <min_angle>-3.14159</min_angle>
        <max_angle>3.14159</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>80</max>
      <resolution>0.005</resolution>
    </range>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.02</stddev>
    </noise>
  </ray>
  <!-- Vertical angles for 32 beams -->
  <plugin name="multibeam_plugin" filename="libgazebo_ros_ray_sensor.so">
    <ros>
      <namespace>/humanoid</namespace>
      <argument>~scan:=lidar/scan</argument>
    </ros>
    <output_type>sensor_msgs/LaserScan</output_type>
  </plugin>
</sensor>
```

## IMU Sensor Configuration

### Basic IMU

```xml
<sensor name="imu" type="imu">
  <pose>0 0 1.5 0 0 0</pose>
  <imu>
    <noise>
      <type>gaussian</type>
      <rate>
        <mean>0.0</mean>
        <stddev>0.0001</stddev>
      </rate>
      <accel>
        <mean>0.0</mean>
        <stddev>0.02</stddev>
      </accel>
    </noise>
  </imu>
  <plugin name="imu_plugin" filename="libgazebo_ros_imu.so">
    <ros>
      <namespace>/humanoid</namespace>
      <argument>~imu:=imu/data</argument>
    </ros>
    <topicName>imu/data</topicName>
    <bodyName>imu_link</bodyName>
    <frameName>imu_link</frameName>
    <yaw_offset>1.5708</yaw_offset>
    <gaussian_noise>0.01</gaussian_noise>
  </plugin>
</sensor>
```

### IMU with Custom Noise Parameters

```xml
<sensor name="high_precision_imu" type="imu">
  <pose>0 0 1.5 0 0 0</pose>
  <imu>
    <angular_velocity>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.0001</stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.0001</stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.0001</stddev>
        </noise>
      </z>
    </angular_velocity>
    <linear_acceleration>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.01</stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.01</stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.01</stddev>
        </noise>
      </z>
    </linear_acceleration>
  </imu>
  <plugin name="imu_plugin" filename="libgazebo_ros_imu.so">
    <ros>
      <namespace>/humanoid</namespace>
      <argument>~data:=imu/data</argument>
    </ros>
    <bodyName>imu_link</bodyName>
    <frameName>imu_link</frameName>
  </plugin>
</sensor>
```

## Complete Humanoid Sensor Package

```xml
<?xml version="1.0"?>
<robot name="humanoid_with_sensors" xmlns:xacro="http://wiki.ros.org/xacro">

  <!-- ===== HEAD SENSOR ARRAY ===== -->
  <link name="head_link">
    <!-- RGB Camera (left eye) -->
    <sensor name="camera_left" type="camera">
      <pose>0.03 0.06 0.0 0 0 0</pose>
      <camera>
        <horizontal_fov>1.047</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
        </image>
        <clip>
          <near>0.1</near>
          <far>50</far>
        </clip>
      </camera>
      <plugin name="cam_left" filename="libgazebo_ros_camera.so">
        <ros>
          <namespace>/humanoid/head</namespace>
          <argument>~image_raw:=camera/left/image</argument>
        </ros>
        <camera_name>left_camera</camera_name>
      </plugin>
    </sensor>

    <!-- RGB Camera (right eye) -->
    <sensor name="camera_right" type="camera">
      <pose>0.03 -0.06 0.0 0 0 0</pose>
      <camera>
        <horizontal_fov>1.047</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
        </image>
        <clip>
          <near>0.1</near>
          <far>50</far>
        </clip>
      </camera>
      <plugin name="cam_right" filename="libgazebo_ros_camera.so">
        <ros>
          <namespace>/humanoid/head</namespace>
          <argument>~image_raw:=camera/right/image</argument>
        </ros>
        <camera_name>right_camera</camera_name>
      </plugin>
    </sensor>

    <!-- LiDAR (forehead) -->
    <sensor name="head_lidar" type="ray">
      <pose>0.05 0 0.0 0 0 0</pose>
      <ray>
        <scan>
          <horizontal>
            <samples>720</samples>
            <resolution>1</resolution>
            <min_angle>-1.57</min_angle>
            <max_angle>1.57</max_angle>
          </horizontal>
          <vertical>
            <samples>1</samples>
            <resolution>1</resolution>
            <min_angle>0</min_angle>
            <max_angle>0</max_angle>
          </vertical>
        </scan>
        <range>
          <min>0.1</min>
          <max>20</max>
          <resolution>0.01</resolution>
        </range>
      </ray>
      <plugin name="lidar_plugin" filename="libgazebo_ros_laser.so">
        <ros>
          <namespace>/humanoid/head</namespace>
          <argument>~scan:=lidar/scan</argument>
        </ros>
      </plugin>
    </sensor>

    <!-- IMU (inside head) -->
    <sensor name="head_imu" type="imu">
      <pose>0.02 0 0.0 0 0 0</pose>
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
          <namespace>/humanoid/head</namespace>
          <argument>~data:=imu/data</argument>
        </ros>
        <bodyName>head_link</bodyName>
      </plugin>
    </sensor>
  </link>

  <!-- ===== BODY SENSOR ARRAY ===== -->
  <link name="torso_link">
    <!-- Chest-mounted LiDAR -->
    <sensor name="chest_lidar" type="ray">
      <pose>0 0 0.2 0 -0.3 0</pose>
      <ray>
        <scan>
          <horizontal>
            <samples>1080</samples>
            <resolution>1</resolution>
            <min_angle>-2.356</min_angle>
            <max_angle>2.356</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.5</min>
          <max>30</max>
          <resolution>0.02</resolution>
        </range>
      </ray>
      <plugin name="chest_lidar_plugin" filename="libgazebo_ros_laser.so">
        <ros>
          <namespace>/humanoid/torso</namespace>
          <argument>~scan:=lidar/scan</argument>
        </ros>
      </plugin>
    </sensor>

    <!-- IMU (center torso) -->
    <sensor name="torso_imu" type="imu">
      <pose>0 0 0.1 0 0 0</pose>
      <imu>
        <noise>
          <type>gaussian</type>
          <rate>
            <mean>0.0</mean>
            <stddev>0.0002</stddev>
          </rate>
          <accel>
            <mean>0.0</mean>
            <stddev>0.02</stddev>
          </accel>
        </noise>
      </imu>
      <plugin name="torso_imu_plugin" filename="libgazebo_ros_imu.so">
        <ros>
          <namespace>/humanoid/torso</namespace>
          <argument>~data:=imu/data</argument>
        </ros>
        <bodyName>torso_link</bodyName>
      </plugin>
    </sensor>
  </link>

</robot>
```

## Sensor Data Visualization

### RViz Configuration

```
Display types for sensor visualization:
├── Image:               /humanoid/head/camera_left/image_raw
├── Camera:              (overlay on 3D view)
├── LaserScan:           /humanoid/head/lidar/scan
├── PointCloud2:         /humanoid/head/lidar/points
└-- IMU:                 /humanoid/head/imu/data
        └── Arrow:       orientation
        └── Axes:        reference frame
```

### RViz Display Config

```yaml
# humanoid_sensors.rviz
Panels:
  - Class: rviz/Displays
    Help Height: 78
    Name: Displays
    Property Tree Widget:
      Expanded:
        - /Global Options1
        - /Status1
        - /Camera1
        - /LaserScan1
        - /IMU1
    Splitter Ratio: 0.5

Visualization Manager:
  Class: ""
  Displays:
    - Alpha: 0.5
      Class: rviz/Grid
      Enabled: true
      Name: Grid
    - Class: rviz/Image
      Enabled: true
      Name: Camera
      Image Topic: /humanoid/head/camera_left/image_raw
      Queue Size: 2
    - Class: rviz/LaserScan
      Enabled: true
      Name: LaserScan
      Topic: /humanoid/head/lidar/scan
      Size: 0.1
      Color: 255; 0; 0
    - Class: rviz/IMU
      Enabled: true
      Name: IMU
      Topic: /humanoid/head/imu/data
      Scale: 0.5
```

## Troubleshooting

### Sensor Not Publishing

1. Check plugin filename is correct
2. Verify ROS namespace is valid
3. Check Gazebo console for plugin load errors
4. Verify sensor `<pose>` is in correct frame

### Noisy Measurements

1. Adjust noise parameters in SDF
2. Increase update_rate for smoother data
3. Check for missing inertial properties on links

### TF Errors

1. Ensure `bodyName` matches link name
2. Verify static transform publisher for sensor frame
3. Check TF tree with `rosrun rqt_tf_tree rqt_tf_tree`

## Summary

Gazebo sensor configuration requires:
- Understanding plugin architecture and SDF syntax
- Proper sensor pose calibration
- Noise parameter tuning for realism
- ROS topic naming and namespace configuration

## Next Section

Proceed to [Unity Sensors](./03-3-unity-sensors.md) for Unity-specific implementation.
