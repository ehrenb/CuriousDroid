import adb
from settings import apktool_executable as apktool
import os
import sys
import re
from subprocess import CalledProcessError, check_call, check_output
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
        if apk[-3:] == 'apk':
            in_path = os.path.join(src_dir, apk)
            out_path = os.path.join(dst_dir, apk)

            apktool_decompile_cmd = [apktool, 'd', in_path, '-o' , out_path]
            print apktool_decompile_cmd
            try:
                check_call(apktool_decompile_cmd)
            except CalledProcessError as e:
                print(e.returncode)

def decompile_apk(apk_src, dst_dir):
    if apk_src[-3:] == 'apk':
        out_path = os.path.join(dst_dir, apk)
        apktool_decompile_cmd = [apktool, 'd', apk_src, '-o' , out_path]
        print apktool_decompile_cmd
        try:
            check_call(apktool_decompile_cmd)
        except CalledProcessError as e:
            print(e.returncode)

def get_apk_uris(apk):
    if apk[-3:] == 'apk':
        apk_unzip_cmd = ['unzip', apk, "-d", apk[:-4]] #unzip and put into dir "flag.apk" -> "flag/"
        classes_dex_content = None
        uris = None
        try:
            check_call(apk_unzip_cmd)
            strings_cmd = ['strings', os.path.join(apk[:-4], "classes.dex")]
            output = check_output(strings_cmd)
            print output
            uris = re.findall("content://.*", output)
           # classes_dex = open(os.path.join(apk[:-3], 'classes.dex'))
            #classes_dex_content = classes_dex.read()
        except CalledProcessError as e:
            print(e.returncode)
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
