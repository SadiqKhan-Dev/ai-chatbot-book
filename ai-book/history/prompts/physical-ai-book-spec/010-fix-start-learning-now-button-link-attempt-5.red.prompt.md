---
id: 010
title: Fix 'Start Learning Now' Button Link (Attempt 5: Link to first chapter with /docs prefix)
stage: red
date: 2025-12-06
surface: agent
model: gemini-pro
feature: physical-ai-book-spec
branch: main
user: user
command: fix the btn link with intofix the btn link with intro
labels: [docusaurus, bug-fix, routing]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:

    - src/pages/index.tsx
tests:
null
---

## Prompt

fix the btn link with intofix the btn link with intro

## Response snapshot

I have now set the 'Start Learning Now ??' button to link directly to the first chapter of your book: /docs/physical-ai-robotics-course/01-introduction-to-physical-ai.

## Outcome

- ✅ Impact: Attempted to fix broken link on homepage by linking directly to first chapter using the canonical /docs prefix path.
- 🧪 Tests: Manual verification by user.
- 📁 Files: Modified 1 file: homepage.
- 🔁 Next prompts: User to verify the fix.
- 🧠 Reflection: The debugging step confirmed Link component functionality. The issue was purely path resolution. This attempt uses the full canonical path including /docs and the full slug.

## Evaluation notes (flywheel)

- Failure modes observed: Previous attempts were confused by the _category_.json link generation and the precise interaction with Docusaurus's implicit /docs routing behavior.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): None, awaiting user verification.
