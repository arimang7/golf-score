import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { LogOut, Plus, Trophy, ChevronRight, AlertCircle } from 'lucide-react';
import { listRounds } from '../api/rounds';

const Home = () => {
  const { user, logout } = useAuthStore();
  const [rounds, setRounds] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRounds = async () => {
      try {
        const response = await listRounds();
        if (response.success) {
          setRounds(response.data);
        }
      } catch (error) {
        console.error("Failed to fetch rounds", error);
      } finally {
        setLoading(false);
      }
    };
    fetchRounds();
  }, []);

  const isApproved = user?.is_approved;

  return (
    <div className="min-h-screen flex flex-col fade-in">
      {/* ── Dark Cinematic Header ── */}
      <header
        className="surface-dark"
        style={{ padding: '48px 24px 40px', textAlign: 'center' }}
      >
        <div className="slide-up" style={{ marginBottom: 20 }}>
          <div
            style={{
              width: 56,
              height: 56,
              borderRadius: '50%',
              border: '1px solid rgba(255,255,255,0.12)',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Trophy size={24} color="#DA291C" strokeWidth={1.5} />
          </div>
        </div>

        <h1
          className="slide-up slide-up-delay-1"
          style={{
            fontSize: '26px',
            fontWeight: 500,
            lineHeight: 1.20,
            color: '#FFFFFF',
            marginBottom: 6,
          }}
        >
          Par Score
        </h1>

        <p className="label-upper slide-up slide-up-delay-2" style={{ color: '#969696' }}>
          {user?.name || 'Golfer'} {user?.is_admin && <Link to="/admin" style={{ color: '#DA291C', fontSize: '10px', marginLeft: 4, textDecoration: 'underline' }}>(Admin)</Link>}
        </p>
      </header>

      {/* ── White Editorial Body ── */}
      <main
        className="surface-light flex-1"
        style={{ padding: '32px 24px 40px' }}
      >
        {!isApproved ? (
          /* Unapproved User Alert */
          <div className="slide-up slide-up-delay-2" style={{ padding: '24px', border: '1px solid #F13A2C', borderRadius: '2px', background: '#FFF5F5', marginBottom: 24 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, color: '#F13A2C', marginBottom: 8 }}>
              <AlertCircle size={20} />
              <strong style={{ fontSize: '15px' }}>승인 대기 중</strong>
            </div>
            <p style={{ fontSize: '13px', color: '#666', lineHeight: 1.5 }}>
              스코어카드를 작성하려면 관리자의 승인이 필요합니다. 관리자에게 문의해 주세요.
            </p>
          </div>
        ) : (
          /* Approved User: New Round CTA */
          <Link
            to="/rounds/new"
            className="btn-ferrari slide-up slide-up-delay-2"
            style={{
              width: '100%',
              padding: '16px 10px',
              fontSize: '16px',
              marginBottom: 32,
            }}
            id="new-round-btn"
          >
            <Plus size={18} strokeWidth={2} />
            새 라운드 시작
          </Link>
        )}

        {isApproved && (
          <div className="slide-up slide-up-delay-3">
            <p className="label-upper" style={{ marginBottom: 16 }}>
              Recent Rounds
            </p>

            {loading ? (
              <p className="label-micro" style={{ textAlign: 'center', padding: '40px 0' }}>Loading history...</p>
            ) : rounds.length === 0 ? (
              <div
                style={{
                  padding: '40px 16px',
                  textAlign: 'center',
                  border: '1px solid #D2D2D2',
                  borderRadius: '2px',
                }}
              >
                <p style={{ fontSize: '13px', color: '#8F8F8F', lineHeight: 1.5 }}>
                  아직 기록된 라운드가 없습니다.<br />
                  새 라운드를 시작해보세요.
                </p>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                {rounds.map(round => (
                  <Link 
                    key={round.id} 
                    to={`/rounds/${round.id}`}
                    style={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      padding: '20px 0', 
                      borderBottom: '1px solid #EEE',
                      textDecoration: 'none',
                      color: 'inherit'
                    }}
                  >
                    <div style={{ flex: 1 }}>
                      <h3 style={{ fontSize: '16px', fontWeight: 700, marginBottom: 4 }}>{round.course_name}</h3>
                      <p style={{ fontSize: '12px', color: '#8F8F8F' }}>
                        {new Date(round.date).toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric' })} • {round.players.join(', ')}
                      </p>
                    </div>
                    <ChevronRight size={18} color="#D2D2D2" />
                  </Link>
                ))}
              </div>
            )}
          </div>
        )}
      </main>

      <footer
        className="surface-dark-secondary"
        style={{
          padding: '16px 24px',
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <button
          onClick={logout}
          className="btn-ghost"
          style={{ fontSize: '13px', padding: '8px 20px', letterSpacing: '1px' }}
          id="logout-btn"
        >
          <LogOut size={14} strokeWidth={1.5} />
          Logout
        </button>
      </footer>
    </div>
  );
};

export default Home;
