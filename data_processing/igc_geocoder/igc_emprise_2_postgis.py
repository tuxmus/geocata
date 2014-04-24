# -*- coding: utf8 -*-

# usage : python script.py igcRasterDirectory
# ou les planches IGC n'ont pas besoin d'être géoréférencées, détecte leurs coord juste à partir du nom
# output : un fichier sql destiné à être exécuté dans postgis, pour dessiner les polygones des emprises de planches 

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
    #igcTifs = os.listdir(rasterDirectory)

    igcTifs = [x for x in os.listdir(rasterDirectory) if x.endswith(".tif")]

    #TODO : remove folder if exist
    #createSubDirectories(rasterDirectory, epsg3857)
    #rasterDirectory3857 = rasterDirectory+os.sep+epsg3857
    
    p = re.compile('\d+')
    id = 0

    sqlFilePath  = rasterDirectory+os.sep+'sql_emprises.sql'

    if ( os.path.exists (sqlFilePath) ) : 
        os.remove(sqlFilePath)

    
    

    strToWrite = "INSERT INTO igc.emprises (id, nom, geom) VALUES \n\n"
    


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


        # on recupere les coordonnees reprojetees de 2 points
        xTopLeftCurrentReprojected, yTopLeftCurrentReprojected = reprojecte(xTopLeftCurrent, yTopLeftCurrent, 27571, 3857)
        xLowerRightCurrentReprojected, yLowerRightCurrentReprojected = reprojecte(xLowerRightCurrent, yLowerRightCurrent, 27571, 3857)

        # on en deduit celles des 2 autres points 

        xTopRightCurrentReprojected = xLowerRightCurrentReprojected
        yTopRightCurrentReprojected = yTopLeftCurrentReprojected

        xLowerLeftCurrentReprojected = xTopLeftCurrentReprojected
        yLowerLeftCurrentReprojected = yLowerRightCurrentReprojected

        #DEBUG
        print str(xTopLeftCurrentReprojected)+" "+str(yTopLeftCurrentReprojected)
        print str(xTopRightCurrentReprojected)+" "+str(yTopRightCurrentReprojected)
        print str(xLowerRightCurrentReprojected)+" "+str(yLowerRightCurrentReprojected)
        print str(xLowerLeftCurrentReprojected)+" "+str(yLowerLeftCurrentReprojected)
        print ""
       # on cree le polygone qui correspondra a une planche 


        # Create ring
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(xTopLeftCurrentReprojected, yTopLeftCurrentReprojected)
        ring.AddPoint(xTopRightCurrentReprojected, yTopRightCurrentReprojected)
        ring.AddPoint(xLowerRightCurrentReprojected, yLowerRightCurrentReprojected )
        ring.AddPoint(xLowerLeftCurrentReprojected, yLowerLeftCurrentReprojected )
        ring.AddPoint(xTopLeftCurrentReprojected, yTopLeftCurrentReprojected)

        # Create polygon
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)

        #print poly.ExportToWkt()


        tifName = tif[:-4]
        id = id+1 

        strToWrite = strToWrite+'('+str(id)+', '+"'"+tifName+"'"+', '+ "ST_GeomFromText(' "+poly.ExportToWkt()+"', 3857)"+"),\n\n"
        #emprisesFile.write('('+str(id)+', '+'"'+tifName+"'"+', '+ "ST_GeomFromText(' "+poly.ExportToWkt()+"', 3857)"+"),\n\n")
          

    strToWrite =  strToWrite[:-3]
    strToWrite =  strToWrite+"\n\n ;"

    emprisesFile = open(sqlFilePath, 'w') 
    emprisesFile.write(strToWrite);
    emprisesFile.close();


        #INSERT INTO igc.emprises (id, nom, geom)
        #    VALUES (44, 'oak',c
        #    ST_GeomFromText(
        #        'POLYGON((6 15, 10 10, 20 10, 25 15, 25 35, 19 40, 11 40, 6 25, 6 15))',
        #       4326))
    
