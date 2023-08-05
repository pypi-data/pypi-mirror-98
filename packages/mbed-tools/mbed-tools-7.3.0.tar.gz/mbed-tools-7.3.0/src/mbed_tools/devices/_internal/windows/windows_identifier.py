#
# Copyright (c) 2020-2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Defines a Windows identifier."""
from functools import total_ordering
from typing import Any, Optional

from mbed_tools.devices._internal.windows.component_descriptor_utils import is_undefined_value

INSTANCE_ID_CHARACTER = "&"


def is_device_instance_id(value: Optional[str]) -> bool:
    """Determines whether a value is a device instance ID generated by Windows or not.

    See https://docs.microsoft.com/it-it/windows-hardware/drivers/install/instance-ids
    Typical IDs generated by Windows for a same device (but different interfaces) are, as follows:
        - 8&2F125EC6&0&0003
        - 8&2f125ec6&0
        - 8&2F125EC6&0&0002
    """
    return is_undefined_value(value) or INSTANCE_ID_CHARACTER in str(value)


@total_ordering
class WindowsUID:
    """Definition of a Windows Universal ID.

    UID in Windows can be either a serial number or an device instance ID depending
    on how underlying interfaces were defined.
    This object tries to hide the complexity of deciding which of the fields should be
    considered as the UID and defining
    equality between UIDs.
    Indeed different components referring to a same device may have completely different UIDs :
    e.g. 8&2F125EC6&0&0002, 8&2F125EC6&0&0003, 8&2f125ec6&0 and 345240562
    may all refer to the same component.
    """

    uid: str  # Processed string which may be the closest to the Universal ID.
    # This could be for the same device:
    # - 345240562
    # - 8&2F125EC6&0
    # - 8&2F125EC6
    # - 8&2f125ec6
    raw_uid: str  # The String from which the UID was derived.
    # Raw form, as it can be a combination of other elements
    # e.g.  8&2F125EC6&0&0003. In this case, the 0003 suffix corresponds to the MI value
    # and has nothing to do with the instance ID per se.
    serial_number: Optional[str]  # a serial number.

    # A string which can be the serial number of the device defined by
    # the underlying bus which may uniquely define the device.
    # e.g. 345240562. However, for some devices,
    # the serial number may not be accessible or defined or may actually be an instance ID.

    def __init__(self, uid: str, raw_uid: str, serial_number: Optional[str]) -> None:
        """Initialiser."""
        self.uid = uid
        self.raw_uid = raw_uid
        self.serial_number = serial_number

    def __eq__(self, other: Any) -> bool:
        """Defines the equality checker.

        The `equal` method does not follow a typical data model equal logic
        because of the complexity of this class which tries to find out which of its
        components is actually relevant and hence matters in determining equality.
        e.g.
        (uid="8&2f125ec6&0", raw_uid="8&2F125EC6&0&0003",serial_number="123456789")
        is the same as (uid="123456789", raw_uid="123456789",serial_number="8&2f125ec6")
        or (uid="8&2f125ec6&0", raw_uid="8&2F125EC6&0&000",serial_number=None)
        """
        if not other or not isinstance(other, WindowsUID):
            return False
        if (
            self.uid == other.uid
            or self.raw_uid == other.raw_uid
            or self.serial_number == other.serial_number
            or self.serial_number == other.uid
            or self.uid == other.serial_number
        ):
            return True
        # Due to the complexity of determining the UID on Windows,
        # we can assume that we are dealing with the same ID if IDs are subsets of each other.
        return str(self.uid).startswith(str(other.uid)) or str(other.uid).startswith(str(self.uid))

    @property
    def presumed_serial_number(self) -> str:
        """Determines what may be the most likely value for the serial number of the component.

        From the different components at its disposal, the system tries to find what may be the serial number.
        """
        if not is_device_instance_id(self.uid):
            # the UID is not an instance ID and should therefore be the serial number.
            return self.uid
        return self.uid if is_device_instance_id(self.serial_number) else str(self.serial_number)

    @property
    def instance_id(self) -> str:
        """Determines what may be the value most likely to be the instance_id of a component as generated by Windows."""
        if is_device_instance_id(self.uid):
            return self.uid
        return self.uid if is_undefined_value(self.serial_number) else str(self.serial_number)

    def contains_genuine_serial_number(self) -> bool:
        """Contains a genuine serial number and not an instance ID."""
        serial_number = self.presumed_serial_number
        return not (is_undefined_value(serial_number) or is_device_instance_id(serial_number))

    def __hash__(self) -> int:
        """Calculates the hash of the UID.

        Due to the complexity of the `equal` method, this implementation of the `hash`
        calculation breaks the hashing/equality rules of typical data objects.
        In the present case, the WindowsUID is mostly used for dictionary lookup and therefore,
        the actual use cases were tested.
        In most cases, the instance ID of a device will be provided rather than the serial number and therefore,
        this field will be considered as differentiators between UIDs.
        """
        return hash(self.instance_id)

    def __repr__(self) -> str:
        """String representation of the UID."""
        return f"WindowsUID({self.uid})"

    def __str__(self) -> str:
        """String representation of the UID."""
        elements = [f"{k}={v!r}" for (k, v) in self.__dict__.items()]
        return f"WindowsUID({', '.join(elements)})"

    def __lt__(self, other: "WindowsUID") -> bool:
        """Defines less than."""
        return self.presumed_serial_number < other.presumed_serial_number
