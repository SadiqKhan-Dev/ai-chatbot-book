/**
 * Protected Route Wrapper
 * Restricts access to authenticated users only
 */

import React, { useState, useEffect, type ReactNode } from 'react';
import { useAuth } from './AuthContext';
import styles from './styles.module.css';

interface ProtectedRouteProps {
  children: ReactNode;
  fallback?: ReactNode;
}

export function ProtectedRoute({ children, fallback }: ProtectedRouteProps) {
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading && !user) {
      // Redirect to login page
      window.location.href = '/login';
    }
  }, [user, loading]);

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <div className={styles.loadingSpinner} />
        <p>Verifying access...</p>
      </div>
    );
  }

  if (!user) {
    return fallback || (
      <div className={styles.loadingContainer}>
        <div className={styles.loadingSpinner} />
        <p>Redirecting to sign in...</p>
      </div>
    );
  }

  return <>{children}</>;
}

interface AccessDeniedProps {
  onRequestAccess: () => void;
  showRedirect?: boolean;
}

export function AccessDenied({ onRequestAccess, showRedirect = true }: AccessDeniedProps) {
  const [countdown, setCountdown] = useState(3);

  useEffect(() => {
    if (showRedirect) {
      const timer = setTimeout(() => {
        window.location.href = '/login';
      }, 3000);
      const counter = setInterval(() => {
        setCountdown((prev) => Math.max(0, prev - 1));
      }, 1000);
      return () => {
        clearTimeout(timer);
        clearInterval(counter);
      };
    }
  }, [showRedirect]);

  return (
    <div className={styles.accessDeniedContainer}>
      <div className={styles.accessDeniedCard}>
        <div className={styles.lockIcon}>
          <svg width="72" height="72" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            <circle cx="12" cy="16" r="1" />
            <path d="M12 16v-2" />
          </svg>
        </div>

        <h1 className={styles.accessDeniedTitle}>Premium Content</h1>
        <p className={styles.accessDeniedDescription}>
          This chapter is part of the Physical AI & Robotics course. Sign in to access all course materials, exercises, and projects.
        </p>

        {showRedirect && (
          <p className={styles.redirectNotice}>
            Redirecting to sign in in {countdown} seconds...
          </p>
        )}

        <a href="/login" className={styles.accessButton}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
            <polyline points="10 17 15 12 10 7" />
            <line x1="15" y1="12" x2="3" y2="12" />
          </svg>
          Sign In to Continue
        </a>

        <div className={styles.accessBenefits}>
          <h3>What You'll Get Access To:</h3>
          <ul>
            <li>Complete Physical AI curriculum with 4 modules</li>
            <li>Hands-on exercises with Gazebo & Unity digital twins</li>
            <li>ROS 2 integration and URDF robot modeling</li>
            <li>Isaac Sim navigation and VLA Humanoid Planning</li>
            <li>Downloadable code examples and project templates</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

/**
 * Component to wrap entire docs content
 * Use this to protect documentation pages
 */
export function DocsProtected({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <div className={styles.loadingSpinner} />
        <p>Loading content...</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className={styles.lockedDocs}>
        <AccessDenied />
      </div>
    );
  }

  return <>{children}</>;
}

/**
 * Inline lock badge for content sections
 */
export function Authenticated({ children }: { children: ReactNode }) {
  const { user } = useAuth();

  if (!user) {
    return null;
  }

  return <>{children}</>;
}

/**
 * Component that shows content preview with a lock overlay
 * Use this for chapter previews
 */
export function ContentPreview({ children }: { children: ReactNode }) {
  const { user } = useAuth();

  if (user) {
    return <>{children}</>;
  }

  return (
    <div className={styles.previewContainer}>
      <div className={styles.previewOverlay}>
        <div className={styles.previewLock}>
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
          </svg>
          <span>Sign in to unlock full content</span>
          <a href="/login" className={styles.previewButton}>
            Continue Reading
          </a>
        </div>
      </div>
      <div className={styles.blurContent}>
        {children}
      </div>
    </div>
  );
}
