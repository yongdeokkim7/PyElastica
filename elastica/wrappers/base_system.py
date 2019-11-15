"""
base_system
-----------

basic coordinating multiple, smaller systems that have an independently integrable
interface (ie. works with symplectic or explicit routines `timestepper.py`.)
"""
from collections.abc import MutableSequence

from elastica.rod.cosserat_rod import RodBase


class BaseSystemCollection(MutableSequence):
    """
    Base System

    Technical note : We can directly subclass a list for the
    most part, but this is a bad idea, as List is non abstract
    https://stackoverflow.com/q/3945940
    """

    def __init__(self):
        # We need to initialize our mixin classes
        super(BaseSystemCollection, self).__init__()
        # List of system types/bases that are allowed
        self.allowed_sys_types = (RodBase,)
        # List of systems to be integrated
        self._systems = []

    def _check_type(self, sys_to_be_added):
        if not issubclass(sys_to_be_added.__class__, self.allowed_sys_types):
            raise TypeError(
                "{0}\n"
                "is not a system passing validity\n"
                "checks, that can be added into BaseSystem. If you are sure that\n"
                "{0}\n"
                "satisfies all criteria for being a system, please add\n"
                "it using BaseSystem.extend_allowed_types.\n"
                "The allowed types are\n"
                "{1}".format(sys_to_be_added.__class__, self.allowed_sys_types)
            )
        return True

    def __len__(self):
        return len(self._systems)

    def __getitem__(self, idx):
        return self._systems[idx]

    def __delitem__(self, idx):
        del self._systems[idx]

    def __setitem__(self, idx, system):
        self._check_type(system)
        self._systems[idx] = system

    def insert(self, idx, system):
        self._check_type(system)
        self._systems.insert(idx, system)

    def __str__(self):
        return str(self._systems)

    def extend_allowed_types(self, additional_types):
        self.allowed_sys_types += additional_types

    def override_allowed_types(self, allowed_types):
        self.allowed_sys_types = allowed_types

    def _get_sys_idx_if_valid(self, sys_to_be_added):
        from numpy import int_ as npint

        n_systems = len(self._systems)  # Total number of systems from mixed-in class

        if isinstance(sys_to_be_added, (int, npint)):
            # 1. If they are indices themselves, check range
            assert (
                -n_systems <= sys_to_be_added < n_systems
            ), "Rod index {} exceeds number of registered rodtems".format(
                sys_to_be_added
            )
            sys_idx = sys_to_be_added
        elif self._check_type(sys_to_be_added):
            # 2. If they are rod objects (most likely), lookup indices
            # index might have some problems : https://stackoverflow.com/a/176921
            try:
                sys_idx = self._systems.index(sys_to_be_added)
            except ValueError:
                raise ValueError(
                    "Rod {} was not found, did you append it to the system?".format(
                        sys_to_be_added
                    )
                )

        return sys_idx

    def synchronize(self, time):
        pass
