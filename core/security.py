import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from errors.error_schema import UnauthorizedAccess
from core.db import MongoDBClient

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

# Bearer token scheme
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Get password hash"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_user_from_db(username: str) -> Optional[dict]:
    """Get user from MongoDB"""
    try:
        user_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Users")
        user = user_collection.find_one({"username": username})
        return user
    except Exception:
        return None

def create_user_in_db(username: str, password: str, email: Optional[str] = None) -> dict:
    """Create a new user in MongoDB"""
    user_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Users")
    
    # Check if user already exists
    if user_collection.find_one({"username": username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Create user document
    user_doc = {
        "username": username,
        "hashed_password": get_password_hash(password),
        "email": email,
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    result = user_collection.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    return user_doc

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user against MongoDB"""
    user = get_user_from_db(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    if not user.get("is_active", True):
        return False
    return True

def init_default_users():
    """Initialize default users if they don't exist"""
    try:
        # Create default admin user if not exists
        if not get_user_from_db("admin"):
            create_user_in_db("admin", "admin123", "admin@portfolio.com")
            print("✅ Created default admin user")
        
        # Create default regular user if not exists
        if not get_user_from_db("user"):
            create_user_in_db("user", "user123", "user@portfolio.com")
            print("✅ Created default user")
            
    except Exception as e:
        print(f"⚠️ Could not initialize default users: {e}")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Dependency to get current user from JWT token"""
    try:
        payload = verify_token(credentials.credentials)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database to ensure they still exist and are active
        user = get_user_from_db(username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {"username": username, "email": user.get("email"), "is_active": user.get("is_active", True)}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
