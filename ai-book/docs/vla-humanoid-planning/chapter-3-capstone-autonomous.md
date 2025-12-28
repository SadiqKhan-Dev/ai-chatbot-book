---
sidebar_position: 3
title: "Chapter 3 - Capstone: The Autonomous Humanoid"
description: "End-to-end VLA integration with perception feedback"
---

# Chapter 3: Capstone - The Autonomous Humanoid

Integrate all VLA components into a complete voice-controlled humanoid system.

---

## 3.1 System Architecture Overview

### End-to-End Data Flow

The complete VLA system connects voice input through perception to robot execution.

**Complete Pipeline:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         VOICE INPUT LAYER                                │
│  Microphone → Audio Capture → Noise Reduction → Whisper STT             │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                      INTENT UNDERSTANDING LAYER                         │
│  Intent Classification → Slot Filling → Ambiguity Resolution            │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                       COGNITIVE PLANNING LAYER                          │
│  LLM Reasoning → Action Decomposition → Sequence Generation             │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                        EXECUTION LAYER                                  │
│  ROS 2 Actions → Navigation → Manipulation → Status Report              │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                      PERCEPTION FEEDBACK LOOP                          │
│  Object Detection → Scene Understanding → State Update → Replanning    │
└─────────────────────────────────────────────────────────────────────────┘
```

### Component Integration Points

| From | To | Interface |
|------|-----|-----------|
| Whisper | Intent Classifier | Text string |
| Intent Classifier | LLM Planner | Structured intent |
| LLM Planner | ROS 2 | Action sequence |
| ROS 2 | Perception | Execution status |
| Perception | LLM Planner | State feedback |

### Latency Budget

End-to-end latency affects user experience.

| Stage | Target Latency | Cumulative |
|-------|----------------|------------|
| Speech recognition | < 3s | 3s |
| Intent classification | < 500ms | 3.5s |
| LLM planning | < 2s | 5.5s |
| Action dispatch | < 100ms | 5.6s |
| **Total (user perception)** | | **< 6s** |

---

## 3.2 Perception Integration

### Closing the Loop

Perception grounds LLM planning in real-world state.

**Perception Roles:**

| Role | Description | Example |
|------|-------------|---------|
| Verification | Confirm object exists | Is the cup in the kitchen? |
| Localization | Find object position | Where exactly is the cup? |
| Obstacle detection | Identify path blocks | Is the path clear? |
| State monitoring | Track execution progress | Is the gripper closed? |

### Feedback to LLM

Perception results inform replanning.

**Feedback Types:**

| Feedback | Meaning | LLM Action |
|----------|---------|------------|
| Object not found | Target absent | Search or report |
| Path blocked | Navigation impossible | Replan route |
| Object moved | State changed | Update target location |
| Execution complete | Action finished | Proceed to next |
| Execution failed | Physical issue | Replan or abort |

**Replanning Example:**

```
Original Plan: [navigate(kitchen), find(cup), pick(cup), navigate(user)]

Perception Report: "Cup not found in kitchen"

LLM Replanning:
"Analyze: Cup not in expected location.
Options: Search nearby, ask user, or find alternative.
Decision: Search adjacent areas."
New Plan: [search(living_room), search(office), find(cup), pick(cup), navigate(user)]
```

### Humanoid Perception Considerations

Perception placement affects capability.

**Camera Configurations:**

| Configuration | Advantage | Limitation |
|---------------|-----------|------------|
| Head-mounted | Human-like perspective | Limited downward view |
| Torso-mounted | Wide field of view | Height bias |
| Combined | Coverage redundancy | Integration complexity |

---

## 3.3 Complete Capstone Project

### Project: Voice-Controlled Multi-Step Task

**Objective:** Implement a complete VLA pipeline for a humanoid task.

**Command:** "Clean up the living room and organize items on the table"

### Pipeline Trace

**Stage 1 - Voice Input:**

```
User speaks: "Clean up the living room and organize items on the table"
Whisper output: "clean up the living room and organize items on the table"
Confidence: 0.92
```

**Stage 2 - Intent Understanding:**

```
Intent: cleanup_and_organize
Slots:
  - action: cleanup, organize
  - location: living_room
  - target: table
Ambiguities: None
```

**Stage 3 - LLM Planning:**

Prompt: "The user wants to clean up the living room and organize items on the table.
Available actions: navigate, find, pick, place, report.
Objects: general items, cups, books, papers.
Output: JSON action sequence."

Response:
```text
[
  {"action": "navigate", "target": "living_room"},
  {"action": "find", "target": "items"},
  {"action": "pick", "target": "cup", "quantity": "all"},
  {"action": "pick", "target": "book", "quantity": "all"},
  {"action": "navigate", "target": "table"},
  {"action": "place", "target": "cups", "location": "table"},
  {"action": "place", "target": "books", "location": "table"}
]
```

**Stage 4 - Perception Integration:**

```
Navigate to living_room: Complete
Find items: Detected 3 cups, 2 books, scattered papers
Pick cups: 3/3 complete
Pick books: 2/2 complete
Navigate to table: Complete
Place cups on table: Complete
Place books on table: Complete
```

**Stage 5 - Execution Complete:**

```
Final Report: "Cleanup complete. 3 cups and 2 books organized on table."
Remaining: Papers (user may want to specify organization)
```

### Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Command understood | 100% | Intent classification confidence > 0.8 |
| Plan valid | 100% | All actions within robot capabilities |
| Execution complete | > 90% | Actions successfully completed |
| Time to complete | < 5 min | Wall clock time |
| User satisfaction | Acceptable | Confirmation query |

---

## 3.4 System Reliability Patterns

### Failure Handling

Robust systems handle failures gracefully.

**Recovery Strategies:**

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Navigation blocked | Costmap timeout | Replan alternative route |
| Object not found | Perception negative | Expand search or report |
| Grip failed | Force feedback | Retry with adjusted approach |
| Command unclear | Low confidence | Request clarification |
| System overload | Latency spike | Degrade gracefully |

### Human-in-the-Loop Safety

Critical decisions require human confirmation.

**Confirmation Points:**

| Decision | Confidence Threshold | User Action |
|----------|---------------------|-------------|
| Navigate unfamiliar area | < 0.7 | Confirm before proceeding |
| Handle fragile items | Always | Ask about handling |
| Enter private space | Always | Request permission |
| Multiple interpretations | < 0.9 | Ask for clarification |

---

## 3.5 Summary

This chapter covered:

- Complete VLA system architecture
- Perception feedback integration
- End-to-end pipeline trace
- Capstone project walkthrough
- Reliability and safety patterns

---

## Exercise 3.1

**Objective:** Complete the capstone VLA integration.

**Steps:**
1. Design a voice command for a household task
2. Trace command through all pipeline stages
3. Identify perception requirements
4. Define success criteria
5. Design failure recovery

**Verification:** Complete pipeline trace with all components addressed.
