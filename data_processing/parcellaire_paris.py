import gdal
from gdalconst import *
import os
import sys
import shutil

## createSubDirectories the subfolders you want in rasterDirectory
# @param rasterDirectory the folder in which you want to create the subdirectories, e.g /home/user
def createSubDirectories(rasterDirectory, *subFolderToCreate):

    for subDir in subFolderToCreate:
        folderToCreate = rasterDirectory+subDir
        if(os.path.exists(folderToCreate)):
            print "\n---Folder "+folderToCreate+" exists---"
            #erase non empty directories
            shutil.rmtree(folderToCreate)
            print "---Delete "+folderToCreate+" ---"
        
        os.mkdir(folderToCreate)
        print "--- "+folderToCreate+"created ---\n"


# usage : python test.py rasterDirectory

if __name__ == '__main__':

    #TODO : test the lenght of sys.argv
    rasterDirectory = sys.argv[1]
    
    epsgLambert1 = "27571"
    epsgLambertOK = "27571_OK"
    epsgWebMapping = "3857"
    
    createSubDirectories(rasterDirectory, epsgLambert1, epsgWebMapping)

    #list all files in the directory
    rasterDirectoryFiles = os.listdir(rasterDirectory);
    
    for filename in rasterDirectoryFiles:
        # for each tif file
        if(filename.endswith('.tif')):
            
            filepath = os.path.join(rasterDirectory, filename)
            #print filepath
            # TODO : fix the warning which appear at the opening of the raster (Warning 1: RowsPerStrip not defined ... assuming all one strip)
            dataset = gdal.Open( filepath, GA_ReadOnly )
            

            if dataset is None:
                print filepath+" cannot be opened, End of the program"
                sys.exit(1)
            else:
                print "Traitement du fichier "+filepath
                #dataset.SetProjection('PROJCS["NTF (Paris) / Lambert zone I",GEOGCS["NTF (Paris)",DATUM["Nouvelle_Triangulation_Francaise_Paris",SPHEROID["Clarke 1880 (IGN)",6378249.2,293.4660212936269,AUTHORITY["EPSG","7011"]],TOWGS84[-168,-60,320,0,0,0,0],AUTHORITY["EPSG","6807"]],PRIMEM["Paris",2.5969213],UNIT["grad",0.01570796326794897],AUTHORITY["EPSG","4807"]],PROJECTION["Lambert_Conformal_Conic_1SP"],PARAMETER["latitude_of_origin",49.5],PARAMETER["central_meridian",0],PARAMETER["scale_factor",0.999877341],PARAMETER["false_easting",600000],PARAMETER["false_northing",1200000],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AUTHORITY["EPSG","27571"]]')
            
                # nb of pixels in x and y
                rows = dataset.RasterYSize
                cols = dataset.RasterXSize
                
                # get georeference info. GeoTransforms are lists of information used to georeference an image
                transform = dataset.GetGeoTransform()
                xOrigin = transform[0]
                yOrigin = transform[3]
                pixelWidth = transform[1]
                pixelHeight = transform[5]

                #debug
                #print "origine : "+str(xOrigin)+" "+str(yOrigin)
                #print "largeur "+str(cols*pixelWidth)
                #print "hauteur "+str(rows*pixelHeight)

                # get image size and translation information
                dx = cols*pixelWidth
                dy = rows*pixelHeight

                #debug
                #print str(xOrigin)+" "+str(yOrigin)+" /// "+str(xOrigin+dx)+" "+str(yOrigin+dy)
                #print "RASTERDIRECTORY "+rasterDirectory
                #print "EPSG Lambert1 "+epsgLambert1
                #print "EPSG Mapping "+epsgWebMapping

                lambertDir = os.path.join(rasterDirectory,epsgLambert1)
                mappingDir = os.path.join(rasterDirectory,epsgWebMapping)

                lambertFile = os.path.join(lambertDir, filename)
                mappingFile = os.path.join(mappingDir, filename)

                print "//// GEOREF 27571 - Fix Lambert 1 coordinates (+1.000.000 en y) ////"
                os.system("gdal_translate -of Gtiff -co COMPRESS=LZW -a_srs EPSG:27571 -a_ullr "+str(xOrigin)+" "+str(yOrigin+1000000)+" "+str(xOrigin+dx)+" "+str(yOrigin+dy+1000000)+" "+filepath+" "+lambertFile)

                print "//// REPROJECT 3857 ////"
                os.system("gdalwarp -of Gtiff -co COMPRESS=LZW -s_srs EPSG:27571 -t_srs EPSG:3857 "+lambertFile+" "+mappingFile)
                
    
    
