from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.voice_parser import parse_voice_text, mock_stt
from pydantic import BaseModel

router = APIRouter(prefix="/voice", tags=["voice"])

class VoiceTextRequest(BaseModel):
    text: str

@router.post("/parse")
async def parse_text(data: VoiceTextRequest, par_hint: int = 4):
    """
    STT로 변환된 텍스트를 파싱하여 데이터를 반환합니다.
    """
    try:
        parsed_data = parse_voice_text(data.text, par_hint)
        return {
            "success": True, 
            "data": {
                "text": data.text,
                "parsed": parsed_data
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_voice(file: UploadFile = File(...), par_hint: int = 4):
    """
    음성 파일을 업로드받아 텍스트로 변환하고, 
    골프 스코어 관련 데이터를 파싱하여 반환합니다.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # 오디오 파일 읽기
    audio_bytes = await file.read()
    
    try:
        # 1. STT (Speech-to-Text) 실행
        text = mock_stt(audio_bytes)
        
        # 2. 추출된 텍스트에서 스코어 파싱
        parsed_data = parse_voice_text(text, par_hint)
        
        return {
            "success": True, 
            "data": {
                "text": text,
                "parsed": parsed_data
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
