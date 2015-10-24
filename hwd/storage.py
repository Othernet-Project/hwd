from . import udev
from . import wrapper


PARTITION_ID_TABLE = (

)


class Partition(wrapper.Wrapper):
    """
    Wrap pyudev Device object to provide extended information about partitions
    """

    def __init__(self, dev, disk):
        self.disk = disk
        super(Partition, self).__init__(dev)

    @property
    def number(self):
        return int(self.device.get('ID_PART_ENTRY_NUMBER', -1))

    @property
    def label(self):
        return self.device.get('ID_FS_LABEL')

    @property
    def usage(self):
        return self.device.get('ID_FS_USAGE')

    @property
    def uuid(self):
        return self.device.get('ID_FS_UUID')

    @property
    def scheme(self):
        return self.device.get('ID_PART_ENTRY_SCHEME')

    @property
    def part_id(self):
        return self.device.get('ID_PART_ENTRY_TYPE')

    @property
    def part_type(self):
        return self.device.get('ID_FS_TYPE')

    @property
    def offset(self):
        return int(self.device.get('ID_PART_ENTRY_OFFSET', -1))

    @property
    def sectors(self):
        return int(self.device.get('ID_PART_ENTRY_SIZE', -1))

    @property
    def size(self):
        return self.sectors * 512


class Disk(wrapper.Wrapper):
    """ Wrap pyudev Device object to provide extended information about disks
    """

    def __init__(self, dev):
        super(Disk, self).__init__(dev)
        self._partitions = None

    @property
    def partitions(self):
        if not self._partitions:
            self._partitions = [Partition(d, self)
                                for d in self.device.children]
        return self._partitions

    @property
    def part_table_type(self):
        return self.device.get('ID_PART_TABLE_TYPE')

    @property
    def uuid(self):
        return self.device.get('ID_PART_TABLE_UUID')
