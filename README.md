CuriousDroid
============

Useful scripts and tools that extract data from Android devices for later static analysis.

*  extract\_all\_apk.py
  *  extract all APK files that are installed on the device (even system apps) into the current working directory (or specifcy a destination dir)
    *  usage (output into cwd): python extract\_all\_apk.py 
    *  usage (output into specified dir): python extract\_all\_apk.py output_dir/

*  adb.py
  *  a module for interfacing with a device using ADB (Android Debug Bridge). functionality will be added as needed
  *  remember to set the adb path correctly in settings.py  
