def cached_value(entry, now):
    if now >= entry["expires_at"]:
        return None
    return entry["value"]
