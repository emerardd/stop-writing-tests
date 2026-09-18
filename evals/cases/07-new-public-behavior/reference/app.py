def status_label(code):
    return {200: "ok", 404: "missing", 429: "retry later"}.get(code, "unknown")
