![chromagnon_512](https://user-images.githubusercontent.com/77356206/228214907-c973f2d3-c784-4ab7-a869-3f5df5afe39b.png)

Chromagnon is a set of tools dedicated to Chrome/Chromium forensics.

The tools are used with the CLI, but a GUI is being created for each tool including a combined GUI. The GUI is preferred for ease of use.

The tools are used with the CLI, but a separate branch "GUI" is being used to create GUI elements for each tool including a combined GUI.
The GUI is preferred for ease of use and will be merged into the main branch at a later date.

## Tools
* `chromagnonHistory.py` parses **Chrome History** file ... [learn more](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonHistory-=-chromagnonHistory.py)
* `chromagnonCache.py` parses **Cache_Data** directory ... [learn more](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonCache-=-chromagnonCache.py)
* `chromagnonVisitedLinks.py` can verify if urls are in Chrome's **Visited Links** file ... [learn more](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonVisitedLinks-=-chromagnonVisitedLinks.py)
* `chromagnonDownload.py` parses **History** file for downloads ... [learn more](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonDownload-=-chromagnonDownload.py)
* `chromagnonSession.py` parses **Session_...** files 
* `chromagnonTab.py` parses **Tab_...** files

## How to Use
To launch the gui, execute `python chromagnonGui.py`. Two tools are currently available:
* History and Download Viewer - This parses and produces an output of a history file. The history file can be drag and dropped into the viewer.
* Session and Tab Viewer - This parses and produces a raw output of a Chromium Session or Tab file. (Note: Work still needs to be done to ensure all session commands are accounted for and the data needs to be processed to increase its usefulness.


## Requirements 
* Python 3 - No other dependencies are needed.


## Work In Progress
The original creator was working on reverse engineering SNSS file format : [see this page](https://github.com/JRBANCEL/Chromagnon/wiki/Reverse-Engineering-SSNS-Format) for details. I (Squiblydoo) am actively reverse engineering the SNSS format and including additional support for SNSS commands in the parser and will likely provide my tools for reverse engineering the commands at a later point.

I've created a pattern for the hex editor [ImHex](https://github.com/WerWolv/ImHex) which highlights each SNSS command. My hex pattern is attached to this project: `snss.hexpat`. This is substiantially speeding up the reversing process. However, it appears not all SNSS commands are forensically interesting so some may be excluded from default output at a later time. (Update: someone pointed me to the [source code for the SNSS commands](https://source.chromium.org/chromium/chromium/src/+/main:components/sessions/core/session_service_commands.cc;l=28;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29), which should speed up this process!)
![image](https://user-images.githubusercontent.com/77356206/206008380-678d3cac-1fa2-413d-91f0-28ca3d23f9a8.png)


I (Squiblydoo) am testing each of the tools and am testing the functionality of each. 
There are currently some issues with chromagnonCache and chromagnonVisitedLinks: chromagnonCache can print the cache to file, but it currently has issues when the user attempts to search for one url within the cache. The issue may be due to "SuperFastHash" with some of my band-aid fixes or it may be due to changes made by Chrome in the last 10 years. 

### Known issue:
The Session parser currently has an issue with parsing the "CommandSetExtensionAppID". Current work-around circumvents this but I will continue to look for a solution.

## Files for analysis are located as follows
### Windows File locations
* User's **History** file is located at "C:\Users\\%user%\AppData\Local\Google\Chrome\User Data\Default\History"
* **Visited Links** file is located at "C:\Users\\%user%\AppData\Local\Google\Chrome\User Data\Default\Visited Links"
* **Cache_Data** directory is located at "C:\Users\\%user%\AppData\Local\Google\Chrome\User Data\Default\Cache\Cache_Data"
* **Session...** files are located at "C:\Users\\%user%\AppData\Local\Google\Chrome\User Data\Default\Sessions\"
* **Tab...** files are located at "C:\Users\\%user%\AppData\Local\Google\Chrome\User Data\Default\Sessions\"

### MacOS File locations
* User's **History** file is located at "/Users/%Username%/Library/Application Support/Google/Chrome/Default/History"
* **Visted Links** file is located at "/Users/%Username%/Library/Application Support/Google/Chrome/Default/Visited Links"
* **Cache_Data** directory is located at "/Users/%Username%/Library/Application Support/Google/Chrome/Default/Cache/Cache_Data"
* **Session...** files are located at "/Users/%Username%/Library/Application Support/Google/Chrome/Default/Sessions/"
* **Tab...** files are located at "/Users/%Username%/Library/Application Support/Google/Chrome/Default/Sessions/"

### Linux File locations
* User's **History** file is located at "/home/%username%/.config/google-chrome/Default/History"
* **Visited Links** file is located at "/home/%username%/.config/google-chrome/Default/Visited Links"
* **Cache_Data** directory is located at "/home/%username%/.config/google-chrome/Default/Cache/Cache_Data"
* **Session..** files are located at "/home/%username%/.config/google-chrome/Default/Sessions/"
* **Tab...** files are located at "/home/%username%/.config/google-chrome/Default/Sessions/"

## Tests
Scripts are in the process of being updated and tested.
* The Scripts appear to be working happily on Win 10, Mac OS; modern Chrome Browsers and MS Edge. More testing to be done.

Help is welcome to test Chromagnon on other plateforms.

## License
The code is released under **New BSD License** or **Modified BSD License**. See LICENSE file for details.

## References:
* [CCL-SSNS Github Repository](https://github.com/cclgroupltd/ccl-ssns)
* [Chromagnon Github Wiki](https://github.com/JRBANCEL/Chromagnon/wiki)
* [Chrome Session and Tabs Files (and the puzzle of the pickle)](https://digitalinvestigation.wordpress.com/2012/09/03/chrome-session-and-tabs-files-and-the-puzzle-of-the-pickle/#comments) - Alex Caithness, CCL Forensics 
* [chromium-snss-parse Github repository](https://github.com/instance01/chromium-snss-parse)
* [python-snss Github repository](https://github.com/deactivated/python-snss/blob/master/snss/constants.py)
* [Session Service source code](https://source.chromium.org/chromium/chromium/src/+/main:components/sessions/core/session_service_commands.cc): 
