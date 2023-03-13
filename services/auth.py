from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config.auth import ALGORITHM, SECRET_KEY
from schemas.token import TokenData
from schemas.user import UserOut
from services.database import get_db
from services.user import get_user_by_email


# tokenUrl - relative URL path used for authentication.
# oauth2_scheme object is Callable, that's why can be used with Depends()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/token')
pwd_context = CryptContext(schemes=['bcrypt'])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str) -> UserOut:
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=400, detail='User is not found.')
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Wrong password')
    return user


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if not email:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db, email=token_data.email)
    if not user:
        raise credentials_exception
    return user
