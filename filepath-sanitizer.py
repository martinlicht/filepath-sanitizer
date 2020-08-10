#!/usr/bin/python3
# 
# MIT License
# 
# Copyright (c) 2020 Martin Licht
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Checks whether directory entries are compatible with common file systems.

When working on several operating systems, it may happen that your files and directories
have names that are permitted in some file systems but not in others. The purpose of this 
script is to identify such file names. 

The main goal is to showcase possible non-compliance with the file systems exFAT, ext3, and NTFS.
This program does not attempt to fix up these problems. Moreover, it may be more restrictive than 
necessary. 
"""




import sys
import os
import os.path

# These lists contain the names of the files, directories, and the full paths
# of everything within the search directory

file_list   = list()
folder_list = list()
path_list   = list()



# build up those three lists by parsing through the directory

def preprocess(target_path):
    global file_list
    global path_list
    global folder_list

    if not os.path.exists( target_path ):
        raise "path invalid:" + target_path
    
    path_list.append( target_path )
        
    if os.path.isdir(target_path):
        folder_list.append( target_path )
        item_list = os.listdir(target_path)
        
        for item1 in item_list:
            for item2 in item_list:
                if item1 != item2 and item1.lower() == item2.lower():
                    print( target_path + ":" )
                    print( item1 + " and " + item2 + "differ only by case" )
                    
        
        for item in item_list:
            item_path = os.path.join(target_path,item)
            preprocess(item_path)
    else:
        file_list.append( target_path )
        




# all items collected
# now go through everything to test 

def test_file( item ):
    name = os.path.basename( item )
    return

def test_folder( item ):
    name = os.path.basename( item )
    return

def test_filefolder( item ):
    name = os.path.basename( item )
    
    warnings = list()
    
    if len(name) > 255:
        warnings.append( "component longer than 255 characters." )
        
    for c in "$/\<>[]|@*=%,;:?!\"\0":
        if c in name:
            warnings.append( "character \'" + c + "\' not permitted by all file systems." )
    
    keywords = ['AUX', 'CLOCK$', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 
                'CON', 'CONFIG$', 'KEYBD$', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9',
                'LST', 'NUL', 'PRN', 'SCREEN$', '$IDLE$' ]
    
    for keyword in []:
        if re.search( keyword, item, re.IGNORECASE):
            warnings.append( "keyword \'" + keyword + " found." )
    
    if len(warnings) > 0:
        print( item + ":" )
        print( '\n'.join(warnings) )
    
    return




def test_path( item ):

    warnings = list()
    
    if len(item) > 32767:
        warnings.append( "path longer than 255 characters." )

    if len(warnings) > 0:
        print( item + ":" )
        print( '\n'.join(warnings) )
    
    return







# read the first commandline argument (if any) and process it.

for i in file_list: print( i )
for i in folder_list: print( i )
for i in path_list: print( i )

initial_path = "."

if len(sys.argv) > 1:
    initial_path = sys.argv[1]

if not os.path.exists( initial_path ):
    raise "path invalid:" + argv[0]
    
preprocess( initial_path )


for filename in file_list:
    test_filefolder( filename )
    test_file( filename )

for foldername in file_list:
    test_filefolder( foldername )
    test_file( foldername )

for pathstring in path_list:
    test_path( pathstring )

