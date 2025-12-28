# Specification: AI Robotics Course

This document outlines the technical and content specifications for the AI Robotics Course book, built on the principles defined in the project Constitution.

## A. Book Structure Rules

The book follows a clear hierarchical structure to ensure a logical and progressive learning path.

-   **Hierarchy**: The content is organized into a three-tier structure: `Module` → `Chapter` → `Lesson`.
    -   **Modules** are high-level topics (e.g., "Introduction to ROS 2").
    -   **Chapters** are specific sub-topics within a module (e.g., "Nodes and Topics").
    -   **Lessons** are atomic, self-contained instructional units (e.g., "Creating a ROS 2 Publisher").

-   **Content Rule**: Each **Chapter** MUST contain exactly **three (3) Lessons**. This ensures consistency and predictable effort for each chapter.

-   **Atomic Unit**: Lessons are the fundamental unit of publication. Each lesson will be rendered as a separate, independent page within the Docusaurus site.

-   **File Mapping Rule**: The file path directly maps to the book's structure. The canonical path for a lesson MUST be:
    `docs/module-<n>/chapter-<m>/lesson-<x>.md`
    -   `<n>`: Module number
    -   `<m>`: Chapter number
    -   `<x>`: Lesson number

-   **Sidebar Labels**: To maintain a clean and navigable table of contents, sidebar labels MUST follow this format:
    `Module <n> — Chapter <m>: <Lesson Title>`
    -   Example: `Module 1 — Chapter 2: Understanding Services`

## B. Content Guidelines

These guidelines ensure the content is effective, engaging, and aligned with our pedagogical principles.

-   **Writing Style**:
    -   Use short, concise paragraphs to improve readability.
    -   Employ the **active voice** wherever possible.
    -   All procedures, installations, or multi-step instructions MUST be presented as **numbered lists**.

-   **Educational Goals**:
    -   Every lesson MUST begin with a clearly stated list of **2–3 learning objectives**. These objectives must be actionable and measurable.

-   **Lesson Structure Template**: Each lesson's markdown file MUST adhere to the following structure:
    1.  **Docusaurus Frontmatter**: Metadata for the page (title, slug, etc.).
    2.  **Learning Objectives**: A bulleted list of what the learner will be able to do after completing the lesson.
    3.  **Introduction**: A brief paragraph setting the context for the lesson.
    4.  **Explanation**: The core instructional content, explaining the concepts.
    5.  **Runnable Code Example**: A complete, self-contained code example that the user can run to see the concept in action. This honors the "Hands-On First" and "Reproducibility" principles.
    6.  **Practical Exercise**: A hands-on task for the learner to complete, applying the concepts from the lesson.
    7.  **Exercise Solution**: The solution to the practical exercise.
    8.  **Further Reading (Optional)**: Links to supplementary materials.
    9.  **References (Optional)**: Citations for any external sources.

## C. Docusaurus Organization Rules

These rules govern the file structure and configuration of the Docusaurus project.

-   **Folder Structure**: The `docs` directory MUST be organized as follows:
    ```
    docs/
    └── module-1/
        ├── chapter-1/
        │   ├── lesson-1.md
        │   ├── lesson-2.md
        │   └── lesson-3.md
        └── chapter-2/
            ├── lesson-1.md
            ├── lesson-2.md
            └── lesson-3.md
    ```

-   **Filenames**: Lesson filenames MUST be in `lower-kebab-case` and correspond to the lesson number (e.g., `lesson-1.md`, `lesson-2.md`).

-   **Frontmatter**: Every lesson file MUST include the following frontmatter keys:
    -   `id` (optional): Unique identifier for the document.
    -   `title`: The main title of the document, displayed at the top of the page.
    -   `description`: A short summary of the content for SEO purposes.
    -   `sidebar_label`: The short title used in the navigation sidebar.
    -   `slug`: The URL slug for the page (e.g., `/module-1/chapter-1/creating-a-publisher`).

-   **Sidebar Configuration**: The `sidebars.ts` file should group lessons logically by module and chapter. The structure should resemble the following example:

    ```javascript
    import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

    const sidebars: SidebarsConfig = {
      tutorialSidebar: [
        {
          type: 'category',
          label: 'Module 1: Introduction to ROS 2',
          items: [
            {
              type: 'category',
              label: 'Chapter 1: Basic Concepts',
              link: {
                type: 'generated-index',
              },
              items: [
                'module-1/chapter-1/lesson-1', // Corresponds to lesson-1.md
                'module-1/chapter-1/lesson-2',
                'module-1/chapter-1/lesson-3',
              ],
            },
            {
              type: 'category',
              label: 'Chapter 2: Intermediate Concepts',
               link: {
                type: 'generated-index',
              },
              items: [
                'module-1/chapter-2/lesson-1',
                'module-1/chapter-2/lesson-2',
                'module-1/chapter-2/lesson-3',
              ],
            },
          ],
        },
      ],
    };

    export default sidebars;
    ```

-   **Admonitions**: Use Docusaurus admonitions to highlight important information:
    -   `:::note` for supplementary information.
    -   `:::tip` for helpful tips or best practices.
    -   `:::warning` for critical warnings, especially regarding safety or potential errors. This aligns with the "Foundational Safety" principle.