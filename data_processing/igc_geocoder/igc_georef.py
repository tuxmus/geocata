# -*- coding: utf8 -*-
import sys
import os
import shutil


# TODO : make catadatamaps API...

## createSubDirectories the subfolders you want in rasterDirectory
# @param rasterDirectory the folder in which you want to create the subdirectories, e.g /home/user
def createSubDirectories(rasterDirectory, *subFolderToCreate):

    for subDir in subFolderToCreate:
        folderToCreate = os.path.join(rasterDirectory,subDir)
        print folderToCreate
        if(os.path.exists(folderToCreate)):
            print "\nFolder "+folderToCreate+" exists"
            #erase non empty directories
            shutil.rmtree(folderToCreate)
            print "Delete "+folderToCreate
        
        os.mkdir(folderToCreate)
        print folderToCreate+" created\n"




if __name__ == '__main__':

    #TODO : test the lenght of sys.argv
    rasterDirectory = sys.argv[1]
 
    igcTifs = os.listdir(rasterDirectory)
    
    for tif in igcTifs
    	print tif