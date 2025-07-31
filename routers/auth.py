import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from models import UserLogin, AuthResponse, Token, User, BaseResponse, UserCreate, UserResponse
from core.security import (
    authenticate_user, 
    create_access_token, 
    get_current_user,
    create_user_in_db,
    get_user_from_db,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    security
)

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/login", response_model=AuthResponse)
async def login(user_credentials: UserLogin):
    """
    Authenticate user and return JWT token
    """
    logger.info(f"Login attempt for user: {user_credentials.username}")
    
    # Verify user credentials
    if not authenticate_user(user_credentials.username, user_credentials.password):
        logger.warning(f"Failed login attempt for user: {user_credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_credentials.username}, 
        expires_delta=access_token_expires
    )
    
    logger.info(f"Successful login for user: {user_credentials.username}")
    
    token = Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
    )
    
    return AuthResponse(result=token)

@router.post("/register", response_model=BaseResponse)
async def register_user(user_data: UserCreate):
    """
    Register a new user
    """
    logger.info(f"Registration attempt for user: {user_data.username}")
    
    try:
        user = create_user_in_db(
            username=user_data.username,
            password=user_data.password,
            email=user_data.email
        )
        
        logger.info(f"User {user_data.username} registered successfully")
        
        return {
            "result": {
                "username": user["username"],
                "email": user.get("email"),
                "created_at": user["created_at"]
            },
            "msg": "User registered successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration failed for {user_data.username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.get("/protected", response_model=BaseResponse)
async def protected_endpoint(current_user: dict = Depends(get_current_user)):
    """
    Example protected endpoint that requires JWT authentication
    """
    logger.info(f"Protected endpoint accessed by user: {current_user['username']}")
    return {
        "result": {
            "message": f"Hello {current_user['username']}, this is a protected endpoint!",
            "user": current_user['username']
        },
        "msg": "Access granted to protected resource"
    }

@router.get("/me", response_model=BaseResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """
    Get current user information
    """
    logger.info(f"User info requested for: {current_user['username']}")
    return {
        "result": {
            "username": current_user['username'],
            "is_active": True
        },
        "msg": "User information retrieved successfully"
    }
