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
    print('    UUID:      {}'.format(disk.uuid))
    print('    Table:     {}'.format(disk.part_table_type.upper()))
    print('    Vendor:    {}'.format(disk.vendor))
    print('    Model:     {}'.format(disk.model))
    print('    Capacity:  {}'.format(humanize(disk.size)))
    print()
    for p in disk.partitions:
        if p.is_extended:
            continue
        print(' {logic}{num}: {size} {ptype} {lbl}'.format(**{
            'num': p.number,
            'logic': 'L ' if p.number > 4 else '  ',
            'lbl': p.label or '(no label)',
            'size': humanize(p.size),
            'ptype': p.format,
        }))
        print('      {}'.format(p.uuid))
        print('      mounts: {}'.format(', '.join(p.mount_points) or 'none'))
        stat = p.stat
        if stat:
            print('      usage: {} used of {} ({} free)'.format(
                humanize(stat.used), humanize(stat.total),
                humanize(stat.free)))
        else:
            print('      usage: n/a')
    print()
