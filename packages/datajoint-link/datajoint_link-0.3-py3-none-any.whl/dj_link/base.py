"""Contains basic code useful for most classes."""
from inspect import signature


class Base:  # pylint: disable=too-few-public-methods
    """Mixin used to add a basic __repr__ method to other classes."""

    def __repr__(self) -> str:
        """Return a string representation of the instance.

        The representation is constructed from the names and values of all instance attributes whose names are also the
        names of parameters in the __init__ method of the class.
        """
        init_params = signature(self.__class__.__init__).parameters
        valid_attrs = {name: value for name, value in self.__dict__.items() if name in init_params}
        attrs_representation = ", ".join(name + "=" + repr(value) for name, value in valid_attrs.items())
        return self.__class__.__name__ + "(" + attrs_representation + ")"
