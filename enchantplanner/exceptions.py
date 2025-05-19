class InvalidTarget(Exception):
    """Raised when a merge is attempted onto a non-book from a book slot."""


class MergeTooExpensive(Exception):
    """Raised when computed anvil cost would exceed the 39-level limit."""


class IncompatibleSelected(Exception):
    """Raised when two incompatible enchants end up together."""
