import netifaces

from . import udev
from . import wrapper


class NetIface(wrapper.Wrapper):
    """
    Wrapper for ``pyudev.Device`` objects of 'net' subclass.
    """

    @property
    def type(self):
        """
        NIC type. Not all network devices have this value. For wireless devices
        this value is ``'wlan'``, and for loopback devices, the value is
        ``'loop'``. When the value is missing, ``'eth'`` is returned as most
        ethernet devices authors have encountered have this value missing.
        """
        if self.name == 'lo':
            return 'loop'
        elif self.name is None:
            return 'eth'
        else:
            return self.device.device_type

    @property
    def mac(self):
        """
        NIC's MAC address.
        """
        return self.device.attributes.get('address')

    @property
    def is_connected(self):
        """
        Whether there is carrier.
        """
        return self.device.attributes.get('carrier') == '1'

    def _get_addrs(self):
        """
        Returns all addresses associated with this NIC.
        """
        return netifaces.ifaddresses(self.name)

    def _get_ipv4_addrs(self):
        """
        Returns the IPv4 addresses associated with this NIC. If no IPv4
        addresses are used, then empty dictionary is returned.
        """
        addrs = self._get_addrs()
        ipv4addrs = addrs.get(netifaces.AF_INET)
        if not ipv4addrs:
            return {}
        return ipv4addrs[0]

    def _get_ipv6addrs(self):
        """
        Returns the IPv6 addresses associated with this NIC. If no IPv6
        addresses are used, empty dict is returned.
        """
        addrs = self._get_addrs()
        ipv6addrs = addrs.get(netifaces.AF_INET6)
        if not ipv6addrs:
            return {}
        return ipv6addrs[0]

    def _get_default_gateway(self, ip=4):
        """
        Returns the default gateway for given IP version. The ``ip`` argument
        is used to specify the IP version, and can be either 4 or 6.
        """
        net_type = netifaces.AF_INET if ip == 4 else netifaces.AF_INET6
        gw = netifaces.gateways()['default'].get(net_type, (None, None))
        if gw[1] == self.name:
            return gw[0]

    @property
    def ipv4addr(self):
        """
        IPv4 address.
        """
        return self._get_ipv4_addrs().get('addr')

    @property
    def ipv4netmask(self):
        """
        IPv4 netmask.
        """
        return self._get_ipv4_addrs().get('netmask')

    @property
    def ipv4gateway(self):
        """
        IPv4 default gateway.
        """
        return self._get_default_gateway(4)

    @property
    def ipv6addr(self):
        """
        IPv6 address.
        """
        return self._get_ipv6addrs().get('addr')

    @property
    def ipv6netmask(self):
        """
        IPv6 netmask.
        """
        return self._get_ipv6addrs().get('netmask')

    @property
    def ipv6gateway(self):
        """
        IPv6 default gateway.
        """
        return self._get_default_gateway(6)
