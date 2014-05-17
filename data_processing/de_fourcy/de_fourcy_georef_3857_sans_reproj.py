# -*- coding: utf8 -*-

try:
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    import ogr
    import osr

import sys
import os


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



if __name__ == '__main__':

    # noms des planches sur le disque

    rasterDirectory = sys.argv[1]
    directoryFiles = os.listdir(rasterDirectory)

    destDirectory_3857 = rasterDirectory+os.sep+"3857_sans_reproj"
    print destDirectory_3857

    os.mkdir(destDirectory_3857)


    fourcy_09_name = "P09_To_gr.tif"
    fourcy_10_name = "P10_To_gr.tif"
    fourcy_11_name = "P11_To_gr.tif"
    fourcy_12_name = "P12_To_gr.tif"
    fourcy_13_name = "P13_To_gr.tif"
    fourcy_14_name = "P14_To_gr.tif"
    fourcy_15_name = "P15_To_gr.tif"
    fourcy_16_name = "P16_To_gr.tif"


    # NOUVEAU DU 16.05.2014
    fourcy_17_name = "P17_To_gr.tif"  
    fourcy_18_name = "P18_To_gr.tif" 
    fourcy_05_name = "P05_To_gr.tif" 
    fourcy_06_name = "P06_To_gr.tif" 
    fourcy_07_name = "P07_To_gr.tif" 
    fourcy_08_name = "P08_To_gr.tif" 
    fourcy_19_name = "P19_To_gr.tif" 
    fourcy_20_name = "P20_To_gr.tif" 
    fourcy_21_name = "P21_To_gr.tif" 
    fourcy_00_name = "P00_To_gr.tif" # index de fourcy 


    # liste de liste de tuples; ou chaque liste de tuple correspond à une planche de l'atlas de fourcy, sur cette base [ (coord Upper Left), (coord Lower Right)]
    fourcys_27571 = [];
    fourcys_3857 = [];

    fourcy_09_27571 = [fourcy_09_name, (600000, 1128024), (601000, 1127424)]
    fourcys_27571.append(fourcy_09_27571)

    fourcy_10_27571 = [fourcy_10_name, (600000, 1127424), (601000, 1126824)]
    fourcys_27571.append(fourcy_10_27571)

    fourcy_11_27571 = [fourcy_11_name, (600000, 1126824), (601000, 1126224)]
    fourcys_27571.append(fourcy_11_27571)

    fourcy_12_27571 = [fourcy_12_name, (600000, 1126224), (601000, 1125624)]
    fourcys_27571.append(fourcy_12_27571)

    fourcy_13_27571 = [fourcy_13_name, (599000, 1128024), (600000, 1127424)]
    fourcys_27571.append(fourcy_13_27571)

    fourcy_14_27571 = [fourcy_14_name, (599000,1127424), (600000, 1126824)]
    fourcys_27571.append(fourcy_14_27571)

    fourcy_15_27571 = [fourcy_15_name, (599000, 1126824), (600000, 1126224)]
    fourcys_27571.append(fourcy_15_27571)

    fourcy_16_27571 = [fourcy_16_name, (599000, 1126224), (600000, 1125624)]
    fourcys_27571.append(fourcy_16_27571)

    # NOUVEAU 16.05.2014

    fourcy_17_27571 =  [fourcy_17_name, (598000, 1127424), (599000, 1126824)]   
    fourcys_27571.append(fourcy_17_27571)

    fourcy_18_27571 =  [fourcy_18_name, (598000, 1126824), (599000, 1126224)]   
    fourcys_27571.append(fourcy_18_27571)

    fourcy_05_27571 =  [fourcy_05_name, (601000, 1127424), (602000, 1126824)]   
    fourcys_27571.append(fourcy_05_27571)

    fourcy_06_27571 =  [fourcy_06_name, (601000, 1126824), (602000, 1126224)]   
    fourcys_27571.append(fourcy_06_27571)

    fourcy_07_27571 =  [fourcy_07_name, (601000,  1126224), (602000, 1125624)]   
    fourcys_27571.append(fourcy_07_27571)

    fourcy_08_27571 =  [fourcy_08_name, (601000, 1125624), (602000, 1126024)]   
    fourcys_27571.append(fourcy_08_27571)

    fourcy_19_27571 =  [fourcy_19_name, (597000, 1129824), (598000, 1129224)]   
    fourcys_27571.append(fourcy_19_27571)

    fourcy_20_27571 =  [fourcy_20_name, (596000, 1129824), (597000, 1129224)]   
    fourcys_27571.append(fourcy_20_27571)

    fourcy_21_27571 =  [fourcy_21_name, (596000, 1129224), (597000, 1128624)]   
    fourcys_27571.append(fourcy_21_27571)

    fourcy_00_27571 =  [fourcy_00_name, (596000, 1129824), (602000, 1126024)]   
    fourcys_27571.append(fourcy_00_27571)




    for planche in fourcys_27571:
        name_planche = planche[0]
        upper_left_planche_27571 = planche[1]
        lower_right_planche_27571 = planche[2]

        # récupération des x et y du upper left
        ulx_27571 = upper_left_planche_27571[0]
        uly_27571 = upper_left_planche_27571[1]

        # récupération des x et y du lower right
        lrx_27571 = lower_right_planche_27571[0]
        lry_27571 = lower_right_planche_27571[1]

        upper_left_planche_3857 = reprojecte(ulx_27571, uly_27571, 27571, 3857)
        lower_right_planche_3857 = reprojecte(lrx_27571, lry_27571, 27571, 3857)

        planche_3857 = [name_planche, upper_left_planche_3857, lower_right_planche_3857]

        ulx_3857 = upper_left_planche_3857[0]
        uly_3857 = upper_left_planche_3857[1]

        lrx_3857 = lower_right_planche_3857[0]
        lry_3857 = lower_right_planche_3857[1]

        fourcys_3857.append(planche_3857)

        if(name_planche in directoryFiles):
            print  name_planche

            process_planche = "gdal_translate -of Gtiff -co COMPRESS=NONE -a_srs EPSG:3857 -a_ullr "+str(ulx_3857)+" "+str(uly_3857)+" "+str(lrx_3857)+" "+str(lry_3857)+" "+rasterDirectory+os.sep+name_planche+" "+destDirectory_3857+os.sep+name_planche
            #print process_planche
            print ""
            print "Traitement de la planche "+name_planche
            print""
            os.system(process_planche)


        #print ""
        #print name_planche
        #print upper_left_planche
        #print lower_right_planche
        #print ""





    #for fourcy_planche in directoryFiles:
    #   if(fourcy_planche.endswith(".tif")):
    #        for 

    #fourcyTifs = [x for x in directoryFiles  if x.endswith(".tif")]
   

   # print fourcyTifs
    #print fourcys_3857