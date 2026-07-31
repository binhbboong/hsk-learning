from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from hsk_api.auth.dependencies import get_current_account, get_repository, get_token
from hsk_api.auth.security import hash_password, new_session_token, verify_password
from hsk_api.models.account import (
    AccountRecord,
    LoginRequest,
    RegisterRequest,
    SessionResponse,
    UserResponse,
)
from hsk_api.repositories.accounts import AccountRepository


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
INVALID_CREDENTIALS = "Email hoặc mật khẩu không đúng."


def public_user(account: AccountRecord, admin_emails: set[str]) -> UserResponse:
    return UserResponse(
        id=account.id,
        display_name=account.display_name,
        email=account.email,
        is_admin=account.email.casefold() in admin_emails,
    )


def start_session(
    account: AccountRecord,
    repository: AccountRepository,
    admin_emails: set[str],
) -> SessionResponse:
    token = new_session_token()
    repository.create_session(account.id, token)
    return SessionResponse(token=token, user=public_user(account, admin_emails))


@router.post("/register", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def register(
    request: RegisterRequest,
    http_request: Request,
    repository: AccountRepository = Depends(get_repository),
) -> SessionResponse:
    account = repository.create_account(
        request.display_name,
        str(request.email),
        hash_password(request.password),
    )
    if account is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email này đã được sử dụng.")
    return start_session(account, repository, http_request.app.state.admin_emails)


@router.post("/login", response_model=SessionResponse)
def login(
    request: LoginRequest,
    http_request: Request,
    repository: AccountRepository = Depends(get_repository),
) -> SessionResponse:
    account = repository.find_by_email(str(request.email))
    if account is None or not verify_password(request.password, account.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS)
    return start_session(account, repository, http_request.app.state.admin_emails)


@router.get("/me", response_model=UserResponse)
def me(
    request: Request,
    account: AccountRecord = Depends(get_current_account),
) -> UserResponse:
    return public_user(account, request.app.state.admin_emails)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    token: str = Depends(get_token),
    repository: AccountRepository = Depends(get_repository),
) -> None:
    repository.revoke_session(token)
    response.status_code = status.HTTP_204_NO_CONTENT
