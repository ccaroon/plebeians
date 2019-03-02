import os.path
import re

from ftplib import FTP

class Publisher:
    def __init__(self, args):
        host = args.get('host')
        user = args.get('username')
        passwd = args.get('password')

        self.__ftp = FTP(host, user, passwd)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__ftp.quit()

    def file(self, local_file, remote_file, **kwargs):
        is_bin = kwargs.get('binmode', self.is_binary(local_file))

        if not os.path.exists(local_file):
            raise Exception("Local file does not exist: '%s" % (local_file))

        cmd = 'STOR %s' % (remote_file)
        if is_bin:
            self.__ftp.storbinary(cmd, open(local_file, "rb"))
        else:
            self.__ftp.storlines(cmd, open(local_file, "rb"))

    # -------------------------------------------------------------
    # local_path: Publish all files in this directory
    # remote_path: Remote base path to publish files to
    # ignore_paths: list of paths to ignore relative to local_path
    def directory(self, local_path, remote_path, ignore_paths=[]):
        count = 0
        for root, dirs, files in os.walk(local_path):
            # Skip ignored paths
            skip = False
            for ipath in ignore_paths:
                full_ignore_path = os.path.join(local_path, ipath)
                if root.startswith(full_ignore_path):
                    skip = True
                    break

            if skip:
                continue

            for fname in files:
                local_file = os.path.join(root, fname)
                remote_file = local_file.replace(local_path, remote_path)

                count += 1
                print("%03d - %s" % (count, remote_file))

                self.file(local_file, remote_file, binmode=True)

        return (count)

    def is_binary(self, file):
        is_bin = False

        with open(file, 'rb') as fh:
            bytes = fh.read(1024)
            is_bin = bool(bytes.translate(None, bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})))

        return is_bin
