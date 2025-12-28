import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Master embodied intelligence and advanced robotics',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://sadiqkhan-dev.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'SadiqKhan-Dev',
  projectName: 'ai-book',

  onBrokenLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/SadiqKhan-Dev/ai-book/tree/main/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/SadiqKhan-Dev/ai-book/tree/main/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI & Robotics',
      logo: {
        alt: 'Physical AI & Robotics Logo',
        src: 'img/logo.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Modules',
        },
        {
          to: '/blog',
          label: 'Blog',
          position: 'left',
        },
        {
          href: 'https://github.com/SadiqKhan-Dev',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Modules',
          items: [
            {
              label: 'Module 1: Physical AI Fundamentals',
              to: '/docs/physical-ai-robotics-course/introduction-to-physical-ai',
            },
            {
              label: 'Module 2: Digital Twin (Gazebo & Unity)',
              to: '/docs/physical-ai-robotics-course',
            },
            {
              label: 'Module 3: Isaac Sim & Nav2',
              to: '/docs/isaac-sim-navigation',
            },
            {
              label: 'Module 4: VLA Humanoid Planning',
              to: '/docs/vla-humanoid-planning',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'ROS 2 & URDF',
              to: '/docs/ros2-urdf-module',
            },
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub Repository',
              href: 'https://github.com/SadiqKhan-Dev',
            },
          ],
        },
        {
          title: 'Connect',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/SadiqKhan-Dev',
            },
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/in/sadiq-rashid-564375158/',
            },
            {
              label: 'Instagram',
              href: 'https://www.instagram.com/sadiqkhan_dev/',
            },
            {
              label: 'X (Twitter)',
              href: 'https://x.com/saiqkhan3333',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Sadiq Khan. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'python', 'typescript', 'json'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
