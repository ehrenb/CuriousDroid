import os
from xml.dom import minidom

import pprint

from decompile import decompile_apk

import xmltodict

"""
The goal of this class is to do some basic static parsing and structuring of APK data.  Most of the work so far
is on the AndroidManifest file.  It should do some very minimal parsing of data, APKAnalysis can be used to
make some conclusions about the data


great ref for AndroidManifest (browse this tofind out what xml fields are mandatory)
https://developer.android.com/guide/topics/manifest/manifest-intro.html


uses-sdk notes: https://developer.android.com/guide/topics/manifest/uses-sdk-element.html
May want to default minSdkVErsion to 1 if not found
May want to default targetSdkVersion to minSdkVErsion if not found

todo:
    Allow option to not decompile apk, instead specify a decompile dir


"""


def manifest_remove_symbol(d):
    """
    Convert a nested dictionary from one convention to another.
    Args:
        d (dict): dictionary (nested or not) to be converted.
        convert_function (func): function that takes the string in one convention and returns it in the other one.
    Returns:
        Dictionary with the new keys.
    SOURCE: https://stackoverflow.com/questions/11700705/python-recursively-replace-character-in-keys-of-nested-dictionary
    Replaces all @ in keys with ''
    """
    new = {}
    for k, v in d.iteritems():
        new_v = v
        if isinstance(v, dict):
            new_v = manifest_remove_symbol(v)
        elif isinstance(v, list):
            new_v = list()
            for x in v:
                new_v.append(manifest_remove_symbol(x))
        new[k.replace('@', '')] = new_v
    return new


def handleKeyError(func):
    """wraps around funcs and returns None if KeyError occurs"""
    def handle(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return None
    return handle

class APK(object):
    STAGING_DIR = ''#Dir for decompiled results to be stored temporarily
    ANDROID_MANIFEST = 'AndroidManifest.xml'
    NAMESPACES = {'http://schemas.android.com/apk/res/android': None}
    FORCE_LIST = ('activity',
                  'uses-permission',
                  'uses-feature',
                  'intent-filter',
                  'service',
                  'provider')
                  #put xml fieldnames in that we may want to iterate over, but only once in androidmanifest.xml
                  #these fields will be forcefully put into a list in _get_manifest(), so we can iterate them gracefully

    def __init__(self, apk_file):
        self.apk_file = apk_file
        self.decompile_root = decompile_apk(self.apk_file, APK.STAGING_DIR)
        self._manifest_dom = minidom.parse(os.path.join(self.decompile_root, APK.ANDROID_MANIFEST))
        #self._manifest_dom = minidom.parse('/home/branden/com.wb.headsup-1/AndroidManifest.xml') #Testing
        self.manifest = self._get_manifest()
        pprint.pprint(self.manifest)

        self.sdk_version = self._get_sdk()#this could be broken down into min/target/max
        self.package_name = self._get_package_name()
        #self.content_uris = self._get_content_uris(self.package_name)
        self.activities = self._get_activities()
        self.uses_permissions = self._get_uses_permissions()
        self.features = self._get_features()
        self.instrumentation = self._get_instrumentation()
        self.providers = self._get_providers()
        self.receivers = self._get_receivers()
        self.services = self._get_services()
        self.libraries = self._get_libraries()
        self.permissions = self._get_permissions()
        self.permissions_tree = self._get_permission_tree()
        self.permissions_group = self._get_permission_group()

        #convenience funcs:
        self.main_activity = self._get_main_activity()
        self.is_debuggable = True if self._get_debuggable() else False#without any processing, we would have None or 'true' or 'false'

    def _get_manifest(self):
        manifest_node = self._manifest_dom.getElementsByTagName('manifest')[0]
        manifest = dict(xmltodict.parse(manifest_node.toxml(), dict_constructor=dict, 
                                                               process_namespaces=True, 
                                                               namespaces=APK.NAMESPACES,
                                                               force_list=APK.FORCE_LIST))
        manifest = manifest_remove_symbol(manifest)
        return manifest

    @handleKeyError
    def _get_debuggable(self):
        return self.manifest['manifest']['application']['debuggable']

    @handleKeyError
    def _get_sdk(self):
        return self.manifest['manifest']['uses-sdk']

    @handleKeyError
    def _get_instrumentation(self):
        return self.manifest['manifest']['instrumentation']
        
    @handleKeyError
    def _get_application(self):
        return self.manifest['manifest']['application']
        
    @handleKeyError#removing this makes it work?
    def _get_activities(self):
        return self.manifest['manifest']['application']['activity']
        
    @handleKeyError
    def _get_activities_alias(self):
        return self.manifest['manifest']['application']['activity-alias']
        
    @handleKeyError
    def _get_uses_permissions(self):
        """permissions from Android OS"""
        return self.manifest['manifest']['uses-permission']
        
    @handleKeyError
    def _get_permissions(self):
        """permissions for comms w/ other apps"""
        return self.manifest['manifest']['permission']

    @handleKeyError
    def _get_permission_tree(self):
        return self.manifest['manifest']['permission-tree']

    @handleKeyError
    def _get_permission_group(self):
        return self.manifest['manifest']['permission-group']

    @handleKeyError
    def _get_features(self):
        return self.manifest['manifest']['uses-feature']
        
    @handleKeyError
    def _get_providers(self):
        return self.manifest['manifest']['application']['provider']
        
    @handleKeyError
    def _get_receivers(self):
        return self.manifest['manifest']['application']['receiver']
        
    @handleKeyError
    def _get_services(self):
        return self.manifest['manifest']['application']['service']

    @handleKeyError
    def _get_main_activity(self):
        for activity in self._get_activities():
            if 'intent-filter' in activity.keys():
                for intent_filter in activity['intent-filter']:
                    if intent_filter['action']['name'] == 'android.intent.action.MAIN':
                        return activity


    @handleKeyError
    def _get_package_name(self):
        return self.manifest['manifest']['package']
        
    @handleKeyError
    def _get_libraries(self):
        return self.manifest['manifest']['application']['uses-library']



