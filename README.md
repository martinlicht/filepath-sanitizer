# filepath-sanitizer
A Python script that checks the names of your files and folders are compliant to common file systems. For example, it checks for overlength paths, forbidden characters, and reserved keywords.

The script recursively traverses subdirectories and files found under the specified location. Whenever the path to a file or directory looks suspicious and might not be usable on common file systems, it emits a warning message.

This script is intended to be a helpful utility, for example, when copies of a project are maintained on different machines with different file systems. Before any transfer of data, you can check whether you need to rename your files or maybe need to flatten your directory structure.
