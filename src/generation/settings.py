from pydantic import BaseSettings


class GeneratorSettings(BaseSettings):
    LOG_LEVEL: str = "info"
