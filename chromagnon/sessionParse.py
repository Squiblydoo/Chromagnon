#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012, Jean-Rémy Bancel <jean-remy.bancel@telecom-paristech.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Chromagon Project nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Jean-Rémy Bancel BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This module parses SNSS session commands used to store session states in chrome
"""

import datetime
import struct
from io import StringIO
from io import BytesIO
import sys

import chromagnon.pickle as pickle
import chromagnon.types as types

# Not all command types are accounted for.
# I have encountered 19, 21, 23, 32
# Presumably some of the numbers between those need accounted for too.
# Some commands were implemented multiple times. The unused versions are being kept
# for historical purposes and for completeness.

TYPE_DICT = {'0': "CommandSetTabWindow",
             '2': "CommandSetTabIndexInWindow",
             '3': "CommandTabClosed", # It appears this was replaced by Command 16
             '4': "CommandWindowClosed", # It appears this was replaced by Command 17
             '5': "CommandTabNavigationPathPrunedFromBack",
             '6': "CommandUpdateTabNavigation",
             '7': "CommandSetSelectedNavigationIndex",
             '8': "CommandSetSelectedTabInIndex",
             '9': "CommandSetWindowType",
             '11': "CommandTabNavigationPathPrunedFromFront",
             '12': "CommandSetPinnedState",
             '13': "CommandSetExtensionAppID",
             '14': "CommandSetWindowBounds3",
             '16': "CommandTabClosed",
             '17': "CommandWindowClosed",
             '21': "CommandLastActiveTime",
             '33': "CommandSideSearch"}

WINDOW_SHOW_STATE = {
    0 : 'default',
    1 : 'normal',
    2 : 'minimized',
    3 : 'maximized',
    4 : 'inactive',
    5 : 'fullscreen',
    6 : 'end'
}


def parse(commandList):
    """
    Given a list of SNSS command, it returns a list of SessionCommand
    """
    output = []

    for command in commandList:
        if str(command.idType) in TYPE_DICT.keys():
            #print("Command type: %d; content %x", command.idType, command.content)
            content = BytesIO(command.content)
            commandClass = sys.modules[__name__].__dict__.get(\
                           TYPE_DICT[str(command.idType)])
            output.append(commandClass(content))
        else:
            output.append
            #print("Command ID not accounted for: %d, %s", command.idType, str(command.content))
    return output

class CommandSetTabWindow():
    """
    Set a Tab in a Window
    """
    def __init__(self, content):
        """
        content is a StringIO of the payload
        """
        # Content is Window ID on 8bits and Tab ID on 8bits
        # Strange alignment : two uint8 takes 8Bytes...
        self.windowId = struct.unpack(types.uint32, content.read(4))[0]
        self.tabId = struct.unpack(types.uint32, content.read(4))[0]
        self.description = self.__doc__
 

    def __str__(self):
        return "SetTabWindow (%s)- Window: %d, Tab: %d" % \
               (self.description.strip(), self.windowId, self.tabId)

class CommandSetTabIndexInWindow():
    """
    Set the Index of a Tab
    """
    def __init__(self, content):
        """
        content is a StringIO of the payload
        """
        # Content is Tab ID on 8bits and Index on 32bits
        # But due to alignment Tab ID is on 32bits

        self.tabId = struct.unpack(types.int32, content.read(4))[0]
        self.index = struct.unpack(types.int32, content.read(4))[0]
        self.description = self.__doc__

    def __str__(self):
        return "SetTabIndexInWindow (%s) - Tab: %d, Index: %d" % \
               (self.description.strip(), self.tabId, self.index)

class CommandTabClosed():
    """
    Store closure of a Tab with Timestamp
    """
    def __init__(self, content):
        # Content is Tab ID on 8bits and Close Time on 64bits
        self.tabId = struct.unpack(types.uint32, content.read(4))[0]

        # This is always null, we dump it so we can get the date correctly.
        self.dumpster = struct.unpack(types.uint32, content.read(4))[0] 
        self.closeTime = struct.unpack(types.uint64, content.read(8))[0]
        self.closeTime = datetime.datetime(1601, 1, 1) + \
                    datetime.timedelta(microseconds=self.closeTime)
        self.description = self.__doc__

    def __str__(self):
        return "TabClosed (%s) - Tab: %d, Close Time: %s" % \
               (self.description.strip(), self.tabId, self.closeTime)

class CommandWindowClosed():
    """
    Store closure of a Window with Timestamp
    """
    def __init__(self, content):
        # Content is Window ID on 8bits and Close Time on 64bits
        self.windowId = struct.unpack(types.uint32, content.read(4))[0]
        self.dumpster = struct.unpack(types.uint32, content.read(4))[0]
        self.closeTime = struct.unpack(types.int64, content.read(8))[0]
        self.closeTime = datetime.datetime(1601, 1, 1) + \
                     datetime.timedelta(microseconds=self.closeTime)
        self.description = self.__doc__

    def __str__(self):
        return "WindowClosed (%s) - Window: %d, CloseTime: %s" % \
               (self.description.strip(), self.windowId, self.closeTime)

class CommandTabNavigationPathPrunedFromBack():
    """
    TODO
    """
    def __init__(self, content):
        # Content is Tab ID on 8bits and Index on 32bits
        self.tabId = struct.unpack(types.uint8, content.read(1))[0]
        # XXX Strange results...
        self.index = 0#struct.unpack(types.int32, content.read(4))[0]

    def __str__(self):
        return "TabNavigationPathPrunedFromBack - Tab: %d, Index: %d" % \
               (self.tabId, self.index)

class CommandUpdateTabNavigation():
    """
    Update Tab information
    """
    def __init__(self, content):
        content = pickle.Pickle(content)
        self.tabId = content.readInt()
        self.index = content.readInt()
        self.url = content.readString()
        #self.title = content.readString16()
        self.description = self.__doc__
        
        #print("State:", content.readString())
        #print("Transition:", (0xFF & content.readInt()))
        # Content is Window ID on 8bits and Tab ID on 8bits
        # Strange alignment : two uint8 takes 8Bytes...

    def __str__(self):
        return "UpdateTabNavigation (%s)- Tab: %d,  Index: %d, Url: %s" % \
               (self.description.strip(), self.tabId, self.index, self.url)

class CommandSetSelectedNavigationIndex():
    """
    TODO
    """
    def __init__(self, content):
        # Content is Tab ID on 8bits and Index on 32bits
        # But due to alignment Tab ID is on 32bits
        self.tabId = struct.unpack(types.uint32, content.read(4))[0]
        self.index = struct.unpack(types.uint32, content.read(4))[0]

    def __str__(self):
        return "SetSelectedNavigationIndex - Tab: %d, Index: %d" % \
               (self.tabId, self.index)

class CommandSetSelectedTabInIndex():
    """
    Set selected Tab in a Window
    """
    def __init__(self, content):
        # Content is Window ID on 8bits and Index on 32bits
        # But due to alignment Window ID is on 32bits
        self.windowId = struct.unpack(types.uint32, content.read(4))[0]
        self.index = struct.unpack(types.uint32, content.read(4))[0]
        self.description = self.__doc__

    def __str__(self):
        return "SetSelectedTabInIndex (%s)- Window: %d, Index: %d" % \
               (self.description.strip(), self.windowId, self.index)

class CommandSetWindowType():
    """
    Set Window Type
    """
    def __init__(self, content):
        # Content is Window ID on 8bits and Window Type on 32bits
        # But due to alignment Window ID is on 32bits
        self.windowId = struct.unpack(types.uint32, content.read(4))[0]
        self.windowType = struct.unpack(types.uint32, content.read(4))[0]
        self.description = self.__doc__

    def __str__(self):
        return "SetWindowType (%s)- Window: %d, Type: %d" % \
               (self.description.strip(), self.windowId, self.windowType)

class CommandTabNavigationPathPrunedFromFront():
    """
    TODO
    """
    def __init__(self, content):
        # Content is Tab ID on 8bits and Count on 32bits
        # But due to alignment Tab ID is on 32bits
        self.tabId = struct.unpack(types.uint32, content.read(4))[0]
        self.count = struct.unpack(types.uint32, content.read(4))[0]

    def __str__(self):
        return "TabNavigationPathPrunedFromFront - Tab: %d, Count: %d" % \
               (self.tabId, self.count)

class CommandSetPinnedState():
    """
    Set Pinned State
    """
    def __init__(self, content):
        # Content is Tab ID on 8bits and Pinned State on 8bits
        # Strange alignment : two uint8 takes 8bits...
        self.tabId = struct.unpack(types.uint32, content.read(4))[0]
        self.pinned = struct.unpack(types.uint32, content.read(4))[0]
        self.description = self.__doc__

    def __str__(self):
        return "SetPinnedState (%s) - Tab: %d, Pinned: %d" % \
               (self.description.strip(), self.tabId, self.pinned)

class CommandSetExtensionAppID():
    """
    TODO
    """
    def __init__(self, content):

        self.tabId = struct.unpack(types.uint32, content.read(4))[0]
        self.appId = struct.unpack(types.int64, content.read(8))[0]


    def __str__(self):
        return "SetExtensionAppID - Tab: %d, " % self.tabId +\
               "Extension: %d" % self.appId

class CommandSetWindowBounds3():
    """
    Set Window size, position and state
    """
    def __init__(self, content):
        # Content is
        #   Window ID on 8bits
        #   x, y, w, h on 32bits
        #   state on 32bits
        # Alignment : Window Id is in the first 32bits
        self.windowId = struct.unpack(types.uint32, content.read(4))[0]
        self.x = struct.unpack(types.int32, content.read(4))[0]
        self.y = struct.unpack(types.int32, content.read(4))[0]
        self.w = struct.unpack(types.int32, content.read(4))[0]
        self.h = struct.unpack(types.int32, content.read(4))[0]
        self.state = struct.unpack(types.int32, content.read(4))[0]
        self.state = WINDOW_SHOW_STATE[self.state]
        self.description = self.__doc__

    def __str__(self):
        return "SetWindowBounds3 (%s) - Window: %d, x: %d, y: %d, w: %d, h: %d, " % \
               (self.description.strip(), self.windowId, self.x, self.y, self.w, self.h) + "State: %s" % \
               self.state

class CommandLastActiveTime():
    """
    Time since active on tab 
    """
    def __init__(self, content):
        #session_service_base.cc defines the parameters as 
        # const SessionID& window_id,
        # const SessionID& tab_id,
        # base::TimeTicks last_active_time
        # 
        # I haven't been unable to determine why my implementation of readDouble() fails
        # I am not using pickle in this instance only due to that variable.
        #content = pickle.Pickle(content)
        #self.windowId = content.readInt()
        #self.tabId = content.readInt()
        #self.lastActiveTime = content.readDouble()

        self.windowId = struct.unpack(types.uint32, content.read(4))[0]
        self.tabId = struct.unpack(types.uint32, content.read(4))[0]
        self.lastActiveTime = struct.unpack(types.int64, content.read(8))[0]

        # I'm not sure that this time is accurate or what it is offset from.
        self.lastActiveTime = datetime.timedelta(microseconds=self.lastActiveTime/1000)
        self.description = self.__doc__
        
    def __str__(self):
        return "LastActiveTime (%s) - Window: %s, Time: %s" % \
            (self.description.strip(), self.windowId, self.lastActiveTime )



class CommandSideSearch():
    """
    Google Side Search Query
    """
    def __init__(self, content):
        content = pickle.Pickle(content)
        self.tabId = content.readInt()
        self.index = content.readInt()
        self.profile = content.readInt()
        self.sideSearchTitle = content.readString16()
        self.something = content.readShort()
        self.somethingShort = content.readChar()
        self.enabledBool = content.readBool()
        self.url = content.readString()
        self.description = self.__doc__

    def __str__(self):
        return "SideSearch (%s) - Tab: %d, Index: %d, Url: %s" % \
            (self.description.strip(), self.tabId, self.index, self.url.strip())