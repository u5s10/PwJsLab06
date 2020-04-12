#!/usr/bin/python
import argparse
import stat
import os
import pwd
import datetime


def lsmode(perm, isdir):
    output = ""
    output += "d" if isdir else "-"

    if perm == "0":
        return output + "---" * 3

    binls = "".join([format(int(a), "03b") for a in str(perm)])
    pattern = "rwx" * 3
    ls = [j if i == "1" else "-" for i, j in zip(binls, pattern)]
    return output + "".join(ls)


parser = argparse.ArgumentParser()
parser.add_argument(
    "directory", help="list content of the directory", nargs="?", default="./"
)
parser.add_argument("-l", help="show long list of results", action="store_true")
parser.add_argument("-L", help="show name of the file owner", action="store_true")
args = parser.parse_args()
path = args.directory if args.directory else "./"
lflag = args.l
Lflag = args.L

arr = os.listdir(path)
for file in sorted(arr):
    if file[0] == ".":
        continue
    filepath = os.path.join(path, file)
    statinfo = os.stat(filepath)
    owner = pwd.getpwuid(statinfo.st_uid).pw_name
    size = statinfo.st_size
    mtime = datetime.datetime.fromtimestamp(statinfo.st_mtime).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    isdir = stat.S_ISDIR(statinfo.st_mode)
    permissions = oct(statinfo.st_mode & 0o777)[2:]
    lsstyle = lsmode(permissions, isdir)
    if lflag and Lflag:
        print(f"{file:<30}{size:<10}{mtime:<20}{lsstyle:<11}{owner:<15}")
    elif lflag and not Lflag:
        print(f"{file:<30}{size:<10}{mtime:<20}{lsstyle:<11}")
    elif not lflag and Lflag:
        print(f"{file:<30}{owner:<15}")
    else:
        print(f"{file:<30}")
