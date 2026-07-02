from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from app.database.db import get_db

from app.schemas.auth import Token
from app.schemas.auth import UserLogin
from app.schemas.auth import UserRegister
from app.schemas.auth import UserResponse

from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    return AuthService.register(
        db,
        user,
    )


@router.post(
    "/login",
    response_model=Token,
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    return AuthService.login(
        db,
        credentials,
    )