import os
import re

"""
The goal of this class is to take a deeper look into the structured data attributes of the APK class, 
with the inention of coming to some "analysis" conclusion

"""
class APKAnalysis(object):
    def __init__(self, APK):
        self.APK = APK

        #do some processing on APK's attributes to come to some conclusions
        self.exported_activities = self._get_exported_activities()
        self.exported_services = self._get_exported_services()
        self.exported_providers = self._get_exported_providers()

        self.content_uris = self._get_content_uris()

    def _get_exported_activities(self):
        exported_activities = []
        for activity in self.APK.activities():
            if activity['exported'] == 'true':
                exported_activities.append(activity)
        return exported_activities

    def _get_exported_services(self):
        exported_services = []
        for service in self.APK.services():
            if service['exported'] == 'true':
                exported_services.append(service)
        return exported_services

    def _get_exported_providers(self):
        exported_providers = []
        for provider in self.APK.providers():
            if provider['exported'] == 'true':
                exported_providers.append(provider)
        return exported_providers


    def _get_content_uris(self):
    """
    look through all smali dirs recursively and match files with content uri patterns
    return list of uris
    """
    content_uri_pattern = re.compile(r'content:\/\/{0}[^"]*'.format(self.APK.package_name))
    uris = []
    #find smali dirs in decompiled_apk_dir
    smali_dirs = [os.path.join(self.APK.decompile_root, subdir) for subdir in os.listdir(self.APK.decompile_root) if 'smali' in subdir]
    for smali_dir in smali_dirs:
        for root, subdirs, fnames in os.walk(smali_dir):
            for fname in fnames:
                smali_fpath = os.path.join(root, fname)
                with open(smali_fpath, 'r') as f:
                    smali_code = f.read()
                    matches = re.findall(content_uri_pattern, smali_code)
                    uris.extend(matches)
    uris = list(set(uris))#remove duplicates
    return uris