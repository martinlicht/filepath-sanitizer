# filepath-sanitizer
A Python script that checks the names of your files and folders are compliant to common file systems. For example, it checks for overlength paths, forbidden characters, and reserved keywords.

Usage: filepath-sanitizer PATH

where PATH is the path to a file or a directory. 

The script recursively traverses subdirectories and files found under the location specified by PATH. Warning messages whenever the path to a file or directory looks suspicious and might not be usable on common file systems. 
