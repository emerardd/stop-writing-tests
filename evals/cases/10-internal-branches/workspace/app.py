def can_read(user, document):
    if user["id"] == document["owner_id"]:
        return True
    if user["role"] == "admin":
        return True
    return False
