import os
import re

def export_flag_is_true(manifest_file):
    """
    Open manifest_file and see if the android:exported flag is true
    Return true if flag is set to true
    Return false if flag is set to false
    """
    f = open(manifest_file,'r')
    if 'android:exported="true"' in f:
        return True
    return False

def target_sdk_is_vulnerable(manifest_file):
    """
    Open manifest file and see if targetSdkVersion='x'
    where x is less than or equal to 17
    Return true if less than or equal to 17
    Return false if greater than 17
    """
    f = open(manifest_file,'r')
    if 'android:targetSdkVersion' in f:
        match = re.search('targetSdkVersion="(.*)"', f.read())
        sdk_version = int(match.group(1))
        if sdk_version <= 17:
            return True
    elif 'android:maxSdkVersion' in f:
        match = re.search('maxSdkVersion="(.*)"', f.read())
        sdk_version = int(match.group(1))
        if sdk_version <= 17:
            return True
    else:
        return False

def parse_all_manifest(src_dir):
    """
    Enumerate all directores in path dir
    and get each dirs androidmanifest.xml file and parse it
    """
    report_list = []
    for src_dir in os.listdir(src_dir):
        #only try to look into directories
        if os.path.isfile(src_dir):
            pass
        else:
            manifest_file = os.path.join(src_dir,'androidmanifest.xml')

            #initialize the report values
            report = {'path':manifest_file,
                      'exported_flag': False,
                      'sdk_version_vuln': False} 

            if export_flag_is_true(manifest_file):
                #record what was parsed, and the path of where it can be found
                report['exported_flag'] = True

            if target_sdk_is_vulnerable(manifest_file):
                report['sdk_version_vuln'] = True

        report_list.append(report)
    return report_list

def generate_report(report_list, dst_dir):
    """
    generate a report of what was parsed
    """
    now = datetime.now()
    report_file_path = os.path.join(dst_dir, 'parse_report_{0}.txt'.format(now.strftime('%Y%m%d%H%M%S')))
    f = open(report_file_path,'w')
    f.write('Timestamp: {0}\n'.format(now.strftime('%Y/%m/%d %H:%M:%S')))
    
    for report in report_list:
        f.write(report['path'])
        f.write('\n\t Parsed results:')
        f.write('\n\t\t')
        f.write('exported flag: '+report['exported_flag'])
        f.write('\n\t\t')
        f.write('targetSdkVersion vuln: '+report['sdk_version_vuln'])
    f.close()

def main():
    src_dir = sys.argv[1]
    if not os.path.isdir(src_dir):
        print 'Error, source directory "{0}" does not exist'.fomat(src_dir)
        sys.exit()

    dst_dir = ''
    try:
        dst_dir = sys.argv[2]
        if not os.path.isdir(dst_dir):
            print 'Error, destination directory "{0}" does not exist'.format(dst_dir)
            sys.exit()
    except IndexError as e:
        print 'No destination dir specified, dumping to "{0}"'.format(os.getcwd())
        pass

    report_list = parse_all_manifest(src_dir)
    generate_report(report_list, dst_dir)

if __name__ == "__main__":
    main()