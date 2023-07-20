from fastapi import status
from fastapi.exceptions import HTTPException


class BaseError(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_description = "Error"
    error_type = "base_error"

    def __init__(self, description=None, *args, **kwargs):
        self.description = self.default_description if description is None else description
        self.status_code = kwargs.get("status_code") or self.status_code
        super().__init__(status_code=self.status_code, detail=self.description)


class BadRequestError(BaseError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_description = "Bad request"
    error_type = "bad_request"


class ValidationError(BadRequestError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_description = "Validation failed"
    error_type = "validation_failed"


class APIError(BaseError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_description = "Error occurred"
    error_type = "api_error"


class ForbiddenError(BaseError):
    status_code = status.HTTP_403_FORBIDDEN
    default_description = "Forbidden"
    error_type = "forbidden"
