import pyudev


class Wrapper(object):
    """
    Generic wrapper class that wraps ``pyudev.Device`` instances.

    ``dev`` is a ``pyudev.Device`` instance. Device's ``sys_name`` property is
    stored as ``name`` property on the wrapper instance.

    """

    def __init__(self, dev):
        self.name = dev.sys_name
        self._device = dev

    @property
    def device(self):
        """
        The underlaying ``pyudev.Device`` instance can be accessed by using the
        ``device`` property. This propety is cached, so only one lookup is
        performed to obtain the device object. This cache is invalidated by
        :py:meth:`~refresh` method.
        """
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

    def get_attrib(self, name, default=None):
        try:
            return self.device.attributes[name]
        except KeyError:
            return default

    def refresh(self):
        """
        Clears the :py:attr:`~device` cache.

        .. note::
            This method does not cause immediate lookup of the udev context.
            Lookup is done when the :py:attr:`~device`
            property is accessed.
        """
        self._device = None

    @property
    def system_path(self):
        """
        System path of the device.
        """
        return self.device.sys_path

    @property
    def devid(self):
        """
        Two-tuple containing device's vendor ID and model ID (hex).
        """
        d = self.device
        vend_id = d.get('ID_VENDOR_ID')
        model_id = d.get('ID_MODEL_ID')
        return (vend_id, model_id)

    @property
    def model(self):
        """
        First non-empty value from the following list:

        - model name from model database
        - model name as reported by the device driver
        - model ID (hex)

        If none of the above attributes are available, evaluates to ``None``.
        """
        return self._get_first([
            'ID_MODEL_FROM_DATABASE',
            'ID_MODEL',
            'ID_MODEL_ID'])

    @property
    def vendor(self):
        """
        First non-empty value from the following list:

        - organization name (OUI) from device database
        - vendor from vendor database
        - vendor as reported by the device driver
        - vendor ID (hex)

        If none of the above attributes are available, evaluates to ``None``.
        """
        return self._get_first([
            'ID_OUI_FROM_DATABASE',
            'ID_VENDOR_FROM_DATABASE',
            'ID_VENDOR',
            'ID_VENDOR_ID'])

    @property
    def node(self):
        """
        Device node. Not all devices have a node. In case a device has no node,
        this property evaluates to ``None``.
        """
        return self.device.device_node

    @property
    def bus(self):
        """
        Device's bus. If device is not on any bus, this property evaluates to
        ``None``.
        """
        return self.device.get('ID_BUS')

    def _get_first(self, keys, default=None):
        """
        For given keys, return value for first key that isn't ``None``. If such
        a key is not found, ``default`` is returned.
        """
        d = self.device
        for k in keys:
            v = d.get(k)
            if not v is None:
                return v
        return default

    @property
    def aliases(self):
        """
        Return a list of device aliases (symlinks) that match this device. This
        list also includes the device node so it can be treated as a list of
        all filesystem objects that point to this device.
        """
        links = list(self.device.device_links)
        links.insert(0, self.node)
        return links
