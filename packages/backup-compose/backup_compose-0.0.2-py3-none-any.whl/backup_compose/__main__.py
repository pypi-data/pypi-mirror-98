from .backup import backup
from .restore import restore

if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('action', type=str, choices=['backup', 'restore'])
    p.add_argument('file', type=str)

    args = p.parse_args()
    if args.action == 'backup':
        backup(args.file)
    if args.action == 'restore':
        restore(args.file)
