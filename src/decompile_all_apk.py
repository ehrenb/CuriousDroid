import os
import re
from subprocess import CalledProcessError, check_call, check_output
import sys
import zipfile

import adb
from settings import apktool_executable as apktool
"""
Run apktool d on all APKs in src_dir
"""

"""
usage
decompile_all_apk src_dir dst_dir
src_dir required
dst_dir defaults to cwd if not set
"""

def decompile_all_apk(src_dir, dst_dir):
    """
    Calls 'apktool d' on all files in src_dir
    Outputs the results into dst_dir
    """
    files_in_src_dir = os.listdir(src_dir)
    for apk in files_in_src_dir:
        in_path = os.path.join(src_dir, apk)
        out_path = os.path.join(dst_dir, apk)
        decompile_apk(in_path, out_path)

def decompile_apk(apk, dst_dir):
    if os.path.splitext(apk) == '.apk':
        out_path = os.path.join(dst_dir, os.path.basename(apk))
        apktool_decompile_cmd = [apktool, 'd', apk, '-o' , out_path]
        print apktool_decompile_cmd
        try:
            check_call(apktool_decompile_cmd)
        except CalledProcessError as e:
            raise

def get_apk_uris(apk):
    if os.path.splitext(apk) == '.apk':
        zip = zipfile.ZipFile(apk)
        zip.extractall(os.path.basename(apk))
        uris = []]
        try:
            check_call(apk_unzip_cmd)
            strings_cmd = ['strings', os.path.join(os.path.basename(apk), "classes.dex")]
            output = check_output(strings_cmd)
            uris = re.findall("content://.*", output)
        except CalledProcessError as e:
            raise
    return uris




def main():
    src_dir = sys.argv[1]
    if not os.path.isdir(src_dir):
        print 'Error, source directory "{0}" does not exist'.fomat(src_dir)
        sys.exit()

    dst_dir = ''
    #destination defaults to cwd if no dst_dir was specified
    try:
        dst_dir = sys.argv[2]
        if not os.path.isdir(dst_dir):
            print 'Error, destination directory "{0}" does not exist'.format(dst_dir)
            sys.exit()
    except IndexError as e:
        print 'No destination dir specified, dumping to "{0}"'.format(os.getcwd())
        pass

    adb.start_server()
    decompile_all_apk(src_dir, dst_dir)

if __name__ == "__main__":
    main()
