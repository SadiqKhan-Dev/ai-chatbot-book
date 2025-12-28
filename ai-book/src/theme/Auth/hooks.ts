/**
 * Auth Hook for Docusaurus
 * Easy way to add authentication to any component
 */

import { useAuth, AuthProvider } from './AuthContext';
import LoginButton from './LoginButton';
import { ProtectedRoute, DocsProtected } from './ProtectedRoute';

export { useAuth, AuthProvider, LoginButton, ProtectedRoute, DocsProtected };
