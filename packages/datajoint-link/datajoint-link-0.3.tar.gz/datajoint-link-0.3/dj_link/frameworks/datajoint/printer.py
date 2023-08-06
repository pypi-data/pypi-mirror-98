"""Contains code for printing to standard output."""
from ...adapters.datajoint.presenter import ViewModel
from ...base import Base


class Printer(Base):  # pylint: disable=too-few-public-methods
    """View that uses Python's built-in print function to display information."""

    def __init__(self, view_model: ViewModel) -> None:
        """Initialize the printer."""
        self.view_model = view_model

    def __call__(self) -> None:
        """Format and print the data contained in the view model."""
        field_lines = [k + ":" + str(v).rjust(self._width)[len(k) + 1 :] for k, v in self.view_model.fields.items()]
        lines = (
            ["=" * self._width, self.view_model.message.center(self._width), "-" * self._width]
            + field_lines
            + ["=" * self._width]
        )
        print("\n".join(lines))

    @property
    def _width(self) -> int:
        """Compute and return the width of the printed output."""
        if len(self.view_model.message) >= self._max_field_length:
            return len(self.view_model.message) + 2
        if (self._max_field_length - len(self.view_model.message)) % 2 != 0:
            return self._max_field_length + 1
        return self._max_field_length

    @property
    def _max_field_length(self) -> int:
        """Compute and return the length of the longest field."""
        return max(len(k + str(v)) + 2 for k, v in self.view_model.fields.items())
