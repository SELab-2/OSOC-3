from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import APIRouter

# to get a string like this run:
# openssl rand -hex 32
# TODO: how should this be stored?
SECRET_KEY = "4d16a9cc83d74144322e893c879b5f639088c15dc1606b11226abbd7e97f5ee5"
ALGORITHM = "HS256"
# TODO: set time wanted
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe@example.com": {
        "email_auth_id": "johndoe@example.com",
        "user_id": "johndoe",
        "pw_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    }
}


class Token(BaseModel):
    """Token generated after login"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data after decoding token"""
    email_auth_id: str | None = None


class User(BaseModel):
    """The fields a user fills in to log in"""
    email_auth_id: str | None = None
    user_id: str | None = None


class UserInDB(User):
    """Hashed password added to user"""
    pw_hash: str


class RegisterUser(User):
    """The fields a user fills in to register"""
    name: str
    plain_pw: str


# used for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db, email_auth_id: str) -> UserInDB:
    if email_auth_id in db:
        user_dict = db[email_auth_id]
        return UserInDB(**user_dict)


def add_user(db, user_in_db: UserInDB):
    db[user_in_db.email_auth_id] = dict(user_in_db)


def authenticate_user(db, email_auth_id: str, password: str) -> bool | UserInDB:
    user = get_user(db, email_auth_id)
    if not user:
        return False
    if not verify_password(password, user.pw_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Encode the user data with an expire timestamp to create the token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # TODO: set time wanted
        expire = datetime.utcnow() + timedelta(minutes=15)
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
        email_auth_id: str = payload.get("sub")
        if email_auth_id is None:
            raise credentials_exception
        token_data = TokenData(email_auth_id=email_auth_id)
    except ExpiredSignatureError:
        raise expire_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, email_auth_id=token_data.email_auth_id)
    if user is None:
        raise credentials_exception
    return user


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """Called when logging in, generates an access token to use in other functions
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email_auth_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/register/")
async def register(registeruser: RegisterUser):
    """Hash the password of a newly registered user and add its data to the database
    """
    hashed_pw = get_password_hash(registeruser.plain_pw)
    user = UserInDB(email_auth_id=registeruser.email_auth_id, user_id=registeruser.user_id, pw_hash=hashed_pw)
    add_user(fake_users_db, user)


# Example functions

@auth_router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@auth_router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.email_auth_id}]
