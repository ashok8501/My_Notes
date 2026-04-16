from fastapi import APIRouter, HTTPException
from database import users_collection
from passlib.hash import bcrypt

router = APIRouter()


# 🔹 Signup
@router.post("/signup")
def signup(user: dict):
    if not user.get("email") or not user.get("password"):
        raise HTTPException(status_code=400, detail="All fields are required")

    existing = users_collection.find_one({"email": user["email"]})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user["password"] = bcrypt.hash(user["password"])
    users_collection.insert_one(user)

    return {"message": "Signup successful"}


# 🔹 Login
@router.post("/login")
def login(user: dict):
    if not user.get("email") or not user.get("password"):
        raise HTTPException(status_code=400, detail="All fields are required")

    db_user = users_collection.find_one({"email": user["email"]})

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.verify(user["password"], db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {
        "message": "Login successful",
        "user_id": str(db_user["_id"]),
        "email": db_user["email"]
    }