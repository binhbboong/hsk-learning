from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Request, status

from hsk_api.auth.dependencies import get_current_account, get_repository
from hsk_api.content.learning_path import LESSONS
from hsk_api.models.account import AccountRecord
from hsk_api.models.content_ops import ContentDraft, ContentEditRequest, UsageSummary
from hsk_api.repositories.accounts import AccountRepository
from hsk_api.services.content_quality import ContentQualityGate


router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


def require_admin(
    request: Request,
    account: AccountRecord = Depends(get_current_account),
) -> AccountRecord:
    if account.email.casefold() not in request.app.state.admin_emails:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản không có quyền quản trị.",
        )
    return account


@router.get("/content", response_model=list[ContentDraft])
def list_content(
    status_filter: Literal["pending", "approved", "rejected"] | None = None,
    status: Literal["pending", "approved", "rejected"] | None = None,
    _admin: AccountRecord = Depends(require_admin),
    repository: AccountRepository = Depends(get_repository),
) -> list[ContentDraft]:
    return repository.list_content_drafts(status or status_filter)


@router.get("/usage", response_model=UsageSummary)
def usage(
    request: Request,
    _admin: AccountRecord = Depends(require_admin),
    repository: AccountRepository = Depends(get_repository),
) -> UsageSummary:
    return repository.usage_summary(
        account_daily_limit=request.app.state.ai_account_daily_limit,
        system_daily_limit=request.app.state.ai_system_daily_limit,
    )


def _previous_lessons(repository: AccountRepository, draft: ContentDraft):
    if draft.path_index == 2:
        return LESSONS
    previous = repository.get_daily_path(draft.account_id, draft.path_index - 1)
    return previous.lessons if previous else LESSONS


@router.put("/content/{draft_id}", response_model=ContentDraft)
def edit_content(
    draft_id: str,
    edit: ContentEditRequest,
    _admin: AccountRecord = Depends(require_admin),
    repository: AccountRepository = Depends(get_repository),
) -> ContentDraft:
    current = repository.get_content_draft(draft_id)
    if current is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy nội dung.")
    if current.status != "pending":
        raise HTTPException(status_code=409, detail="Nội dung đã được quyết định.")
    report, _ = ContentQualityGate().assess(
        edit.payload,
        previous_lessons=_previous_lessons(repository, current),
    )
    updated = repository.update_content_draft(
        draft_id,
        payload=edit.payload,
        quality=report,
    )
    if updated is None:
        raise HTTPException(status_code=409, detail="Không thể cập nhật nội dung.")
    return updated


@router.post("/content/{draft_id}/approve", response_model=ContentDraft)
def approve_content(
    draft_id: str,
    admin: AccountRecord = Depends(require_admin),
    repository: AccountRepository = Depends(get_repository),
) -> ContentDraft:
    current = repository.get_content_draft(draft_id)
    if current is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy nội dung.")
    if current.status != "pending":
        raise HTTPException(status_code=409, detail="Nội dung đã được quyết định.")
    report, bundle = ContentQualityGate().assess(
        current.payload,
        previous_lessons=_previous_lessons(repository, current),
    )
    if not report.passed or bundle is None:
        raise HTTPException(
            status_code=422,
            detail="Nội dung vẫn còn lỗi chất lượng trước khi duyệt.",
        )
    repository.save_daily_path(current.account_id, bundle)
    decided = repository.decide_content_draft(
        draft_id,
        status="approved",
        reviewed_by=admin.id,
    )
    if decided is None:
        raise HTTPException(status_code=409, detail="Nội dung đã được quyết định.")
    return decided


@router.post("/content/{draft_id}/reject", response_model=ContentDraft)
def reject_content(
    draft_id: str,
    admin: AccountRecord = Depends(require_admin),
    repository: AccountRepository = Depends(get_repository),
) -> ContentDraft:
    decided = repository.decide_content_draft(
        draft_id,
        status="rejected",
        reviewed_by=admin.id,
    )
    if decided is None:
        raise HTTPException(status_code=409, detail="Nội dung đã được quyết định.")
    return decided

