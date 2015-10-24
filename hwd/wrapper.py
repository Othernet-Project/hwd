import pyudev


class Wrapper:
    """ Generic wrapper class that wraps ``pyudev.Device`` class
    """

    def __init__(self, dev):
        self.name = dev.sys_name
        self._device = dev

    @property
    def device(self):
        # We always create a new context and look up the devices because they
        # may disappear or change their state between lookups.
        if not self._device:
            ctx = pyudev.Context()
            devs = ctx.list_devices(sys_name=self.name)
            try:
                self._device = list(devs)[0]
            except IndexError:
                raise ValueError(
                    'Device {} no longer present in context'.format(self.name))
        return self._device

    def refresh(self):
        self._device = None

    @property
    def system_path(self):
        return self.device.sys_path
