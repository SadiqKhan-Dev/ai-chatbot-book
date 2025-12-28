/**
 * Authentication Context
 * Provides authentication state to the entire application
 */

import React, { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import {
  auth,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  firebaseSignOut,
  GoogleAuthProvider,
  DEMO_MODE,
  DEMO_USER,
  type User,
} from './firebase';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signInWithGoogle: () => Promise<void>;
  signOut: () => Promise<void>;
  clearError: () => void;
  isDemoMode: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (DEMO_MODE) {
      // Demo mode: check localStorage
      const storedUser = localStorage.getItem('demoUser');
      if (storedUser) {
        try {
          setUser(JSON.parse(storedUser));
        } catch {
          localStorage.removeItem('demoUser');
        }
      }
      setLoading(false);
      return;
    }

    if (!auth) {
      setLoading(false);
      return;
    }

    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const signIn = async (email: string, password: string) => {
    setError(null);
    try {
      if (DEMO_MODE) {
        // Demo mode: simulate sign in
        const demoUser = { ...DEMO_USER, email } as User;
        setUser(demoUser);
        localStorage.setItem('demoUser', JSON.stringify(demoUser));
      } else if (auth) {
        await signInWithEmailAndPassword(auth, email, password);
      }
    } catch (err: unknown) {
      const firebaseError = err as { code?: string; message?: string };
      setError(firebaseError.message || 'Failed to sign in');
      throw err;
    }
  };

  const signUp = async (email: string, password: string) => {
    setError(null);
    try {
      if (DEMO_MODE) {
        // Demo mode: simulate sign up
        const demoUser = { ...DEMO_USER, email } as User;
        setUser(demoUser);
        localStorage.setItem('demoUser', JSON.stringify(demoUser));
      } else if (auth) {
        await createUserWithEmailAndPassword(auth, email, password);
      }
    } catch (err: unknown) {
      const firebaseError = err as { code?: string; message?: string };
      setError(firebaseError.message || 'Failed to create account');
      throw err;
    }
  };

  const signInWithGoogle = async () => {
    setError(null);
    try {
      if (DEMO_MODE) {
        const demoUser = { ...DEMO_USER } as User;
        setUser(demoUser);
        localStorage.setItem('demoUser', JSON.stringify(demoUser));
      } else if (auth) {
        const provider = new GoogleAuthProvider();
        await signInWithPopup(auth, provider);
      }
    } catch (err: unknown) {
      const firebaseError = err as { code?: string; message?: string };
      setError(firebaseError.message || 'Failed to sign in with Google');
      throw err;
    }
  };

  const signOut = async () => {
    setError(null);
    try {
      if (DEMO_MODE) {
        setUser(null);
        localStorage.removeItem('demoUser');
      } else if (auth) {
        await firebaseSignOut(auth);
      }
    } catch (err: unknown) {
      const firebaseError = err as { code?: string; message?: string };
      setError(firebaseError.message || 'Failed to sign out');
      throw err;
    }
  };

  const clearError = () => setError(null);

  const value: AuthContextType = {
    user,
    loading,
    error,
    signIn,
    signUp,
    signInWithGoogle,
    signOut,
    clearError,
    isDemoMode: DEMO_MODE,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
