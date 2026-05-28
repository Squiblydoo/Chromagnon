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
This module is a basic and incomplete implementation of the pickle module
used in Chrome.
"""

import os
import struct

import chromagnon.types as types

class Pickle():

    def __init__(self, data):
        """
        Reads the header of the pickle object and extract payload from it.
        data is a StringIO or a file descriptor
        """
        self.data = data
        # len function seems to exists for StringIO
        self.data.seek(0, os.SEEK_END)
        self.dataSize = self.data.tell()
        self.data.seek(0, os.SEEK_SET)

        self.payloadSize = struct.unpack(types.uint32, self.data.read(4))[0]
        self.payloadStart = self.dataSize - self.payloadSize
#        print "dataSize: %d, payloadSize: %d, payloadStart: %d" % \
#              (self.dataSize, self.payloadSize, self.payloadStart)

    def readBool(self):
        """Reading Bool as 4-byte int (Chrome Pickle stores bools as int32)"""
        return struct.unpack(types.uint32, self.data.read(4))[0] != 0

    def readChar(self):
        return struct.unpack(types.uint8, self.data.read(1))[0]

    def readShort(self):
        return struct.unpack(types.uint16, self.data.read(2))[0]


    def readInt(self):
        """Reading Int on 32bits"""
        return struct.unpack(types.uint32, self.data.read(4))[0]

    def readString(self):
        """Reading String on 8bits"""
        # Reading String length
        length = self.readInt()
        # XXX Some Length are two big...
        if length > self.dataSize - self.data.tell():
            return None
        result = self.data.read(length)
        # Consume alignment padding to the next 4-byte boundary
        remainder = length % 4
        if remainder:
            self.data.read(4 - remainder)
        return result.decode('utf-8', 'ignore')

    def readString16(self):
        """Reading String on 16bits"""
        # Reading String length (number of characters)
        length = self.readInt()
        byte_length = length * 2
        # XXX Some Length are two big...
        if byte_length > self.dataSize - self.data.tell():
            return None
        result = self.data.read(byte_length)
        # Consume alignment padding to the next 4-byte boundary
        remainder = byte_length % 4
        if remainder:
            self.data.read(4 - remainder)
        return result.decode('utf-16', 'ignore')

    def readDouble(self):
        return struct.unpack(types.int64, self.data.read(8))[0]

    def readUInt32(self):
        """Reading unsigned 32-bit integer"""
        return struct.unpack(types.uint32, self.data.read(4))[0]

    def readUInt64(self):
        """Reading unsigned 64-bit integer"""
        return struct.unpack(types.uint64, self.data.read(8))[0]
