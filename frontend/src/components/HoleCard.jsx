import React, { useState, useRef } from 'react';
import { Mic, Square, Loader2 } from 'lucide-react';
import { parseVoiceText } from '../api/rounds';

const HoleCard = ({ hole, players, onScoreChange, onBulkScoreChange }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [debugText, setDebugText] = useState("");
  const recognitionRef = useRef(null);

  const stopVoiceInput = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }
    setIsRecording(false);
    setDebugText("수동 중지");
    setTimeout(() => setDebugText(""), 2000);
  };

  const startVoiceInput = async () => {
    if (isRecording) {
      stopVoiceInput();
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setDebugText("음성 인식 미지원");
      setTimeout(() => setDebugText(""), 3000);
      return;
    }

    // 모바일에서 SpeechRecognition 전에 마이크 권한을 먼저 획득
    // (일부 모바일 브라우저는 getUserMedia 없이 SpeechRecognition 마이크 접근을 거부)
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      // 권한 획득 후 즉시 해제 (SpeechRecognition이 자체적으로 마이크 사용)
      stream.getTracks().forEach(track => track.stop());
    } catch (e) {
      console.error("[마이크 권한] 거부됨:", e.name);
      if (e.name === 'NotAllowedError' || e.name === 'PermissionDeniedError') {
        setDebugText("마이크 허용 필요");
      } else {
        setDebugText("마이크 오류");
      }
      setTimeout(() => setDebugText(""), 4000);
      return;
    }

    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;

    // 블루투스 마이크 연결 딜레이를 버티기 위해 continuous를 true로 설정해야 합니다.
    recognition.lang = 'ko-KR';
    recognition.interimResults = true;
    recognition.continuous = true; 

    recognition.onstart = () => {
      console.log("[음성 인식] 시작됨 (엔진 준비)");
      setIsRecording(true);
      setDebugText("마이크 연결 중...");
    };

    recognition.onaudiostart = () => {
      console.log("[음성 인식] 오디오 캡처 시작됨 (마이크 활성화)");
      setDebugText("말씀하세요!");
    };

    recognition.onsoundstart = () => {
      console.log("[음성 인식] 소리 감지됨");
    };

    recognition.onspeechstart = () => console.log("[음성 인식] 목소리 감지됨");

    recognition.onresult = async (event) => {
      if (isProcessing) return; // Race condition 방지

      let fullTranscript = '';
      for (let i = 0; i < event.results.length; ++i) {
        fullTranscript += event.results[i][0].transcript;
      }
      
      setDebugText(`(인식 중) ${fullTranscript}`);

      const isFinal = event.results[event.results.length - 1].isFinal;
      
      // 프론트엔드에서는 단순 길이/종료 여부만 체크하여 서버로 전송
      if (fullTranscript.split(' ').length >= players.length || isFinal) {
        console.log("[음성 인식] 서버 분석 요청:", fullTranscript);
        
        setIsProcessing(true);

        try {
          const result = await parseVoiceText(fullTranscript, hole.par);
          if (result.success && result.data.parsed.scores) {
            const parsedScores = result.data.parsed.scores;
            const scoreCount = Object.keys(parsedScores).length;

            if (scoreCount > 0) {
              if (onBulkScoreChange) {
                await onBulkScoreChange(hole.hole_number, parsedScores);
              }
              setDebugText(`${scoreCount}명 반영 완료!`);
              
              if (scoreCount >= players.length) {
                recognition.stop();
                setIsRecording(false);
              }
            }
          }
        } catch (error) {
          console.error("Voice parsing failed:", error);
          setDebugText("분석 오류");
        } finally {
          setIsProcessing(false);
        }
      }
    };

    recognition.onerror = (event) => {
      console.error("[음성 인식] 오류:", event.error);
      if (event.error === 'not-allowed') {
        setDebugText("마이크 허용 필요 🔒");
      } else if (event.error === 'no-speech') {
        setDebugText("음성 감지 안됨");
      } else if (event.error === 'network') {
        setDebugText("네트워크 오류");
      } else if (event.error === 'service-not-allowed') {
        setDebugText("음성 서비스 차단됨");
      } else {
        setDebugText(`오류: ${event.error}`);
      }
      setIsRecording(false);
      setTimeout(() => setDebugText(""), 3000);
      recognitionRef.current = null;
    };

    recognition.onend = () => {
      console.log("[음성 인식] 종료됨");
      if (isRecording) {
        setIsRecording(false);
        setDebugText("녹음 종료");
        setTimeout(() => setDebugText(""), 2000);
      }
      recognitionRef.current = null;
    };

    // 3. 녹음 시작
    try {
      recognition.start();
    } catch (e) {
      console.error("recognition start failed", e);
      setDebugText("시작 실패");
      setIsRecording(false);
    }
  };

  return (
    <div
      style={{
        background: '#FFFFFF',
        border: 'none',
        borderBottom: '1px solid #D2D2D2',
        padding: '16px 0',
      }}
    >
      {/* Header row: hole number + record btn + par select */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#181818', lineHeight: 1.30 }}>
            {hole.hole_number}번 홀
          </h3>
          <button
            onClick={isRecording ? stopVoiceInput : startVoiceInput}
            disabled={isProcessing && !isRecording}
            style={{
              background: isRecording ? '#DA291C' : 'transparent',
              border: '1px solid #D2D2D2',
              borderRadius: '2px',
              width: 32,
              height: 32,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              color: isRecording ? '#FFFFFF' : '#181818',
              transition: 'all 0.2s ease'
            }}
            title={isRecording ? "녹음 중지" : "음성 스코어 입력"}
          >
            {isProcessing ? (
              <Loader2 size={16} className="animate-spin" />
            ) : isRecording ? (
              <Square size={14} fill="currentColor" />
            ) : (
              <Mic size={16} />
            )}
          </button>
          
          {debugText && (
            <span style={{ fontSize: '11px', color: '#DA291C', marginLeft: '8px', maxWidth: '100px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {debugText}
            </span>
          )}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span className="label-micro" style={{ color: '#8F8F8F' }}>Par</span>
          <select
            value={hole.par}
            onChange={(e) => onScoreChange(hole.hole_number, 'par', parseInt(e.target.value))}
            style={{
              fontFamily: 'var(--font-ferrari)',
              fontSize: '13px',
              fontWeight: 500,
              padding: '4px 8px',
              background: '#FFFFFF',
              color: '#181818',
              border: '1px solid #CCCCCC',
              borderRadius: '2px',
              cursor: 'pointer',
              outline: 'none',
            }}
          >
            {[3, 4, 5].map(p => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Score grid */}
      <div style={{ display: 'grid', gridTemplateColumns: `repeat(${players.length}, 1fr)`, gap: 8 }}>
        {players.map((player, index) => {
          const scoreKey = `score_${['a', 'b', 'c', 'd'][index]}`;
          // score_a, b, c, d 가 null인 경우 빈 값으로 표시하거나 0으로 표시
          // 요건상 0이 '파'이므로, 입력되지 않은 상태는 null로 관리하는 것이 좋음
          const currentScore = hole[scoreKey];
          const hasScore = currentScore !== null && currentScore !== undefined;

          // Score color based on par
          let scoreColor = '#181818';
          if (hasScore) {
            if (currentScore < 0) scoreColor = '#DA291C'; // Under par — red (birdie!)
            else if (currentScore > 0) scoreColor = '#3860BE'; // Over par — link blue
            else scoreColor = '#03904A'; // Par — success green
          }

          return (
            <div key={index} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              {/* Player name */}
              <span
                className="label-micro"
                style={{
                  color: '#969696',
                  marginBottom: 6,
                  display: 'block',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                  width: '100%',
                  textAlign: 'center',
                }}
              >
                {player}
              </span>

              {/* Score stepper */}
              <div style={{ width: '100%' }}>
                <button
                  onClick={() => onScoreChange(hole.hole_number, scoreKey, (currentScore || 0) + 1)}
                  style={{
                    width: '100%',
                    padding: '6px 0',
                    fontSize: '14px',
                    fontWeight: 700,
                    color: '#666666',
                    background: 'transparent',
                    border: '1px solid #D2D2D2',
                    borderRadius: '2px 2px 0 0',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                  }}
                  onMouseEnter={(e) => { e.target.style.background = '#F5F5F5'; }}
                  onMouseLeave={(e) => { e.target.style.background = 'transparent'; }}
                >
                  +
                </button>

                <div
                  style={{
                    width: '100%',
                    textAlign: 'center',
                    padding: '8px 0',
                    fontSize: '20px',
                    fontWeight: 500,
                    color: scoreColor,
                    borderLeft: '1px solid #D2D2D2',
                    borderRight: '1px solid #D2D2D2',
                    transition: 'color 0.2s ease',
                  }}
                >
                  {hasScore ? (currentScore > 0 ? `+${currentScore}` : currentScore) : '-'}
                </div>

                <button
                  onClick={() => onScoreChange(hole.hole_number, scoreKey, (currentScore || 0) - 1)}
                  style={{
                    width: '100%',
                    padding: '6px 0',
                    fontSize: '14px',
                    fontWeight: 700,
                    color: '#666666',
                    background: 'transparent',
                    border: '1px solid #D2D2D2',
                    borderRadius: '0 0 2px 2px',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                  }}
                  onMouseEnter={(e) => { e.target.style.background = '#F5F5F5'; }}
                  onMouseLeave={(e) => { e.target.style.background = 'transparent'; }}
                >
                  −
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default HoleCard;
