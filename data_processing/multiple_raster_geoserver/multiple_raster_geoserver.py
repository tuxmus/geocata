# -*- coding: utf8 -*-

import sys
import os



# ou login et mdp sont les identifiants de connexion de geoserver
# et le workspace a été préalablement créé


#curl -v -u admin:geoserver -XPOST -H "Content-type: text/xml" -d "<workspace><name>geotiff_test_1</name></workspace>" http://localhost:8080/geoserver/rest/workspaces


if __name__ == '__main__':

	# usage : multiple_raster_geoserver.py rasterDirectory login mdp workspace

	# TODO : usage
	# ex : 
	# cd F:\PROJET_MAPPING\GEOCATA\data_processing\multiple_raster_geoserver
	# python multiple_raster_geoserver.py F:\PROJET_MAPPING\DATA\IGC_SARATTE\SARATTE_GEOREF_3857 admin geoserver JCS

	rasterDirectory = sys.argv[1]
	login = sys.argv[2]
	mdp = sys.argv[3]
	workspace = sys.argv[4]

	igcTifs = os.listdir(rasterDirectory)

	for raster in igcTifs:

		rasterSansExtension = raster[:-4]
	
		os.system('curl -u '+login+':'+mdp+' -XPUT -H "Content-type:image/tiff" --data-binary @'+rasterDirectory+os.sep+raster+' http://philibertaspairt.com:8080/geoserver/rest/workspaces/'+workspace+'/coveragestores/'+rasterSansExtension+'/file.geotiff ')