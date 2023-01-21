import structlog
import logging
from logging.handlers import TimedRotatingFileHandler
from structlog import configure, stdlib, processors

# Create the file handlers
fastapi_file_handler = TimedRotatingFileHandler(
    filename='logs/fastapi.log', when='midnight', interval=1, backupCount=7
)
app_file_handler = TimedRotatingFileHandler(
    filename='logs/app.log', when='midnight', interval=1, backupCount=7
)

# Set the formatter for the handlers
fastapi_file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
app_file_handler.setFormatter(logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — "
                                                "%(message)s"))

# Create the loggers
fastapi_log = logging.getLogger("fastapi")
app_log = logging.getLogger("app")

# Add the handlers to the appropriate logger
fastapi_log.addHandler(fastapi_file_handler)
app_log.addHandler(app_file_handler)

# Set the level for the loggers
fastapi_log.setLevel(logging.DEBUG)
app_log.setLevel(logging.DEBUG)

# Configure structlog to use the standard library logger
configure(
    processors=[
        processors.TimeStamper(fmt='iso'),
        processors.JSONRenderer(indent=2)
    ],
    logger_factory=stdlib.LoggerFactory(),
)
