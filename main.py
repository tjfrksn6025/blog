from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime, timedelta
import os

load_dotenv()

app = FastAPI(
    title="Blog API",
    description="FastAPI 블로그 애플리케이션",
    version="1.0.0"
)
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blogs.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production-min-32-chars")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(String, nullable=False)

    blogs = relationship("BlogModel", back_populates="author")

class BlogModel(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

    author = relationship("UserModel", back_populates="blogs")

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class BlogCreate(BaseModel):
    title: str
    content: str

class BlogUpdate(BaseModel):
    title: str
    content: str

class Blog(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class BlogWithAuthor(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    author_email: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return TokenData(email=email)
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보를 확인할 수 없습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token)
    if token_data is None or token_data.email is None:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.email == token_data.email).first()
    if user is None:
        raise credentials_exception

    return user

def init_db():
    db = SessionLocal()
    try:
        if db.query(UserModel).count() == 0:
            admin_user = UserModel(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                created_at=datetime.now().strftime("%Y-%m-%d"),
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

            initial_blogs = [
                BlogModel(
                    title="Hello",
                    content="World",
                    author_id=admin_user.id,
                    created_at="2025-01-06",
                    updated_at="2025-01-06",
                ),
                BlogModel(
                    title="Python",
                    content="FastAPI is awesome!",
                    author_id=admin_user.id,
                    created_at="2025-01-06",
                    updated_at="2025-01-06",
                ),
                BlogModel(
                    title="JavaScript",
                    content="Fetch API is great",
                    author_id=admin_user.id,
                    created_at="2025-01-06",
                    updated_at="2025-01-06",
                ),
            ]
            for blog in initial_blogs:
                db.add(blog)
            db.commit()
    finally:
        db.close()

init_db()

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Blog API 서버가 정상적으로 실행 중입니다."}

@app.get("/api/hello")
async def hello():
    return {"message": "안녕하세요! FastAPI 블로그입니다."}

@app.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")

    hashed_password = get_password_hash(user_data.password)
    db_user = UserModel(
        email=user_data.email,
        hashed_password=hashed_password,
        created_at=datetime.now().strftime("%Y-%m-%d")
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@app.get("/blogs", response_model=list[BlogWithAuthor])
def read_blogs(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).order_by(BlogModel.id.desc()).all()

    result = []
    for blog in blogs:
        result.append(BlogWithAuthor(
            id=blog.id,
            title=blog.title,
            content=blog.content,
            author_id=blog.author_id,
            author_email=blog.author.email,
            created_at=blog.created_at,
            updated_at=blog.updated_at
        ))

    return result

@app.get("/blogs/{blog_id}", response_model=BlogWithAuthor)
def read_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="블로그 글을 찾을 수 없습니다.")

    return BlogWithAuthor(
        id=blog.id,
        title=blog.title,
        content=blog.content,
        author_id=blog.author_id,
        author_email=blog.author.email,
        created_at=blog.created_at,
        updated_at=blog.updated_at
    )

@app.post("/blogs", response_model=Blog)
def create_blog(
    blog_create_data: BlogCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    now = datetime.now()
    created_at = now.strftime("%Y-%m-%d")

    new_blog = BlogModel(
        title=blog_create_data.title,
        content=blog_create_data.content,
        author_id=current_user.id,
        created_at=created_at,
        updated_at=created_at,
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(
    blog_id: int,
    blog_update_data: BlogUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="블로그 글을 찾을 수 없습니다.")

    if blog.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="이 글을 수정할 권한이 없습니다.")

    blog.title = blog_update_data.title
    blog.content = blog_update_data.content
    blog.updated_at = datetime.now().strftime("%Y-%m-%d")

    db.commit()
    db.refresh(blog)

    return blog

@app.delete("/blogs/{blog_id}")
def delete_blog(
    blog_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="블로그 글을 찾을 수 없습니다.")

    if blog.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="이 글을 삭제할 권한이 없습니다.")

    db.delete(blog)
    db.commit()

    return {"message": "블로그 글이 삭제되었습니다.", "deleted_blog": {"id": blog.id, "title": blog.title}}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
