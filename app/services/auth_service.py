from sqlalchemy.orm import Session

from fastapi import HTTPException
from fastapi import status

from app.core.security import create_access_token
from app.core.security import verify_password

from app.database.crud import create_user
from app.database.crud import get_user_by_email
from app.database.crud import get_user_by_username

from app.schemas.auth import Token
from app.schemas.auth import UserLogin
from app.schemas.auth import UserRegister


class AuthService:

    @staticmethod
    def register(
        db: Session,
        user: UserRegister,
    ):

        if get_user_by_email(db, user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists.",
            )

        if get_user_by_username(db, user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists.",
            )

        return create_user(
            db,
            user,
        )

    @staticmethod
    def login(
        db: Session,
        credentials: UserLogin,
    ) -> Token:

        user = get_user_by_email(
            db,
            credentials.email,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials.",
            )

        if not verify_password(
            credentials.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials.",
            )

        token = create_access_token(
            subject=user.email,
        )

        return Token(
            access_token=token,
        )