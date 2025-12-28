<!--
    Sync Impact Report
    - Version change: 0.0.0 -> 1.0.0
    - Added sections: Vision Statement, Core Principles, Success Criteria, Project Constraints, Stakeholders & Roles, Brand Voice & Tone Guidelines, Governance
    - Removed sections: None
    - Templates requiring updates:
      - ✅ .specify/templates/plan-template.md
      - ✅ .specify/templates/spec-template.md
      - ✅ .specify/templates/tasks-template.md
      - ✅ .claude/commands/sp.plan.md
      - ✅ .gemini/commands/sp.plan.toml
    - Follow-up TODOs: None
    -->

# AI Robotics Course Constitution

## Vision Statement
This book aims to provide a comprehensive, hands-on introduction to AI in robotics for beginners and intermediate learners. The ultimate goal is to empower readers with the practical skills to build, program, and deploy intelligent robotic systems using real-world tools and reproducible examples.

## Core Principles

### I. Hands-On First
All learning MUST be driven by practical application. Each lesson will prioritize hands-on exercises, coding examples, and interactive simulations over purely theoretical explanations. The goal is to learn by doing.

### II. Absolute Reproducibility
Every code snippet, command, and project MUST be fully reproducible. Instructions will be explicit, environments will be clearly defined (e.g., via Docker or setup scripts), and dependencies will be version-locked to ensure learners achieve the same results consistently.

### III. Foundational Safety
Safety is a non-negotiable core tenet. All examples involving simulated or physical hardware MUST include explicit safety warnings, established protocols (e.g., E-stops, workspace clearance), and code that defaults to a safe state.

### IV. Deliberate Explainability
Complex topics MUST be deconstructed into simple, digestible concepts. We avoid jargon where possible and explain it clearly when necessary. The "why" behind a technique is just as important as the "how."

### V. Real-World Relevance
Content MUST be grounded in practical, real-world robotics applications. Examples and projects should reflect current industry practices and challenges, preparing learners for actual robotics engineering work.

### VI. Beginner-Friendly & Accessible
The material MUST be accessible to an audience with basic programming knowledge but no prior robotics experience. Concepts are introduced gradually, building on previous lessons, with clear prerequisites stated for each section.

## Success Criteria
The project is considered successful when the following measurable outcomes are achieved:
-   **Capstone Demonstration:** A final capstone project is fully documented and functions as described, integrating multiple concepts from the course.
-   **ROS 2 Packages:** All major exercises are organized into functioning, standalone ROS 2 packages that can be built and run.
-   **Docusaurus Deployment:** The entire book is successfully built and deployed as a live Docusaurus website with no broken links or missing content.

## Project Constraints
-   **Platform:** All content MUST be created for the Docusaurus framework.
-   **Technology Stack:** The primary technologies are Python and ROS 2. All code examples must adhere to standards for these tools.
-   **Licensing:** All original content is licensed under MIT, and any third-party assets must have compatible licenses.
-   **Hardware Assumptions:** The course is primarily simulation-based. Any optional physical hardware sections must use common, accessible components.
-   **Audience Prerequisites:** Learners are assumed to have basic Python proficiency and comfort with the command line.

## Stakeholders & Roles
-   **Author:** Responsible for creating the primary content and narrative.
-   **Technical Reviewers:** Responsible for verifying the accuracy, reproducibility, and safety of all code and instructions.
-   **Editors:** Responsible for ensuring clarity, consistency, and adherence to voice and tone guidelines.
-   **Contributors:** Community members who submit improvements via pull requests.
-   **CI/CD Maintainer:** Responsible for the automated build, test, and deployment pipeline.

## Brand Voice & Tone Guidelines
-   **DO:** Use a professional, formal, clear, and instructive tone. Provide concise, step-by-step instructions. Keep explanations simple and direct.
-   **DON'T:** Use overly casual language, slang, or humor that might obscure the instructional purpose. Avoid making assumptions about the reader's implicit knowledge.

## Governance
This Constitution is the authoritative guide for the project. All contributions, reviews, and documentation must align with its principles. Amendments require a documented proposal, review by stakeholders, and a clear rationale for the change.
-   **Compliance:** All pull requests MUST be checked against these principles before being merged.
-   **Versioning:** Changes to this Constitution will follow semantic versioning.

**Version**: 1.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06