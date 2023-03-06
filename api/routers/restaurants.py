from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from models.restaurant import Restaurant
from services.database import get_db
from services.user import get_user_by_id

router = APIRouter(tags=['restaurants'])


@router.get(path='/',
            response_model=list[Restaurant],
            status_code=status.HTTP_200_OK,
            tags='restaurants')
async def get_all_restaurants(db: Session = Depends(get_db),
                              current_user = Depends(get_user_by_id)):
    ...
