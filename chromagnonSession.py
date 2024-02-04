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

import argparse
import sys
import textwrap

from pathlib import Path
import re 
import datetime

import chromagnon.SNSSParse
import chromagnon.sessionParse

def guiParse(path):
    snss = chromagnon.SNSSParse.parse(path)
    # Parse Retrived data
    sessionCommand = chromagnon.sessionParse.parse(snss)

    # returnData output
    output = []
    for command in sessionCommand:
        output.append(command)

    return output


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''
[Chromagnon Chrome Session Parser]

[Input File]
    The input file of this program is the Chrome Session File.
    It is encoded and the usual names are "Current Session" and
    "Session_..." whereas the underscore is followed with numerical 
    values.

[Output Format]
    Current output is raw ordering of Session data. Other formats to come.
        ''')
    )

    # These options and formats will come at a later time. Currently, the sections are
    # hard coded so these formats don't won't work.

    #parser.add_argument('-f', '-format', action='store', default='classical', 
    #                    choices=['csv','column','classical','json'],
    #                    help='Choose format for output formatting (csv, column, clasical, json)')
    #parser.add_argument('-d', '-delimiter', action='store',
    #                    help='Specify a delimiter for use in output formatting')
    parser.add_argument('filename', help='Path to Session file', action='store',
     type=str)
    
    args = parser.parse_args()

    
    # Getting Data
    snss = chromagnon.SNSSParse.parse(sys.argv[1])

    # Parse Retrived data
    sessionCommand = chromagnon.sessionParse.parse(snss)

    # Print data based on SNSS Commands
    output = []

    # Parse timestamp from file name
    try:
        filename = Path(args.filename).stem
        match = re.search(r'\d+$', filename )

        if match:
            timestamp = int(match.group())
            epoch_start = datetime.datetime(1601,1,1)
            delta = datetime.timedelta(microseconds=int(timestamp))
            human_readable_time = epoch_start + delta
        print(f"File Name: {filename}")
        print(f"Timestamp: {timestamp}")
        print(f"Human Readable Time: {human_readable_time} UTC")

    except Exception as e:
        print( e)
    
    for command in sessionCommand:
        
        print(command)

    # Handle table printing


if __name__ == "__main__":
    main()
