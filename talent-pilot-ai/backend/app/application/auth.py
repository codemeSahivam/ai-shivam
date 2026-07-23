"""Authentication use cases."""

from __future__ import annotations

import bcrypt
from sqlalchemy.orm import Session

from app.domain.exceptions import AuthError, UnauthorizedError
from app.infrastructure.db.orm import UserModel
from app.infrastructure.db.repositories.user_repository import UserRepository


class AuthUseCase:
    def __init__(self, session: Session) -> None:
        self._users = UserRepository(session)

    def register(self, email: str, password: str) -> UserModel:
        normalized = email.strip().lower()
        if len(password) < 8:
            raise AuthError("Password must be at least 8 characters.")
        if self._users.get_by_email(normalized) is not None:
            raise AuthError("An account with this email already exists.")
        return self._users.create(normalized, self._hash_password(password))

    def login(self, email: str, password: str) -> UserModel:
        normalized = email.strip().lower()
        user = self._users.get_by_email(normalized)
        if user is None or not self._verify_password(password, user.password_hash):
            raise AuthError("Invalid email or password.")
        return user

    def get_user(self, user_id: int) -> UserModel:
        user = self._users.get_by_id(user_id)
        if user is None:
            raise UnauthorizedError()
        return user

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def _verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
