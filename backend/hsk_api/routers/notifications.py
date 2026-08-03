from secrets import compare_digest

from fastapi import APIRouter, HTTPException, Request, status


router = APIRouter(prefix="/api/cron", tags=["notifications"])


def verify_cron_secret(request: Request) -> None:
    expected = request.app.state.cron_secret
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="CRON_SECRET chưa được cấu hình.",
        )
    authorization = request.headers.get("authorization", "")
    if not compare_digest(authorization, f"Bearer {expected}"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cron token không hợp lệ.",
        )


@router.get("/learning-reminder")
def learning_reminder(request: Request) -> dict[str, str]:
    verify_cron_secret(request)
    result = request.app.state.learning_reminder_service.run_hourly_reminder()
    return {"status": result}


@router.post("/learning-progress")
def learning_progress(request: Request) -> dict[str, str]:
    verify_cron_secret(request)
    result = request.app.state.learning_reminder_service.send_progress_summary()
    return {"status": result}
