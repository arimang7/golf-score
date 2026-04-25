import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { createRound } from '../api/rounds';
import api from '../api/client';
import { ArrowLeft } from 'lucide-react';

const RoundNew = () => {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [courseId, setCourseId] = useState('');
  const [showNewCourseForm, setShowNewCourseForm] = useState(false);
  const [newCourse, setNewCourse] = useState({ name: '', holes: 18 });
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [players, setPlayers] = useState(['A', 'B', 'C', 'D']);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch courses
    const fetchCourses = async () => {
      try {
        const response = await api.get('/courses/');
        if (response.data.success) {
          setCourses(response.data.data);
          if (response.data.data.length > 0) {
            setCourseId(response.data.data[0].id);
          }
        }
      } catch (error) {
        console.error("Failed to fetch courses", error);
      }
    };
    fetchCourses();
  }, []);

  const handleCourseChange = (e) => {
    const val = e.target.value;
    if (val === 'new') {
      setShowNewCourseForm(true);
      setCourseId('');
    } else {
      setShowNewCourseForm(false);
      setCourseId(val);
    }
  };

  const handlePlayerChange = (index, value) => {
    const newPlayers = [...players];
    newPlayers[index] = value;
    setPlayers(newPlayers);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    let finalCourseId = courseId;

    setLoading(true);
    try {
      if (showNewCourseForm) {
        const courseResponse = await api.post('/courses/', newCourse);
        if (courseResponse.data.success) {
          finalCourseId = courseResponse.data.data.id;
        } else {
          throw new Error("Failed to create course");
        }
      }

      if (!finalCourseId) return;

      const response = await createRound({
        course_id: parseInt(finalCourseId),
        date: new Date(date).toISOString(),
        players: players.filter(p => p.trim() !== '')
      });

      if (response.success) {
        navigate(`/rounds/${response.data.id}`);
      }
    } catch (error) {
      console.error("Failed to create round", error);
      alert("라운드 생성에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col fade-in">
      {/* ── Dark Cinematic Header ── */}
      <header
        className="surface-dark"
        style={{ padding: '20px 24px' }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <Link to="/" style={{ color: '#FFFFFF', display: 'flex' }}>
            <ArrowLeft size={20} strokeWidth={1.5} />
          </Link>
          <h1
            style={{
              fontSize: '18px',
              fontWeight: 700,
              lineHeight: 1.20,
              color: '#FFFFFF',
            }}
          >
            새 라운드
          </h1>
        </div>
        <p className="label-micro" style={{ color: '#969696', marginTop: 4, marginLeft: 32 }}>
          New Round Setup
        </p>
      </header>

      {/* ── White Editorial Form ── */}
      <main className="surface-light flex-1" style={{ padding: '32px 24px 40px' }}>
        <form onSubmit={handleSubmit}>
          {/* Course Select */}
          <div style={{ marginBottom: 24 }}>
            <label className="label-upper" style={{ display: 'block', marginBottom: 8 }}>
              골프장
            </label>
            <select
              value={showNewCourseForm ? 'new' : courseId}
              onChange={handleCourseChange}
              className="select-ferrari"
              required
              id="course-select"
            >
              <option value="" disabled>골프장을 선택하세요</option>
              {courses.map(course => (
                <option key={course.id} value={course.id}>
                  {course.name} ({course.holes}홀)
                </option>
              ))}
              <option value="new">+ 직접 입력...</option>
            </select>
          </div>

          {/* New Course Form (Conditional) */}
          {showNewCourseForm && (
            <div style={{ marginBottom: 24, padding: '16px', background: '#F8F8F8', borderRadius: '2px', border: '1px solid #EEE' }}>
              <div style={{ marginBottom: 12 }}>
                <label className="label-micro" style={{ display: 'block', marginBottom: 4 }}>골프장 이름</label>
                <input
                  type="text"
                  value={newCourse.name}
                  onChange={(e) => setNewCourse({...newCourse, name: e.target.value})}
                  className="input-ferrari"
                  placeholder="예: 페라리 CC"
                  required={showNewCourseForm}
                />
              </div>
              <div>
                <label className="label-micro" style={{ display: 'block', marginBottom: 4 }}>홀 수</label>
                <select
                  value={newCourse.holes}
                  onChange={(e) => setNewCourse({...newCourse, holes: parseInt(e.target.value)})}
                  className="select-ferrari"
                >
                  <option value={9}>9홀</option>
                  <option value={18}>18홀</option>
                  <option value={27}>27홀</option>
                  <option value={36}>36홀</option>
                </select>
              </div>
            </div>
          )}

          {/* Date */}
          <div style={{ marginBottom: 24 }}>
            <label className="label-upper" style={{ display: 'block', marginBottom: 8 }}>
              날짜
            </label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="input-ferrari"
              required
              id="date-input"
            />
          </div>

          {/* Players */}
          <div style={{ marginBottom: 32 }}>
            <label className="label-upper" style={{ display: 'block', marginBottom: 8 }}>
              플레이어
            </label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {players.map((player, index) => (
                <input
                  key={index}
                  type="text"
                  value={player}
                  onChange={(e) => handlePlayerChange(index, e.target.value)}
                  placeholder={`플레이어 ${index + 1}`}
                  className="input-ferrari"
                  id={`player-input-${index}`}
                />
              ))}
            </div>
          </div>

          {/* Submit — Ferrari Red CTA */}
          <button
            type="submit"
            disabled={loading || (!courseId && !showNewCourseForm)}
            className="btn-ferrari"
            style={{ width: '100%', padding: '16px 10px' }}
            id="start-round-btn"
          >
            {loading ? '생성 중...' : '라운드 시작하기'}
          </button>
        </form>
      </main>
    </div>
  );
};

export default RoundNew;
