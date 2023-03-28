import logging
import sys

from generation.settings import GeneratorSettings


settings = GeneratorSettings()
logging_levels = {value: key for key, value in logging._levelToName.items()}
logging_level_name = settings.LOG_LEVEL.upper()
if logging_level_name not in logging_levels:
    raise ValueError(f"{logging_level_name} is not a valid log level")

logging.basicConfig(stream=sys.stdout, level=logging_levels[logging_level_name], force=True)
