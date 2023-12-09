# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Literal, Union


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP METHOD LITERAL
# └─────────────────────────────────────────────────────────────────────────────────────

HTTPMethodLiteral = Literal["GET", "POST"]

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ JSON
# └─────────────────────────────────────────────────────────────────────────────────────

# Define a generic JSON value type
JSONValue = str | int | float | bool | None

# Define a generic JSON dict type
JSONDict = dict[str, Union[JSONValue, "JSON", list["JSON"]]]

# Define a generic JSON list type
JSONList = list[Union[JSONValue, "JSON", JSONDict]]

# Define a generic JSON type
JSON = JSONValue | JSONDict | JSONList

# Define a generic JSON schema type
JSONSchema = dict[str, str]
