from fastapi import APIRouter, HTTPException
from database import users_collection
from passlib.context import CryptContext

router = APIRouter()

# 🔐 Password hashing setup (correct way)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 🔹 SIGNUP
@router.post("/signup")
def signup(user: dict):
    try:
        email = user.get("email")
        password = user.get("password")

        # Validation
        if not email or not password:
            raise HTTPException(status_code=400, detail="All fields are required")

        # Limit password length (bcrypt limit)
        password = password[:72]

        # Check if user already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Hash password
        hashed_password = pwd_context.hash(password)

        # Save user
        users_collection.insert_one({
            "email": email,
            "password": hashed_password
        })

        return {"message": "Signup successful"}

    except HTTPException as e:
        raise e

    except Exception as e:
        print("Signup Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# 🔹 LOGIN
@router.post("/login")
def login(user: dict):
    try:
        email = user.get("email")
        password = user.get("password")

        # Validation
        if not email or not password:
            raise HTTPException(status_code=400, detail="All fields are required")

        # Limit password length (same as signup)
        password = password[:72]

        db_user = users_collection.find_one({"email": email})

        # User not found
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verify password
        if not pwd_context.verify(password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid password")

        return {
            "message": "Login successful",
            "user_id": str(db_user["_id"]),
            "email": db_user["email"]
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print("Login Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")