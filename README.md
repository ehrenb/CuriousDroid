CuriousDroid
============

Useful scripts and tools that extract data from Android devices for later static analysis.

*  extract\_all\_apk.py
  *  extract all APK files that are installed on the device (even system apps) into the current working directory (or specifcy a destination dir)
    *  usage (output into cwd): python extract\_all\_apk.py 
    *  usage (output into specified dir): python extract\_all\_apk.py \<dst\_dir\>

*  decompile\_all\_apk.py
  *  run 'apktool d' on all files in a directory
  *  usage (output into cwd): python decompile\_all\_apk.py \<src\_dir\>
  *  usage (output into specified dir): python decompile\_all\_apk.py \<src\_dir\> \<dst\_dir\>

* parse_manifest.py
  *  parse each directory within a directory (src_dir) for an androidmanifest.xml file, and parse interesting strings, and generate a report
  *  usage (output report into cwd): python parse\_manifest.py <src_dir>
  *  usage (output report into specified dir): python parse\_manifest.py \<src\_dir\> \<dst\_dir\>

*  adb.py
  *  a module for interfacing with a device using ADB (Android Debug Bridge). functionality will be added as needed
  *  remember to set the adb path correctly in settings.py  


*  settings.py
  *  settings that may vary depending on the machine, such as paths to binaries.  note to self: avoid keeping settings.py up to date in the 
     repo, as the values will vary