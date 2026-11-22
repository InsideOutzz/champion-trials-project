import secrets
import hashlib

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, DeveloperKey
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/developer-keys",
    tags=["Developer Keys"]
)


# Generate a secure developer key
def generate_key():
    return "BCM-" + secrets.token_urlsafe(32)


# Hash key before storing it
def hash_key(key: str):
    return hashlib.sha256(key.encode()).hexdigest()


# GENERATE DEVELOPER KEY
@router.post("/")
def create_developer_key(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if the user already has a key
    existing_key = db.query(DeveloperKey).filter(
        DeveloperKey.user_id == current_user.id
    ).first()

    if existing_key:
        raise HTTPException(
            status_code=400,
            detail="You already have a developer key"
        )

    raw_key = generate_key()
    hashed_key = hash_key(raw_key)

    new_key = DeveloperKey(
        user_id=current_user.id,
        key_hash=hashed_key
    )

    db.add(new_key)
    db.commit()
    db.refresh(new_key)

    # Return the actual key only once
    return {
        "developer_key": raw_key,
        "message": "Developer key generated successfully"
    }


# VERIFY DEVELOPER KEY
@router.post("/verify")
def verify_developer_key(
    data: dict,
    db: Session = Depends(get_db)
):
    key = data.get("key")

    if not key:
        raise HTTPException(
            status_code=400,
            detail="Developer key is required"
        )

    hashed_key = hash_key(key)

    developer_key = db.query(DeveloperKey).filter(
        DeveloperKey.key_hash == hashed_key
    ).first()

    if not developer_key:
        return {
            "valid": False,
            "message": "Invalid developer key"
        }

    return {
        "valid": True,
        "message": "Developer key verified successfully"
    }


# GET CURRENT USER'S DEVELOPER KEY STATUS
@router.get("/status")
def developer_key_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    developer_key = db.query(DeveloperKey).filter(
        DeveloperKey.user_id == current_user.id
    ).first()

    return {
        "has_key": developer_key is not None
    }
