from subprocess import CalledProcessError, check_output, call, check_call
from settings import adb_executable as adb
"""
A multipurpose module for using ADB
"""

def get_list_of_connected_devices():
    """
    Calls 'adb devices' and returns results as a list
    Returns output if good, returns No
    """
    adb_devices_cmd = [adb,'devices']
    result = None
    try:
        output = check_output(adb_devices_cmd).replace('device','').replace('\t','')
        output = output.split('\n')
        del output[0]   #remove the 'List of devices attached' message
        result = list(filter(None,output))#remove anomalous empty strings

        ##Further filtering if needed:
        # devices = []
        # for device in output:
        #   if '*' in device:
        #       continue
        #   if 'attached' in device:
        #       continue
        #   if '?' in device:
        #       continue
        #   devices.append(device.replace('\t',''))
        # print devices
    except CalledProcessError as e:
        print(e.returncode)
    return result

def pull_file(device_id, src_path, dst_dir=''):
    """adb pull a file from the device given its src
       and optionally, specify a desination path
       if no dst specified, it will go to the cwd"""
    adb_pull_cmd = [adb, '-s', device_id, 'pull', src_path]
    #append destination path to cmd if it was set 
    if dst_dir:
        print 'dst_dir detected'
        adb_pull_cmd.append(dst_dir)
    try:
        check_call(adb_pull_cmd)
    except CalledProcessError as e:
        print(e.returncode)

def get_apk_path(device_id, package):
    """given a device id and list of package
       return the corresponding apk path for the package"""
    adb_package_paths_cmd = [adb, '-s', device_id, 'shell', 'pm', 'path', package]
    path = None
    try:
        path = check_output(adb_package_paths_cmd).replace('package:','').replace('\r','').replace('\n','')
    except CalledProcessError as e:
        print(e.returncode)
    return path

def list_all_packages(device_id):
    """call adb shell pm list packages and return the result in a list"""
    adb_list_packages_cmd = [adb, '-s', device_id, 'shell', 'pm', 'list', 'packages']
    result = None
    try:
        output = check_output(adb_list_packages_cmd).replace('package:','').replace('\r','')
        output = output.split('\n')
        result = list(filter(None,output))
    except CalledProcessError as e:
        print(e.returncode)
    return result

def run_monkey(device_id, mky_parameters, mky_event_count):
    """
    Calls 'adb monkey' with mky_parameters as its parameters
    """
    adb_monkey_cmd = [adb,'-s',device_id,'shell','monkey']

    option_syntax = []
    for parameter in mky_parameters.items():
        if parameter[1][1]:
            option = parameter[1][0]
            value = parameter[1][1]
            option_syntax.append(option)
            option_syntax.append(value)

    adb_monkey_cmd.extend(option_syntax)
    adb_monkey_cmd.append(mky_event_count)

    print adb_monkey_cmd

    output = None
    try:
        output = check_output(adb_monkey_cmd)
    except CalledProcessError as e:
        print(e.returncode)

    print output
    return output

def flush_logcat(device):
    adb_flush_logcat_cmd = [adb,'-s',device,'logcat','-c']
    try:
        check_call(adb_flush_logcat_cmd)
    except CalledProcessError as e:
        print(e.returncode)

def get_logcat(device):
    adb_get_logcat_cmd = [adb,'-s',device,'logcat','-d']
    output = None
    try:
        output = check_output(adb_get_logcat_cmd)
    except CalledProcessError as e:
        print(e.returncode)
    return output


def start_server():
    """
    Calls 'adb start-server'
    """
    print 'Starting adb server'
    adb_start_cmd = [adb,'start-server']
    try:
        check_call(adb_start_cmd)
    except CalledProcessError as e:
        print (e.returncode)

def restart_server():
    """
    Calls 'adb kill-server'
    followed by 'adb start-server'
    """
    stop_server()
    start-server()

def stop_server():
    """
    Calls 'adb kill-server'
    """
    print 'Killing adb server'
    adb_stop_cmd = [adb,'kill-server']
    try:
        check_call(adb_stop_cmd)
    except CalledProcessError as e:
        print (e.returncode)

def test():
    device = get_list_of_connected_devices()[0]
    print list_all_packages(device)

if __name__ == "__main__":
    test()