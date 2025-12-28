---
sidebar_position: 1
---

# Prerequisites

## Software Requirements

### Ubuntu 22.04 (Recommended)
```bash
# Add ROS 2 repository
sudo apt update && sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2
sudo apt update
sudo apt install ros-humble-desktop

# Setup environment
source /opt/ros/humble/setup.bash
```

### Windows 11
```powershell
# Install via chocolatey (requires admin)
choco install ros-humble-desktop

# Or manual: Download from https://docs.ros.org/en/humble/Installation/Windows-Install-Binary.html
```

### macOS
```bash
# Install via Homebrew
brew install ros/humble/ros2-humble

# Or: Download from https://docs.ros.org/en/humble/Installation/macOS-Install-Binary.html
```

## Development Tools

| Tool | Purpose | Install |
|------|---------|---------|
| VS Code | Editor | `sudo apt install code` |
| colcon | Build tool | `pip install -U colcon-common-extensions` |
| Git | Version control | `sudo apt install git` |

## Knowledge Prerequisites

- Python basics: variables, functions, classes, imports
- Terminal navigation and file operations
- Understanding of basic data structures (lists, dicts)

## Verification

```bash
# Check ROS 2 installation
source /opt/ros/humble/setup.bash
ros2 doctor  # Should report no errors

# Create test workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
```

## Resources

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [rclpy API](https://docs.ros2.org/latest/api/rclpy/)
- [URDF Tutorial](http://wiki.ros.org/urdf/Tutorials)
