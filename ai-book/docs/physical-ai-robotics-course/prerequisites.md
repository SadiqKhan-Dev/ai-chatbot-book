---
sidebar_position: 0
---

# Prerequisites for Module 2

## Required Prerequisites

### Software Installation

#### Gazebo Requirements
- **ROS Noetic** (Ubuntu 20.04) or **ROS 2 Humble** (Ubuntu 22.04)
- **Gazebo Classic 11**
- Python 3.8+

```bash
# ROS Noetic installation
sudo apt-get install ros-noetic-desktop-full
source /opt/ros/noetic/setup.bash
sudo apt-get install ros-noetic-gazebo-ros-pkgs
```

#### Unity Requirements
- **Unity 2021.3 LTS** or newer
- **Unity Hub** for version management
- **Visual Studio** or **VS Code** for C# scripting

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8 GB | 16 GB |
| CPU | Quad-core | 6+ cores |
| GPU | Integrated | Dedicated GPU (4+ GB VRAM) |
| Storage | 20 GB free | 50+ GB free |

### Knowledge Prerequisites

#### Programming
- Python fundamentals (variables, loops, functions, classes)
- Basic C# syntax understanding
- Familiarity with command-line operations

#### Mathematics
- Linear algebra (vectors, matrices, transformations)
- 3D coordinate systems (Euler angles, quaternions)
- Basic physics (forces, torques, inertia)

#### Linux
- Terminal navigation and file operations
- Environment variable management
- Package installation with `apt`

## Environment Setup Checklist

- [ ] ROS/Gazebo installed and `gazebo` command launches
- [ ] Unity Hub installed with Unity Editor
- [ ] Test project created in both platforms
- [ ] Basic scene runs without errors

## External Resources

- [Gazebo Documentation](http://gazebosim.org/docs)
- [Unity Physics Documentation](https://docs.unity3d.com/Physics.html)
- [ROS Documentation](https://docs.ros.org)
- [URDF Documentation](http://wiki.ros.org/urdf)
