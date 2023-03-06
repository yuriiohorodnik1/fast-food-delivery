from models.user import User as UserModel
from schemas.user import UserIn, UserOut
from fastapi import APIRouter, status, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from services.database import get_db
from services.user import get_user_by_email, create_user as service_create_user
from services.auth import get_password_hash

router = APIRouter(tags=['users'])


@router.post(path='/user',
             response_model=UserOut,
             summary='Create new user',
             status_code=status.HTTP_201_CREATED
             )
async def create_user(user: UserIn = Body(...),
                      db: Session = Depends(get_db)):
    """Create a new user and save it to the database."""
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='User with such email already exists')
    user.password = get_password_hash(password=user.password)
    created_user = service_create_user(db, user)
    return UserOut.from_orm(created_user)


@router.get(path='/user',
            response_model=UserOut,
            summary='Get user detail info',
            status_code=status.HTTP_200_OK
            )
async def get_user_info(current_user: UserIn, db: Session = Depends(get_db)):
    """Show detailed user info."""

