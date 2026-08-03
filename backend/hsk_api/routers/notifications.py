from secrets import compare_digest

from fastapi import APIRouter, HTTPException, Request, status


router = APIRouter(prefix="/api/cron", tags=["notifications"])


@router.get("/learning-reminder")
def learning_reminder(request: Request) -> dict[str, str]:
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
    result = request.app.state.learning_reminder_service.run_hourly_reminder()
    return {"status": result}
