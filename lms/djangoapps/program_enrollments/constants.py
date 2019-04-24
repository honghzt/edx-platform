"""
  Constants and strings for the course-enrollment app
"""

class ResponseStatuses:
    ENROLLED = "enrolled"
    ENROLLED_WAITING = "enrolled-waiting"
    PENDING = "pending"
    PENDING_WAITING = "pending-waiting"
    DUPLICATED = "duplicated"
    INVALID_STATUS = "invalid-status"
    CONFLICT = "conflict"
    NOT_FOUND = "not-found"
    INTERNAL_ERROR = "internal-error"

    ERROR_STATUSES = (
        DUPLICATED,
        INVALID_STATUS,
        CONFLICT,
        NOT_FOUND
        INTERNAL_ERROR
    )

    @classmethod
    def get_waiting(cls, status):
        if status == ENROLLED:
            return ENROLLED_WAITING
        if status == PENDING:
            return PENDING_WAITING
        return status