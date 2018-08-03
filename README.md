# No longer maintaned

CuriousDroid
============

Useful scripts and tools that extract data from Android devices for later static analysis.

*  extract.py
  *  functions for extracting an apk from an Android device

*  decompile.py
  *  functions for wrapping 'apktool d' into functions

*  Apk.py
  *  class representing an apk once decompiled.  basic apk attributes are resolved by examining AndroidManifest.xml and smali code
  * attributes examples: activities, providers, package name, permissions...

*  ApkAnalysis.py
  *  class representing detailed static analysis of an apk.  takes in an APK object to do processing on its attributes to get to static analysis conclusions
  * attributes examples: exported activities, exported providers, content uris (parsed from smali)

*  adb.py
  *  a module for interfacing with a device using ADB (Android Debug Bridge). functionality will be added as needed
  *  remember to set the adb path correctly in settings.py  

*  settings.py
  *  settings that may vary depending on the machine, such as paths to binaries.  note to self: avoid keeping settings.py up to date in the 
     repo, as the values will vary
