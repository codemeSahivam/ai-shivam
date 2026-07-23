"""User persistence."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.db.orm import UserModel


class UserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_email(self, email: str) -> UserModel | None:
        statement = select(UserModel).where(UserModel.email == email)
        return self._session.scalars(statement).first()

    def get_by_id(self, user_id: int) -> UserModel | None:
        statement = select(UserModel).where(UserModel.id == user_id)
        return self._session.scalars(statement).first()

    def create(self, email: str, password_hash: str) -> UserModel:
        user = UserModel(email=email, password_hash=password_hash)
        self._session.add(user)
        self._session.flush()
        self._session.refresh(user)
        return user
