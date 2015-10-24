import hwd.udev
import hwd.network


for device in hwd.udev.devices_by_subsystem('net'):
    niface = hwd.network.NetIface(device)
    print('{}:'.format(niface.name))
    print('    {}: {}'.format('Bus', niface.bus))
    print('    {}: {}'.format('Vendor', niface.vendor))
    print('    {}: {}'.format('Model', niface.model))
    print('    {}: {}'.format('IP address', niface.ipv4addr))
    print('    {}: {}'.format('IP netmask', niface.ipv4netmask))
    print('    {}: {}'.format('IP gateway', niface.ipv4gateway))
    print('    {}: {}'.format('IPv6 address', niface.ipv6addr))
    print('    {}: {}'.format('IPv6 netmask', niface.ipv6netmask))
    print('    {}: {}'.format('IPv6 gateway', niface.ipv6gateway))
    print('    {}: {}'.format('MAC', niface.mac))
    print('    {}: {}'.format('Connected?',
                              'yes' if niface.is_connected else 'no'))
