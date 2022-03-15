from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import APIRouter
import settings
from src.database.database import get_session
from src.database import models
from sqlalchemy.orm import Session


from src.app.routers.tags import Tags

login_router = APIRouter(prefix="/login", tags=[Tags.LOGIN])

# used for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

fake_users_db = {
    123456789: {
        "email": "johndoe@example.com",
        "user_id": "123456789",
        "pw_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    }
}


class Token(BaseModel):
    """Token generated after login"""
    access_token: str
    token_type: str


class User(BaseModel):
    """The fields used to find a user in the DB"""
    user_id: int | None = None


class UserInDB(User):
    """Hashed password added to user"""
    pw_hash: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# TODO: fix to actual db
# def get_user(email: str, db: Session = Depends(get_session)) -> UserInDB:
#     user = db.query(models.User).filter(models.User.email == email).first()
#     user_auth = db.query(models.AuthEmail).filter(models.AuthEmail.user_id == user.user_id).first()
#     return UserInDB(user_id=user.user_id, pw_hash=user_auth.pw_hash)

def get_user(email: str, db = fake_users_db) -> UserInDB | None:
    """Request the user_id and hashed password from the db"""
    for key in db:
        if db[key]["email"] == email:
            return UserInDB(user_id=int(db[key]["user_id"]), pw_hash=db[key]["pw_hash"])

    return None


# TODO: fix to actual db
# def get_user_by_id(id: int, db: Session = Depends(get_session)) -> UserInDB:
#     user = db.query(models.User).filter(models.User.user_id == id).first()
#     user_auth = db.query(models.AuthEmail).filter(models.AuthEmail.user_id == user.user_id).first()
#     return UserInDB(user_id=user.user_id, pw_hash=user_auth.pw_hash)


def get_user_by_id(id: int, db=fake_users_db) -> UserInDB:
    """Request the hashed password from the db"""
    return UserInDB(user_id=db[id]["user_id"], pw_hash=db[id]["pw_hash"])


def authenticate_user(email: str, password: str) -> UserInDB | None:
    user = get_user(email)
    if user is None:
        return None
    if not verify_password(password, user.pw_hash):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Encode the user data with an expire timestamp to create the token
    """
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_active_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """Check which user is making a request by decoding its token
    This function is used as a dependency for other functions
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    expire_exception = HTTPException(status_code=400, detail="Inactive user")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        user = get_user_by_id(int(user_id))
        if user is None:
            raise credentials_exception
        return user
    except ExpiredSignatureError:
        raise expire_exception
    except JWTError:
        raise credentials_exception


@login_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """Called when logging in, generates an access token to use in other functions
    """
    user = authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


#Example functions
"""
@login_router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@login_router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.user_id}]
"""