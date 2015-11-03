Base wrapper class
==================

Basic usage
-----------

:py:class:`~hwd.wrapper.Wrapper` class provides access to common basic
information about all device types.

Example::

    >>> devs = list(udev.devices_by_subsystem('net'))
    >>> device = wrapper.Wrapper(devs[0])
    >>> device.bus
    u'pci'
    >>> device.model
    u'Wireless 7260 (Dual Band Wireless-AC 7260)'
    >>> device.name
    u'wlp2s0'
    >>> device.vendor
    u'Intel Corporate'
    >>> device.system_path
    u'/sys/devices/pci0000:00/0000:00:1c.3/0000:02:00.0/net/wlp2s0'
    >>> device.devid
    (u'0x8086', u'0x08b1')

Module contents
---------------

.. automodule:: hwd.wrapper
   :members:

