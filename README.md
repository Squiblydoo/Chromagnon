Chromagnon is a set of small tools dedicated to _Chrome_/_Chromium_ forensic.

## Tools
* `chromagnonHistory.py` parses **Chrome History** file ... [learn more](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonHistory-=-chromagnonHistory.py)
* `chromagnonCache.py` parses **Cache_Data** directory ... [learn more](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonCache-=-chromagnonCache.py)
* `chromagnonVisitedLinks.py` can verify if urls are in Chrome's **Visited Links** file ... [learn more](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonVisitedLinks-=-chromagnonVisitedLinks.py)
* `chromagnonDownload.py` parses **History** file for downloads ... [learn more](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonDownload-=-chromagnonDownload.py)
* `chromagnonSession.py` parses **Session_...** files 
* `chromagnonTab.py` parses **Tab_...** files

## Files for analysis are located as follows
* User's **Hisotry** file is located at "C:\Users\\%user%\AppData\Local\Google\Chrome\User Data\Default\History"
* **Visited Links** file is located at "C:\Users\\%user%\AppData\Local\Google\Chrome\User Data\Default\Visited Links"
* **Cache_Data** directory is located at "C:\Users\\%user%\AppData\Local\Google\Chrome\User Data\Default\Cache\Cache_Data"
* **Session...** files are located at "C:\Users\\%user%\AppData\Local\Google\Chrome\User Data\Default\Sessions\"
* **Tab...** files are located at "C:\Users\\%user%\AppData\Local\Google\Chrome\User Data\Default\Sessions\"

## Requirements 
* Updates to Python 3 in progress - Squiblydoo

## Remarks from original project - I don't know if they are true or not
* Most of the code is Endianness dependant and tested only on little endian hosts
* The code is alignment dependant. If Chrome was compiled with custom alignment flags, it probably won't work.

## Work In Progress
The original creator was working on reverse engineering SSNS file format : [see this page](https://github.com/JRBANCEL/Chromagnon/wiki/Reverse-Engineering-SSNS-Format) for details. Will this fork include SSNS file parsing? Who knows! I hope it will at some point.

I (Squiblydoo) am testing each of the tools and am testing the functionality of each. There are currently some issues with chromagnonCache and chromagnonVisitedLinks: chromagnonCache can print the cache to file, but it currently has issues when the user attempts to search for one url within the cache. The issue may be due to "SuperFastHash" with some of my band-aid fixes or it may be due to changes made by Chrome in the last 10 years. 

## Tests
Scripts are in the process of being updated and tested.
* The Scripts appear to be working happily on Win 10, Mac OS; modern Chrome Browsers and MS Edge. More testing to be done.

Help is welcome to test Chromagnon on other plateforms.

## License
The code is released under **New BSD License** or **Modified BSD License**. See LICENSE file for details.
