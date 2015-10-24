import pyudev


class Wrapper(object):
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

    @property
    def devid(self):
        d = self.device
        vend_id = d.get('ID_VENDOR_ID')
        model_id = d.get('ID_MODEL_ID')
        return (vend_id, model_id)

    @property
    def model(self):
        return self.get_first([
            'ID_MODEL_FROM_DATABASE',
            'ID_MODEL',
            'ID_MODEL_ID'])

    @property
    def vendor(self):
        return self.get_first([
            'ID_OUI_FROM_DATABASE',
            'ID_VENDOR_FROM_DATAASE',
            'ID_VENDOR',
            'ID_VENDOR_ID'])

    @property
    def node(self):
        return self.device.device_node

    @property
    def bus(self):
        return self.device.get('ID_BUS')

    def get_first(self, keys, default=None):
        """ For given keys, return value for first key that isn't none """
        d = self.device
        for k in keys:
            v = d.get(k)
            if v:
                return v
        return default
