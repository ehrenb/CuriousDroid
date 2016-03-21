from hashlib import md5
import sys
import adb
import os
from datetime import datetime
from subprocess import CalledProcessError, check_output, call, check_call
"""
Extract all APKs from a device
"""

"""
usage
extract_all_apk dst_dir
dst_dir defaults to cwd if not set
"""


def extract_all_apk(device_id, package_list, dst_dir=''):
    """
    Convenience func for calling extract_apk on package in package_list
    """
    report_list = []
    for package in package_list:
        report_dict = extract_apk(device_id, package, dst_dir=dst_dir)
        report_list.append(report_dict)
    return report_list

def extract_apk(device_id, package, dst_dir=''):
    """
    Extract apk with package name package to dst_dir
    if dst_dir not specified, it is cwd
    Return: dictionary with info about apk
    """
    apk_path_on_device = adb.get_apk_path(device_id, package)
    adb.pull_file(device_id, apk_path_on_device, dst_dir) #extract file to dst_dir
    apk_file_name = parse_apk_from_path(apk_path_on_device) #parse file name
    report_dict = {}
    result_full_path = None

    result_full_path = os.path.join(dst_dir, apk_file_name)

    report_dict['file_name'] = apk_file_name
    report_dict['path_on_device'] = apk_path_on_device
    report_dict['path_dst'] = result_full_path
    report_dict['md5sum'] = md5(open(result_full_path, 'rb').read()).hexdigest()
    print "Extracted app: {0} --> {1}".format(package, result_full_path)
    return report_dict

def parse_apk_from_path(path):
    """
    return last part of a path (after last '/')
    """
    apk_file = os.path.basename(path)
    return apk_file

# def generate_report(report_list, dst_dir):
#     """
#     generate a report of what was extracted
#     """
#     now = datetime.now()
#     report_file_path = os.path.join(dst_dir, 'extract_report_{0}.txt'.format(now.strftime('%Y%m%d%H%M%S')))
#     f = open(report_file_path,'w')
#     f.write('Timestamp: {0}\n'.format(now.strftime('%Y/%m/%d %H:%M:%S')))

#     for report in report_list:
#         f.write(report['file_name'])
#         f.write('\n\t Path on device: ')
#         f.write(report['path_on_device'])
#         f.write('\n\t MD5sum: ')
#         f.write(report['md5sum'])
#         f.write('\n')
#     f.close()

def main():
    adb.start_server()#start adb server
    dst_dir = ''
    #destination defaults to cwd if no dst_dir was specified
    try:
        dst_dir = sys.argv[1]
        if not os.path.isdir(dst_dir):
            print 'Error, directory "{0}" does not exist'.format(dst_dir)
            sys.exit()
    except IndexError as e:
        print 'No destination dir specified, dumping to "{0}"'.format(os.getcwd())

    devices = adb.get_list_of_connected_devices()
    if len(devices) == 0:
        print "Error, no devices connected..exiting"
        sys.exit()

    if len(devices) > 1:
        print "Warning, multiple devices..choosing the first: {0}".format(devices[0])

    device_id = devices[0]#default to the first device found
    package_list = adb.list_all_packages(device_id)
    report_list = extract_all_apk(device_id, package_list, dst_dir)
    generate_report(report_list, dst_dir)

if __name__ == "__main__":
    main()
