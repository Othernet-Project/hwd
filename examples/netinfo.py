import hwd.udev
import hwd.network


for device in hwd.udev.devices_by_subsystem('net'):
    niface = hwd.network.NetIface(device)
    print('{}:'.format(niface.name))
    print('    {}: {}'.format('IP address', niface.ipv4addr))
    print('    {}: {}'.format('IP netmask', niface.ipv4netmask))
    print('    {}: {}'.format('IPv6 address', niface.ipv6addr))
    print('    {}: {}'.format('IPv6 netmask', niface.ipv6netmask))
    print('    {}: {}'.format('MAC', niface.mac))
    print('    {}: {}'.format('Connected?',
                              'yes' if niface.is_connected else 'no'))
