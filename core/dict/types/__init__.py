# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any, Callable


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DICT SCHEMA
# └─────────────────────────────────────────────────────────────────────────────────────

# Define a dict schema type
DictSchema = dict[str | tuple[str, ...], str | Callable[[Any, Any], Any]]