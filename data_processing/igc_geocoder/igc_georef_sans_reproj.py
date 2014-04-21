# -*- coding: utf8 -*-

try:
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    import ogr
    import osr

import sys
import os
import shutil
import re

def reprojecte(x, y, from_epsg, to_epsg):
    to_srs = osr.SpatialReference()
    to_srs.ImportFromEPSG(to_epsg)
    from_srs = osr.SpatialReference()
    from_srs.ImportFromEPSG(from_epsg)

    wkt = 'POINT(%f %f)' % (x, y)
    
    pt = ogr.CreateGeometryFromWkt(wkt)
    pt.AssignSpatialReference(from_srs)
    #print pt
    pt.TransformTo(to_srs)
    xReproj =  pt.GetX()
    yReproj =  pt.GetY()
    return (xReproj, yReproj)


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
    
    p = re.compile('\d+')

    for tif in igcTifs:

        print tif
        print "\n-- Traitement de la planche "+tif + " --"
        integerValues = p.findall(tif)

        igcAbs = integerValues[0]
        igcOrd = integerValues[1]

        xTopLeftCurrent = xHautGaucheOrigine+largeurPlanche*(int(igcAbs)-1)
        yTopLeftCurrent = yHautGaucheOrigine-hauteurPlanche*(int(igcOrd)-1)

        xLowerRightCurrent = xTopLeftCurrent+largeurPlanche
        yLowerRightCurrent = yTopLeftCurrent-hauteurPlanche

        xTopLeftCurrentReprojected, yTopLeftCurrentReprojected = reprojecte(xTopLeftCurrent, yTopLeftCurrent, 27571, 3857)
        xLowerRightCurrentReprojected, yLowerRightCurrentReprojected = reprojecte(xLowerRightCurrent, yLowerRightCurrent, 27571, 3857)

     
        print "*georeferencing 3857 without reprojection...*"
        os.system("gdal_translate -of Gtiff -co COMPRESS=JPEG -a_srs EPSG:3857 -a_ullr "+str(xTopLeftCurrentReprojected)+' '+str(yTopLeftCurrentReprojected)+' '+str(xLowerRightCurrentReprojected)+' '+str(yLowerRightCurrentReprojected)+' '+rasterDirectory+os.sep+tif+' '+rasterDirectory3857+os.sep+tif)
    
