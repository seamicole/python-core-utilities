# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import asyncio

from typing import Any, AsyncGenerator, Generator

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.api.classes.api_endpoint import APIEndpoint
from core.client.types import JSONDict, JSONSchema
from core.collection.classes.dict_collection import DictCollection
from core.placeholders import nothing
from core.placeholders.types import Nothing


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ API ENDPOINT COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class APIEndpointCollection(DictCollection[APIEndpoint]):
    """A dict-based collection utility class for APIEndpoint instances"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST DICTS
    # └─────────────────────────────────────────────────────────────────────────────────

    def request_dicts(
        self,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        with_schema: bool = False,
    ) -> Generator[JSONDict | tuple[JSONDict, JSONSchema | None], None, None]:
        """Yields a series of object dicts for all APIEndpoints in the collection"""

        # Iterate over endpoints
        for endpoint in self:
            # Get JSON path and schema
            json_path_endpoint = (
                endpoint.json_path if isinstance(json_path, Nothing) else json_path
            )
            json_schema_endpoint = (
                endpoint.json_schema
                if isinstance(json_schema, Nothing)
                else json_schema
            )

            # Iterate over items
            for item in endpoint.request_dicts(
                json_path=json_path_endpoint, json_schema=json_schema_endpoint
            ):
                yield (item, json_schema_endpoint) if with_schema else item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST DICTS ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_dicts_async(
        self,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        with_schema: bool = False,
    ) -> AsyncGenerator[JSONDict | tuple[JSONDict, JSONSchema | None], None]:
        """Yields a series of object dicts for all APIEndpoints in the collection"""

        # Initialize requests
        requests = []

        # Initialize JSON arguments
        json_arguments = []

        # Iterate over endpoints
        for endpoint in self:
            # Get JSON path and schema
            json_path_endpoint = (
                endpoint.json_path if isinstance(json_path, Nothing) else json_path
            )
            json_schema_endpoint = (
                endpoint.json_schema
                if isinstance(json_schema, Nothing)
                else json_schema
            )

            # Append to requests
            requests.append(endpoint.request_async())

            # Append to JSON arguments
            json_arguments.append((json_path_endpoint, json_schema_endpoint))

        # Iterate over requests
        for response, (json_path_endpoint, json_schema_endpoint) in zip(
            await asyncio.gather(*requests), json_arguments
        ):
            # Iterate over items
            for item in response.yield_dicts(
                json_path=json_path_endpoint, json_schema=json_schema_endpoint
            ):
                yield (item, json_schema_endpoint) if with_schema else item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST INSTANCES
    # └─────────────────────────────────────────────────────────────────────────────────

    def request_instances(
        self,
        InstanceClass: type,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        with_schema: bool = False,
    ) -> Generator[Any, None, None]:
        """Yields a series of object instances for all APIEndpoints in the collection"""

        # Iterate over endpoints
        for endpoint in self:
            # Get JSON path and schema
            json_path_endpoint = (
                endpoint.json_path if isinstance(json_path, Nothing) else json_path
            )
            json_schema_endpoint = (
                endpoint.json_schema
                if isinstance(json_schema, Nothing)
                else json_schema
            )

            # Iterate over instances
            for instance in endpoint.request_instances(
                InstanceClass=InstanceClass,
                json_path=json_path_endpoint,
                json_schema=json_schema_endpoint,
            ):
                # Yield instance
                yield (instance, json_schema_endpoint) if with_schema else instance

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST INSTANCES ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_instances_async(
        self,
        InstanceClass: type,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        with_schema: bool = False,
    ) -> AsyncGenerator[Any | tuple[Any, JSONSchema], None]:
        """Yields a series of object instances for all APIEndpoints in the collection"""

        # Iterate over items
        async for item in self.request_dicts_async(
            json_path=json_path, json_schema=json_schema, with_schema=with_schema
        ):
            # Check if with schema
            if isinstance(item, tuple):
                # Yield instance
                yield (InstanceClass(**item[0]), item[1])

            # Otherwise, yield instance
            else:
                # Initialize and yield instance
                yield InstanceClass(**item)