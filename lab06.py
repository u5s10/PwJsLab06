#!/usr/bin/python
import stat
import os
import pwd
import datetime
#    for bit in str(permn):
#        tt = int(bit)
#        out = format(tt,'03b')
#        binls += out

#    for i, j in zip(binls, pattern):
#        if i == '1':
#            output+=j
#        else:
#            output+='-'

def lsmode(perm, isdir):
    output = ""
    output += 'd' if isdir else '-'

    if perm == '0':
        return output + '---'*3
    
    binls = ''.join([format(int(a),'03b') for a in str(perm)])
    pattern = 'rwx'*3
    ls = [j if i == '1' else '-' for i, j in zip(binls,pattern)]
    return output + ''.join(ls)

path = './'
arr = os.listdir(path)
for file in sorted(arr):
    if file[0] == '.': # skip hidden files/directories
        continue
    filepath = os.path.join(path,file)
    statinfo = os.stat(filepath)
    owner = pwd.getpwuid(statinfo.st_uid).pw_name
    size = statinfo.st_size
    mtime = datetime.datetime.fromtimestamp(statinfo.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    isdir = stat.S_ISDIR(statinfo.st_mode)
    permissions = oct(statinfo.st_mode & 0o777)[2:]
    lsstyle = lsmode(permissions,isdir)
    print(f'{file} {size} {owner} {mtime} {lsstyle}')
    

