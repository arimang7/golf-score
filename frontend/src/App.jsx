import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import RoundNew from './pages/RoundNew';
import RoundDetail from './pages/RoundDetail';
import Admin from './pages/Admin';
import { useAuthStore } from './store/authStore';
import api from './api/client';

const App = () => {
  const { isAuthenticated, isLoading, setUser, setLoading } = useAuthStore();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await api.get('/auth/me');
        if (response.data.success && response.data.user) {
          setUser(response.data.user);
        } else {
          setLoading(false);
        }
      } catch (error) {
        console.error("Auth check failed:", error);
        setLoading(false);
      }
    };
    
    checkAuth();
  }, [setUser, setLoading]);

  if (isLoading) {
    return (
      <div className="surface-dark min-h-screen flex items-center justify-center">
        <p className="label-upper" style={{ color: '#969696' }}>Loading...</p>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen surface-dark">
        <Routes>
          <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/" />} />
          <Route 
            path="/" 
            element={isAuthenticated ? <Home /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/rounds/new" 
            element={isAuthenticated ? <RoundNew /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/rounds/:id" 
            element={isAuthenticated ? <RoundDetail /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/admin" 
            element={isAuthenticated ? <Admin /> : <Navigate to="/login" />} 
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
