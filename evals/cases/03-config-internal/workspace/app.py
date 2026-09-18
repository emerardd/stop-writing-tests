from dataclasses import dataclass


@dataclass
class Settings:
    timeout: int = 30


def request_timeout(config):
    settings = Settings(timeout=config.get("timeout", 30))
    return settings.timeout
