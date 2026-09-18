def can_read(user, document):
    return user["id"] == document["owner_id"] or user["role"] == "admin"
