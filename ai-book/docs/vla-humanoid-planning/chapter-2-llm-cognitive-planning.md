---
sidebar_position: 2
title: "Chapter 2 - LLM Cognitive Planning"
description: "Task decomposition and ROS 2 integration with LLMs"
---

# Chapter 2: LLM Cognitive Planning

Use large language models to decompose natural language commands into executable action sequences.

---

## 2.1 LLM Capabilities for Robotics

### What LLMs Bring to Robotics

Large language models provide reasoning capabilities that extend beyond rule-based systems.

**Core Capabilities:**

| Capability | Description | Robotic Application |
|------------|-------------|---------------------|
| Commonsense reasoning | General world knowledge | "Cups are in kitchens" |
| Language understanding | Parse complex commands | Multi-step instructions |
| Flexibility | Handle novel situations | Unseen object arrangements |
| Context integration | Use conversation history | Reference previous actions |

### LLM Limitations

Understanding limitations prevents unsafe execution.

**Key Limitations:**

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Hallucination | Incorrect facts | Verification against real state |
| Latency | Delayed responses | Async processing, streaming |
| Context window | Memory constraints | Summarization, truncation |
| Cost | Economic constraints | Caching, local alternatives |

### Reasoning Example

**User Input:** "The user is thirsty"

**LLM Reasoning Path:**

```
1. User is thirsty → user needs hydration
2. Hydration → water or beverage
3. Beverage location → kitchen or fridge
4. Delivery → navigate to kitchen, find cup, get water, navigate to user
5. Complete → hand over to user
```

**Output Sequence:**
```
[navigate(kitchen), find(cup), pick(cup), fill(water), navigate(user), give(cup)]
```

---

## 2.2 Prompt Engineering for Actions

### Prompt Structure

Effective prompts define robot capabilities and constrain output format.

**Prompt Components:**

```
System Prompt: Defines role, capabilities, constraints
├─ Robot persona and purpose
├─ Available actions and parameters
├─ Safety constraints
└─ Output format specification

User Input: The command to process
└─ Raw natural language command

Output: Structured action sequence
└─ JSON or specified format
```

### System Prompt Design

**Core Elements:**

```
You are a humanoid robot assistant. You help users with tasks in home environments.

Available actions:
- navigate(location): Move to a location
- pick(object): Grasp an object
- place(object, location): Put an object at a location
- find(object): Search for and locate an object
- report(description): Describe what you perceive

Output format:
```text
actions = [
  {"action": "navigate", "target": "kitchen"}
]
```

### Constraining Outputs

Structured outputs ensure parseable action sequences.

**Output Schema:**

```text
{
  "actions": [
    {
      "action": "string",
      "parameters": {
        "target": "string",
        "object": "string",
        "location": "string"
      },
      "confidence": "0.0-1.0"
    }
  ],
  "reasoning": "explanation of plan"
}
```

### Few-Shot Examples

Examples teach the LLM expected output format.

**Example Set:**

```text
User: "Bring me water"
Response:
[
  {"action": "navigate", "target": "kitchen"},
  {"action": "find", "target": "cup"},
  {"action": "pick", "target": "cup"},
  {"action": "fill", "target": "water"},
  {"action": "navigate", "target": "user_location"},
  {"action": "give", "target": "water"}
]

User: "Pick up the book"
Response:
[
  {"action": "find", "target": "book"},
  {"action": "pick", "target": "book"}
]
```

---

## 2.3 ROS 2 Action Bridging

### From LLM Output to ROS 2 Actions

Parsing LLM output into ROS 2 action client calls.

**Action Mapping:**

| LLM Action | ROS 2 Action | Topic/Service |
|------------|--------------|---------------|
| navigate | NavigateToPose | /navigate_to_pose |
| pick | GripperControl | /gripper_controller |
| place | GripperControl | /gripper_controller |
| find | ObjectDetection | /detected_objects |

### Action Sequencing

Executing multiple actions in order with dependency awareness.

**Sequence Execution Model:**

```
Action 1: navigate(kitchen)
    └─ Complete → Action 2: find(cup)
                      └─ Complete → Action 3: pick(cup)
                                        └─ Complete → Action 4: navigate(user)
```

**Dependencies:**

| Action | Depends On | Reason |
|--------|------------|--------|
| pick(cup) | find(cup), navigate(kitchen) | Must be at location with object |
| place(cup) | pick(cup) | Must have object |
| navigate(user) | place(cup) | Must complete delivery |

### Error Handling

Handling invalid or failed actions.

**Error Types:**

| Error | Cause | Response |
|-------|-------|----------|
| Unknown action | LLM generated invalid action | Filter, request clarification |
| Capability mismatch | Action outside robot abilities | Replan with constraints |
| Execution failure | Physical obstruction | Replan with alternative |
| Ambiguous target | Multiple matching objects | Request clarification |

---

## 2.4 Planning with Commonsense Reasoning

### Humanoid Context Awareness

LLMs incorporate commonsense about humanoid capabilities.

**Capability Awareness:**

```
User: "Reach through the wall and grab the cup"
LLM Response: "I cannot reach through walls. I can navigate to the kitchen and retrieve the cup from there."
```

**Physical Constraints:**

| Constraint | LLM Understanding |
|------------|-------------------|
| Height | "Top shelf" may be unreachable |
| Strength | Heavy objects require both hands |
| Balance | Carrying large items affects stability |
| Reach | Extended arms have limits |

### Handling Novel Situations

LLMs generalize to unseen scenarios.

**Example Novel Situation:**

```
User: "The vase is broken. Clean up the shards carefully."

LLM Planning:
1. navigate(vase_location)
2. find(shards) - perception required
3. pick(shard, careful=True) - reduced grip force
4. place(shard, container) - proper disposal
5. repeat until area clear
```

---

## 2.5 Summary

This chapter covered:

- LLM capabilities and limitations for robotics
- Prompt engineering for action generation
- Bridging LLM outputs to ROS 2 actions
- Action sequencing and dependencies
- Commonsense reasoning for humanoid contexts

**Next**: Chapter 3 covers the capstone autonomous humanoid.

---

## Exercise 2.1

**Objective**: Design an LLM planning system for humanoid tasks.

**Steps**:
1. Write a system prompt for a home assistant humanoid
2. Define the action vocabulary (5-8 actions)
3. Create 3 few-shot examples
4. Design an output schema for action parsing
5. Test with a novel command

**Verification**: System prompt and examples produce valid action sequences.
