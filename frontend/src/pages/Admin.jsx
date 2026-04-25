import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import api from '../api/client';
import { ArrowLeft, UserCheck, UserX, Shield } from 'lucide-react';

const Admin = () => {
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user && !user.is_admin) {
      navigate('/');
      return;
    }
    fetchUsers();
  }, [user]);

  const fetchUsers = async () => {
    try {
      const response = await api.get('/auth/users');
      if (response.data.success) {
        setUsers(response.data.data);
      }
    } catch (error) {
      console.error("Failed to fetch users", error);
    } finally {
      setLoading(false);
    }
  };

  const toggleApproval = async (userId, currentStatus) => {
    try {
      const response = await api.post('/auth/users/approve', {
        user_id: userId,
        is_approved: !currentStatus
      });
      if (response.data.success) {
        setUsers(users.map(u => u.id === userId ? { ...u, is_approved: !currentStatus } : u));
      }
    } catch (error) {
      console.error("Failed to toggle approval", error);
      alert("권한 변경에 실패했습니다.");
    }
  };

  if (loading) return <div className="surface-dark min-h-screen flex items-center justify-center"><p className="label-upper">Loading Users...</p></div>;

  return (
    <div className="min-h-screen flex flex-col fade-in">
      <header className="surface-dark" style={{ padding: '20px 24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <Link to="/" style={{ color: '#FFFFFF', display: 'flex' }}><ArrowLeft size={20} /></Link>
          <h1 style={{ fontSize: '18px', fontWeight: 700, color: '#FFFFFF' }}>사용자 관리 (Admin)</h1>
        </div>
      </header>

      <main className="surface-light flex-1" style={{ padding: '24px' }}>
        <p className="label-upper" style={{ marginBottom: 20 }}>Registered Users</p>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {users.map(u => (
            <div key={u.id} style={{ padding: '16px', border: '1px solid #EEE', borderRadius: '2px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                {u.picture_url ? (
                  <img src={u.picture_url} alt="" style={{ width: 40, height: 40, borderRadius: '50%' }} />
                ) : (
                  <div style={{ width: 40, height: 40, borderRadius: '50%', background: '#EEE', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><Shield size={20} color="#8F8F8F" /></div>
                )}
                <div>
                  <h3 style={{ fontSize: '14px', fontWeight: 600 }}>{u.name || 'No Name'}</h3>
                  <p style={{ fontSize: '12px', color: '#8F8F8F' }}>{u.email}</p>
                  <div style={{ marginTop: 4 }}>
                    {u.is_admin && <span style={{ background: '#DA291C', color: '#FFF', fontSize: '10px', padding: '2px 6px', borderRadius: '2px', marginRight: 4 }}>ADMIN</span>}
                    {u.is_approved ? 
                      <span style={{ color: '#03904A', fontSize: '10px', fontWeight: 700 }}>● 승인됨</span> : 
                      <span style={{ color: '#F13A2C', fontSize: '10px', fontWeight: 700 }}>● 미승인</span>
                    }
                  </div>
                </div>
              </div>
              
              {!u.is_admin && (
                <button 
                  onClick={() => toggleApproval(u.id, u.is_approved)}
                  className="btn-small"
                  style={{ padding: '8px 12px', fontSize: '12px', display: 'flex', alignItems: 'center', gap: 6 }}
                >
                  {u.is_approved ? <><UserX size={14} /> 승인 취소</> : <><UserCheck size={14} /> 사용 승인</>}
                </button>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default Admin;
