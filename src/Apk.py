from decompile import decompile_apk
from xml.dom import minidom


class APK(object):
    STAGING_DIR = ''#Dir for decompiled results to be stored temporarily
    ANDROID_MANIFEST = 'AndroidManifest.xml'
    NS_ANDROID_URI = 'http://schemas.android.com/apk/res/android'
    def __init__(self, apk_file):
        self.apk_file = apk_file
        self.decompile_root = decompile_apk(self.apk_file, STAGING_DIR)
        self._manifest_dom = minidom.parse(os.path.join(self.decompile_root, ANDROID_MANIFEST))

        self.package_name = _get_package_name()
        self.content_uris = _get_content_uris(self.package_name)
        self.activities = _get_activities()
        self.main_activity = _get_main_activity()


    def _get_activities(self):
        nodes = self._manifest_dom.getElementsByTagName('activity')
        return [a for node.getAttribute('android:name') in nodes]

    def _get_main_activity(self):
        """ todo """

    def _get_package_name(self):
        node = dom.getElementsByTagName('manifest')[0]
        return node.getAttribute('package')

    def _get_content_uris(self):
        """
        look through all smali dirs recursively and match files with content uri patterns
        return list of uris
        """
        content_uri_pattern = re.compile(r'content:\/\/{0}[^"]*'.format(self.package_name))
        uris = []
        #find smali dirs in decompiled_apk_dir
        smali_dirs = [os.path.join(self.decompile_root, subdir) for subdir in os.listdir(self.decompile_root) if 'smali' in subdir]
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



