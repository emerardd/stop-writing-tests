def _normalize_name(name):
    return name.strip().title()


def greeting(name):
    return "Hello, " + _normalize_name(name)
