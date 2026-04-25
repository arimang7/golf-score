import React, { useState } from 'react';
import { useAuthStore } from '../store/authStore';
import api from '../api/client';
import { Shield } from 'lucide-react';

const Login = () => {
  const { setUser } = useAuthStore();
  const [isAdminMode, setIsAdminMode] = useState(false);
  const [adminCreds, setAdminCreds] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);

  const handleGoogleLogin = () => {
    // 백엔드 Google Login 엔드포인트로 리다이렉트
    window.location.href = 'http://localhost:8000/auth/google/login';
  };

  const handleAdminLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await api.post('/auth/admin/login', adminCreds);
      if (response.data.success) {
        const meRes = await api.get('/auth/me');
        if (meRes.data.success) {
          setUser(meRes.data.user);
        }
      }
    } catch (error) {
      alert("관리자 로그인 실패: 정보를 확인하세요.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="surface-dark flex flex-col items-center justify-center min-h-screen fade-in"
         style={{ padding: '40px 24px' }}>
      
      {/* Prancing Horse — Logo Hero */}
      <div className="slide-up flex flex-col items-center" style={{ marginBottom: '64px' }}>
        {/* Emblem circle on void-black */}
        <div
          style={{
            width: 80,
            height: 80,
            borderRadius: '50%',
            border: '1px solid rgba(255,255,255,0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: 24,
          }}
        >
          {isAdminMode ? <Shield size={36} color="#DA291C" /> : (
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#DA291C" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5C7 4 6 9 6 9Z" />
              <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5C17 4 18 9 18 9Z" />
              <path d="M12 2c-2.5 0-6 3-6 7 0 3 1.5 5 3 6.5s2 3 2 5.5h2c0-2.5.5-4 2-5.5S18 12 18 9c0-4-3.5-7-6-7Z" />
              <path d="M9 18h6" />
              <path d="M10 22h4" />
            </svg>
          )}
        </div>

        <h1 style={{ fontSize: '26px', fontWeight: 500, color: '#FFFFFF', textAlign: 'center', marginBottom: 8 }}>
          Par Score
        </h1>

        <p className="label-upper slide-up slide-up-delay-1" style={{ color: '#969696', textAlign: 'center' }}>
          {isAdminMode ? 'Administrator Portal' : 'AI Voice Golf Scorer'}
        </p>
      </div>

      {/* CTA Section */}
      <div className="slide-up slide-up-delay-2" style={{ width: '100%', maxWidth: 320 }}>
        {!isAdminMode ? (
          <>
            <button
              onClick={handleGoogleLogin}
              className="btn-primary"
              style={{ width: '100%', fontSize: '14px', padding: '14px 10px', marginBottom: 16 }}
              id="google-login-btn"
            >
              <img
                src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
                alt="Google logo"
                width={18}
                height={18}
              />
              Sign in with Google
            </button>
            <button 
              onClick={() => setIsAdminMode(true)}
              className="btn-ghost"
              style={{ width: '100%', fontSize: '12px', border: 'none', color: '#8F8F8F' }}
            >
              관리자 계정 로그인
            </button>
          </>
        ) : (
          <form onSubmit={handleAdminLogin}>
            <div style={{ marginBottom: 12 }}>
              <input 
                type="text" 
                placeholder="Admin ID" 
                className="input-dark"
                value={adminCreds.username}
                onChange={(e) => setAdminCreds({...adminCreds, username: e.target.value})}
                required
              />
            </div>
            <div style={{ marginBottom: 24 }}>
              <input 
                type="password" 
                placeholder="Password" 
                className="input-dark"
                value={adminCreds.password}
                onChange={(e) => setAdminCreds({...adminCreds, password: e.target.value})}
                required
              />
            </div>
            <button 
              type="submit" 
              className="btn-ferrari" 
              style={{ width: '100%', marginBottom: 12, padding: '14px 10px' }}
              disabled={loading}
            >
              {loading ? '로그인 중...' : '관리자 접속'}
            </button>
            <button 
              type="button"
              onClick={() => setIsAdminMode(false)}
              className="btn-ghost"
              style={{ width: '100%', fontSize: '12px', border: 'none' }}
            >
              돌아가기
            </button>
          </form>
        )}
      </div>

      <p className="slide-up slide-up-delay-3" style={{ fontSize: '13px', color: '#8F8F8F', textAlign: 'center', marginTop: 40, maxWidth: 260 }}>
        준비물은 스마트폰과 목소리뿐입니다.<br />
        필드 위에서 더 집중하세요.
      </p>
    </div>
  );
};

export default Login;
