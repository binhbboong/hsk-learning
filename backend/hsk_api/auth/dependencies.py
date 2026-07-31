from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from hsk_api.models.account import AccountRecord
from hsk_api.repositories.accounts import AccountRepository


bearer = HTTPBearer(auto_error=False)


def get_repository(request: Request) -> AccountRepository:
    return request.app.state.account_repository


def get_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bạn cần đăng nhập.")
    return credentials.credentials


def get_current_account(
    token: str = Depends(get_token),
    repository: AccountRepository = Depends(get_repository),
) -> AccountRecord:
    account = repository.account_for_token(token)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập đã hết hạn.",
        )
    return account


def get_optional_current_account(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    repository: AccountRepository = Depends(get_repository),
) -> AccountRecord | None:
    if credentials is None:
        return None
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Phiên không hợp lệ.")
    account = repository.account_for_token(credentials.credentials)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập đã hết hạn.",
        )
    return account
