import argparse
import dataclasses
import itertools
import os
from copy import deepcopy
from enum import Enum
from typing import Any, Dict, Optional, Sequence, Tuple, Union


class ConfigField(Enum):
    ARGUMENT = "argument"
    ATTRIBUTE = "attribute"
    VARIABLE = "variable"


class PrefixSeparator(Enum):
    ARGUMENT = "-"
    ATTRIBUTE = "."
    VARIABLE = "_"


@dataclasses.dataclass
class ConfigMapping:
    attribute: str
    argument: Optional[str] = None
    variable: Optional[str] = None
    default: Any = None
    description: str = None
    group: Optional[Union[str, Sequence[str]]] = None

    def __post_init__(self):
        self.argument = (self.argument or self.attribute).lower()
        self.variable = (self.variable or self.attribute).upper()

        if isinstance(self.group, str):
            self.group = [self.group]
        elif isinstance(self.group, list):
            self.group = self.group
        else:
            self.group = []

    def as_dict(self) -> Dict[Any, Any]:
        """Return class attributes as dictionary"""
        return dataclasses.asdict(self)

    def as_tuple(self) -> Sequence[Tuple[Any, Any]]:
        """Return class attributes as list of tuples"""
        return list(dataclasses.asdict(self).items())


class BaseConfig:
    mappings: Sequence[ConfigMapping] = []

    def __init__(self, mappings: Optional[Sequence[ConfigMapping]] = None):
        mappings = deepcopy(mappings) if mappings is not None else []

        self.merge(mappings=mappings)
        self.update()

    def generate_mappings(self) -> None:
        """Generate mappings for attributes that were set directly"""
        attributes = [(k, v) for k, v in vars(self).items() if k != "mappings"]
        _mapped = set([x.attribute for x in self.mappings])
        _unmapped = [(k, v) for k, v in attributes if k not in _mapped]

        mappings = [ConfigMapping(attribute=k, default=v) for k, v in _unmapped]

        self.merge(mappings=mappings)

    def merge(self, mappings: Optional[Sequence[ConfigMapping]]) -> None:
        """Merge multiple ConfigMapping definitions"""
        assert type(mappings) in (tuple, list), f"Not a valid sequence: {mappings=}"

        mappings = deepcopy(mappings)

        _mappings_merged = {x.attribute: x for x in [*self.mappings, *mappings]}
        self.mappings = list(_mappings_merged.values())

    def remove_unmapped_attributes(self):
        """Remove attributes without valid attribute mappings, retain groups"""
        attributes = set([k for k, v in vars(self).items() if k != "mappings"])
        _mapped = set([x.attribute for x in self.mappings])

        for attribute in set(attributes).difference(_mapped):
            if isinstance(getattr(self, attribute), BaseConfig):
                continue

            delattr(self, attribute)

    def _set_prefix(
        self,
        field: ConfigField,
        prefix: str,
        group: Optional[Union[Sequence[str], str]] = None,
        merge_group: bool = False,
    ):
        """Set a common prefix for arguments or variables, optionally group-only"""
        fields = {
            ConfigField.ARGUMENT: (
                ConfigField.ARGUMENT.value,
                PrefixSeparator.ARGUMENT.value,
            ),
            ConfigField.VARIABLE: (
                ConfigField.VARIABLE.value,
                PrefixSeparator.VARIABLE.value,
            ),
        }

        conversions = {
            ConfigField.ARGUMENT: lambda x: x.lower(),
            ConfigField.VARIABLE: lambda x: x.upper(),
        }

        _field, _separator = fields[field]
        _prefix = conversions[field](prefix)

        _group = group or []
        _group = [group] if isinstance(group, str) else _group
        _group = [conversions[field](g) for g in _group]

        mappings = [x for x in self.mappings if x.group == _group] if group is not None else self.mappings

        _mappings = []

        for mapping in mappings:
            _mapping = mapping.as_dict()

            if isinstance(_group, list) and merge_group is True:
                _members = [_prefix, *_group, _mapping[_field]]
            else:
                _members = [_prefix, _mapping[_field]]

            _prefixed = _separator.join(_members)

            _mappings.append(ConfigMapping(**{**_mapping, _field: _prefixed}))

        self.merge(mappings=_mappings)

    def set_argument_prefix(self, prefix: str, group: str = None):
        """Set a common prefix for arguments, optionally group-only"""
        self._set_prefix(field=ConfigField.ARGUMENT, prefix=prefix, group=group)

    def set_variable_prefix(self, prefix: str, group: str = None):
        """Set a common prefix for arguments, optionally group-only"""
        self._set_prefix(field=ConfigField.VARIABLE, prefix=prefix, group=group)

    def update(self, reset: bool = False) -> None:
        """Update attributes self.mappings"""
        for mapping in self.mappings:
            if (
                hasattr(self, mapping.attribute)
                and getattr(self, mapping.attribute) != mapping.default
                and reset is False
            ):
                continue

            setattr(self, mapping.attribute, mapping.default)

    def update_from_args(self, args: argparse.Namespace) -> None:
        """Update attribute values from argparse arguments"""
        # Transform Namespace into dict, remove None values to honour defaults
        _args = {k: v for k, v in vars(args).items() if v is not None}

        for m in self.mappings:
            setattr(
                self, m.attribute, _args.get(m.argument, getattr(self, m.attribute))
            )

    def update_from_env(self) -> None:
        """Update attribute values from environment variables"""
        for m in self.mappings:
            _variable = m.variable.upper()

            setattr(self, m.attribute, os.getenv(_variable, getattr(self, m.attribute)))

    def update_groups(self) -> None:
        """Recursively create groups from mappings, resulting in a nested class tree"""

        def __grouper(_mapping: ConfigMapping) -> str:
            return _mapping.group[0]

        _groups = [x for x in self.mappings if x.group not in ([], None)]
        _sorted = sorted(_groups, key=__grouper)
        _grouped = [(k, list(g)) for k, g in itertools.groupby(_sorted, __grouper)]

        for group, mappings in _grouped:
            # Remove mappings from parent
            self.mappings = [x for x in self.mappings if x not in mappings]

            _mappings = deepcopy(mappings)

            # Push mapping groups down one level
            for mapping in _mappings:
                mapping.group = mapping.group[1:]

            if not hasattr(self, group):
                setattr(self, group, BaseConfig())

            _group = getattr(self, group)
            _group.merge(mappings=_mappings)

            # Recurse into subgroups
            if any([x.group is not None for x in _group.mappings]):
                _group.update_groups()

            # Update ungrouped mappings
            _group.update()

        # Clean up any attributes which have been pushed into a group
        self.remove_unmapped_attributes()

    def validate(self):
        """Validate that mappings are correct and mapped attributes exist"""
        assert type(self.mappings) in (
            list,
            tuple,
        ), f"Invalid sequence: {self.mappings=}"

        for mapping in self.mappings:
            assert isinstance(
                mapping, ConfigMapping
            ), f"Invalid mapping type: {mapping=}"
            assert hasattr(
                self, mapping.attribute
            ), f"Missing attribute: {mapping.attribute}"
