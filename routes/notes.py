from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from bson import ObjectId
import shutil
import os
import mimetypes

from database import notes_collection
from schemas import note_serializer

router = APIRouter()

UPLOAD_FOLDER = "files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🔹 Upload Note
@router.post("/upload")
async def upload_note(
    title: str = Form(...),
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    note = {
        "title": title,
        "filename": file.filename,
        "filepath": file_path,
        "user_id": user_id
    }

    result = notes_collection.insert_one(note)

    return {"message": "Uploaded successfully", "id": str(result.inserted_id)}


# 🔹 Get Notes for Logged-in User
@router.get("/{user_id}")
def get_notes(user_id: str):
    notes = notes_collection.find({"user_id": user_id})
    return [note_serializer(n) for n in notes]


# 🔹 View File (OPEN in browser)
@router.get("/view/{note_id}")
def view_note(note_id: str):
    note = notes_collection.find_one({"_id": ObjectId(note_id)})

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    file_path = note["filepath"]
    mime_type, _ = mimetypes.guess_type(file_path)

    return FileResponse(
        path=file_path,
        media_type=mime_type or "application/octet-stream"
    )


# 🔹 Delete Note
@router.delete("/{note_id}")
def delete_note(note_id: str):
    note = notes_collection.find_one({"_id": ObjectId(note_id)})

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if os.path.exists(note["filepath"]):
        os.remove(note["filepath"])

    notes_collection.delete_one({"_id": ObjectId(note_id)})

    return {"message": "Deleted successfully"}