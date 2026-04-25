import React, { useState, useRef } from 'react';
import { Mic, Square, Loader2 } from 'lucide-react';
import { uploadVoice } from '../api/rounds';

const VoiceInput = ({ onResult, onError }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    // 1. mediaDevices API 지원 여부 체크
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      if (onError) onError('이 브라우저는 마이크를 지원하지 않습니다. Chrome이나 Safari를 사용해주세요.');
      return;
    }

    // 2. 권한 상태 사전 체크 (지원되는 브라우저)
    try {
      if (navigator.permissions && navigator.permissions.query) {
        const permStatus = await navigator.permissions.query({ name: 'microphone' });
        if (permStatus.state === 'denied') {
          if (onError) onError('마이크 권한이 차단되어 있습니다. 브라우저 설정 > 사이트 설정 > 마이크에서 허용해주세요.');
          return;
        }
      }
    } catch (e) {
      // permissions.query를 지원하지 않는 브라우저 (Safari 등) — 무시하고 진행
    }

    // 3. 마이크 접근 요청
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // MediaRecorder 지원 확인
      if (typeof MediaRecorder === 'undefined') {
        stream.getTracks().forEach(track => track.stop());
        if (onError) onError('이 브라우저는 녹음을 지원하지 않습니다.');
        return;
      }

      // MIME 타입 결정 (브라우저 호환성)
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : MediaRecorder.isTypeSupported('audio/webm')
          ? 'audio/webm'
          : MediaRecorder.isTypeSupported('audio/mp4')
            ? 'audio/mp4'
            : '';

      const mediaRecorder = mimeType
        ? new MediaRecorder(stream, { mimeType })
        : new MediaRecorder(stream);

      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const ext = mimeType.includes('mp4') ? 'mp4' : 'webm';
        const audioBlob = new Blob(audioChunksRef.current, { type: mimeType || 'audio/webm' });
        const audioFile = new File([audioBlob], `voice.${ext}`, { type: mimeType || 'audio/webm' });

        setIsProcessing(true);
        try {
          const result = await uploadVoice(audioFile);
          if (result.success && onResult) {
            onResult(result.data);
          }
        } catch (error) {
          console.error('Voice processing failed', error);
          if (onError) onError('음성 인식에 실패했습니다.');
        } finally {
          setIsProcessing(false);
        }

        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Microphone error:', error.name, error.message);
      if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        if (onError) onError('마이크 권한을 허용해주세요. 주소창 왼쪽 🔒 아이콘을 눌러 마이크를 허용할 수 있습니다.');
      } else if (error.name === 'NotFoundError') {
        if (onError) onError('마이크가 감지되지 않습니다. 기기의 마이크를 확인해주세요.');
      } else if (error.name === 'NotReadableError') {
        if (onError) onError('마이크가 다른 앱에서 사용 중입니다.');
      } else {
        if (onError) onError(`마이크 오류: ${error.message}`);
      }
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  // Ferrari-styled mic button: razor-sharp 2px radius, NOT rounded-pill
  const baseStyle = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: 56,
    height: 56,
    borderRadius: '2px',
    border: 'none',
    cursor: 'pointer',
    transition: 'all 0.25s ease',
    color: '#FFFFFF',
  };

  let buttonStyle;
  if (isProcessing) {
    buttonStyle = { ...baseStyle, background: '#666666', cursor: 'not-allowed' };
  } else if (isRecording) {
    buttonStyle = { ...baseStyle, background: '#DA291C' };
  } else {
    buttonStyle = { ...baseStyle, background: '#181818', border: '1px solid rgba(255,255,255,0.15)' };
  }

  return (
    <div
      style={{
        position: 'fixed',
        bottom: 24,
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 50,
      }}
    >
      <button
        onClick={isRecording ? stopRecording : startRecording}
        disabled={isProcessing}
        style={buttonStyle}
        className={isRecording ? 'pulse-ring' : ''}
        id="voice-input-btn"
      >
        {isProcessing ? (
          <Loader2 size={24} className="animate-spin" />
        ) : isRecording ? (
          <Square size={20} fill="currentColor" />
        ) : (
          <Mic size={24} />
        )}
      </button>

      {/* State label */}
      {(isRecording || isProcessing) && (
        <p
          className="label-micro"
          style={{
            textAlign: 'center',
            marginTop: 6,
            color: isRecording ? '#DA291C' : '#969696',
          }}
        >
          {isRecording ? 'Recording' : 'Processing'}
        </p>
      )}
    </div>
  );
};

export default VoiceInput;
