from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config.auth import ACCESS_TOKEN_EXPIRE_MINUTES
from services.database import get_db
from schemas.token import Token
from services.auth import authenticate_user, create_access_token

router = APIRouter(tags=['auth'])


@router.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    """Endpoint to share the access token with the user. Set expiration time and fields for authentication."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # "sub" is a special field meaning the user that sends a request.
    # In our case we need to encode user's email for authentication.
    # https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#technical-details-about-the-jwt-subject-sub
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}
