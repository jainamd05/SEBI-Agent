from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.core.security import verify_password

from app.database.crud import create_user
from app.database.crud import get_user_by_email
from app.database.crud import get_user_by_username

from app.database.db import get_db

from app.schemas.auth import Token
from app.schemas.auth import UserLogin
from app.schemas.auth import UserRegister
from app.schemas.auth import UserResponse

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
    """
    Register a new user.
    """

    existing_email = get_user_by_email(
        db,
        user.email,
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered.",
        )

    existing_username = get_user_by_username(
        db,
        user.username,
    )

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists.",
        )

    return create_user(
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
    """
    Login user.
    """

    user = get_user_by_email(
        db,
        credentials.email,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    if not verify_password(
        credentials.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(
        subject=user.email,
    )

    return Token(
        access_token=access_token,
    )