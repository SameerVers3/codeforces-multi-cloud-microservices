'use client';

import { useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import axios from 'axios';

export default function Navigation() {
  const router = useRouter();
  const pathname = usePathname();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userInfo, setUserInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, [pathname]);

  const checkAuthStatus = async () => {
    if (typeof window === 'undefined') return;
    
    const token = localStorage.getItem('access_token');
    if (!token) {
      setIsLoggedIn(false);
      setLoading(false);
      return;
    }

    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_AUTH_SERVICE_URL}/api/v1/auth/me`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setIsLoggedIn(true);
      setUserInfo(response.data);
    } catch (error) {
      setIsLoggedIn(false);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsLoggedIn(false);
    setUserInfo(null);
    router.push('/');
  };

  // Don't show navigation on login/register pages
  if (pathname === '/login' || pathname === '/register') {
    return null;
  }

  if (loading) {
    return (
      <nav className="bg-white shadow-md border-b">
        <div className="container mx-auto px-4 py-3">
          <div className="flex justify-between items-center">
            <a href="/" className="text-xl font-bold text-blue-600">
              Codeforces Platform
            </a>
            <div className="text-gray-500">Loading...</div>
          </div>
        </div>
      </nav>
    );
  }

  return (
    <nav className="bg-white shadow-md border-b">
      <div className="container mx-auto px-4 py-3">
        <div className="flex justify-between items-center">
          <a href="/" className="text-xl font-bold text-blue-600">
            Codeforces Platform
          </a>
          
          <div className="flex items-center gap-4">
            {isLoggedIn ? (
              <>
                {userInfo?.role === 'STAFF' && (
                  <a
                    href="/contests/create"
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                  >
                    Create Contest
                  </a>
                )}
                <div className="flex items-center gap-3">
                  <span className="text-gray-700">
                    {userInfo?.full_name || userInfo?.username}
                  </span>
                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
                  >
                    Logout
                  </button>
                </div>
              </>
            ) : (
              <div className="flex items-center gap-3">
                <a
                  href="/login"
                  className="px-4 py-2 text-blue-600 hover:text-blue-800 transition-colors"
                >
                  Login
                </a>
                <a
                  href="/register"
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                >
                  Register
                </a>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

