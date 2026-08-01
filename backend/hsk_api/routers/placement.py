from fastapi import APIRouter, Depends, File, HTTPException, Request, Response, UploadFile, status

from hsk_api.auth.dependencies import get_current_account
from hsk_api.models.account import AccountRecord
from hsk_api.models.placement import (
    PlacementAnswerRequest, PlacementAttemptResponse, PlacementSelectionRequest, PlacementSelectionResponse,
    PlacementStatusResponse,
)
from hsk_api.services.placement import PlacementError, PlacementService
from hsk_api.services.daily_paths import DailyPathGenerationError, DailyPathQuotaError


router = APIRouter(prefix="/api/v1/placement", tags=["placement"])


def service(request: Request) -> PlacementService:
    return request.app.state.placement_service


@router.get("/status", response_model=PlacementStatusResponse)
def get_status(request: Request, account: AccountRecord = Depends(get_current_account)):
    return service(request).status(account.id)


@router.post("/attempts", response_model=PlacementAttemptResponse)
def start_attempt(request: Request, response: Response, account: AccountRecord = Depends(get_current_account)):
    try:
        attempt_response, created = service(request).start_or_resume(account.id)
    except PlacementError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    response.status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return attempt_response


@router.post("/attempts/{attempt_id}/answers", response_model=PlacementAttemptResponse)
def answer(attempt_id: str, payload: PlacementAnswerRequest, request: Request,
           account: AccountRecord = Depends(get_current_account)):
    try:
        return service(request).answer(account.id, attempt_id, payload.option_id, payload.skip)
    except PlacementError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/skip", response_model=PlacementSelectionResponse)
def skip(request: Request, account: AccountRecord = Depends(get_current_account)):
    return PlacementSelectionResponse(selected_level=service(request).skip(account.id))


@router.post("/attempts/{attempt_id}/pronunciation", response_model=PlacementAttemptResponse)
async def pronunciation(attempt_id: str, request: Request, audio: UploadFile = File(...),
                        account: AccountRecord = Depends(get_current_account)):
    content_type = (audio.content_type or "").split(";")[0]
    if content_type not in {"audio/webm", "audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp4", "audio/ogg"}:
        raise HTTPException(status_code=415, detail="Định dạng âm thanh chưa được hỗ trợ.")
    content = await audio.read(5 * 1024 * 1024 + 1)
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Bản thu âm phải nhỏ hơn 5 MB.")
    placement = service(request)
    attempt = placement.repository.get_placement_attempt(attempt_id)
    from hsk_api.content.placement_test import placement_question
    question = placement_question(attempt.current_question_id or "") if attempt and attempt.account_id == account.id else None
    if question is None or question.skill != "pronunciation":
        raise HTTPException(status_code=409, detail="Câu hiện tại không phải câu phát âm.")
    analyzer = request.app.state.pronunciation_analyzer
    if analyzer is None:
        raise HTTPException(status_code=503, detail="AI phát âm chưa được cấu hình.")
    try:
        result = analyzer.analyze(
            audio=content, filename=audio.filename or "recording.webm", content_type=content_type,
            target_text=question.target_text or "", target_pinyin=question.target_pinyin or "",
        )
        score = result.score if hasattr(result, "score") else int(result.get("score", 0))
        return placement.record_pronunciation(account.id, attempt_id, score)
    except PlacementError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=502, detail="AI chưa thể phân tích bản thu này. Vui lòng thử lại.") from error


@router.post("/attempts/{attempt_id}/audio", response_class=Response)
def listening_audio(attempt_id: str, request: Request,
                    account: AccountRecord = Depends(get_current_account)):
    placement = service(request)
    attempt = placement.repository.get_placement_attempt(attempt_id)
    from hsk_api.content.placement_test import placement_question
    question = placement_question(attempt.current_question_id or "") if attempt and attempt.account_id == account.id else None
    if question is None or question.skill != "listening" or not question.audio_text:
        raise HTTPException(status_code=409, detail="Câu hiện tại không có âm thanh nghe.")
    synthesizer = request.app.state.speech_synthesizer
    if synthesizer is None:
        raise HTTPException(status_code=503, detail="Giọng đọc AI chưa được cấu hình.")
    try:
        return Response(content=synthesizer.synthesize(text=question.audio_text, speed=0.82), media_type="audio/mpeg")
    except Exception as error:
        raise HTTPException(status_code=502, detail="Chưa thể tạo âm thanh câu nghe.") from error


@router.post("/selection", response_model=PlacementSelectionResponse)
def select_level(payload: PlacementSelectionRequest, request: Request,
                 account: AccountRecord = Depends(get_current_account)):
    try:
        selected = service(request).select_level(account.id, payload.selected_level)
        return PlacementSelectionResponse(selected_level=selected)
    except (DailyPathGenerationError, DailyPathQuotaError) as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except PlacementError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
