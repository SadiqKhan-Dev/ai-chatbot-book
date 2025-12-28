---
sidebar_position: 2
---

# 2. Communication Primitives

Master nodes, topics, and services for robot communication.

## Learning Objectives

1. Create ROS 2 nodes with rclpy
2. Implement publisher-subscriber patterns
3. Implement request-response services

## Nodes

A **node** is a single-purpose process:

```
+----------+     +----------+     +----------+
|  Node A  | <-> |  Node B  | <-> |  Node C  |
+----------+     +----------+     +----------+
   Process         Process          Process
```

### Minimal Node

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_node')
        self.get_logger().info('Hello from ROS 2!')

def main(args=None):
    rclpy.init(args=args)
    node = MinimalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Run with: `ros2 run my_pkg minimal_node`

## Topics (Publish-Subscribe)

Topics are named buses for async communication:

```
                    +------------+
Camera ---- Topic ----> |  Display   |
    (image_raw)    +------------+
```

### Publisher Node

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.pub = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello at {time.time()}'
        self.pub.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')

def main():
    rclpy.init()
    talker = Talker()
    rclpy.spin(talker)
    talker.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Node

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.sub = self.create_subscription(
            String, 'chatter', self.listener_callback, 10)

    def listener_callback(self, msg):
        self.get_logger().info(f'Heard: {msg.data}')

def main():
    rclpy.init()
    listener = Listener()
    rclpy.spin(listener)
    listener.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Services (Request-Response)

Services are synchronous request-response:

```
Client ---- Request ----> Server
          <--- Response ---
```

### Service Server

```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class ServiceServer(Node):
    def __init__(self):
        super().__init__('service_server')
        self.srv = self.create_service(
            SetBool, 'enable_motor', self.enable_callback)

    def enable_callback(self, request, response):
        if request.data:
            response.success = True
            response.message = 'Motor enabled'
            self.get_logger().info('Motor ON')
        else:
            response.success = True
            response.message = 'Motor disabled'
            self.get_logger().info('Motor OFF')
        return response

def main():
    rclpy.init()
    server = ServiceServer()
    rclpy.spin(server)
    server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Service Client

```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class ServiceClient(Node):
    def __init__(self):
        super().__init__('service_client')
        self.cli = self.create_client(SetBool, 'enable_motor')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

    def send_request(self, enable):
        req = SetBool.Request()
        req.data = enable
        self.future = self.cli.call_async(req)
        return self.future

def main():
    rclpy.init()
    client = ServiceClient()
    future = client.send_request(True)
    rclpy.spin_until_future_complete(client, future)
    result = future.result()
    client.get_logger().info(f'Result: {result.message}')
    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Quick Reference

| Element | Code | Use Case |
|---------|------|----------|
| Create node | `rclpy.create_node('name')` | Any node |
| Publisher | `create_publisher(Msg, 'topic', 10)` | Sensor data |
| Subscriber | `create_subscription(Msg, 'topic', cb)` | Data receiving |
| Service | `create_service(Srv, 'name', cb)` | Actions |
| Client | `create_client(Srv, 'name')` | Trigger actions |
| Timer | `create_timer(1.0, callback)` | Periodic tasks |

## Monitor Your System

```bash
ros2 topic list                    # View all topics
ros2 topic info /chatter           # Topic details
ros2 topic echo /chatter           # See messages live
ros2 service list                  # View services
ros2 node list                     # Running nodes
```

## Next Section

Proceed to [Python Agent Integration](../03-python-agent-integration/index.md)
