/**
 * Firebase Configuration
 * IMPORTANT: API keys should be loaded from environment variables in production
 *
 * For development, create a .env file with:
 * VITE_FIREBASE_API_KEY=your_api_key
 * VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
 * VITE_FIREBASE_PROJECT_ID=your-project-id
 * VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
 * VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
 * VITE_FIREBASE_APP_ID=1:123456789:web:abc123
 * VITE_FIREBASE_MEASUREMENT_ID=G-XXXXXXXX
 * VITE_USE_FIREBASE=true (set to false for demo mode)
 *
 * Demo mode allows testing without Firebase credentials
 */

import { initializeApp, getApps, type FirebaseApp } from 'firebase/app';
import {
  getAuth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  GoogleAuthProvider,
  signInWithPopup,
  type Auth,
  type User,
} from 'firebase/auth';

// Demo mode flag - enabled when explicitly set to 'false'
// By default, we try to use Firebase if API key is available
// Set VITE_USE_FIREBASE=false in .env to force demo mode
const DEMO_MODE = (() => {
  if (typeof process !== 'undefined' && process.env?.VITE_USE_FIREBASE === 'false') {
    return true;
  }
  // Check for Firebase API key in environment
  const hasApiKey = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_FIREBASE_API_KEY) ||
    (typeof process !== 'undefined' && process.env?.VITE_FIREBASE_API_KEY);
  return !hasApiKey;
})();

// Firebase configuration - Use environment variables
// For security, NEVER hardcode API keys in production
const getFirebaseConfig = () => {
  return {
    apiKey: process.env.VITE_FIREBASE_API_KEY || 'demo-api-key',
    authDomain: process.env.VITE_FIREBASE_AUTH_DOMAIN || 'demo-project.firebaseapp.com',
    projectId: process.env.VITE_FIREBASE_PROJECT_ID || 'demo-project',
    storageBucket: process.env.VITE_FIREBASE_STORAGE_BUCKET || 'demo-project.appspot.com',
    messagingSenderId: process.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '123456789',
    appId: process.env.VITE_FIREBASE_APP_ID || '1:123456789:web:abc123',
    measurementId: process.env.VITE_FIREBASE_MEASUREMENT_ID || 'G-XXXXXXXX',
  };
};

// Initialize Firebase - only on client side
let app: FirebaseApp | undefined;
let auth: Auth | undefined;

const initFirebase = () => {
  if (typeof window === 'undefined') return;

  if (!app && !DEMO_MODE) {
    const config = getFirebaseConfig();
    app = getApps().length === 0 ? initializeApp(config) : getApps()[0];
    auth = getAuth(app);
  }
};

// Initialize on import
initFirebase();

// Demo user for testing (when Firebase is not configured)
const DEMO_USER: User = {
  uid: 'demo-user-123',
  email: 'demo@aibook.com',
  displayName: 'Demo User',
  photoURL: null,
  emailVerified: true,
  isAnonymous: false,
  metadata: {} as User['metadata'],
  providerData: [],
  providerId: 'firebase',
  refreshToken: '',
  tenantId: null,
  deleteUser: async () => {},
  getIdToken: async () => 'demo-token',
  getIdTokenResult: async () => ({
    token: 'demo-token',
    expirationTime: new Date(Date.now() + 3600000).toISOString(),
    claims: {},
    signInProvider: null,
    signInSecondFactor: null,
  }),
  reload: async () => {},
  toJSON: () => ({}),
} as User;

export {
  app,
  auth,
  DEMO_MODE,
  DEMO_USER,
  getFirebaseConfig,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  firebaseSignOut,
  onAuthStateChanged,
  GoogleAuthProvider,
};
export type { User };
