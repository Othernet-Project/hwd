import pyudev


def devices_by_subsystem(subsys, only=lambda x: True):
    """
    Iterator that yields devices that belong to specified subsystem. Returned
    values are ``pydev.Device`` instances.

    The ``only`` argument can be used to further filter devices. It should be
    a function that takes a ``pyudev.Device`` object, and returns ``True`` or
    ``False`` to indicate whether device should be returned.

    Example::

        >>> devices_by_subsystem('net')
        [Device('/sys/devices/pci0000:00/0000:00:1c.3/0000:02:00.0/net/wlp2s0'),
         Device('/sys/devices/virtual/net/lo')]
    """
    ctx = pyudev.Context()
    for d in ctx.list_devices():
        if d.subsystem != subsys:
            continue
        if not only(d):
            continue
        yield d
