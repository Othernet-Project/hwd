import netifaces

from . import udev
from . import wrapper


class NetIface(wrapper.Wrapper):
    """ Wraps pyudev Device object to provide extended information about NICs
    """

    @property
    def type(self):
        if self.name == 'lo':
            return 'loop'
        else:
            return self.device.device_type

    @property
    def mac(self):
        return self.device.attributes.get('address')

    @property
    def model(self):
        return self.device.get('ID_MODEL_FROM_DATABASE')

    @property
    def is_connected(self):
        return self.device.attributes.get('carrier') == '1'

    def _get_addrs(self):
        return netifaces.ifaddresses(self.name)

    def _get_ipv4_addrs(self):
        addrs = self._get_addrs()
        ipv4addrs = addrs.get(netifaces.AF_INET)
        if not ipv4addrs:
            return {}
        return ipv4addrs[0]

    def _get_ipv6addrs(self):
        addrs = self._get_addrs()
        ipv6addrs = addrs.get(netifaces.AF_INET6)
        if not ipv6addrs:
            return {}
        return ipv6addrs[0]

    @property
    def ipv4addr(self):
        return self._get_ipv4_addrs().get('addr')

    @property
    def ipv4netmask(self):
        return self._get_ipv4_addrs().get('netmask')

    @property
    def ipv6addr(self):
        return self._get_ipv6addrs().get('addr')

    @property
    def ipv6netmask(self):
        return self._get_ipv6addrs().get('netmask')
