"""Contains DataJoint helper functions."""
import re
import warnings
from inspect import isclass
from typing import Collection, Dict, Optional, Type

from datajoint import Part
from datajoint.user_tables import UserTable


def replace_stores(definition: str, stores: Dict[str, str]) -> str:
    """Replace the store in the definition according to a mapping of replacement to original stores."""
    stores = {original: replacement for replacement, original in stores.items()}

    def replace_store(match):
        try:
            return match.groups()[0] + stores[match.groups()[1]]
        except KeyError:
            warnings.warn(f"No replacement for store '{match.groups()[1]}' specified. Skipping!", category=UserWarning)
            return match.group(0)

    pattern = re.compile(r"(attach@)(\S+)")
    return re.sub(pattern, replace_store, definition)


def get_part_table_classes(
    table_cls: Type[UserTable], ignored_parts: Optional[Collection[str]] = None
) -> Dict[str, Type[Part]]:
    """Return all part table classes found on the provided table class."""
    if ignored_parts is None:
        ignored_parts = []
    part_table_classes = {}
    for name in dir(table_cls):
        if name[0].isupper() and name not in ignored_parts:
            attr = getattr(table_cls, name)
            if isclass(attr) and issubclass(attr, Part):
                part_table_classes[name] = attr
    return part_table_classes
