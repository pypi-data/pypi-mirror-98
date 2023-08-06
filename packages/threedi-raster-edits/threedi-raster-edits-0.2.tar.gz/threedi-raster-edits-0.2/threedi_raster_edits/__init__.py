try:
    from osgeo import ogr
except ImportError:
    raise (
        """ ERROR: Could not find the GDAL/OGR Python library bindings. 
               On anaconda, use conda install gdal >= 3.2.0
               otherwise look at https://pypi.org/project/GDAL/"""
    )

# gis
from .gis.raster import Raster
from .gis.rastergroup import RasterGroup
from .gis.vector import Vector
from .gis.linestring import LineString, MultiLineString
from .gis.polygon import Polygon, MultiPolygon
from .gis.point import Point, MultiPoint

# Threedi
from .threedi.rastergroup import RasterGroup as ThreediRasterGroup

# Lizard
from .lizard.rextract import RasterExtraction
