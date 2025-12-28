---
sidebar_position: 3
---

# 3.3 Unity Sensors

Camera, LiDAR, and IMU sensor simulation in Unity.

## Unity Sensor Architecture

### Sensor Components

```
Unity Sensor System
+------------------+
| Sensor Script    |  <-- C# component on GameObject
+------------------+
        |
        v
+------------------+
| Unity Component  |  <-- Camera, Raycast, etc.
+------------------+
        |
        v
+------------------+
| Data Output      |  <-- Events, topics (ROS#)
+------------------+
```

## Camera Simulation

### RGB Camera Implementation

```csharp
using UnityEngine;

public class CameraSensor : MonoBehaviour
{
    [Header("Camera Parameters")]
    public int width = 640;
    public int height = 480;
    public float focalLength = 800f;  // pixels
    public float fieldOfView = 60f;

    [Header("Noise")]
    public bool enableNoise = true;
    public float noiseStdDev = 0.01f;
    public float dropoutRate = 0.001f;

    [Header("Output")]
    public string topicName = "/camera/image_raw";

    [Events]
    public delegate void ImageCallback(Color32[] image);
    public event ImageCallback OnImageCaptured;

    private Texture2D texture;
    private Color32[] pixelData;
    private float[,] depthBuffer;
    private Camera cam;

    private void Start()
    {
        SetupCamera();
        InitializeBuffers();
    }

    private void SetupCamera()
    {
        cam = GetComponent<Camera>();
        if (cam == null)
        {
            cam = gameObject.AddComponent<Camera>();
        }

        cam.fieldOfView = fieldOfView;
        cam.nearClipPlane = 0.1f;
        cam.farClipPlane = 100f;
        cam.projectionMatrix = CalculateIntrinsics();
    }

    private Matrix4x4 CalculateIntrinsics()
    {
        float fovRad = fieldOfView * Mathf.Deg2Rad;
        float fy = height / (2 * Mathf.Tan(fovRad / 2));
        float fx = fy;  // Assuming square pixels

        Matrix4x4 intrinsics = Matrix4x4.identity;

        // Camera matrix (simplified, assumes principal point at center)
        intrinsics[0, 0] = fx;
        intrinsics[1, 1] = fy;
        intrinsics[0, 2] = width / 2f;
        intrinsics[1, 2] = height / 2f;
        intrinsics[2, 2] = 1f;

        return intrinsics;
    }

    private void InitializeBuffers()
    {
        texture = new Texture2D(width, height, TextureFormat.RGBA32, false);
        pixelData = new Color32[width * height];
        depthBuffer = new float[width, height];
    }

    private void OnRenderImage(RenderTexture source, RenderTexture destination)
    {
        if (enableNoise)
        {
            RenderTexture noisy = RenderTexture.GetTemporary(width, height);
            Graphics.Blit(source, noisy);
            AddNoise(noisy);
            Graphics.Blit(noisy, destination);
            RenderTexture.ReleaseTemporary(noisy);
        }
        else
        {
            Graphics.Blit(source, destination);
        }

        // Capture image data
        CopyImageData();
        OnImageCaptured?.Invoke(pixelData);
    }

    private void AddNoise(RenderTexture rt)
    {
        // Simple Gaussian noise
        RenderTexture temp = RenderTexture.GetTemporary(width, height);
        Texture2D noiseTex = GenerateNoiseTexture(width, height, noiseStdDev);

        Graphics.Blit(noiseTex, temp);
        Graphics.Blit(temp, rt, new Vector2(1, 0), new Vector2(0, 0));

        RenderTexture.ReleaseTemporary(temp);
        Object.Destroy(noiseTex);
    }

    private Texture2D GenerateNoiseTexture(int w, int h, float stdDev)
    {
        Texture2D noise = new Texture2D(w, h, TextureFormat.RGFloat, false);
        Color[] pixels = new Color[w * h];

        for (int i = 0; i < pixels.Length; i++)
        {
            float noiseVal = Mathf.PerlinNoise(
                Random.value * w, Random.value * h) - 0.5f;
            pixels[i] = new Color(noiseVal * stdDev, 0, 0, 0);
        }

        noise.SetPixels(pixels);
        noise.Apply();
        return noise;
    }

    private void CopyImageData()
    {
        RenderTexture.active = cam.activeTexture;
        texture.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        texture.Apply();
        pixelData = texture.GetPixels32();
        RenderTexture.active = null;
    }
}
```

### Depth Camera Implementation

```csharp
using UnityEngine;

public class DepthCameraSensor : MonoBehaviour
{
    [Header("Parameters")]
    public int width = 640;
    public int height = 480;
    public float minDepth = 0.5f;
    public float maxDepth = 10f;
    public bool enableNoise = true;
    public float depthNoiseStd = 0.02f;

    [Events]
    public delegate void DepthCallback(float[] depthImage);
    public delegate void PointCloudCallback(Vector3[] points);
    public event DepthCallback OnDepthCaptured;
    public event PointCloudCallback OnPointCloudGenerated;

    private float[] depthData;
    private Vector3[] pointCloud;
    private Camera cam;
    private Matrix4x4 intrinsics;

    private void Start()
    {
        SetupCamera();
        InitializeBuffers();
    }

    private void SetupCamera()
    {
        cam = GetComponent<Camera>();
        cam.nearClipPlane = minDepth;
        cam.farClipPlane = maxDepth;
        cam.depthTextureMode = DepthTextureMode.Depth;

        CalculateIntrinsics();
    }

    private void CalculateIntrinsics()
    {
        float fovRad = cam.fieldOfView * Mathf.Deg2Rad;
        float fy = height / (2 * Mathf.Tan(fovRad / 2));
        float fx = fy;

        intrinsics = Matrix4x4.identity;
        intrinsics[0, 0] = fx;
        intrinsics[1, 1] = fy;
        intrinsics[0, 2] = width / 2f;
        intrinsics[1, 2] = height / 2f;
    }

    private void InitializeBuffers()
    {
        depthData = new float[width * height];
        pointCloud = new Vector3[width * height];
    }

    private void Update()
    {
        CaptureDepth();
    }

    private void CaptureDepth()
    {
        // Get depth texture
        RenderTexture depthRT = RenderTexture.GetTemporary(width, height);
        Graphics.Blit(null, depthRT, new Material(Shader.Find("Hidden/DepthShader")));

        Texture2D depthTex = new Texture2D(width, height, TextureFormat.RFloat, false);
        RenderTexture.active = depthRT;
        depthTex.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        depthTex.Apply();
        RenderTexture.active = null;

        float[] rawDepth = depthTex.GetPixels().Select(p => p.r).ToArray();

        // Process depth data
        for (int i = 0; i < depthData.Length; i++)
        {
            float z = rawDepth[i] * (maxDepth - minDepth) + minDepth;

            if (enableNoise)
            {
                z += Random.Range(-1f, 1f) * depthNoiseStd;
            }

            depthData[i] = z;
        }

        OnDepthCaptured?.Invoke(depthData);

        // Generate point cloud
        GeneratePointCloud();

        RenderTexture.ReleaseTemporary(depthRT);
        Object.Destroy(depthTex);
    }

    private void GeneratePointCloud()
    {
        for (int v = 0; v < height; v++)
        {
            for (int u = 0; u < width; u++)
            {
                int idx = v * width + u;

                // Back-project
                float z = depthData[idx];
                float x = (u - intrinsics[0, 2]) / intrinsics[0, 0] * z;
                float y = (v - intrinsics[1, 2]) / intrinsics[1, 1] * z;

                pointCloud[idx] = new Vector3(x, -y, z);  // Flip Y for Unity
            }
        }

        OnPointCloudGenerated?.Invoke(pointCloud);
    }
}
```

## LiDAR Simulation

### Raycast-Based LiDAR

```csharp
using UnityEngine;
using System.Collections.Generic;

public class LidarSensor : MonoBehaviour
{
    [Header("Scan Parameters")]
    public int horizontalSamples = 720;
    public int verticalSamples = 32;
    public float horizontalFOV = 360f;
    public float verticalFOV = 40f;
    public float minRange = 0.1f;
    public float maxRange = 100f;
    public float rangeResolution = 0.01f;

    [Header("Beam Parameters")]
    public float beamDivergence = 0.003f;  // radians
    public float noiseStdDev = 0.02f;
    public float dropoutRate = 0.001f;

    [Header("Output")]
    public string topicName = "/lidar/scan";

    [Events]
    public delegate void ScanCallback(float[] ranges, float[] intensities);
    public event ScanCallback OnScanCaptured;

    private float[] ranges;
    private float[] intensities;
    private float[] horizontalAngles;
    private float[] verticalAngles;

    private void Start()
    {
        InitializeArrays();
        CalculateAngles();
    }

    private void InitializeArrays()
    {
        int totalSamples = horizontalSamples * verticalSamples;
        ranges = new float[totalSamples];
        intensities = new float[totalSamples];
    }

    private void CalculateAngles()
    {
        horizontalAngles = new float[horizontalSamples];
        verticalAngles = new float[verticalSamples];

        float hStart = -horizontalFOV / 2;
        float hStep = horizontalFOV / horizontalSamples;

        for (int i = 0; i < horizontalSamples; i++)
        {
            horizontalAngles[i] = hStart + i * hStep;
        }

        float vStart = -verticalFOV / 2;
        float vStep = verticalFOV / verticalSamples;

        for (int i = 0; i < verticalSamples; i++)
        {
            verticalAngles[i] = vStart + i * vStep;
        }
    }

    private void Update()
    {
        Scan();
    }

    private void Scan()
    {
        for (int v = 0; v < verticalSamples; v++)
        {
            for (int h = 0; h < horizontalSamples; h++)
            {
                int idx = v * horizontalSamples + h;

                // Calculate ray direction
                float azimuth = horizontalAngles[h] * Mathf.Deg2Rad;
                float elevation = verticalAngles[v] * Mathf.Deg2Rad;

                Vector3 direction = transform.rotation *
                    new Vector3(
                        Mathf.Cos(elevation) * Mathf.Sin(azimuth),
                        Mathf.Sin(elevation),
                        Mathf.Cos(elevation) * Mathf.Cos(azimuth)
                    );

                // Cast ray
                Ray ray = new Ray(transform.position, direction);
                RaycastHit hit;

                if (Physics.Raycast(ray, out hit, maxRange))
                {
                    // Add noise
                    float noise = Random.Range(-1f, 1f) * noiseStdDev;
                    ranges[idx] = hit.distance + noise;

                    // Calculate intensity based on material
                    Renderer rend = hit.collider.GetComponent<Renderer>();
                    if (rend != null)
                    {
                        intensities[idx] = rend.material.color.grayscale;
                    }
                    else
                    {
                        intensities[idx] = 0.5f;
                    }
                }
                else
                {
                    // Dropout
                    if (Random.value < dropoutRate)
                    {
                        ranges[idx] = float.MaxValue;  // NaN representation
                    }
                    else
                    {
                        ranges[idx] = maxRange;
                    }
                    intensities[idx] = 0f;
                }
            }
        }

        OnScanCaptured?.Invoke(ranges, intensities);
    }

    // Visualization
    private void OnDrawGizmos()
    {
        Gizmos.color = Color.green;
        Gizmos.DrawWireSphere(transform.position, 0.1f);

        if (Application.isPlaying)
        {
            // Draw first beam direction
            if (horizontalAngles.Length > 0 && verticalAngles.Length > 0)
            {
                Vector3 dir = transform.rotation * new Vector3(
                    Mathf.Cos(verticalAngles[0]) * Mathf.Sin(horizontalAngles[0]),
                    Mathf.Sin(verticalAngles[0]),
                    Mathf.Cos(verticalAngles[0]) * Mathf.Cos(horizontalAngles[0])
                );
                Gizmos.DrawLine(transform.position, transform.position + dir * 2);
            }
        }
    }
}
```

### GPU-Based Point Cloud (Advanced)

```csharp
using UnityEngine;
using System.Runtime.InteropServices;

public class GpuLidar : MonoBehaviour
{
    [Header("Parameters")]
    public int width = 1920;
    public int height = 128;
    public ComputeShader computeShader;
    public Material pointCloudMaterial;

    [Header("Output")]
    public ComputeBuffer pointBuffer;
    public int pointCount;

    private struct Point
    {
        public Vector3 position;
        public float intensity;
    }

    private void Start()
    {
        InitializeCompute();
    }

    private void InitializeCompute()
    {
        if (computeShader == null)
        {
            computeShader = Resources.Load<ComputeShader>("LidarCompute");
        }
    }

    private void OnRenderObject()
    {
        if (pointCloudMaterial != null && pointBuffer != null)
        {
            pointCloudMaterial.SetBuffer("points", pointBuffer);
            pointCloudMaterial.SetPass(0);
            Graphics.DrawProceduralNow(MeshTopology.Points, pointCount);
        }
    }

    private void OnDestroy()
    {
        if (pointBuffer != null)
        {
            pointBuffer.Release();
        }
    }
}
```

## IMU Simulation

### Unity IMU Implementation

```csharp
using UnityEngine;

public class IMUSensor : MonoBehaviour
{
    [Header("IMU Parameters")]
    public float updateRate = 100f;
    public Vector3 accelerometerNoise = new Vector3(0.02f, 0.02f, 0.02f);
    public Vector3 gyroscopeNoise = new Vector3(0.0001f, 0.0001f, 0.0001f);
    public Vector3 accelerometerBias = new Vector3(0.01f, 0.01f, 0.01f);
    public Vector3 gyroscopeBias = new Vector3(0.0001f, 0.0001f, 0.0001f);

    [Header("Calibration")]
    public bool enableBiasDrift = true;
    public Vector3 biasDriftRate = new Vector3(0.0001f, 0.0001f, 0.0001f);

    [Events]
    public delegate void IMUCallback(Vector3 linearAccel, Vector3 angularVel, Quaternion orientation);
    public event IMUCallback OnIMUData;

    [State]
    private Vector3 currentAccelBias;
    private Vector3 currentGyroBias;
    private float lastUpdateTime;
    private float updateInterval;

    private Rigidbody rb;
    private Transform sensorFrame;

    private void Start()
    {
        rb = GetComponentInParent<Rigidbody>();
        sensorFrame = transform;
        updateInterval = 1f / updateRate;

        InitializeBias();
    }

    private void InitializeBias()
    {
        currentAccelBias = accelerometerBias;
        currentGyroBias = gyroscopeBias;
    }

    private void FixedUpdate()
    {
        float now = Time.time;
        if (now - lastUpdateTime < updateInterval) return;
        lastUpdateTime = now;

        UpdateIMU();
    }

    private void UpdateIMU()
    {
        // Get true acceleration (in world frame)
        Vector3 trueAccel = rb ? rb.linearAcceleration : Vector3.zero;

        // Get true angular velocity (in world frame)
        Vector3 trueOmega = rb ? rb.angularVelocity : Vector3.zero;

        // Transform to sensor frame
        Vector3 sensorTrueAccel = sensorFrame.InverseTransformDirection(trueAccel);
        Vector3 sensorTrueOmega = sensorFrame.InverseTransformDirection(trueOmega);

        // Add bias (with optional drift)
        if (enableBiasDrift)
        {
            currentAccelBias += biasDriftRate * Time.fixedDeltaTime;
            currentGyroBias += biasDriftRate * Time.fixedDeltaTime;
        }

        // Add noise
        Vector3 accelNoise = new Vector3(
            Random.Range(-1f, 1f),
            Random.Range(-1f, 1f),
            Random.Range(-1f, 1f)
        ) * accelerometerNoise;

        Vector3 gyroNoise = new Vector3(
            Random.Range(-1f, 1f),
            Random.Range(-1f, 1f),
            Random.Range(-1f, 1f)
        ) * gyroscopeNoise;

        // Final measurement
        Vector3 measuredAccel = sensorTrueAccel + currentAccelBias + accelNoise;
        Vector3 measuredOmega = sensorTrueOmega + currentGyroBias + gyroNoise;

        // Add gravity to accelerometer reading (sensor frame)
        Vector3 gravityWorld = Physics.gravity;
        Vector3 gravitySensor = sensorFrame.InverseTransformDirection(gravityWorld);
        measuredAccel -= gravitySensor;

        // Get orientation (as if from magnetometer/sensor fusion)
        Quaternion measuredOrientation = sensorFrame.rotation;

        // Publish data
        OnIMUData?.Invoke(measuredAccel, measuredOmega, measuredOrientation);
    }
}
```

### Mobile Device IMU Integration

```csharp
using UnityEngine;

#if UNITY_ANDROID || UNITY_IOS
public class DeviceIMU : MonoBehaviour
{
    [Header("Device Sensors")]
    public bool useAccelerometer = true;
    public bool useGyroscope = true;
    public bool useAttitude = true;

    [Header("Output")]
    public float updateRate = 60f;

    private float lastUpdate;
    private float updateInterval;

    [Events]
    public delegate void DeviceIMUCallback(Vector3 accel, Vector3 gyro, Quaternion attitude);
    public event DeviceIMUCallback OnIMUData;

    private void Start()
    {
        updateInterval = 1f / updateRate;

        // Enable sensors
        if (useAccelerometer) Input.gyro.enabled = true;
        if (useGyroscope) Input.gyro.enabled = true;
        if (useAttitude) Input.gyro.enabled = true;
    }

    private void Update()
    {
        if (Time.time - lastUpdate < updateInterval) return;
        lastUpdate = Time.time;

        Vector3 accel = useAccelerometer ? Input.acceleration : Vector3.zero;
        Vector3 gyro = useGyroscope ? Input.gyro.rotationRate : Vector3.zero;
        Quaternion attitude = useAttitude ? Input.gyro.attitude : Quaternion.identity;

        OnIMUData?.Invoke(accel, gyro, attitude);
    }
}
#endif
```

## ROS Integration (ROS#)

### ROS Publisher Bridge

```csharp
using UnityEngine;
using System.Collections.Generic;
using ROSMessage = ROSConnector.Messages;

public class ROSPublisher : MonoBehaviour
{
    [Header("ROS Connection")]
    public string serverIP = "127.0.0.1";
    public int serverPort = 5000;

    [Header("Topics")]
    public string cameraTopic = "/camera/image_raw";
    public string lidarTopic = "/lidar/scan";
    public string imuTopic = "/imu/data";

    private ROSConnection ros;
    private Dictionary<string, Publisher> publishers;

    private void Start()
    {
        InitializeROS();
    }

    private void InitializeROS()
    {
        ros = ROSConnection.GetInstance(serverIP, serverPort);

        publishers = new Dictionary<string, Publisher>
        {
            { "camera", ros.RegisterPublisher<ROSMessage.sensor_msgs.Image>(cameraTopic) },
            { "lidar", ros.RegisterPublisher<ROSMessage.sensor_msgs.LaserScan>(lidarTopic) },
            { "imu", ros.RegisterPublisher<ROSMessage.sensor_msgs.Imu>(imuTopic) }
        };
    }

    public void PublishCamera(Texture2D image, string frameId)
    {
        ROSMessage.sensor_msgs.Image msg = new ROSMessage.sensor_msgs.Image
        {
            header = new ROSMessage.std_msgs.Header
            {
                frame_id = frameId,
                stamp = ROSConnection.GetTime()
            },
            height = (uint)image.height,
            width = (uint)image.width,
            encoding = "rgba8",
            is_bigendian = 0,
            step = (uint)(image.width * 4),
            data = image.GetRawTextureData()
        };

        publishers["camera"].Publish(msg);
    }

    public void PublishLidar(float[] ranges, float[] intensities, string frameId)
    {
        ROSMessage.sensor_msgs.LaserScan msg = new ROSMessage.sensor_msgs.LaserScan
        {
            header = new ROSMessage.std_msgs.Header
            {
                frame_id = frameId,
                stamp = ROSConnection.GetTime()
            },
            angle_min = -Mathf.PI,
            angle_max = Mathf.PI,
            angle_increment = (2 * Mathf.PI) / ranges.Length,
            time_increment = 0.0001f,
            scan_time = Time.deltaTime,
            range_min = 0.1f,
            range_max = 100f,
            ranges = ranges,
            intensities = intensities
        };

        publishers["lidar"].Publish(msg);
    }

    public void PublishIMU(Vector3 linearAccel, Vector3 angularVel, Quaternion orientation, string frameId)
    {
        ROSMessage.sensor_msgs.Imu msg = new ROSMessage.sensor_msgs.Imu
        {
            header = new ROSMessage.std_msgs.Header
            {
                frame_id = frameId,
                stamp = ROSConnection.GetTime()
            },
            orientation = new ROSMessage.geometry_msgs.Quaternion
            {
                x = orientation.x,
                y = orientation.y,
                z = orientation.z,
                w = orientation.w
            },
            orientation_covariance = new double[9]
            {
                0.001, 0, 0, 0, 0.001, 0, 0, 0, 0.001
            },
            angular_velocity = new ROSMessage.geometry_msgs.Vector3
            {
                x = angularVel.x,
                y = angularVel.y,
                z = angularVel.z
            },
            angular_velocity_covariance = new double[9]
            {
                0.0001, 0, 0, 0, 0.0001, 0, 0, 0, 0.0001
            },
            linear_acceleration = new ROSMessage.geometry_msgs.Vector3
            {
                x = linearAccel.x,
                y = linearAccel.y,
                z = linearAccel.z
            },
            linear_acceleration_covariance = new double[9]
            {
                0.0001, 0, 0, 0, 0.0001, 0, 0, 0, 0.0001
            }
        };

        publishers["imu"].Publish(msg);
    }
}
```

## Summary

Unity sensor simulation requires:
- Camera components with intrinsics and noise modeling
- Raycast-based LiDAR for point cloud generation
- IMU simulation with bias and noise parameters
- ROS# bridge for publishing sensor data

## Next Section

Proceed to [Exercises](./03-4-exercises.md) to practice sensor implementation.
