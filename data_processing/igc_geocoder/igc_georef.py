# -*- coding: utf8 -*-
import sys
import os
import shutil
import re


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

    #origine index planches IGC
    xHautGaucheOrigine = 585000
    yHautGaucheOrigine = 1145824

    hauteurPlanche = 400
    largeurPlanche = 600

    epsg3857 = "3857"
    epsg27571 = "27571"

    #TODO : test the lenght of sys.argv
    rasterDirectory = sys.argv[1]
    igcTifs = os.listdir(rasterDirectory)

    #TODO : remove folder if exist
    createSubDirectories(rasterDirectory, epsg3857)
    rasterDirectory3857 = rasterDirectory+os.sep+epsg3857
    createSubDirectories(rasterDirectory, epsg27571)
    rasterDirectory27571 = rasterDirectory+os.sep+epsg27571
    
    p = re.compile('\d+')

    for tif in igcTifs:

    	print "\n-- Traitement de la planche "+tif + " --"
        integerValues = p.findall(tif)
        igcAbs = integerValues[0]
        igcOrd = integerValues[1]

        #print type(igcAbs)

        xTopLeftCurrent = xHautGaucheOrigine+largeurPlanche*(int(igcAbs)-1)
        yTopLeftCurrent = yHautGaucheOrigine-hauteurPlanche*(int(igcOrd)-1)

        xLowerRightCurrent = xTopLeftCurrent+largeurPlanche
        yLowerRightCurrent = yTopLeftCurrent-hauteurPlanche

        print "coords 27571 : topLeft "+str(xTopLeftCurrent)+" "+str(yTopLeftCurrent)+" lowerRight "+str(xLowerRightCurrent)+" "+str(yLowerRightCurrent)
        print "*georeferencing 27571...*"
        #print "gdal_translate -of Gtiff -co COMPRESS=JPEG -a_srs EPSG:27571 -a_ullr "+str(xTopLeftCurrent)+' '+str(yTopLeftCurrent)+' '+str(xLowerRightCurrent)+' '+str(yLowerRightCurrent)+' '+rasterDirectory+os.sep+tif+' '+rasterDirectory3857+os.sep+tif
        os.system("gdal_translate -of Gtiff -co COMPRESS=JPEG -a_srs EPSG:27571 -a_ullr "+str(xTopLeftCurrent)+' '+str(yTopLeftCurrent)+' '+str(xLowerRightCurrent)+' '+str(yLowerRightCurrent)+' '+rasterDirectory+os.sep+tif+' '+rasterDirectory27571+os.sep+tif)
       
        print "*reprojecting 3857...*"
        os.system("gdalwarp -of Gtiff -co COMPRESS=JPEG -s_srs EPSG:27571 -t_srs EPSG:3857 "+rasterDirectory27571+os.sep+tif+' '+rasterDirectory3857+os.sep+tif)
        
   