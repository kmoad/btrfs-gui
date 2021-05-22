with open('/proc/mounts') as f:
    for l in f:
        toks = l.strip().split()
        device, mountpoint, vfstype, mntops = toks[:4]
        if vfstype == 'btrfs':
            print(device, mountpoint)
