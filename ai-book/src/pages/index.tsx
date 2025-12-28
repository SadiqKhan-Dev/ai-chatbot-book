import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

// Module data for the course
const modules = [
  {
    number: '01',
    title: 'Physical AI Fundamentals',
    description: 'Introduction to embodied intelligence, robotics foundations, and core concepts.',
    chapters: 10,
    duration: '8 hours',
    to: '/docs/physical-ai-robotics-course/introduction-to-physical-ai',
    color: '#3b82f6',
  },
  {
    number: '02',
    title: 'Digital Twin: Gazebo & Unity',
    description: 'Create realistic robot simulations in Gazebo and Unity environments.',
    chapters: 4,
    duration: '6 hours',
    to: '/docs/physical-ai-robotics-course',
    color: '#10b981',
  },
  {
    number: '03',
    title: 'Isaac Sim & Nav2',
    description: 'Advanced navigation with NVIDIA Isaac Sim and ROS 2 Nav2 integration.',
    chapters: 3,
    duration: '5 hours',
    to: '/docs/isaac-sim-navigation',
    color: '#f59e0b',
  },
  {
    number: '04',
    title: 'ROS 2 & URDF Module',
    description: 'Master ROS 2 communication and robot modeling with URDF.',
    chapters: 4,
    duration: '6 hours',
    to: '/docs/ros2-urdf-module',
    color: '#ef4444',
  },
  {
    number: '05',
    title: 'VLA Humanoid Planning',
    description: 'Vision-Language-Action pipelines for humanoid robot control.',
    chapters: 3,
    duration: '5 hours',
    to: '/docs/vla-humanoid-planning',
    color: '#8b5cf6',
  },
];

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className={clsx('container', styles.heroContent)}>
        <div className={styles.heroBadge}>Physical AI & Robotics Course</div>
        <Heading as="h1" className="hero__title">
          Master Embodied Intelligence
        </Heading>
        <p className="hero__subtitle">
          Your comprehensive journey through physical AI, humanoid robotics, and advanced automation.
          From simulation to deployment, learn to build the robots of tomorrow.
        </p>
        <div className={styles.heroCta}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Start Learning 🚀
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/docs/physical-ai-robotics-course/introduction-to-physical-ai">
            Explore Modules
          </Link>
        </div>
        <div className={styles.heroStats}>
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>5</span>
            <span className={styles.heroStatLabel}>Modules</span>
          </div>
          <div className={styles.heroStatDivider} />
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>24+</span>
            <span className={styles.heroStatLabel}>Chapters</span>
          </div>
          <div className={styles.heroStatDivider} />
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>30h</span>
            <span className={styles.heroStatLabel}>Content</span>
          </div>
        </div>
      </div>
    </header>
  );
}

function ModuleCard({module, index}: {module: typeof modules[0]; index: number}) {
  return (
    <div
      className={clsx('col', styles.moduleCardCol)}
      style={{'--module-color': module.color} as React.CSSProperties}
    >
      <Link to={module.to} className={styles.moduleCard}>
        <div className={styles.moduleCardHeader}>
          <span className={styles.moduleNumber}>{module.number}</span>
          <div className={styles.moduleCardIcon}>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            </svg>
          </div>
        </div>
        <div className={styles.moduleCardBody}>
          <h3 className={styles.moduleTitle}>{module.title}</h3>
          <p className={styles.moduleDescription}>{module.description}</p>
        </div>
        <div className={styles.moduleCardFooter}>
          <span className={styles.moduleMeta}>
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
            </svg>
            {module.chapters} chapters
          </span>
          <span className={styles.moduleMeta}>
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
            {module.duration}
          </span>
        </div>
        <div className={styles.moduleCardArrow}>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
          </svg>
        </div>
      </Link>
    </div>
  );
}

function LearningPathSection() {
  return (
    <section className={clsx(styles.homeSection, styles.learningPathSection)}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <Heading as="h2" className={styles.sectionTitle}>
            Learning Path
          </Heading>
          <p className={styles.sectionSubtitle}>
            Progress through the modules sequentially or jump to any topic that interests you.
          </p>
        </div>
        <div className="row stagger-children">
          {modules.map((module, index) => (
            <ModuleCard key={module.number} module={module} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
}

function FeaturesSection() {
  const features = [
    {
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polygon points="12 2 2 7 12 12 22 7 12 2"/>
          <polyline points="2 17 12 22 22 17"/>
          <polyline points="2 12 12 17 22 12"/>
        </svg>
      ),
      title: 'Hands-On Simulations',
      description: 'Build and test robots in Gazebo, Unity, and NVIDIA Isaac Sim environments.',
    },
    {
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
          <line x1="8" y1="21" x2="16" y2="21"/>
          <line x1="12" y1="17" x2="12" y2="21"/>
        </svg>
      ),
      title: 'Real Robot Integration',
      description: 'Deploy your code to physical robots using ROS 2 and modern tooling.',
    },
    {
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
          <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
          <line x1="12" y1="22.08" x2="12" y2="12"/>
        </svg>
      ),
      title: 'Complete Workflow',
      description: 'From modeling and simulation to deployment and testing.',
    },
  ];

  return (
    <section className={clsx(styles.homeSection, styles.featuresSection)}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <Heading as="h2" className={styles.sectionTitle}>
            Why This Course?
          </Heading>
        </div>
        <div className="row">
          {features.map((feature, index) => (
            <div key={index} className={clsx('col', styles.featureCol)}>
              <div className={styles.featureCard}>
                <div className={styles.featureIcon}>{feature.icon}</div>
                <h3 className={styles.featureTitle}>{feature.title}</h3>
                <p className={styles.featureDescription}>{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function FutureTechSection() {
  const futureTopics = [
    {
      emoji: '🌟',
      title: 'Quantum Robotics',
      description: 'Quantum computing for ultra-fast robot decision-making in complex environments.',
    },
    {
      emoji: '🌌',
      title: 'Bio-Integrated Humanoids',
      description: 'Robotics merging with synthetic biology for self-repairing machines.',
    },
    {
      emoji: '🌐',
      title: 'Swarm Intelligence',
      description: 'Billions of interconnected robots solving global challenges collaboratively.',
    },
    {
      emoji: '🚀',
      title: 'Empathic AI Companions',
      description: 'Robots that understand and respond to human emotions naturally.',
    },
  ];

  return (
    <section className={clsx(styles.homeSection, styles.futureTechSection)}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <Heading as="h2" className={styles.sectionTitle}>
            The Future of Robotics
          </Heading>
          <p className={styles.sectionSubtitle}>
            Explore cutting-edge concepts that will shape the next generation of intelligent machines.
          </p>
        </div>
        <div className="row">
          {futureTopics.map((topic, index) => (
            <div key={index} className={clsx('col', styles.futureTechCol)}>
              <div className={styles.futureTechCard}>
                <span className={styles.futureTechEmoji}>{topic.emoji}</span>
                <h3 className={styles.futureTechTitle}>{topic.title}</h3>
                <p className={styles.futureTechDescription}>{topic.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Physical AI & Humanoid Robotics"
      description="Master embodied intelligence and advanced robotics through hands-on simulations and real robot deployment.">
      <HomepageHeader />
      <main>
        <LearningPathSection />
        <FeaturesSection />
        <FutureTechSection />
      </main>
    </Layout>
  );
}
