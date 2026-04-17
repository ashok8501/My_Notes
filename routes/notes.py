from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from bson import ObjectId

from database import notes_collection

router = APIRouter()


# 🔹 Upload Note (STORE FILE IN DB)
@router.post("/upload")
async def upload_note(
    title: str = Form(...),
    subject: str = Form(...),
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # read file as binary
        file_data = await file.read()

        subject = subject.strip().title()

        note = {
            "title": title,
            "subject": subject,
            "filename": file.filename,
            "file_data": file_data,   # 🔥 IMPORTANT CHANGE
            "user_id": user_id,
            "is_bookmarked": False
        }

        result = notes_collection.insert_one(note)

        return {"id": str(result.inserted_id)}

    except Exception as e:
        print("Upload Error:", e)
        raise HTTPException(status_code=500, detail="Upload failed")


# 🔹 Bookmark
@router.put("/bookmark/{note_id}")
def toggle_bookmark(note_id: str):
    note = notes_collection.find_one({"_id": ObjectId(note_id)})

    if not note:
        raise HTTPException(status_code=404, detail="Not found")

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

    result = []
    for n in notes:
        result.append({
            "id": str(n["_id"]),
            "title": n["title"],
            "subject": n.get("subject", "General"),
            "is_bookmarked": n.get("is_bookmarked", False)
        })

    return result


# 🔹 View Note (FROM DB)
@router.get("/view/{note_id}")
def view_note(note_id: str):
    note = notes_collection.find_one({"_id": ObjectId(note_id)})

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return Response(
        content=note["file_data"],   # 🔥 IMPORTANT
        media_type="application/pdf"
    )


# 🔹 Delete Note
@router.delete("/delete/{note_id}")
def delete_note(note_id: str):
    note = notes_collection.find_one({"_id": ObjectId(note_id)})

    if not note:
        raise HTTPException(status_code=404, detail="Not found")

    notes_collection.delete_one({"_id": ObjectId(note_id)})

    return {"message": "Deleted"}