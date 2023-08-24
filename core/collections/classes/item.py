# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from datetime import datetime
from typing import Any, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collections.classes.collection import Collection
from core.collections.classes.items import Items
from core.functions.dictionary import dget, dset

if TYPE_CHECKING:
    from core.types import JSONDict, JSONList
    from core.clients.types import JSONSchema


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ITEM METACLASS
# └─────────────────────────────────────────────────────────────────────────────────────


class ItemMetaclass(type):
    """A metaclass for the Item class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of Meta
    Meta: type[Item.Meta]

    # Declare type of InstanceMeta
    InstanceMeta: type[Item.InstanceMeta]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of class meta
    _cmeta: Item.Meta

    # Declare type of instance meta
    _imeta: Item.InstanceMeta

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __CALL__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __call__(cls, *args: Any, **kwargs: Any) -> Item:
        """Call Method"""

        # Create instance
        instance: Item = super().__call__(*args, **kwargs)

        # Initialize meta
        instance._imeta = cls.InstanceMeta()

        # Return instance
        return instance

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]
    ) -> None:
        """Init Method"""

        # Call super method
        super().__init__(name, bases, attrs)

        # Get Meta
        Meta = cls.Meta

        # Ensure that keys is a tuple
        Meta.KEYS = tuple(Meta.KEYS)

        # Ensure that indexes is a tuple
        Meta.INDEXES = tuple(Meta.INDEXES)

        # Initialize meta
        cls._cmeta = Meta()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ITEMS
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def items(cls) -> Collection | Items:
        """Returns the items of the item's meta instance"""

        # Return meta items
        return cls._cmeta.items


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ITEM
# └─────────────────────────────────────────────────────────────────────────────────────


class Item(metaclass=ItemMetaclass):
    """A utility class that represents an arbitrary Python object"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of class meta
    _cmeta: Item.Meta

    # Declare type of instance meta
    _imeta: Item.InstanceMeta

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __EQ__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __eq__(self, other: Any) -> bool:
        """Equality Method"""

        # Check if other is an item
        if isinstance(other, Item):
            # Check if items have the same ID
            if self._imeta.id == other._imeta.id:
                return True

        # Call super method
        return super().__eq__(other)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        """Representation Method"""

        # Get representation
        representation = self.__class__.__name__

        # Add angle brackets to representation
        representation = f"<{representation}: {str(self)}>"

        # Return representation
        return representation

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __STR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __str__(self) -> str:
        """String Method"""

        # Iterate over keys
        for key in self._cmeta.KEYS:
            # Check if key is a string
            if isinstance(key, str):
                # Continue if item does not have key
                if not hasattr(self, key):
                    continue

                # Get value
                value = getattr(self, key)

                # Continue if value is null
                if value in (None, ""):
                    continue

                # Return the string of the value
                return str(value)

            # Otherwise check if key is a tuple
            elif isinstance(key, tuple):
                # Get values
                values = tuple(getattr(self, k, None) for k in key)

                # Return the string of the values
                return "(" + ", ".join(str(value) for value in values) + ")"

        # Return the hex ID of the item
        return hex(id(self))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FROM DICT
    # └─────────────────────────────────────────────────────────────────────────────────

    @classmethod
    def from_dict(
        cls: type[Item],
        data: dict[Any, Any],
        schema: JSONSchema | None = None,
        root_data: JSONList | JSONDict | None = None,
    ) -> Item:
        """Initializes an item from a dictionary"""

        # Initialize kwargs
        kwargs = data

        # Check if data is a dictionary
        if schema is not None and isinstance(data, dict):
            # Initialize kwargs
            kwargs = {}

            # Iterate over schema
            for setter, getter in (schema or {}).items():
                # Check if getter is callable
                if callable(getter):
                    # Get value to set
                    value_to_set = getter(root_data, data)

                # Otherwise handle case of string path
                else:
                    # Get value to set
                    value_to_set = dget(data, getter, delimiter=".")

                # Check if the setter is a tuple
                if isinstance(setter, tuple):
                    # Check if the value to set is not a tuple or list
                    if not isinstance(value_to_set, (tuple, list)):
                        # Convert value to set to a list
                        value_to_set = [value_to_set] * len(setter)

                    # Iterate over zip of setter and value to set
                    for setter_item, value_to_set_item in zip(setter, value_to_set):
                        # Remap data
                        dset(kwargs, setter_item, value_to_set_item)

                # Otherwise, simply remap data
                else:
                    # Remap data
                    dset(kwargs, setter, value_to_set)

        # Initialize item
        item = cls(**kwargs)

        # Return item
        return item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PUSH
    # └─────────────────────────────────────────────────────────────────────────────────

    def push(self) -> None:
        """Pushes an item to the collection"""

        # Iterate over attributes
        for val in self.__dict__.values():
            # Check if value is an item
            if isinstance(val, Item) and val._imeta.id is None:
                # Push item
                val.push()

        # Push item to items collection
        self.__class__.items.push(self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ META
    # └─────────────────────────────────────────────────────────────────────────────────

    class Meta:
        """Meta Class"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CLASS ATTRIBUTES
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize items
        ITEMS: Collection | Items | None = None

        # Initialize keys
        KEYS: tuple[str | tuple[str, ...], ...] = ()

        # Initialize indexes
        INDEXES: tuple[str | tuple[str, ...], ...] = ()

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INSTANCE ATTRIBUTES
        # └─────────────────────────────────────────────────────────────────────────────

        # Declare type of _items
        _items: Items | None = None

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ __INIT__
        # └─────────────────────────────────────────────────────────────────────────────

        def __init__(self) -> None:
            """Init Method"""

            # Initialize items
            self._items = (
                self.ITEMS.all() if isinstance(self.ITEMS, Collection) else self.ITEMS
            )

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ ITEMS
        # └─────────────────────────────────────────────────────────────────────────────

        @property
        def items(self) -> Items:
            """Returns the items of the meta instance"""

            # Get items
            items = self._items

            # Check if items is None
            if items is None:
                # Raise AttributeError
                raise AttributeError(
                    f"{self.__class__.__name__}.Meta.ITEMS is undefined."
                )

            # Return items
            return items

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE META
    # └─────────────────────────────────────────────────────────────────────────────────

    class InstanceMeta:
        """Instance Meta Class"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INSTANCE ATTRIBUTES
        # └─────────────────────────────────────────────────────────────────────────────

        # Declare type of ID
        id: str | None

        # Declare type of pushed at
        pushed_at: datetime | None

        # Declare type of pulled at
        pulled_at: datetime | None

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ __INIT__
        # └─────────────────────────────────────────────────────────────────────────────

        def __init__(self) -> None:
            """Init Method"""

            # Initialize ID
            self.id = None

            # Initialize pushed at
            self.pushed_at = None

            # Initialize pulled at
            self.pulled_at = None
