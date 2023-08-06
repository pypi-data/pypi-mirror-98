"""
Internal module providing access to the inspection result of a job
"""

from contextlib import contextmanager
from typing import Any, List, Optional, Union

from ._errors import KOError, InternalError, TimeoutError, BailOutError


class Scope:
    """
    Class representing a scope of a job result
    """

    def __init__(self, name: str, hidden: bool = False, entries: List[Union['Scope', Any]] = None):
        self.name = name
        self.entries = entries or []
        self.hidden = hidden

    def add_entry(self, entry: Union['Scope', Any]):
        """
        Add a new entry to the scope

        :param entry:       the entry to add
        """
        self.entries.append(entry)

    def dump(self, indent=0):
        print(indent * " " + "Scope(")
        print(indent * " " + f"  name={self.name!r}")
        print(indent * " " + f"  hidden={self.hidden!r}")
        print(indent * " " + f"  entries=[")
        for e in self.entries:
            if isinstance(e, Scope):
                e.dump(indent=indent + 4)
            else:
                print(indent * " " + f"    {e!r}")
        print(indent * " " + f"  ]")
        print(indent * " " + ")")


_active_scope: Optional[Scope] = None


def active_scope() -> Scope:
    """
    Retrieve the current active scope

    :return:                        the scope
    """
    return _active_scope


@contextmanager
def new_scope(name: str, hidden: bool = False) -> Scope:
    """
    Create a new scope in the inspection result

    The new scope is a children of the current active scope

    :param name:                    the name of the scope
    :param hidden:                  whether or not the scope is marked as hidden
    """
    global _active_scope
    parent_scope = _active_scope

    scope = Scope(name, hidden)
    if parent_scope is not None:
        parent_scope.add_entry(scope)
    _active_scope = scope
    try:
        yield scope
    except (KOError, InternalError, AssertionError, TimeoutError) as e:
        scope.add_entry({"assertion_failure": str(e)})
        raise BailOutError  # the error was handled locally, the root scope will just need to bail out
    finally:
        _active_scope = parent_scope


@contextmanager
def new_inspection_result() -> Scope:
    """
    Create a new inspection result for the duration of a with-block

    :return:                        the inspection result
    """
    with new_scope(name="root") as root:
        yield root
