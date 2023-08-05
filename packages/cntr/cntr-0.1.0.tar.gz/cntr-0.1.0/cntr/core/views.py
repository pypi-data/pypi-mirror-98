from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from cntr.core import models, service
from cntr.core.celery_app import celery_app
from cntr.auth.models import User
from cntr.auth.service import (
    get_current_active_user,
    get_current_active_superuser,
    user,
)
from pydantic.networks import EmailStr
from cntr.utils import send_test_email
from cntr.database import get_db

items_router = APIRouter()
utils_router = APIRouter()


@items_router.get("/", response_model=List[models.ItemRead])
def read_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    if service.user.is_superuser(current_user):
        items = service.item.get_multi(db, skip=skip, limit=limit)
    else:
        items = service.item.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return items


@items_router.post("/", response_model=models.ItemRead)
def create_item(
    *,
    db: Session = Depends(get_db),
    item_in: models.ItemCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = service.item.create_with_owner(
        db=db, obj_in=item_in, owner_id=current_user.id
    )
    return item


@items_router.put("/{id}", response_model=models.ItemRead)
def update_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    item_in: models.ItemUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    item = service.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = service.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@items_router.get("/{id}", response_model=models.ItemRead)
def read_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = service.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@items_router.delete("/{id}", response_model=models.ItemRead)
def delete_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = service.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = service.item.remove(db=db, id=id)
    return item


@utils_router.post("/test-celery/", response_model=models.Msg, status_code=201)
def test_celery(
    msg: models.Msg,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("cntr.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@utils_router.post("/test-email/", response_model=models.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
