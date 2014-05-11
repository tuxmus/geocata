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



if __name__ == '__main__':

	# noms des planches sur le disque

	fourcy_10_name = "P10_To_gr.tif"
	fourcy_11_name = "P11_To_gr.tif"


	# liste de liste de tuples; ou chaque liste de tuple correspond à une planche de l'atlas de fourcy, sur cette base [ (coord Upper Left), (coord Lower Right)]
	fourcys_27571 = [];
	fourcys_3857 = [];

	fourcy_10_27571 = [fourcy_10_name, (600000, 1127424), (601000, 1126824)]
	fourcys_27571.append(fourcy_10_27571)

	fourcy_11_27571 = [fourcy_11_name, (600000, 1126824), (601000, 1126224)]
	fourcys_27571.append(fourcy_11_27571)

	for planche in fourcys_27571:
		name_planche = planche[0]
		upper_left_planche_27571 = planche[1]
		lower_right_planche_27571 = planche[2]

		# récupération des x et y du upper left
		ulx = upper_left_planche_27571[0]
		uly = upper_left_planche_27571[1]

		# récupération des x et y du lower right
		lrx = lower_right_planche_27571[0]
		lry = lower_right_planche_27571[1]

		upper_left_planche_3857 = reprojecte(ulx, uly, 27571, 3857)
		lower_right_planche_3857 = reprojecte(lrx, lry, 37571, 3857)

		fourcys_3857.append[upper_left_planche_3857, lower_right_planche_3857]


		#print ""
		#print name_planche
		#print upper_left_planche
		#print lower_right_planche
		#print ""

	print fourcys_3857