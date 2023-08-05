from typing import Any, List
from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from cntr import utils
from cntr.config import settings
from cntr.utils import send_new_account_email
from cntr.auth import models, service, security
from cntr.core.models import Msg
from cntr.database import get_db

user_router = APIRouter()
auth_router = APIRouter()


@user_router.get("/", response_model=List[models.UserRead])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(service.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = service.user.get_multi(db, skip=skip, limit=limit)
    return users


@user_router.post("/", response_model=models.UserRead)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: models.UserCreate,
    current_user: models.User = Depends(service.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = service.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = service.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@user_router.put("/me", response_model=models.UserRead)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(service.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = models.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = service.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@user_router.get("/me", response_model=models.UserRead)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(service.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@user_router.post("/open", response_model=models.UserRead)
def create_user_open(
    *,
    db: Session = Depends(get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = service.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = models.UserCreate(password=password, email=email, full_name=full_name)
    user = service.user.create(db, obj_in=user_in)
    return user


@user_router.get("/{user_id}", response_model=models.UserRead)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(service.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = service.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not service.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@user_router.put("/{user_id}", response_model=models.UserRead)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: models.UserUpdate,
    current_user: models.User = Depends(service.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = service.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = service.user.update(db, db_obj=user, obj_in=user_in)
    return user


@auth_router.post("/login/access-token", response_model=models.Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = service.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not service.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@auth_router.post("/login/test-token", response_model=models.UserRead)
def test_token(current_user: models.User = Depends(service.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@auth_router.post("/password-recovery/{email}", response_model=Msg)
def recover_password(email: str, db: Session = Depends(get_db)) -> Any:
    """
    Password Recovery
    """
    user = service.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = utils.generate_password_reset_token(email=email)
    utils.send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@auth_router.post("/reset-password/", response_model=Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db),
) -> Any:
    """
    Reset password
    """
    email = utils.verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = service.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not service.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = utils.get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}
