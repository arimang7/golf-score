import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getRound, updateHoleScore } from '../api/rounds';
import HoleCard from '../components/HoleCard';
import { ArrowLeft } from 'lucide-react';

const RoundDetail = () => {
  const { id } = useParams();
  const [round, setRound] = useState(null);
  const [loading, setLoading] = useState(true);
  const [voiceMessage, setVoiceMessage] = useState('');

  useEffect(() => { fetchRound(); }, [id]);

  const fetchRound = async () => {
    try {
      const response = await getRound(id);
      if (response.success) {
        setRound(response.data);
      }
    } catch (error) {
      console.error("Failed to fetch round", error);
    } finally {
      setLoading(false);
    }
  };

  const handleScoreChange = async (holeNumber, field, value) => {
    const updatedScores = round.scores.map(hole =>
      hole.hole_number === holeNumber ? { ...hole, [field]: value } : hole
    );
    setRound({ ...round, scores: updatedScores });
    try {
      let scoresToUpdate = {};
      let parToUpdate = undefined;
      if (field === 'par') { 
        parToUpdate = value; 
      } else { 
        scoresToUpdate[field] = value; 
      }
      await updateHoleScore(id, holeNumber, scoresToUpdate, parToUpdate);
    } catch (error) {
      console.error("Failed to update score", error);
      fetchRound();
    }
  };

  const handleBulkScoreChange = async (holeNumber, scoresToUpdate) => {
    const updatedScores = round.scores.map(hole => {
      if (hole.hole_number === holeNumber) {
        return { ...hole, ...scoresToUpdate };
      }
      return hole;
    });
    setRound({ ...round, scores: updatedScores });
    try {
      await updateHoleScore(id, holeNumber, scoresToUpdate);
    } catch (error) {
      console.error("Failed to bulk update scores", error);
      fetchRound();
    }
  };

  if (loading) {
    return (
      <div className="surface-dark min-h-screen flex items-center justify-center">
        <p className="label-upper">Loading...</p>
      </div>
    );
  }
  if (!round) {
    return (
      <div className="surface-dark min-h-screen flex items-center justify-center">
        <p style={{ fontSize: '13px', color: '#8F8F8F' }}>Round not found</p>
      </div>
    );
  }

  const totalRelative = [0, 0, 0, 0];
  const totalStrokes = [0, 0, 0, 0];
  const totalPar = round.scores.reduce((sum, h) => sum + (h.par || 0), 0);

  round.scores.forEach(hole => {
    if (hole.score_a !== null && hole.score_a !== undefined) {
      totalRelative[0] += hole.score_a;
      totalStrokes[0] += hole.score_a + (hole.par || 0);
    }
    if (hole.score_b !== null && hole.score_b !== undefined) {
      totalRelative[1] += hole.score_b;
      totalStrokes[1] += hole.score_b + (hole.par || 0);
    }
    if (hole.score_c !== null && hole.score_c !== undefined) {
      totalRelative[2] += hole.score_c;
      totalStrokes[2] += hole.score_c + (hole.par || 0);
    }
    if (hole.score_d !== null && hole.score_d !== undefined) {
      totalRelative[3] += hole.score_d;
      totalStrokes[3] += hole.score_d + (hole.par || 0);
    }
  });

  return (
    <div className="min-h-screen flex flex-col fade-in" style={{ paddingBottom: 32 }}>
      {/* Dark Cinematic Sticky Header */}
      <div className="surface-dark" style={{ position: 'sticky', top: 0, zIndex: 40, padding: '16px 24px 20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
          <Link to="/" style={{ color: '#FFFFFF', display: 'flex' }}>
            <ArrowLeft size={20} strokeWidth={1.5} />
          </Link>
          <h1 style={{ fontSize: '18px', fontWeight: 700, lineHeight: 1.20, color: '#FFFFFF', flex: 1 }}>
            Scorecard
          </h1>
          <span className="label-micro" style={{ color: '#969696' }}>Total Par {totalPar}</span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: `repeat(${round.players.length}, 1fr)`, gap: 8 }}>
          {round.players.map((p, i) => (
            <div key={i} style={{ textAlign: 'center', padding: '8px 4px', borderRadius: '2px', background: 'rgba(255,255,255,0.05)' }}>
              <span className="label-micro" style={{ color: '#969696', display: 'block', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{p}</span>
              <div style={{ marginTop: 4 }}>
                <span style={{ fontSize: '20px', fontWeight: 500, color: '#FFFFFF', lineHeight: 1.2, display: 'block' }}>
                  {totalStrokes[i]}
                </span>
                <span className="label-micro" style={{ color: totalRelative[i] < 0 ? '#DA291C' : totalRelative[i] > 0 ? '#3860BE' : '#03904A' }}>
                  {totalRelative[i] > 0 ? `+${totalRelative[i]}` : totalRelative[i]}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Voice Message Toast */}
      {voiceMessage && (
        <div style={{ position: 'fixed', top: 140, left: '50%', transform: 'translateX(-50%)', background: 'var(--color-overlay-dark)', color: '#FFFFFF', padding: '8px 20px', borderRadius: '2px', zIndex: 50, fontSize: '12px', letterSpacing: '0.1px', whiteSpace: 'nowrap' }}>
          {voiceMessage}
        </div>
      )}

      {/* White Editorial Body */}
      <main className="surface-light flex-1" style={{ padding: '20px 16px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {round.scores.sort((a, b) => a.hole_number - b.hole_number).map(hole => (
            <HoleCard 
              key={hole.id} 
              hole={hole} 
              players={round.players} 
              onScoreChange={handleScoreChange} 
              onBulkScoreChange={handleBulkScoreChange}
            />
          ))}
        </div>
      </main>
    </div>
  );
};

export default RoundDetail;
