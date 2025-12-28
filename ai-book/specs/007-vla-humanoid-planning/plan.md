# Implementation Plan: Module 4 - VLA Humanoid Planning

**Branch**: `[007-vla-humanoid-planning]`
**Date**: `2025-12-28`
**Spec**: [spec.md](spec.md)
**Input**: "Add Module 4 to Docusaurus with three chapters covering VLA, planning, and the capstone. Link the module as the final section in the course sidebar."

## Summary

This plan creates Module 4 for VLA (Vision-Language-Action) humanoid planning. The module enables voice-to-action pipelines using OpenAI Whisper and LLM-driven task planning over ROS 2. Three chapters progressively build from speech recognition through cognitive planning to capstone integration.

## Technical Context

**Language/Version**: Markdown (Docusaurus), Python 3.10+ (OpenAI SDK), ROS 2 Humble
**Primary Dependencies**: Docusaurus 3.x, OpenAI API (Whisper, GPT), Python 3.10+
**Storage**: Markdown files in `docs/vla-humanoid-planning/` directory structure
**Testing**: Documentation module - content validated against spec requirements
**Target Platform**: Docusaurus static site generator
**Scale/Scope**: 3 chapters, ~13 hours total content

## Project Structure

```
ai-book/docs/vla-humanoid-planning/
├── _category_.json                    # Module navigation config (position: 4)
├── index.md                           # Module landing page
├── prerequisites.md                   # Prerequisites (Modules 1-3)
├── chapter-1-voice-action-pipelines/
│   ├── _category_.json
│   ├── index.md
│   ├── 01-1-vla-pipeline-overview.md
│   ├── 01-2-whisper-integration.md
│   ├── 01-3-intent-classification.md
│   └── 01-4-exercise.md
├── chapter-2-llm-cognitive-planning/
│   ├── _category_.json
│   ├── index.md
│   ├── 02-1-llm-capabilities.md
│   ├── 02-2-prompt-engineering.md
│   ├── 02-3-ros2-action-bridging.md
│   └── 02-4-exercise.md
└── chapter-3-capstone-autonomous/
    ├── _category_.json
    ├── index.md
    ├── 03-1-system-architecture.md
    ├── 03-2-perception-integration.md
    └── 03-3-capstone-project.md
```

## Chapter Structure (3 Chapters, 12 Content Files)

### Chapter 1: Voice to Action Pipelines

**Purpose**: Build the voice input layer with speech-to-text and intent recognition

| Section | File | Content | Time |
|---------|------|---------|------|
| 1.1 | 01-1-vla-pipeline-overview.md | VLA architecture, components | 45 min |
| 1.2 | 01-2-whisper-integration.md | Whisper API, audio processing | 60 min |
| 1.3 | 01-3-intent-classification.md | Intent parsing, slot filling | 75 min |
| 1.4 | 01-4-exercise.md | Voice-controlled trigger | 30 min |

**Learning Path**:
1. Understand VLA pipeline architecture
2. Integrate Whisper for speech-to-text
3. Classify intents and extract entities
4. Trigger ROS 2 actions from voice

**Minimal Example - Whisper**:
```python
import openai

audio_file = open("command.wav", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
```

**Minimal Example - Intent**:
```python
command = transcript.text
intent = classify_intent(command)  # "navigate", "pick", "place"
entities = extract_entities(command)  # {"location": "kitchen", "object": "cup"}
```

---

### Chapter 2: Cognitive Planning with LLMs

**Purpose**: Use LLMs to decompose natural language into action sequences

| Section | File | Content | Time |
|---------|------|---------|------|
| 2.1 | 02-1-llm-capabilities.md | LLM reasoning for robotics | 60 min |
| 2.2 | 02-2-prompt-engineering.md | Prompt design for actions | 75 min |
| 2.3 | 02-3-ros2-action-bridging.md | LLM to ROS 2 integration | 75 min |
| 2.4 | 02-4-exercise.md | LLM task planner | 60 min |

**Learning Path**:
1. Understand LLM capabilities and limitations
2. Design prompts for consistent action output
3. Bridge LLM outputs to ROS 2 action clients
4. Handle failures and replanning

**Minimal Example - LLM Planning**:
```python
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a robot planner. "
         "Output JSON actions: [{\"action\": \"navigate\", \"target\": \"kitchen\"}]"},
        {"role": "user", "content": "Get me a cup from the kitchen"}
    ]
)
actions = parse_actions(response)
```

**Minimal Example - ROS 2 Action**:
```python
action_client = ActionClient(self, NavigateToPose, '/navigate_to_pose')
goal = NavigateToPose.Goal()
goal.pose = target_pose
action_client.send_goal(goal)
```

---

### Chapter 3: Capstone - The Autonomous Humanoid

**Purpose**: Integrate all components into complete voice-controlled humanoid system

| Section | File | Content | Time |
|---------|------|---------|------|
| 3.1 | 03-1-system-architecture.md | End-to-end integration | 45 min |
| 3.2 | 03-2-perception-integration.md | Perception in the loop | 60 min |
| 3.3 | 03-3-capstone-project.md | Complete autonomous task | 75 min |

**Learning Path**:
1. Design end-to-end VLA architecture
2. Integrate perception feedback
3. Complete capstone project

**Pipeline Flow**:
```
Voice Input → Whisper STT → Intent → LLM Planning → Action Sequence → ROS 2 Execution
```

---

## Sidebar Ordering (Docusaurus Integration)

The module will be integrated at position 4 in the sidebar:

```json
{
  "label": "Module 4: VLA Humanoid Planning",
  "position": 4
}
```

Within the module:
1. Chapter 1 (position 1): Voice to Action Pipelines
2. Chapter 2 (position 2): LLM Cognitive Planning
3. Chapter 3 (position 3): Capstone - The Autonomous Humanoid

## Content Requirements Mapping

| Spec Requirement | Chapter | Implementation |
|-----------------|---------|----------------|
| FR-001: Learning objectives | All | Each section has numbered objectives |
| FR-002: Whisper integration | Ch 1 | 01-2 covers Whisper API |
| FR-003: Intent classification | Ch 1 | 01-3 covers intent/slot extraction |
| FR-004: LLM prompting | Ch 2 | 02-2 covers prompt engineering |
| FR-005: VLA pipeline | Ch 1, Ch 3 | Architecture overview in 01-1, integration in 03-1 |
| FR-006: ROS 2 bridging | Ch 2 | 02-3 covers action client integration |
| FR-007: Hands-on exercises | All | Exercises at end of each chapter |
| FR-008: Assessments | All | Quiz questions per section |
| FR-009: Troubleshooting | All | Common issues in each chapter |
| FR-010: Prerequisites | index.md | Modules 1-3 reference |

## Success Criteria Validation

| Criterion | Target | Chapter |
|-----------|--------|---------|
| Whisper transcription in 5s | 100% | Ch 1.2 |
| Intent classification accuracy | 80% | Ch 1.3 |
| LLM action sequence valid | Demonstrable | Ch 2.2 |
| ROS 2 action execution | Demonstrable | Ch 2.3 |
| End-to-end pipeline | Capstone | Ch 3.3 |
| 80% quiz accuracy | 80% score | All chapters |
| Completable without external | Yes | All content self-contained |

## Implementation Phases

### Phase 1: Chapter 1 - Voice to Action
- Create directory structure
- Write VLA pipeline overview
- Document Whisper integration
- Create intent classification content
- Add Chapter 1 exercise

### Phase 2: Chapter 2 - LLM Cognitive Planning
- Write LLM capabilities section
- Document prompt engineering
- Create ROS 2 action bridging content
- Add Chapter 2 exercise

### Phase 3: Chapter 3 - Capstone
- Write system architecture overview
- Document perception integration
- Create capstone project content
- Final integration exercise

### Phase 4: Module Navigation
- Create module landing page
- Write prerequisites document
- Configure _category_.json files
- Verify sidebar ordering

### Phase 5: Review and Validation
- Validate against spec requirements
- Check success criteria
- Review for clarity and completeness
- Test navigation structure

## Exclusions (Per Specification)

- Model training (ML modules)
- Real hardware deployment (hardware modules)
- Production safety systems (industrial modules)
- Custom speech models (ASR modules)
- Multimodal foundation models (research modules)
- Edge deployment (embedded AI modules)
- Real-time LLM inference (performance modules)
- Continuous learning (lifelong learning modules)
- Dialogue systems (HRI modules)

## Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| Docusaurus | 3.x | Documentation framework |
| OpenAI API | Latest | Whisper + GPT models |
| Python | 3.10+ | API integration |
| ROS 2 | Humble | Action client |

## Risks and Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| API dependency | Medium | Document rate limits, local alternatives |
| Latency concerns | Low | Async processing, response streaming |
| Prompt variability | Medium | Strict JSON schemas, few-shot examples |

## Follow-up Actions

- `/sp.tasks` - Generate executable tasks for content creation
- `/sp.implement` - Create documentation content
- Review PHR routing: Feature stage is `plan`, routed to `history/prompts/vla-humanoid-planning/`

---

**Plan Status**: Ready for `/sp.tasks`
**Next Step**: Run `/sp.tasks` to generate executable tasks
