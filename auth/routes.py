from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from db.database import get_db
from db.models import User
from core.security import hash_password, verify_password, create_access_token
from schemas.user import RegisterRequest, LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


# ✅ REGISTER
@router.post("/register")
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(User).where(User.email == data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        qualification=data.qualification,
        aim=data.aim
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "User registered successfully"}


# ✅ LOGIN
@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})


    return TokenResponse(access_token=token)
