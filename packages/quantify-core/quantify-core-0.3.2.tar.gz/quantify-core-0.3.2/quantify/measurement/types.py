# -----------------------------------------------------------------------------
# Description:    Module containing the core types for use with the MeasurementControl.
# Repository:     https://gitlab.com/quantify-os/quantify-core
# Copyright (C) Qblox BV & Orange Quantum Systems Holding BV (2020-2021)
# -----------------------------------------------------------------------------
from jsonschema import Draft7Validator
from jsonschema.validators import extend
from quantify.utilities.general import load_json_schema


class Settable:
    """
    Defines the Settable concept, which is considered complete if the given type satisfies the following:
    This class does not wrap the passed in object but simply verifies and returns it.

    .. jsonschema:: schemas/Settable.json#/attrs
    .. jsonschema:: schemas/Settable.json#/methods
    """

    __slots__ = ()  # avoid unnecessary overheads
    schema = load_json_schema(__file__, "Settable.json")

    def __new__(cls, obj):
        return _validade_schema(cls, obj)


class Gettable:
    """
    Defines the Gettable concept, which is considered complete if the given type satisfies the following:
    This class does not wrap the passed in object but simply verifies and returns it.

    .. jsonschema:: schemas/Gettable.json#/attrs
    .. jsonschema:: schemas/Gettable.json#/methods
    """

    __slots__ = ()  # avoid unnecessary overheads
    schema = load_json_schema(__file__, "Gettable.json")

    def __new__(cls, obj):
        return _validade_schema(cls, obj)


def _validade_schema(cls, obj):
    for attr_type in ("attrs", "methods"):
        attr_names = cls.schema[attr_type]["properties"].keys()
        validator.validate(
            # Only the relevant keys are selected, this is to avoid evaluating other
            # attributes that have been potentially added with an @property decorator.
            # We use `dir()` to avoid undesired evaluations as well.
            # `vars()` cannot be used because some attributes might have been injected
            # using the @property decorator and will not show up.
            # `callable()` cannot be used to find methods because it will evaluate
            # attributes that have been injected with @property decorator.
            {attr: getattr(obj, attr) for attr in dir(obj) if attr in attr_names},
            cls.schema[attr_type],
        )
    return obj


def is_object_or_function(checker, instance):
    return Draft7Validator.TYPE_CHECKER.is_type(instance, "object") or callable(
        instance
    )


type_checker = Draft7Validator.TYPE_CHECKER.redefine("object", is_object_or_function)
ObjectValidator = extend(Draft7Validator, type_checker=type_checker)
validator = ObjectValidator(schema={"type": "number"})


def is_batched(obj) -> bool:
    """
    Returns
    -------
        the `.batched` attribute of the settable/gettable `obj`, `False` if not present.
    """
    return getattr(obj, "batched", False)
