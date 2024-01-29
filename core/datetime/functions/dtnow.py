# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from datetime import datetime

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.datetime.functions.dtto_utc import dtto_utc


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DTNOW
# └─────────────────────────────────────────────────────────────────────────────────────


def dtnow() -> datetime:
    """Returns a datetime object with the current date and time"""

    # Return datetime
    return datetime.now()


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DTNOW UTC
# └─────────────────────────────────────────────────────────────────────────────────────


def dtnow_utc() -> datetime:
    """Returns a datetime object with the current date and time in UTC"""

    # Return datetime
    return dtto_utc(dtnow())
