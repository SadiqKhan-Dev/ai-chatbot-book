/**
 * Custom Navbar with Auth Integration
 * Only shows user menu when logged in
 */

import React, { useState } from 'react';
import Navbar from '@theme-original/Navbar';
import { useAuth } from '@site/src/theme/Auth/AuthContext';
import styles from './navbar.module.css';

// User menu component - only visible when logged in
function UserMenu() {
  const { user, signOut } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);

  if (!user) return null;

  return (
    <div className={styles.userMenu}>
      <button
        onClick={() => setShowDropdown(!showDropdown)}
        className={styles.userButton}
      >
        <span className={styles.avatar}>
          {(user.displayName || user.email || 'U')[0].toUpperCase()}
        </span>
        <span className={styles.userName}>
          {user.displayName || user.email?.split('@')[0] || 'User'}
        </span>
      </button>

      {showDropdown && (
        <div className={styles.dropdown}>
          <div className={styles.dropdownHeader}>
            <span className={styles.dropdownEmail}>{user.email}</span>
          </div>
          <button
            className={styles.dropdownSignOut}
            onClick={() => {
              signOut();
              setShowDropdown(false);
            }}
          >
            Sign Out
          </button>
        </div>
      )}
    </div>
  );
}

// Wrap the original Navbar - auth button hidden, only user menu shows when logged in
export default function NavbarWithAuth(props: any) {
  return (
    <>
      <UserMenu />
      <Navbar {...props} />
    </>
  );
}
