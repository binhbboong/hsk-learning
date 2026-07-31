from typing import Protocol
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, Response, UploadFile
from hsk_api.auth.dependencies import get_current_account
from hsk_api.models.account import AccountRecord
from hsk_api.models.pronunciation import PronunciationResult, SpeechSampleRequest

router = APIRouter(prefix="/api/v1/pronunciation", tags=["pronunciation"])
ALLOWED_AUDIO_TYPES = {"audio/webm", "audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp4", "audio/ogg"}
MAX_AUDIO_BYTES = 5 * 1024 * 1024


class Analyzer(Protocol):
    def analyze(self, **kwargs) -> PronunciationResult | dict: ...


class SpeechSynthesizer(Protocol):
    def synthesize(self, *, text: str, speed: float) -> bytes: ...


@router.post("/analyze", response_model=PronunciationResult)
async def analyze_pronunciation(
    request: Request, audio: UploadFile = File(...),
    target_text: str = Form(..., min_length=1, max_length=200),
    target_pinyin: str = Form("", max_length=300),
    _account: AccountRecord = Depends(get_current_account),
) -> PronunciationResult | dict:
    content_type = (audio.content_type or "").split(";")[0]
    if content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(status_code=415, detail="Định dạng âm thanh chưa được hỗ trợ.")
    content = await audio.read(MAX_AUDIO_BYTES + 1)
    if len(content) > MAX_AUDIO_BYTES:
        raise HTTPException(status_code=413, detail="Bản thu âm phải nhỏ hơn 5 MB.")
    analyzer: Analyzer | None = request.app.state.pronunciation_analyzer
    if analyzer is None:
        raise HTTPException(status_code=503, detail="AI phát âm chưa được cấu hình.")
    try:
        return analyzer.analyze(audio=content, filename=audio.filename or "recording.webm",
                                content_type=content_type, target_text=target_text, target_pinyin=target_pinyin)
    except Exception as error:
        raise HTTPException(status_code=502, detail="AI chưa thể phân tích bản thu này. Vui lòng thử lại.") from error


@router.post("/sample", response_class=Response)
def generate_speech_sample(
    payload: SpeechSampleRequest,
    request: Request,
    _account: AccountRecord = Depends(get_current_account),
) -> Response:
    synthesizer: SpeechSynthesizer | None = request.app.state.speech_synthesizer
    if synthesizer is None:
        raise HTTPException(status_code=503, detail="Giọng đọc AI chưa được cấu hình.")
    try:
        audio = synthesizer.synthesize(text=payload.text, speed=payload.speed)
        return Response(content=audio, media_type="audio/mpeg")
    except Exception as error:
        raise HTTPException(status_code=502, detail="Chưa thể tạo giọng đọc mẫu. Vui lòng thử lại.") from error
