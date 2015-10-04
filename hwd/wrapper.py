import pyudev


class Wrapper:
    """ Generic wrapper class that wraps ``pyudev.Device`` class
    """

    def __init__(self, dev):
        self.name = dev.sys_name

    @property
    def device(self):
        # We always create a new context and look up the devices because they
        # may disappear or change their state between lookups.
        ctx = pyudev.Context()
        devs = ctx.list_devices(sys_name=self.name)
        try:
            return list(devs)[0]
        except IndexError:
            raise ValueError('Device {} no longer present in context'.format(
                self.name))

    @property
    def system_path(self):
        return self.device.sys_path
