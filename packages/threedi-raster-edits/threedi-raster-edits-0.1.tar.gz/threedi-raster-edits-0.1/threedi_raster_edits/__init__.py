try:
    from osgeo import ogr
except ImportError:
    raise (""" ERROR: Could not find the GDAL/OGR Python library bindings. 
               On anaconda, use conda install gdal >= 3.2.0
               otherwise look at https://pypi.org/project/GDAL/""") 
               
    