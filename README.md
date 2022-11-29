Chromagnon is a set of small tools dedicated to _Chrome_/_Chromium_ forensic.

## Tools
* `chromagnonHistory.py` parses **Chrome History** file ... [learn more](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonHistory-=-chromagnonHistory.py)
* `chromagnonCache.py` parses **Cache_Data** directory ... [learn more](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonCache-=-chromagnonCache.py)
* `chromagnonVisitedLinks.py` can verify if urls are in Chrome's **Visited Links** file ... [learn more](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonVisitedLinks-=-chromagnonVisitedLinks.py)
* `chromagnonDownload.py` parses **History** file for downloads ... [learn more](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonDownload-=-chromagnonDownload.py)
    * This requires a path to the user's History file "C:\Users\%user%\AppData\Local\Google\Chrome\User Data\Default\History"

## Files for analysis are located as follows
* User's **Hisotry** file is located at "C:\Users\%user%\AppData\Local\Google\Chrome\User Data\Default\History"
* **Visited Links** file is located at "C:\Users\%user%\AppData\Local\Google\Chrome\User Data\Default\Visited Links"
* **Cache_Data** directory is located at "C:\Users\Karol\AppData\Local\Google\Chrome\User Data\Default\Cache\Cache_Data"

## Requirements (tbd)
* Python 2.7
* Updates to Python 3 in progress - Squiblydoo

## Remarks
* Most of the code is Endianness dependant and tested only on little endian hosts
* The code is alignment dependant. If Chrome was compiled with custom alignment flags, it probably won't work.

## Work In Progress
The original creator was working on reverse engineering SSNS file format : [see this page](https://github.com/JRBANCEL/Chromagnon/wiki/Reverse-Engineering-SSNS-Format) for details. Will this fork include SSNS file parsing? Who knows! I hope it will at some point.

I (Squiblydoo) am testing each of the tools and am testing the functionality of each. There are currently some issues with chromagnonCache and chromagnonVisitedLinks. 

## Tests
Scripts are in the process of being updated and tested.
* ChromagnonHistory and ChromagnonDownload on Windows 10 amd64 parsing history file from Windows 10 64 bit (Chrome Build 107)

Help is welcome to test Chromagnon on other plateforms.

## License
The code is released under **New BSD License** or **Modified BSD License**. See LICENSE file for details.
