def status_label(code):
    return {200: "ok", 404: "missing"}.get(code, "unknown")
