def note_serializer(note):
    return {
        "id": str(note["_id"]),
        "title": note["title"],
        "filename": note["filename"]
    }