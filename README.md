Chromagnon is a set of small tools dedicated to _Chrome_/_Chromium_ forensic.

## Tools
* `chromagnonHistory.py` parses **Chrome History** file
* `chromagnonCache.py` parses **Cache_Data** directory
* `chromagnonVisitedLinks.py` can verify if urls are in Chrome's **Visited Links** file
* `chromagnonDownload.py` parses **History** file for downloads
    * This requires a path to the user's History file "C:\Users\%user%\AppData\Local\Google\Chrome\User Data\Default\History"

##Files for analysis are located as follows
* User's Hisotry file "C:\Users\%user%\AppData\Local\Google\Chrome\User Data\Default\History"
* The Visited Links file "C:\Users\%user%\AppData\Local\Google\Chrome\User Data\Default\Visited Links"
* 
## Requirements (tbd)
* Python 2.7
* Updates to Python 3 in progress - Squiblydoo

## Remarks
* Most of the code is Endianness dependant and tested only on little endian hosts
* The code is alignment dependant. If Chrome was compiled with custom alignment flags, it probably won't work.

## Work In Progress
I am working on reverse engineering SSNS file format : [see this page](https://github.com/JRBANCEL/Chromagnon/wiki/Reverse-Engineering-SSNS-Format) for details.

## Tests
Following cases have been tested with success
From main fork:
* Chromagnon on FreeBSD 9.0 amd64 parsing file from Windows 7 64bits (Chrome 20)
* Chromagnon on FreeBSD 9.0 amd64 parsing file from Linux Mint 12 amd64 (Chrome 18)
* Chromagnon on FreeBSD 9.0 amd64 parsing file from FreeBSD 9.0 amd64 (Chrome 15)
* Chromagnon on Arch Linux x86_64 parsing file from Arch Linux x86_64 (Chrome 20)

From new testing:
* ChromagnonHistory on Windows 10 amd64 parsing history file from Windows 10 64 bit (Chrome Build 107)

Help is welcome to test Chromagnon on other plateforms.

## License
The code is released under **New BSD License** or **Modified BSD License**. See LICENSE file for details.
