/**
 * Custom Auth Navbar Item for Docusaurus
 * Shows login button or user menu in navbar
 */

import React, { useState } from 'react';
import {
  useAuth,
  LoginButton as LoginButtonComponent,
} from '@site/src/theme/Auth';

export default function AuthNavbarItem() {
  const { user, signOut } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);

  if (!user) {
    return <LoginButtonComponent />;
  }

  return (
    <div className="auth-navbar-item" style={{ position: 'relative' }}>
      <button
        onClick={() => setShowDropdown(!showDropdown)}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '6px 12px',
          background: 'var(--bg-secondary, #f1f5f9)',
          border: '1px solid var(--border-light, #e2e8f0)',
          borderRadius: '24px',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
        }}
      >
        <span
          style={{
            width: '28px',
            height: '28px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontSize: '12px',
            fontWeight: 'bold',
          }}
        >
          {(user.displayName || user.email || 'U')[0].toUpperCase()}
        </span>
        <span
          style={{
            fontSize: '14px',
            fontWeight: '500',
            color: 'var(--text-primary, #0f172a)',
            maxWidth: '100px',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
          }}
        >
          {user.displayName || user.email?.split('@')[0] || 'User'}
        </span>
      </button>

      {showDropdown && (
        <div
          style={{
            position: 'absolute',
            top: 'calc(100% + 8px)',
            right: 0,
            minWidth: '180px',
            background: 'var(--bg-card, #ffffff)',
            border: '1px solid var(--border-light, #e2e8f0)',
            borderRadius: '8px',
            boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
            zIndex: 1000,
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              padding: '12px 16px',
              borderBottom: '1px solid var(--border-light, #e2e8f0)',
              fontSize: '13px',
              color: 'var(--text-secondary, #64748b)',
            }}
          >
            {user.email}
          </div>
          <button
            onClick={() => {
              signOut();
              setShowDropdown(false);
            }}
            style={{
              width: '100%',
              padding: '12px 16px',
              background: 'transparent',
              border: 'none',
              textAlign: 'left',
              cursor: 'pointer',
              fontSize: '14px',
              color: 'var(--text-secondary, #64748b)',
              transition: 'all 0.15s ease',
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.background = 'var(--bg-secondary, #f1f5f9)';
              e.currentTarget.style.color = 'var(--color-error, #ef4444)';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.background = 'transparent';
              e.currentTarget.style.color = 'var(--text-secondary, #64748b)';
            }}
          >
            Sign Out
          </button>
        </div>
      )}
    </div>
  );
}
