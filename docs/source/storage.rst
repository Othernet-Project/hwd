Storage device wrappers
=======================

Quick example
-------------

Basic usage of storage wrappers uses the disk device type wrapped in
:py:class:`~hwd.storage.Disk` wrapper, and accessing disk and partition
information using properties on that object. All partitions are accessible
through the object's :py:attr:`~hwd.storage.Disk.partitions` attribute, so it
is not necessary to separately wrap partition objects (though there is nothing
wrong with that).

Example::

    >>> devs = list(udev.devices_by_subsystem('block'))
    >>> device = storage.Disk(devs[0])
    >>> device.bus
    u'ata'
    >>> device.size
    256060514304
    >>> device.sectors
    500118192
    >>> device.part_table_type
    u'gpt'
    >>> p1 = device.partitions[0]
    >>> p1.offset
    4097
    >>> p1.size
    314573312
    >>> p1.format
    u'vfat'

Module contents
---------------

.. automodule:: hwd.storage
   :members:

