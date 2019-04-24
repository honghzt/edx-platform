"""
  Constants and strings for the course-enrollment app
"""

class ResponseStatuses:
    ACTIVE = "active"
    INACTIVE = "inactive"
    DUPLICATED = "duplicated"
    INVALID_STATUS = "invalid-status"
    CONFLICT = "conflict"
    ILLEGAL_OPERATION = "illegal-operation"
    NOT_IN_PROGRAM = "not-in-program"
    INTERNAL_ERROR = "internal-error"

    ERROR_STATUSES = (
        DUPLICATED,
        INVALID_STATUS,
        CONFLICT,
        ILLEGAL_OPERATION,
        NOT_IN_PROGRAM,
        INTERNAL_ERROR,
    )