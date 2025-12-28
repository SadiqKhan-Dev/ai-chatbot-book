/**
 * Root Wrapper with Auth Provider
 * Wraps the entire Docusaurus app with authentication
 */

import React, { type ReactNode } from 'react';
import { AuthProvider } from './AuthContext';

interface RootWrapperProps {
  children: ReactNode;
}

export default function RootWrapper({ children }: RootWrapperProps) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}
