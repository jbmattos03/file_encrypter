import structlog
from logging import NOTSET
from typing import Optional, Any

def logger_config(name: Optional[str] = None, pretty: bool = True) -> Any:
    processors = [
        # Context-local context
        structlog.contextvars.merge_contextvars,

        # Add log level
        structlog.processors.add_log_level,

        # Stack information
        structlog.processors.StackInfoRenderer(),

        # Add possibility to add exception info
        structlog.dev.set_exc_info,

        # Timestamps
        structlog.processors.TimeStamper(fmt="%Y%m%d %H:%M:%S", utc=False),

        # Renderer
        # ConsoleRenderer for pretty console rendering
        # JSONRenderer for JSON logs
        structlog.dev.ConsoleRenderer() if pretty else structlog.processors.JSONRenderer()
    ]

    structlog.configure(
        # Processors
        processors=processors,

        # Filter logs based on log level
        # Use NOTSET to show all logs
        wrapper_class=structlog.make_filtering_bound_logger(NOTSET),

        # Context class
        context_class=dict,

        # Logger factory
        logger_factory=structlog.PrintLoggerFactory(),

        # Cache assembled logger
        cache_logger_on_first_use=False
    )

    logger = structlog.get_logger()

    if name:
        logger = logger.bind(process_name=name)
    
    return logger