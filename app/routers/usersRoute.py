from fastapi import APIRouter, Depends, HTTPException, status
from app.dependency import get_db
from .. import models
from ..schemas.usersSchema import *
from sqlalchemy.orm import session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta



SECRET_KEY = "akdfklasdfklashfsadf4s5d4f89a4gdsf547s5d4f54a8777a564df65ads"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl= "token")

router = APIRouter(
    prefix="/user",
    tags=["User"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

# create hash pass function
def create_hash_pass(password):
    return bcrypt_context.hash(password)

# validate hash pass word matched
def verify_password (plain_pass, hash_pass):
    return bcrypt_context.verify(plain_pass, hash_pass)

#check if user is authenticate
def auth_user(username:str, password:str, db):
    # get specific user with his or her metadata like email, username, this is an object
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_pass):
        return False
    return user


@router.post("/create_user", response_model = UserBaseSchema)
def hello(user: UserInSchema, db:session = Depends(get_db)):
    # remember pydantic models attribute or metadata name and model's metadata or table column header data name must be same

    get_email = db.query(models.Users).filter(models.Users.email == user.email).first()
    get_username = db.query(models.Users).filter(models.Users.username == user.username).first()

    print (get_username)
    if get_email:
        raise HTTPException (status_code= status.HTTP_406_NOT_ACCEPTABLE, detail="email already reigstered")

    if get_username:
        raise HTTPException (status_code= status.HTTP_406_NOT_ACCEPTABLE, detail="user already reigstered")
    # password hashing
    hash_pass = user.password
    hash_pass =  create_hash_pass(hash_pass)
    # userModel = models.Users(**user.dict(), hashed_pass = hash_pass )
    userModel = models.Users()
    userModel.email = user.email
    userModel.username = user.username
    userModel.fname = user.fname
    userModel.lnam = user.lnam
    userModel.hashed_pass = hash_pass
    userModel.email = user.email
    userModel.is_active = user.is_active
    db.add(userModel)
    db.commit()

    return userModel

####### create login  path and take access token
@router.post("/login" )
async def login_for_access_token (
    form_data : OAuth2PasswordRequestForm = Depends(),
    db:session = Depends(get_db)):

    user = auth_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "user not found")
    
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username , user.id, expires_delta= token_expires )
    return {"access_token" : token , "bearer" : "oauth2passwordbearer"}

def create_access_token(username:str, user_id: int , expires_delta : timedelta | None ):
    encode = {"sub" : username, "id" : user_id}
    if expires_delta:
        expire = datetime.utcnow()+ expires_delta
    else:
        expire = datetime.utcnow()+ timedelta(minutes=15)

    encode.update({"exp" : expire})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)