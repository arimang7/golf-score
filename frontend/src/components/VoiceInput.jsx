import React, { useState, useRef } from 'react';
import { Mic, Square, Loader2 } from 'lucide-react';
import { uploadVoice } from '../api/rounds';

const VoiceInput = ({ onResult, onError }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const audioFile = new File([audioBlob], 'voice.webm', { type: 'audio/webm' });

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
      console.error('Error accessing microphone:', error);
      if (onError) onError('마이크 접근 권한이 필요합니다.');
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
