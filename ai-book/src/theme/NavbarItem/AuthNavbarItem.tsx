/**
 * Custom Navbar Item for Authentication
 * Replaces the default navbar with login/user menu
 */

import React from 'react';
import { useAuth } from '../Auth';
import LoginButton from '../Auth/LoginButton';

export default function AuthNavbarItem() {
  const { user, isDemoMode } = useAuth();

  // If user is logged in, show user info in navbar
  if (user) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        padding: '4px 12px',
        background: 'var(--bg-secondary)',
        borderRadius: '24px',
        border: '1px solid var(--border-light)',
      }}>
        <span style={{
          width: '28px',
          height: '28px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, var(--color-primary-500), var(--color-primary-600))',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          fontSize: '12px',
          fontWeight: 'bold',
        }}>
          {(user.displayName || user.email || 'U')[0].toUpperCase()}
        </span>
        <span style={{
          fontSize: '14px',
          fontWeight: '500',
          color: 'var(--text-primary)',
          maxWidth: '100px',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          whiteSpace: 'nowrap',
        }}>
          {user.displayName || user.email?.split('@')[0]}
        </span>
        {isDemoMode && (
          <span style={{
            fontSize: '10px',
            padding: '2px 6px',
            background: 'var(--color-warning-light)',
            color: 'var(--color-warning)',
            borderRadius: '4px',
          }}>
            Demo
          </span>
        )}
      </div>
    );
  }

  // Show login button
  return <LoginButton />;
}
