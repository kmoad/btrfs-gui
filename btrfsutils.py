import btrfs
import logging
from pathlib import Path

logger = logging.getLogger('btrfs-gui-server')

def subvolumes_inside(fs, parent_tree):
    min_key = btrfs.ctree.Key(parent_tree, btrfs.ctree.ROOT_REF_KEY, 0)
    max_key = btrfs.ctree.Key(parent_tree, btrfs.ctree.ROOT_REF_KEY + 1, 0) - 1
    for header, data in btrfs.ioctl.search_v2(fs.fd, 1, min_key, max_key):
        ref = btrfs.ctree.RootRef(header, data)
        path = (btrfs.ioctl.ino_lookup(fs.fd, ref.parent_tree, ref.dirid).name_bytes +
                ref.name).decode()
        yield ref.tree, path


def print_subvolumes_inside(fs, parent_tree, parent_path):
    for tree, path in subvolumes_inside(fs, parent_tree):
        sub_path = "{}/{}".format(parent_path, path)
        print("ID {} parent {} path {}".format(tree, parent_tree, sub_path))
        print_subvolumes_inside(fs, tree, sub_path)

class BtrfsUtils(object):
    
    def __init__(self, *args, **kwargs):
        pass

    def get_mounts(self):
        mounts = []
        with open('/proc/mounts') as f:
            for l in f:
                toks = l.strip().split()
                device, mountpoint, vfstype, mntops = toks[:4]
                if vfstype == 'btrfs':
                    mounts.append(mountpoint)
        return mounts

    def get_filesystem(self, mountpoint):
        return btrfs.FileSystem(mountpoint)
    
    def iter_sv(self, fs):
        parent_tree = 5
        min_key = btrfs.ctree.Key(parent_tree, btrfs.ctree.ROOT_REF_KEY, 0)
        max_key = btrfs.ctree.Key(parent_tree, btrfs.ctree.ROOT_REF_KEY + 1, 0) - 1
        for ref in fs.search(btrfs.ctree.ROOT_TREE_OBJECTID, min_key, max_key):
            yield Subvolume(fs, ref)

class Subvolume(object):
    def __init__(self, fs, ref):
        self.fs = fs
        self.ref = ref
        parent = btrfs.ioctl.ino_lookup(self.fs.fd, self.ref.parent_tree, self.ref.dirid).name_bytes.decode()
        self.path = Path(fs.path)/Path(parent)/Path(self.ref.name.decode())