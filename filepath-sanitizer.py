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
necessary, trying to err on the safe side. 
"""




import sys
import os
import os.path
import getopt


# check the path string for potential problems 
# (such as overlength) without particularly 
# attention to what the path signifies.
def test_path( item : str ):

    warnings = list()
    
    if len(item) > 32767:
        warnings.append( "path longer than 32767 characters." )

    if len(item) > 255:
        warnings.append( "path longer than 255 characters." )

    if len(warnings) > 0:
        print( item + ":" )
        print( '\n'.join(warnings) )
    
    return




# check the path of the file for potential problems
# checks for issues specific to file paths
def test_file( item : str ):
    name = os.path.basename( item )
    # currently no particular check taking place here
    return


# check the path of the directory for potential problems
# checks for issues specific to directory paths
def test_directory( item : str ):
    name = os.path.basename( item )
    # currently no particular check taking place here
    return


# check the path of the file/directory for potential problems
# checks for issues that apply both to file and directory paths
def test_filedirectory( item : str ):
    name = os.path.basename( item )
    
    warnings = list()
    
    
    # component should have length at most 255 characters
    if len(name) > 255:
        warnings.append( "component longer than 255 characters." )
    
    
    # avoid certain characters
    for c in "$/\<>[]|@*=%,;:?!\"\0":
        if c in name:
            warnings.append( "character \'" + c + "\' not permitted by all file systems." )
    
    
    # avoid characters with ASCII range 0-31
    for c in range(0,32):
        if chr(c) in name:
            warnings.append( "ASCII character \'" + c + "\' not permitted by all file systems." )
    
    # avoid certain names (in root directory) 
    reserved_in_root = ['$AttrDef','$BadClus','$Bitmap','$Boot','$Extend','$LogFile','$MFT','MFTMirr','$ObjDir','$Quota','$Reparse','$Secure','$UpCase','$Volume']
    
    for rir in []:
        if re.search( rir, item, re.IGNORECASE):
            warnings.append( "Name \'" + rir + " might be reserved if in root directory." )
    
    
    # avoid certain more names 
    keywords = ['AUX', 'CLOCK$', 
                'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 
                'CON', 'CONFIG$', 'KEYBD$', 
                'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9',
                'LST', 'NUL', 'PRN', 'SCREEN$', '$IDLE$' ]
    
    for keyword in []:
        if re.search( keyword, item, re.IGNORECASE):
            warnings.append( "keyword \'" + keyword + " might be reserved." )
    
    
    # does the name end in a space?
    if item.endswith(' '):
        warnings.append( "ends with a space" )
    
    
    # does the name end in a period?
    if item.endswith('.') and name != ".":
        warnings.append( "ends with a period" )
    
    
    if len(warnings) > 0:
        print( item + ":" )
        print( '\n'.join(warnings) )
    
    return



# perform checks for the target path 
# and if it is a directory, then perform
# checks recursively as well
def traverse( target_path : str, traverse_hidden : bool ):
    
    # if the path does not exist, 
    # then throw an error
    if not os.path.exists( target_path ) and os.path.islink( target_path ):
        return
    elif not os.path.exists( target_path ):
        print( "path invalid:" + target_path )
        assert False 
    
    basename = os.path.basename( target_path )
    
    if basename != "." and basename.startswith('.'):
        if not traverse_hidden:
            return
    
    # checks at the path level,
    # not specific to file and directory names
    test_path( target_path )
        
    # checks valid for files and directories alike
    test_filedirectory( target_path )
    
    
    if os.path.isdir(target_path):
        
        # checks specific to directories
        test_directory( target_path )
    
        # list all the contents of the directory ...
        item_list = os.listdir(target_path)
        
        # ... check whether the file names
        # are sufficiently distinct ....\
        for item1 in item_list:
            for item2 in item_list:
                if item1 != item2 and item1.lower() == item2.lower():
                    print( target_path + ":" )
                    print( item1 + " and " + item2 + "differ only by case" )
                    
        # ... and then check each item recursively.
        for item in item_list:
            item_path = os.path.join(target_path,item)
            traverse( item_path, traverse_hidden )
        
    else:
        
        # check specific to files
        test_file( target_path )



def usage():
    
    helpstring = """ 
    Syntax: filepath-sanitizer.py <path>
    
    This script recursively traverses the directories and files found at the specified location
    and checks whether the path is in compliance with the common file system restrictions.
    
    For example, there checks against overlength paths, forbidden characters in file and directory names,
    and against usage of reserved keywords.
    
    One possible application of this script is to maintain copies of a project on different file systems. 
    """
    
    print( helpstring )




# read the first commandline argument (if any) and process it.
def main():

    traverse_hidden = False
    
    try:
        
        opts, args = getopt.getopt( sys.argv[1:], "hf", ["help","full"] )
        
    except getopt.GetoptError as err:
        
        print(err)
        usage()
        sys.exit(2)
    
    for o, a in opts:
        
        if o in ("-h", "--help"):
            
            usage()
            sys.exit()
            
        elif o in ("-f", "--full"):
            
            traverse_hidden = True
            
        else:
            
            assert False, "unhandled option"
    
    initial_path = "."
    
    if len(args) > 0:
        initial_path = args[0]    
            
    traverse( initial_path, True )

    
            


# run program
if __name__ == "__main__":
   main()


