import pyudev


def devices_by_subsystem(subsys, only=lambda x: x):
    """ Iterator that yields devices that belong to specified subsystem

    This iterator yields ``pyudev.Device`` objects.

    Example::

        >>> get_devices_by_subsystem('net')
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
