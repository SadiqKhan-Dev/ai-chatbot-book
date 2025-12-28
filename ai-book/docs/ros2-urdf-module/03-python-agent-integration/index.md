---
sidebar_position: 3
---

# 3. Python Agent Integration

Connect AI/ML agents with ROS 2 using rclpy.

## Learning Objectives

1. Build rclpy nodes for agent integration
2. Implement sensor-to-agent data pipelines
3. Publish control commands to actuators

## Agent-Controller Pattern

```
+----------------+     +----------------+     +----------------+
|   Sensors      | --> | Python Agent   | --> | ROS Controller |
+----------------+     +----------------+     +----------------+
   (subscribers)            (AI logic)          (publishers)
```

## Sensor Subscriber Agent

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class ReflexAgent(Node):
    """
    Simple reflex agent that avoids obstacles.
    Subscribes to laser scan, makes decisions, publishes commands.
    """

    def __init__(self):
        super().__init__('reflex_agent')

        # Output: velocity commands
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Input: laser scan
        self.scan_sub = self.create_subscription(
            LaserScan, 'scan', self.scan_callback, 10)

        self.get_logger().info('Reflex agent started')

    def scan_callback(self, msg):
        """Process laser scan and decide movement."""
        # Get minimum distance in front
        front_distances = msg.ranges[len(msg.ranges)//4:3*len(msg.ranges)//4]
        min_distance = min(front_distances) if front_distances else float('inf')

        # Create velocity command
        twist = Twist()

        if min_distance < 0.5:  # Obstacle too close
            twist.linear.x = 0.0
            twist.angular.z = 0.5  # Turn left
            self.get_logger().warning(f'Obstacle at {min_distance:.2f}m - turning')
        else:  # Path clear
            twist.linear.x = 0.2
            twist.angular.z = 0.0
            self.get_logger().debug(f'Clear path: {min_distance:.2f}m')

        self.cmd_pub.publish(twist)

def main():
    rclpy.init()
    agent = ReflexAgent()
    rclpy.spin(agent)
    agent.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Multi-Sensor Agent

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, WrenchStamped
from sensor_msgs.msg import Image, JointState
import numpy as np

class MultiSensorAgent(Node):
    """
    Agent using multiple sensor inputs for decision making.
    """

    def __init__(self):
        super().__init__('multi_sensor_agent')

        # Publishers
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.wrench_pub = self.create_publisher(WrenchStamped, 'wrench', 10)

        # Subscribers
        self.joint_sub = self.create_subscription(
            JointState, 'joint_states', self.joint_callback, 10)

        # State storage
        self.joint_positions = {}
        self.last_joint_time = None

        self.get_logger().info('Multi-sensor agent online')

    def joint_callback(self, msg):
        """Track joint positions."""
        self.joint_positions = dict(zip(msg.name, msg.position))
        self.last_joint_time = msg.header.stamp

    def compute_control(self):
        """Compute control based on all sensor data."""
        twist = Twist()

        # Example: Check if arm is extended
        if 'arm_extension' in self.joint_positions:
            extension = self.joint_positions['arm_extension']

            if extension > 0.9:  # Fully extended
                twist.linear.x = 0.0
                self.get_logger().info('Arm extended - stopping')
            else:
                twist.linear.x = 0.15

        return twist

    def timer_callback(self):
        """Periodic control loop."""
        if not self.joint_positions:
            return

        twist = self.compute_control()
        self.cmd_pub.publish(twist)

def main():
    rclpy.init()
    agent = MultiSensorAgent()
    agent.create_timer(0.1, agent.timer_callback)  # 10Hz control
    rclpy.spin(agent)
    agent.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Image Processing Agent

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import cv2

class VisionAgent(Node):
    """
    Agent that processes camera images for navigation.
    """

    def __init__(self):
        super().__init__('vision_agent')
        self.bridge = CvBridge()

        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.image_sub = self.create_subscription(
            Image, 'camera/image_raw', self.image_callback, 10)

        self.get_logger().info('Vision agent active')

    def image_callback(self, msg):
        """Process image and find target (red objects)."""
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except Exception as e:
            self.get_logger().error(f'CV bridge error: {e}')
            return

        # Convert to HSV
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # Red color range (two ranges due to HSV wrap)
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        twist = Twist()

        if contours:
            # Get largest contour
            largest = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest)

            if M['m00'] > 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

                # Center of image
                h, w = cv_image.shape[:2]
                center_x = w // 2

                # Steer towards target
                error = center_x - cx
                twist.angular.z = error * 0.001
                twist.linear.x = 0.1
                self.get_logger().debug(f'Target at x={cx}')

        self.cmd_pub.publish(twist)

def main():
    rclpy.init()
    agent = VisionAgent()
    rclpy.spin(agent)
    agent.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Agent Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Reflex | Immediate response to sensor | Safety, simple navigation |
| Deliberative | Plan before acting | Complex tasks |
| Hybrid | Combine reflex + planning | Most robots |

## Best Practices

```python
# 1. Use multi-threaded executor for blocking calls
from rclpy.executors import MultiThreadedExecutor

executor = MultiThreadedExecutor(num_threads=2)
executor.add_node(agent)

# 2. Handle shutdown gracefully
try:
    rclpy.spin(agent)
except KeyboardInterrupt:
    pass
finally:
    agent.get_logger().info('Shutting down...')
    agent.destroy_node()
    rclpy.shutdown()

# 3. Use QoS for reliable communication
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

qos = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.VOLATILE,
    depth=10
)
self.pub = self.create_publisher(Twist, 'cmd_vel', qos)
```

## Next Section

Proceed to [URDF Humanoid Modeling](../04-urdf-humanoid-modeling/index.md)
