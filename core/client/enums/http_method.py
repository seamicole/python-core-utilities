# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from enum import Enum


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP METHOD
# └─────────────────────────────────────────────────────────────────────────────────────


class HTTPMethod(Enum):
    """An HTTP method enum class"""

    # Set DELETE
    DELETE = "DELETE"

    # Set GET
    GET = "GET"

    # Set POST
    POST = "POST"
