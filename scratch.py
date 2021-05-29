from btrfsutils import BtrfsUtils
from collections import Counter, defaultdict

doc = lambda x: print(x.__doc__)


bu = BtrfsUtils()
fs = bu.get_filesystem('/local/rust')

usage = defaultdict(lambda: {'used':0,'total':0})
for chunk in fs.chunks():
    bg = fs.block_group(chunk.vaddr)
    usage[bg.flags_str]['used'] += bg.used
    usage[bg.flags_str]['total'] += chunk.length
print(usage)
for k,v in usage.items():
    print(k, v['used']/v['total'])
fsinfo = fs.fs_info()
print(f'Mounted at: {fs.path}')
print(f'Using {fsinfo.num_devices} devices')
for device in fs.devices():
    print(device.devid, device.bytes_used/device.total_bytes)
for space in fs.space_info():
    print(space)
for sv in bu.iter_sv(fs):
    print(sv.path)