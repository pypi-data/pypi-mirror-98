import argparse
import os
from copy import deepcopy

import pytest

from rmk2.config import BaseConfig, ConfigField, ConfigMapping, PrefixSeparator


@pytest.mark.parametrize("group", ("abc", ["abc"], [], None))
@pytest.mark.parametrize("description", ("Foobar", None))
@pytest.mark.parametrize("default", (42, None))
@pytest.mark.parametrize("variable", ("baz", "BAZ", None))
@pytest.mark.parametrize("argument", ("bar", "BAR", None))
def test_configmapping_init(argument, variable, default, description, group) -> None:
    """Check that creating ConfigMapping instances meets expectations"""
    attribute = "foo"

    config = ConfigMapping(
        attribute=attribute,
        argument=argument,
        variable=variable,
        default=default,
        description=description,
        group=group,
    )

    assert isinstance(config, ConfigMapping)
    assert config.attribute == attribute

    assert config.argument == (argument if argument is not None else config.attribute).lower()
    assert config.variable == (variable if variable is not None else config.attribute).upper()
    assert config.default == default
    assert config.description == description

    if group is None:
        assert config.group == []
    elif isinstance(group, str):
        assert config.group == [group]
    else:
        assert config.group == group


def test_configmapping_as_dict() -> None:
    """Check that returning ConfigMapping attributes as dict meets expectations"""
    attribute = "foo"
    default = 42

    config = ConfigMapping(attribute=attribute, default=default)

    config_dict = config.as_dict()

    assert isinstance(config_dict, dict)

    assert all(x in config_dict for x in vars(config))

    assert config_dict["attribute"] == config.attribute == attribute
    assert config_dict["default"] == config.default == default


def test_configmapping_as_tuple() -> None:
    """Check that returning ConfigMapping attributes as tuples meets expectations"""
    attribute = "foo"
    default = 42

    config = ConfigMapping(attribute=attribute, default=default)

    config_tuple = config.as_tuple()

    assert isinstance(config_tuple, list)
    assert all(isinstance(x, tuple) for x in config_tuple)

    assert set([k for k, v in config_tuple]) == set(vars(config))

    for key, value in (("attribute", attribute), ("default", default)):
        assert all([k == key and v == value for k, v in config_tuple if k == key])


@pytest.mark.parametrize(
    "mappings",
    (
        None,
        [],
        [ConfigMapping(attribute="foo", default=42)],
        [ConfigMapping(attribute="foo"), ConfigMapping(attribute="bar")],
    ),
)
def test_baseconfig_init(mappings) -> None:
    """Check that creating ConfigMapping instances meets expectations"""
    config = BaseConfig(mappings=mappings)

    assert isinstance(config, BaseConfig)

    if mappings is not None:
        for mapping in mappings:
            assert hasattr(config, mapping.attribute)
            assert getattr(config, mapping.attribute) == mapping.default


@pytest.mark.parametrize("reset", (True, False))
@pytest.mark.parametrize("override", (None, 42))
def test_baseconfig_update(override, reset) -> None:
    """Check that merging ConfigMappings meets expectations"""
    mappings = [ConfigMapping(attribute="foo", default=21)]

    config = BaseConfig()

    assert isinstance(config, BaseConfig)

    assert not any(hasattr(config, x.attribute) for x in mappings)

    config.mappings = mappings
    config.update()

    for mapping in mappings:
        assert hasattr(config, mapping.attribute)

    if override is not None:
        for mapping in mappings:
            setattr(config, mapping.attribute, override)
            assert getattr(config, mapping.attribute) == override != mapping.default

    if reset is True:
        config.update(reset=True)

        for mapping in mappings:
            assert getattr(config, mapping.attribute) == mapping.default != override


@pytest.mark.parametrize(
    "mappings", ([ConfigMapping("bar")], [ConfigMapping("foo"), ConfigMapping("bar")])
)
def test_baseconfig_merge(mappings) -> None:
    """Check that merging ConfigMappings meets expectations"""
    initial_mappings = [ConfigMapping(attribute="foo", default=42)]

    config = BaseConfig(mappings=initial_mappings)
    config.merge(mappings=mappings)

    mappings_dict = {}

    for mapping in initial_mappings:
        mappings_dict[mapping.attribute] = mapping

    for mapping in mappings:
        mappings_dict[mapping.attribute] = mapping

    mappings_merged = list(mappings_dict.values())

    assert isinstance(config.mappings, list)
    assert all([isinstance(x, ConfigMapping) for x in config.mappings])
    assert config.mappings == mappings_merged


@pytest.mark.parametrize(
    "mappings",
    (
        [ConfigMapping(attribute="foo", argument="foo")],
        [ConfigMapping(attribute="foo", argument="bar")],
    ),
)
def test_baseconfig_update_from_args(mappings) -> None:
    """Check that updating a BaseConfig instance from argparse meets expectations"""
    config = BaseConfig(mappings=mappings)

    parser = argparse.ArgumentParser()

    for mapping in mappings:
        parser.add_argument(mapping.argument)

    args_parsed = parser.parse_args([str(idx) for idx, _ in enumerate(mappings)])

    assert all(hasattr(config, x.attribute) for x in mappings)
    assert all(getattr(config, x.attribute) == x.default for x in mappings)

    config.update_from_args(args=args_parsed)

    for idx, mapping in enumerate(mappings):
        assert getattr(config, mapping.attribute) == str(idx) != mapping.default


@pytest.mark.parametrize(
    "mappings",
    (
        [ConfigMapping(attribute="foo", variable="foo")],
        [ConfigMapping(attribute="foo", variable="bar")],
    ),
)
def test_baseconfig_update_from_env(mappings) -> None:
    """Check that updating a BaseConfig instance from ENV meets expectations"""
    config = BaseConfig(mappings=mappings)

    for idx, mapping in enumerate(mappings):
        os.environ[mapping.variable.upper()] = str(idx)

    assert all(hasattr(config, x.attribute) for x in mappings)
    assert all(getattr(config, x.attribute) == x.default for x in mappings)

    config.update_from_env()

    for idx, mapping in enumerate(mappings):
        assert mapping.variable.upper() in os.environ
        assert (
            getattr(config, mapping.attribute)
            == str(idx)
            == os.getenv(mapping.variable.upper())
            != mapping.default
        )


def test_baseconfig_validate() -> None:
    """Check that validating BaseConfig mappings meets expectations"""
    config = BaseConfig()

    # Invalid mapping sequence
    with pytest.raises(AssertionError) as e:
        mappings_not_sequence = {}
        config.mappings = mappings_not_sequence
        config.validate()

    assert e
    assert str(e.value) == f"Invalid sequence: self.mappings={mappings_not_sequence}"

    # Invalid mapping type
    with pytest.raises(AssertionError) as e:
        mappings_wrong_type = [("a", 1), ("b", 2)]
        config.mappings = mappings_wrong_type
        config.validate()

    assert e
    assert str(e.value) == f"Invalid mapping type: mapping={mappings_wrong_type[0]}"

    # Valid mappings, config not updated
    with pytest.raises(AssertionError) as e:
        mappings_not_updated = [ConfigMapping(attribute="foo")]
        config.mappings = mappings_not_updated
        config.validate()

    assert e
    assert str(e.value) == f"Missing attribute: {mappings_not_updated[0].attribute}"

    # Valid mappings, config updated
    mappings_valid = [ConfigMapping(attribute="foo")]
    config.mappings = mappings_valid
    config.update()
    config.validate()


@pytest.mark.parametrize("mappings", ([("foo", 42)], [("foo", 42), ("bar", 42)]))
def test_baseconfig_generate_mappings(mappings) -> None:
    """Check that generating mappings from attributes meets expectations"""
    config = BaseConfig()

    for attribute, value in mappings:
        setattr(config, attribute, value)

    config.generate_mappings()

    mappings_generated = [(x.attribute, x.default) for x in config.mappings]

    assert len(config.mappings) == len(mappings_generated) == len(mappings)
    assert set(mappings_generated) == set(mappings)


def test_baseconfig_remove_unmapped_attributes() -> None:
    """Check that removing attributes without mappings matches expectations"""
    mappings = [
        ConfigMapping("foo"),
        ConfigMapping("bar"),
        ConfigMapping("abc", group="xyz"),
    ]

    unmapped = [ConfigMapping("baz", default=42), ConfigMapping("bat", default=42)]

    config = BaseConfig(mappings=mappings)

    for mapping in unmapped:
        setattr(config, mapping.attribute, mapping.default)

    assert all([hasattr(config, x.attribute) for x in [*mappings, *unmapped]])

    config.remove_unmapped_attributes()

    assert all([hasattr(config, x.attribute) for x in mappings])
    assert not any([hasattr(config, x.attribute) for x in unmapped])


def test_baseconfig_update_groups() -> None:
    """Check that recursively creating groups meets expectations"""

    def __recursive_check(_config: BaseConfig, _mapping: ConfigMapping) -> bool:
        _mapping = deepcopy(_mapping)
        _group = _mapping.group

        if isinstance(_group, list) and len(_group) > 0:
            _mapping.group = _group[1:]
            __recursive_check(getattr(_config, _group[0]), _mapping)
            _result = hasattr(_config, _group[0])
        else:
            _result = hasattr(_config, _mapping.attribute)

        return _result

    mappings = [
        ConfigMapping("foo", group=["rst", "uvw", "xyz"]),
        ConfigMapping("bar", group=["rst", "uvw"]),
        ConfigMapping("baz", group=["rst"]),
        ConfigMapping("bat", group=None),
    ]

    config = BaseConfig(mappings=mappings)

    assert all([hasattr(config, x.attribute) for x in mappings])

    config.update_groups()

    for mapping in mappings:
        assert __recursive_check(_config=config, _mapping=mapping)


@pytest.mark.parametrize("merge_group", (True, False))
@pytest.mark.parametrize("group", (None, "abc", ["abc"]))
@pytest.mark.parametrize("prefix", ("x", "y"))
@pytest.mark.parametrize("field", (ConfigField.ARGUMENT, ConfigField.VARIABLE))
def test_baseconfig_set_prefix(field, prefix, group, merge_group) -> None:
    """Check that setting a common prefix for all arguments meets expectations"""
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

    mappings = [
        ConfigMapping(attribute="foo", argument="foo", group=None),
        ConfigMapping(attribute="bar", argument="bar", group="abc"),
    ]

    config = BaseConfig(mappings=mappings)
    config._set_prefix(field=field, prefix=prefix, group=group, merge_group=merge_group)

    # For simplicity's sake, assumes argument == attribution (see above)
    for mapping in config.mappings:
        _mapping = mapping.as_dict()
        _prefix = conversions[field](prefix)
        _attribute = conversions[field](mapping.attribute)

        if group is not None:
            _group = [group] if isinstance(group, str) else group
            _group = [conversions[field](g) for g in _group]

            if mapping.group == _group:
                if merge_group is True:
                    assert _mapping[_field] == _separator.join(
                        [_prefix, *_group, _attribute]
                    )
                else:
                    assert _mapping[_field] == _separator.join(
                        [_prefix, _attribute]
                    )
            else:
                assert _mapping[_field] == _attribute
        else:
            assert _mapping[_field] == _separator.join([_prefix, _attribute])
