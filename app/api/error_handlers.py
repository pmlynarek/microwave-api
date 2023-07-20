from typing import Dict
from typing import List

from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError

from app.api.errors import APIError
from app.api.errors import ValidationError
from app.core.logging import get_logger

logger = get_logger(__name__)


class ErrorMessage(BaseModel):
    description: str
    type: str
    errors: Dict[str, List[str]] = None
    duplicated_readings: List[dict] = None


def register_error_handlers(application):
    for exception, handler in HANDLERS["exception"]:
        application.add_exception_handler(exception, handler)


def default_handler(request, exception):
    error_msg = ErrorMessage(description=exception.description, type=exception.error_type).model_dump(exclude_none=True)

    return ORJSONResponse(error_msg, status_code=exception.status_code)


def validation_error_handler(request, exception):
    logger.info(f"Validation error occurred. Exception: {exception}")
    exception_errors = getattr(exception, "errors", [])
    errors = {}

    if exception_errors:
        if isinstance(exception_errors, dict):
            errors = exception_errors
        else:
            for error in exception.errors():
                field_name = error["loc"][-1]
                error_message = error["msg"]
                errors[field_name] = [error_message]
    try:
        description = exception.description
        error_type = exception.error_type
    except AttributeError:
        description = ValidationError.default_description
        error_type = ValidationError.error_type

    error_msg = ErrorMessage(description=description, type=error_type, errors=errors or None).model_dump(
        exclude_none=True
    )

    return ORJSONResponse(error_msg, status_code=ValidationError.status_code)


HANDLERS = {
    "exception": (
        (PydanticValidationError, validation_error_handler),
        (RequestValidationError, validation_error_handler),
        (APIError, default_handler),
    ),
}
