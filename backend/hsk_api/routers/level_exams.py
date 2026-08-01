from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from hsk_api.auth.dependencies import get_current_account
from hsk_api.models.account import AccountRecord
from hsk_api.models.level_exam import (
    LevelExamAttemptResponse, LevelExamResult, LevelExamSaveRequest, LevelExamStatusResponse,
)
from hsk_api.services.level_exams import LevelExamError, LevelExamService


router = APIRouter(prefix="/api/v1/level-exams", tags=["level-exams"])


def service(request: Request) -> LevelExamService:
    return request.app.state.level_exam_service


@router.get("/status", response_model=LevelExamStatusResponse)
def exam_status(request: Request, account: AccountRecord = Depends(get_current_account)):
    return service(request).status(account.id)


@router.post("/attempts", response_model=LevelExamAttemptResponse)
def start(request: Request, response: Response,
          account: AccountRecord = Depends(get_current_account)):
    try:
        payload, created = service(request).start_or_resume(account.id)
        response.status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return payload
    except LevelExamError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.put("/attempts/{attempt_id}", response_model=LevelExamAttemptResponse)
def save(attempt_id: str, payload: LevelExamSaveRequest, request: Request,
         account: AccountRecord = Depends(get_current_account)):
    try:
        return service(request).save(account.id, attempt_id, **payload.model_dump())
    except LevelExamError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/attempts/{attempt_id}/submit", response_model=LevelExamResult)
def submit(attempt_id: str, request: Request,
           account: AccountRecord = Depends(get_current_account)):
    try:
        return service(request).submit(account.id, attempt_id)
    except LevelExamError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/attempts/{attempt_id}/questions/{question_id}/audio", response_class=Response)
def audio(attempt_id: str, question_id: str, request: Request,
          account: AccountRecord = Depends(get_current_account)):
    try:
        text = service(request).audio_text(account.id, attempt_id, question_id)
        synthesizer = request.app.state.speech_synthesizer
        if synthesizer is None:
            raise HTTPException(status_code=503, detail="Giọng đọc AI chưa được cấu hình.")
        return Response(content=synthesizer.synthesize(text=text, speed=0.82), media_type="audio/mpeg")
    except LevelExamError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=502, detail="Chưa thể tạo âm thanh câu nghe.") from error
