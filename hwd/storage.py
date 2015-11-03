from __future__ import division

import os
from collections import namedtuple

from . import udev
from . import wrapper

SECTOR_SIZE = 512


#: namedtuple representing a single mtab entry
MtabEntry = namedtuple('MtabEntry', ['dev', 'mdir', 'fstype', 'opts', 'cfreq',
                                     'cpass'])

#: namedtuple representing filesystem usage statistics
Fstat = namedtuple('Fstat', ['total', 'used', 'free', 'pct_used', 'pct_free'])


def mounts():
    """
    Iterator yielding mount points that appear in /proc/mounts. If /proc/mounts
    is not readable or does not exist, this function raises an exception.
    """
    with open('/proc/mounts', 'r') as fd:
        for l in fd:
            yield MtabEntry(*l.strip().split())


class Partition(wrapper.Wrapper):
    """
    Wrapper for ``pyudev.Device`` objects of 'partition' type.

    As with all wrappers, this class takes ``dev`` as its first argument.  The
    optional ``disk`` argument can be passed, and is stored as the ``disk``
    property. This is mostly used by :py:class:`~hwd.storage.Disk` class to
    maintain a refrence to itself.
    """

    def __init__(self, dev, disk=None):
        self.disk = disk
        super(Partition, self).__init__(dev)

    @property
    def number(self):
        """
        Partition number. This specifies a position of the partition in the
        partition table. If the value is not known for some reason, this
        property evaluates to ``-1``.
        """
        return int(self.device.get('ID_PART_ENTRY_NUMBER', -1))

    @property
    def label(self):
        """
        Volume label. This property evaluates to ``None`` if no volume label is
        not set on a partition.
        """
        return self.device.get('ID_FS_LABEL')

    @property
    def usage(self):
        """
        Filesystem usage (purpose). In most cases this should evaluate to
        ``'filesystem'``. In some cases (e.g., swap partition), it may evaluate
        to ``'other'`` or some other value.
        """
        return self.device.get('ID_FS_USAGE')

    @property
    def uuid(self):
        """
        Filesystem UUID. Note that this is not the same as the partition UUID
        (which is not available through this wrapper, other than directly
        accessing the underlying ``pyudev.Device`` object).
        """
        return self.device.get('ID_FS_UUID')

    @property
    def scheme(self):
        """
        Partition entry scheme. This evaluates to either ``'dos'`` or
        ``'gpt'``.
        """
        return self.device.get('ID_PART_ENTRY_SCHEME')

    @property
    def part_type(self):
        """
        Partition type ID. This is expressed in hex string. Note that this is
        not the same as filesystem type which is available through the
        :py:attr:`~part_type` property.
        """
        return self.device.get('ID_PART_ENTRY_TYPE')

    @property
    def format(self):
        """
        Fiesystem type. This evaluates to any number of supported file system
        types such as ``'ext4'`` or ``'vfat'``.

        .. note::
            Extended partitions will have this property evaluate to ``None``.
        """
        return self.device.get('ID_FS_TYPE')

    @property
    def is_extended(self):
        """
        Whether partition is extended.
        """
        return self.part_type == '0x5'

    @property
    def offset(self):
        """
        Partition offset in sectors. If this information is not available for
        some reason, it evaluates to ``-1``.
        """
        return int(self.device.get('ID_PART_ENTRY_OFFSET', -1))

    @property
    def sectors(self):
        """
        Partition size in sectors. If this information is not available for
        some reason, it evaluates to ``-1``.
        """
        return int(self.device.get('ID_PART_ENTRY_SIZE', -1))

    @property
    def size(self):
        """
        Partition size in bytes. This value is obtained by multiplying the
        sector size by 512.
        """
        return self.sectors * SECTOR_SIZE

    @property
    def mount_points(self):
        """
        Iterator of partition's mount points obtained by reading /proc/mounts.
        Returns empty list if /proc/mounts is not readable or if there are no
        mount points.
        """
        aliases = self.aliases
        try:
            return [e.mdir for e in mounts() if e.dev in aliases]
        except (OSError, IOError):
            return []

    @property
    def stat(self):
        """
        Return disk usage information for the partition in :py:class:`Fstat`
        format. If disk usage information is not available, then ``None`` is
        returned. Disk usage information is only available for regular
        filesystems that are mounted.
        """
        try:
            mp = self.mount_points[0]
        except IndexError:
            return None
        stat = os.statvfs(mp)
        free = stat.f_frsize * stat.f_bavail
        total = self.size
        used = total - free
        used_pct = round(used / total * 100)
        free_pct = 100 - used_pct
        return Fstat(total, used, free, used_pct, free_pct)


class Disk(wrapper.Wrapper):
    """
    Wrapper for ``pyudev.Device`` objects of 'disk' type.
    """

    def __init__(self, dev):
        super(Disk, self).__init__(dev)
        self._partitions = None

    @property
    def partitions(self):
        """
        Iterable containing disk's partition objects. Objects in the iterable
        are :py:class:`~hwd.storage.Partition` instances.
        """
        if not self._partitions:
            self._partitions = [Partition(d, self)
                                for d in self.device.children]
        return self._partitions

    @property
    def part_table_type(self):
        """
        Partition table type. Evaluates to either ``'dos'`` or ``'gpt'``.
        """
        return self.device.get('ID_PART_TABLE_TYPE')

    @property
    def uuid(self):
        """
        Partition table UUID. Note that UUIDs for different partition table
        types have different fomats.
        """
        return self.device.get('ID_PART_TABLE_UUID')

    @property
    def sectors(self):
        """
        Disk size in sectors. If for some reason, this information is not
        available, this property evaluates to ``-1``.
        """
        return int(self.device.attributes.get('size', -1))

    @property
    def size(self):
        """
        Disk capacity in bytes. This value is obtained by multiplying sector
        size by 512.
        """
        return self.sectors * SECTOR_SIZE

    @property
    def is_read_only(self):
        """
        Whether disk is read-only. This evaluates to ``True`` if disk is
        read-only.
        """
        return self.device.attributes.get('ro') == '1'

    @property
    def is_removable(self):
        """
        Whether disk is removable. This property evaluates to ``True`` if disk
        is removable. Note that this does not mean disk is USB-attached, and
        does not necessarily match the common notion of removable devices.

        If you wish to know whether a device is USB-attached, check whether
        the value of the :py:attr:`~hwd.wrapper.Wrapper.bus` property is
        ``'usb'``.
        """
        return self.device.attributes.get('removable') == '1'
