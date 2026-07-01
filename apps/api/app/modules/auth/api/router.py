"""Authentication HTTP routes."""

from fastapi import APIRouter

from app.modules.auth.api.dependencies import (
    ActiveUser,
    AuthServiceDependency,
)
from app.modules.auth.api.schemas import (
    CurrentUserResponse,
    LoginRequest,
    TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, service: AuthServiceDependency) -> TokenResponse:
    token = service.login(payload.username_or_email, payload.password)
    return TokenResponse(
        access_token=token.access_token,
        token_type=token.token_type,
        expires_in=token.expires_in,
    )


@router.get("/me", response_model=CurrentUserResponse)
def me(
    identity: ActiveUser,
) -> CurrentUserResponse:
    return CurrentUserResponse.from_identity(identity)
