from datetime import datetime

import os
import re
import sys

def activity_export_flag_is_true(manifest_file):
    """
    Open manifest_file and see if the android:exported flag is true
    Return true if flag is set to true
    Return false if flag is set to false
    """
    f = open(manifest_file,'r')
    manifest = f.read()
    number_of_activities = manifest.count("<activity")#number of providers in the manifest

    activities_parsed = 0
    activity_start_index = 0
    activity_end_index = 0
    #while this provider isnt exported, check the next one
    while activities_parsed < number_of_activities:
        activity_start_index = manifest.find('<activity', activity_end_index) #find start of activity, starting with manifest[activity_end_index]
        activity_end_index = manifest.find('/>', activity_start_index) #find end of activity, starting with manifest[activity_start_index]
        single_activity = manifest[activity_start_index:activity_end_index]
        if 'android:exported="true"' in single_activity:
            return True
        activities_parsed+=1
    return False

def provider_export_flag_is_true(manifest_file):
    """
    Open manifest_file and see if the android:exported flag is true
    Return true if flag is set to true
    Return false if flag is set to false
    """
    f = open(manifest_file,'r')
    manifest = f.read()
    number_of_providers = manifest.count("<provider")#number of providers in the manifest

    providers_parsed = 0
    provider_start_index = 0
    provider_end_index = 0
    #while this provider isnt exported, check the next one
    while providers_parsed < number_of_providers:
        provider_start_index = manifest.find('<provider', provider_end_index) #find start of provider, starting with manifest[provider_end_index]
        provider_end_index = manifest.find('/>', provider_start_index) #find end of provider, starting with manifest[provider_start_index]
        single_provider = manifest[provider_start_index:provider_end_index]
        if 'android:exported="true"' in single_provider:
            return True
        providers_parsed+=1
    return False

def target_sdk_is_vulnerable(manifest_file):
    """
    Open manifest file and see if targetSdkVersion='x'
    where x is less than or equal to 17
    Return true if less than or equal to 17
    Return false if greater than 17
    """
    f = open(manifest_file,'r')
    if 'android:targetSdkVersion' in f.read():
        match = re.search('targetSdkVersion="(.*)"', f.read())
        sdk_version = int(match.group(1))
        if sdk_version <= 17:
            return True
    elif 'android:maxSdkVersion' in f.read():
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
    for decompile_dir in os.listdir(src_dir):
        #only try to look into directories
        if os.path.isdir(os.path.join(src_dir, decompile_dir)):
            manifest_file = os.path.join(src_dir, decompile_dir, 'AndroidManifest.xml')
            #initialize the report values
            report = {'path':manifest_file,
                      'activity_exported_flag': False,
                      'content_provider_exported_flag': False,
                      'sdk_version_vuln': False} 

            if activity_export_flag_is_true(manifest_file):
                #record what was parsed, and the path of where it can be found
                report['activity_exported_flag'] = True

            if provider_export_flag_is_true(manifest_file):
                report['content_provider_exported_flag'] = True

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
        f.write('activity exported flag: '+ str(report['activity_exported_flag']))
        f.write('\n\t\t')
        f.write('content provider exported flag: '+ str(report['content_provider_exported_flag']))
        f.write('\n\t\t')
        f.write('targetSdkVersion vuln: '+ str(report['sdk_version_vuln']))
        f.write('\n\n')
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