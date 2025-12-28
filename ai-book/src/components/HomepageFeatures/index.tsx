import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  icon: string; // Using string for emoji
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Comprehensive Curriculum',
    icon: '📚',
    description: (
      <>
        Dive deep into the foundations of Physical AI and the intricacies of Humanoid Robotics with a structured, in-depth curriculum.
      </>
    ),
  },
  {
    title: 'Interactive AI Assistant',
    icon: '🤖',
    description: (
      <>
        Get instant answers and clarification on course material with our integrated AI agent, powered by Gemini 2.5 Flash.
      </>
    ),
  },
  {
    title: 'Practical Applications',
    icon: '💡',
    description: (
      <>
        Explore real-world examples and practical applications, bridging the gap between theory and hands-on robotics.
      </>
    ),
  },
  {
    title: 'Cutting-Edge Topics',
    icon: '⚡',
    description: (
      <>
        Stay ahead with chapters on advanced topics like Machine Learning for Robotics and Human-Robot Interaction.
      </>
    ),
  },
  {
    title: 'Self-Paced Learning',
    icon: '⏱️',
    description: (
      <>
        Learn at your own pace with a clear, well-organized textbook format, designed for both beginners and advanced learners.
      </>
    ),
  },
  {
    title: 'Docusaurus Powered',
    icon: '📄',
    description: (
      <>
        Enjoy a modern and responsive reading experience built with Docusaurus, making navigation and content consumption seamless.
      </>
    ),
  },
];

function Feature({title, icon, description}: FeatureItem) { // Updated props
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <span style={{fontSize: '48px'}}>{icon}</span> {/* Display emoji */}
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
