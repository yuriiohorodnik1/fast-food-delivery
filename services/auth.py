from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/login')
pwd_context = CryptContext(schemes=['sha256_crypt'])


def get_password_hash(password: str):
    return pwd_context.hash(password)
