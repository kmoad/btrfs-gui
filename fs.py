import btrfs

# class FileSystem(object):
#     def __init__(self, device, mountpoint, mntops):
#         self.device = device
#         self.mountpoint = mountpoint
#         self.mntops = {}
#         for opt in mntops.split(','):
#             if '=' in opt:
#                 k, v = opt.split('=')
#                 self.mntops[k] = v
#             else:
#                 self.mntops[opt] = True

# def get_filesystems():
#     fsys = []
#     with open('/proc/mounts') as f:
#         for l in f:
#             toks = l.strip().split()
#             device, mountpoint, vfstype, mntops = toks[:4]
#             if vfstype == 'btrfs':
#                 fsys.append(FileSystem(device, mountpoint, mntops))
#     return fsys

def get_filesystems():
    fsys = []
    with open('/proc/mounts') as f:
        for l in f:
            toks = l.strip().split()
            device, mountpoint, vfstype, mntops = toks[:4]
            if vfstype == 'btrfs':
                fsys.append(btrfs.FileSystem(mountpoint))
    return fsys

if __name__ == '__main__':
    import json
    fss = get_filesystems()
    fs = fss[1]
    # print(json.dumps([fs.__dict__ for fs in fss],
    #     indent=2,
    #     sort_keys=True)
    # )
