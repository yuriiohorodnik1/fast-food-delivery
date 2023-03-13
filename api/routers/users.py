from fastapi import APIRouter, status, Depends, Body, HTTPException
from sqlalchemy.orm import Session

from schemas.user import UserIn, UserOut
from services.auth import get_password_hash, get_current_user
from services.database import get_db
from services.user import (delete_user as service_delete_user,
                           create_user as service_create_user,
                           get_user_by_email)

router = APIRouter(tags=['users'])


@router.post(path='/user',
             response_model=UserOut,
             summary='Create new user',
             status_code=status.HTTP_201_CREATED
             )
def create_user(user: UserIn = Body(...),
                db: Session = Depends(get_db),
                current_user: UserOut = Depends(get_current_user)):
    """Create a new user and save it to the database."""
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='User with such email already exists.')
    user.password = get_password_hash(password=user.password)
    return service_create_user(db, user)


@router.delete(path='/user/<user_id>',
               response_model=UserOut,
               status_code=status.HTTP_200_OK,
               summary='Delete a user')
def delete_user(user_id: int,
                db: Session = Depends(get_db),
                current_user: UserOut = Depends(get_current_user)):
    """Delete the user with specific id. Raise exception if the user is not found."""
    db_user: UserOut = service_delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail='User not found.')
    return db_user


@router.get(path='/user',
            response_model=UserOut,
            summary='Get user details info',
            status_code=status.HTTP_200_OK
            )
def get_current_user_info(current_user: UserOut = Depends(get_current_user)):
    """Return detailed user info."""
    return current_user
