
adb_executable = '/home/branden/android-sdks/platform-tools/adb'  #path to adb executable
apktool_executable = 'apktool'
# {key: [cmd,value]}
#set value to None if you don't want to use that option
#to enable an option, give it a value as a string
mky_parameters = {
    'seed':['-s',None],
    'throttle':['--throttle','120'],
    'pct-touch':['--pct-touch','50'],
    'pct-motion':['--pct-motion','50'],
    'pct-trackball':['--pct-trackball',None],
    'pct-nav':['--pct-nav',None],
    'pct-majornav':['--pct-majornav',None],
    'pct-syskeys':['--pct-syskeys',None],
    'pct-appswitch':['--pct-appswitch',None],
    'pct-anyevent':['--pct-anyevent',None],
    'package':['-p','com.groupme.android']
}
mky_event_count = '500' #number of events per test 
###end monkey options



###monkeyrunner options:
app_package_name = 'mic.messenger.im'
activity_to_fuzz = 'com.mim.android.ui.ChatViewer'
num_of_tests = 3 #number of tests to run

#coordinates to use for touches
touch_coords = [(977,912)]
###end monkeyrunner options




#test packages and activities:
#GroupMe:
    #package_name = com.groupme.android
    #activity_to_fuz = com.groupme.android.chat.ChatActivity
    #coord 1 (open keyboard): 473,1695
    #coord 2 (send): 969,900

#refs: 
#https://developer.android.com/tools/help/monkey.html
#https://stackoverflow.com/questions/16019290/android-monkey-test-choose-a-specific-activity <-- specify activity to fuzz

#to get a specific chat activity:
    #launch the app
    #keep an eye on the logcat
    #open the chat activity
    #what does logcat say it is?




# mky_parameters = {
#     'seed':['-s',None],  <--- generated randomly by caller
#     'throttle':['--throttle',None],   <--- delay between events in milliseconds
#     'pct-touch':['--pct-touch',None],
#     'pct-motion':['--pct-motion',None],
#     'pct-trackball':['--pct-trackball',None],
#     'pct-nav':['--pct-nav',None],
#     'pct-majornav':['--pct-majornav',None],
#     'pct-syskeys':['--pct-syskeys',None],
#     'pct-appswitch':['--pct-appswitch',None],
#     'pct-anyevent':['--pct-anyevent',None],
#     'package':['-p',None]
# }
