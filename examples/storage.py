from __future__ import print_function, division

import hwd.udev
import hwd.storage

PREFIXES = ('', 'K', 'M', 'G', 'T', 'P')


def humanize(size, order=0):
    if size < 1000 or order == 5:
        return '{}{}B'.format(round(size, 2), PREFIXES[order])
    return humanize(size / 1000, order + 1)

# Obtain block devices
disks = hwd.udev.devices_by_subsystem('block',
                                      lambda d: d.device_type == 'disk')

for d in disks:
    disk = hwd.storage.Disk(d)
    print('{} disk {}:'.format(disk.bus.upper(), disk.node))
    print('    UUID:   {}'.format(disk.uuid))
    print('    Table:  {}'.format(disk.part_table_type.upper()))
    print('    Vendor: {}'.format(disk.vendor))
    print('    Model:  {}'.format(disk.model))
    print()
    for p in disk.partitions:
        print('    {num}: {lbl} {size} {ptype} partition'.format(**{
            'num': p.number,
            'lbl': p.label or '(no label)',
            'size': humanize(p.size),
            'ptype': p.part_type
        }))
        print('       {}'.format(p.uuid))
    print()
