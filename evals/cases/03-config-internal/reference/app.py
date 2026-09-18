from dataclasses import dataclass


@dataclass
class Settings:
    timeout_seconds: int = 30


def request_timeout(config):
    settings = Settings(timeout_seconds=config.get("timeout", 30))
    return settings.timeout_seconds
