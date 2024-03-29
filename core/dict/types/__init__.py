# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any, Callable

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.dict.classes.dict_schema_context import DictSchemaContext


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DICT SCHEMA
# └─────────────────────────────────────────────────────────────────────────────────────

# Define a dict schema type
DictSchema = dict[str | tuple[str, ...], str | Callable[[DictSchemaContext], Any]]
