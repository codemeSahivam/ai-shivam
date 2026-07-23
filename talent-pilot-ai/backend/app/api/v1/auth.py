"""Authentication API."""

from __future__ import annotations

from fastapi import APIRouter, Request

from app.api.deps import AuthUseCaseDep, UserIdDep
from app.schemas.auth import (
    AuthSuccessResponse,
    LoginRequest,
    LogoutResponse,
    RegisterRequest,
    UserResponse,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=AuthSuccessResponse,
    summary="Register a new account",
)
async def register(
    body: RegisterRequest,
    request: Request,
    use_case: AuthUseCaseDep,
) -> AuthSuccessResponse:
    user = use_case.register(body.email, body.password)
    request.session["user_id"] = user.id
    return AuthSuccessResponse(success=True, user=UserResponse(id=user.id, email=user.email))


@router.post(
    "/login",
    response_model=AuthSuccessResponse,
    summary="Sign in",
)
async def login(
    body: LoginRequest,
    request: Request,
    use_case: AuthUseCaseDep,
) -> AuthSuccessResponse:
    user = use_case.login(body.email, body.password)
    request.session["user_id"] = user.id
    return AuthSuccessResponse(success=True, user=UserResponse(id=user.id, email=user.email))


@router.post(
    "/logout",
    response_model=LogoutResponse,
    summary="Sign out",
)
async def logout(request: Request) -> LogoutResponse:
    request.session.clear()
    return LogoutResponse(success=True)


@router.get(
    "/me",
    response_model=AuthSuccessResponse,
    summary="Current user",
)
async def me(user_id: UserIdDep, use_case: AuthUseCaseDep) -> AuthSuccessResponse:
    user = use_case.get_user(user_id)
    return AuthSuccessResponse(success=True, user=UserResponse(id=user.id, email=user.email))
