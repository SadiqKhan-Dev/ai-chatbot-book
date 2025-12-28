/**
 * Custom Layout with Auth Integration
 * Wraps the default Docusaurus layout with authentication
 */

import React from 'react';
import Layout from '@theme-original/Layout';
import { AuthProvider } from '@site/src/theme/Auth/AuthContext';
import { LoginButton } from '@site/src/theme/Auth';
import type { LayoutProps } from '@theme/Layout';

// Inject auth button after navbar
function NavbarWithAuth() {
  return (
    <div style={{ position: 'relative' }}>
      {/* Original navbar is rendered by Layout */}
    </div>
  );
}

export default function LayoutWithAuth(props: LayoutProps) {
  return (
    <AuthProvider>
      <Layout {...props} />
    </AuthProvider>
  );
}

// Theme API - expose components
export const components = {
  LoginButton,
};
