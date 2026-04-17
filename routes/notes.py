from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from bson import ObjectId

from database import notes_collection

router = APIRouter()


# 🔹 Upload
@router.post("/upload")
async def upload_note(
    title: str = Form(...),
    subject: str = Form(...),
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    file_data = await file.read()

    note = {
        "title": title,
        "subject": subject.strip().title(),
        "filename": file.filename,
        "file_data": file_data,
        "user_id": user_id,
        "is_bookmarked": False
    }

    result = notes_collection.insert_one(note)
    return {"id": str(result.inserted_id)}


# 🔹 Bookmark
@router.put("/bookmark/{note_id}")
def toggle_bookmark(note_id: str):
    note = notes_collection.find_one({"_id": ObjectId(note_id)})

    new_status = not note.get("is_bookmarked", False)

    notes_collection.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": {"is_bookmarked": new_status}}
    )

    return {"is_bookmarked": new_status}


# 🔹 Get Notes
@router.get("/user/{user_id}")
def get_notes(user_id: str):
    notes = notes_collection.find({"user_id": user_id})

    return [
        {
            "id": str(n["_id"]),
            "title": n["title"],
            "subject": n.get("subject", "General"),
            "is_bookmarked": n.get("is_bookmarked", False)
        }
        for n in notes
    ]


# 🔹 View (INLINE)
@router.get("/view/{note_id}")
def view_note(note_id: str):
    note = notes_collection.find_one({"_id": ObjectId(note_id)})

    return Response(
        content=note["file_data"],
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename={note['filename']}"
        }
    )


# 🔹 Download
@router.get("/download/{note_id}")
def download_note(note_id: str):
    note = notes_collection.find_one({"_id": ObjectId(note_id)})

    return Response(
        content=note["file_data"],
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={note['filename']}"
        }
    )


# 🔹 Delete
@router.delete("/delete/{note_id}")
def delete_note(note_id: str):
    notes_collection.delete_one({"_id": ObjectId(note_id)})
    return {"message": "Deleted"}