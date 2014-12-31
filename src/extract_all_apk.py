from hashlib import md5
import sys
import adb
import os
from subprocess import CalledProcessError, check_output, call, check_call
"""
Extract all APKs from a device 
"""


def extract_all_apk(device_id, package_list, dst_dir=''):
    """
    Extract all APK files associated with the package_list
    Create a report 
    """
    report_list = []
    for package in package_list:
        apk_path_on_device = adb.get_apk_path(device_id, package)
        adb.pull_file(device_id, apk_path_on_device, dst_dir) #extract file to dst_dir
        apk_file_name = parse_apk_from_path(apk_path_on_device) #parse file name
        report = {}
        result_full_path = None
        #if destination was set, then get the full path (dst_dir+apk_file_name)
        if dst_dir:
            result_full_path = os.path.join(dst_dir, apk_file_name)
        #if destination was not set, then get full path (cwd+apk_file_name)
        else:
            result_full_path = os.path.join(os.getcwd(), apk_file_name)
        print "Extracted app: {0} --> {1}".format(package, result_full_path)

        #generate a basic report
        report['file_name'] = apk_file_name
        report['path_on_device'] = apk_path_on_device
        report['md5sum'] = md5(open(result_full_path, 'rb').read()).hexdigest()
        report_list.append(report)
        
    report_file_path = os.path.join(dst_dir, 'report.txt')
    f = open(report_file_path,'w')
    for report in report_list:
        f.write(report['file_name'])
        f.write('\n\t Path on device: ')
        f.write(report['path_on_device'])
        f.write('\n\t MD5sum: ')
        f.write(report['md5sum'])
        f.write('\n')
    f.close()

def parse_apk_from_path(path):
    apk_file = path[path.rfind('/')+1:]
    return apk_file

def main():

    dst_dir = ''
    try:
        dst_dir = sys.argv[1]
        if os.path.isdir(dst_dir):
            print 'Dumping results to {0}'.format(dst_dir)
        else:
            print 'Error, directory "{0}"" does not exist'.format(dst_dir)
    except IndexError as e:
        print 'No destination dir specified, dumping to current working directory..'
        pass

    devices = adb.get_list_of_connected_devices()
    if len(devices) == 0:
        print "Error, no devices connected..exiting"
        sys.exit()

    if len(devices) > 1:
        print "Warning, multiple devices..choosing the first: {0}".format(devices[0])

    device_id = devices[0]#default to the first device found
    package_list = adb.list_all_packages(device_id)
    extract_all_apk(device_id, package_list, dst_dir)

if __name__ == "__main__":
    main()