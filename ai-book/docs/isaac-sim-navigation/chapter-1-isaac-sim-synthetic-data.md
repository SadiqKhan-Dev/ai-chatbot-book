---
sidebar_position: 1
title: Chapter 1 - Isaac Sim & Synthetic Data
description: Photorealistic simulation and synthetic data generation
---

# Chapter 1: Isaac Sim & Synthetic Data

NVIDIA Isaac Sim provides photorealistic simulation for humanoid robot development. This chapter covers simulation concepts and synthetic data generation for perception training.

---

## 1.1 Isaac Sim Architecture

### Universal Scene Description (USD)

Isaac Sim uses USD as its scene representation format. USD encodes hierarchical scene structure, geometry, materials, and animation data in a single file format.

**USD Core Concepts:**

- **Stage**: The root container for all scene content. A stage represents a complete simulation environment.
- **Prim** (Primitive): Any node in the USD scene graph. Prims include geometry, lights, cameras, and transforms.
- **Schema**: Typed prims with specific attributes. Examples include `UsdGeomCube`, `UsdGeomMesh`, `UsdLuxLight`.
- **Attribute**: Named values attached to prims. Attributes store position, rotation, scale, material properties.

**USD Hierarchy Example:**

```
/World
  ├── /World/Camera (UsdGeomCamera)
  ├── /World/Lights (UsdLuxDistantLight)
  └── /World/Humanoid
      ├── /World/Humanoid/Torso (UsdGeomXform)
      ├── /World/Humanoid/Head (UsdGeomXform)
      └── /World/Humanoid/LeftArm (UsdGeomXform)
```

### Simulation Loop

Isaac Sim operates on a simulation loop that advances physics and rendering in discrete time steps.

- **Physics Step**: Isaac Sim uses PhysX 5 for physics simulation. The physics step advances rigid body dynamics, joint constraints, and contact physics.
- **Render Step**: RTX rendering generates sensor outputs. Render frequency may differ from physics frequency.
- **ROS Bridge**: Isaac Sim publishes sensor data to ROS 2 topics at each render step.

---

## 1.2 Photorealistic Rendering

### RTX Path Tracing

RTX ray tracing simulates light propagation through the scene to generate photorealistic images.

**Key Rendering Concepts:**

- **Path Tracing**: Monte Carlo simulation of light paths from camera through scene to light sources.
- **Ambient Occlusion**: Contact shadows in corners and crevices.
- **Global Illumination**: Indirect lighting from bounced light.
- **Reflections**: Specular and diffuse reflections from surfaces.

**Isaac Sim Rendering Settings:**

| Parameter | Range | Effect |
|-----------|-------|--------|
| Path Tracing Samples | 1-256 | Image quality vs. render time |
| Max Bounces | 1-16 | Light bounce depth |
| Texture Compression | On/Off | Memory usage vs. quality |
| DLSS | On/Off | AI upscaling for real-time |

### Materials

Isaac Sim uses MDL (Material Definition Language) for physically-based materials.

**Common Material Types:**

- **OmniPBR**: Physically-based rendering with albedo, roughness, metallic, normal maps.
- **OmniGlass**: Transmissive material for windows and lenses.
- **OmniSurface**: Subsurface scattering for skin and organic materials.

**Humanoid Materials:**

When simulating humanoid robots, configure materials for:
- Skin tones with subsurface scattering
- Clothing fabric properties (roughness, weave pattern)
- Metal joints with appropriate metallic values

---

## 1.3 Sensor Simulation

### RGB Camera

The RGB camera sensor simulates a pinhole camera model with lens effects.

**Camera Parameters:**

```yaml
camera:
  focal_length: 35mm          # 35mm equivalent focal length
  resolution: [1280, 720]     # Image dimensions in pixels
  hfov: 60.0                  # Horizontal field of view in degrees
  exposure_time: 0.01         # Shutter speed in seconds
  noise:                      # Optional noise model
    type: gaussian
    mean: 0.0
    stddev: 1.0
```

**Camera Model:**

The pinhole camera model projects 3D points to 2D image coordinates:

```
u = fx * (X / Z) + cx
v = fy * (Y / Z) + cy
```

Where (fx, fy) are focal lengths in pixels, (cx, cy) is the principal point, and (X, Y, Z) is the 3D point.

### Depth Camera

Depth cameras measure distance from the sensor to scene geometry.

**Depth Sensing Methods:**

- **Stereo**: Two cameras with known baseline compute depth via triangulation.
- **Structured Light**: Pattern projection and deformation analysis.
- **Time-of-Flight (ToF)**: Measures round-trip time of emitted light.

**Isaac Sim Depth Output:**

```
depth_image[x, y] = distance from camera optical center to point at pixel (x, y)
```

### Semantic Segmentation

Semantic segmentation classifies each pixel with an object class.

**Isaac Sim Segmentation Output:**

```
segmentation_image[x, y] = instance ID or class ID
```

**Class Mapping:**

| ID | Class |
|----|-------|
| 0 | Background |
| 1 | Humanoid |
| 2 | Table |
| 3 | Chair |
| 4 | Cup |
| ... | ... |

---

## 1.4 Synthetic Data Generation Pipeline

### Data Flow

```
Isaac Sim → Sensor → Ground Truth → Dataset
    ↓
ROS 2 Topics → Isaac ROS Packages
```

### Ground Truth Generation

Isaac Sim provides ground truth annotations alongside sensor data.

**Available Ground Truth:**

- **2D Bounding Boxes**: (x_min, y_min, x_max, y_max) for detected objects
- **3D Bounding Boxes**: 8-vertex bounding boxes in world coordinates
- **Segmentation Masks**: Per-pixel class or instance labels
- **Depth Maps**: Distance from camera to each pixel
- **Surface Normals**: Per-pixel surface orientation
- **Object Poses**: 6D pose (position + orientation) for each instance

### Dataset Export

Synthetic data exports in standard formats for machine learning.

**Supported Formats:**

- **COCO**: MS COCO format with annotations in JSON
- **KITTI**: KITTI benchmark format
- **VOC**: Pascal VOC format
- **Custom**: User-defined schema

---

## 1.5 Humanoid Integration

### Robot Import

Import humanoid robot models from URDF or USD formats.

```python
# Load humanoid from URDF
from omni.isaac.robot_benchmark import RobotImporter

importer = RobotImporter(urdf_path="humanoid.urdf")
robot = importer.import_robot(stage, "/World/Humanoid")
```

### Sensor Placement

Configure sensors at humanoid-specific locations.

**Head-Mounted Camera:**

```
Position: [0, 0, 1.7]  # Eye level (1.7m height)
Orientation: [0, 0, 0]  # Forward facing
FOV: 60 degrees horizontal
```

**Torso Camera:**

```
Position: [0, 0, 1.2]  # Chest level
Orientation: [0, -15, 0]  # Slightly downward
FOV: 90 degrees horizontal
```

---

## 1.6 Summary

This chapter covered:

- USD scene representation for Isaac Sim
- RTX photorealistic rendering concepts
- RGB, depth, and segmentation sensor simulation
- Synthetic data generation for perception training
- Humanoid robot integration with sensor placement

**Next**: Chapter 2 covers Isaac ROS perception and VSLAM.

---

## Exercise 1.1

**Objective**: Create a basic Isaac Sim environment with humanoid and sensors.

**Steps**:
1. Create a new USD stage
2. Add a ground plane and basic lighting
3. Import a humanoid robot model
4. Add an RGB camera at head height
5. Verify camera publishes to ROS topic

**Verification**: Confirm RGB images appear on the ROS topic.
