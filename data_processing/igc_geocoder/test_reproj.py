try:
	from osgeo import ogr
	from osgeo import osr
except ImportError:
	import ogr
	import osr
import sys
import getopt