import { useState, useEffect } from 'react';
import { signInWithEmailAndPassword, signInWithPopup, onAuthStateChanged, signOut, User } from 'firebase/auth';
import { auth, googleProvider } from '../lib/firebase';
import { useRouter } from 'next/navigation';

export function useAuthViewModel() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
      // Optional: automatically redirect if they hit a login page while authed
      if (currentUser && typeof window !== 'undefined' && window.location.pathname === '/login') {
        router.push('/dashboard');
      }
    });
    return () => unsubscribe();
  }, [router]);

  const loginWithEmail = async () => {
    setLoading(true);
    setError(null);
    try {
      await signInWithEmailAndPassword(auth, email, password);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || "Failed to login");
    } finally {
      setLoading(false);
    }
  };

  const loginWithGoogle = async () => {
    setLoading(true);
    setError(null);
    try {
      await signInWithPopup(auth, googleProvider);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || "Failed to login with Google");
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    await signOut(auth);
    router.push('/login');
  };

  return {
    user,
    email,
    setEmail,
    password,
    setPassword,
    error,
    loading,
    loginWithEmail,
    loginWithGoogle,
    logout
  };
}
