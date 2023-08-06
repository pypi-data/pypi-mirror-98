# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 13:49:48 2021

@author: chris.kerklaan

Wrapper for an ogr geometry

TODO:
    1. Convert/fix geometry should have an input geom_type and a target_geom_type

"""
# First-party imports
import logging

# Third-party imports
from osgeo import ogr

# Local imports
from .spatial_reference import SpatialReference

# GLOBALS
logger = logging.getLogger(__name__)

POLYGON = "POLYGON (({x1} {y1},{x2} {y1},{x2} {y2},{x1} {y2},{x1} {y1}))"
POINT = "POINT ({x1} {y1})"
LINESTRING = "LINESTRING ({x1} {y1}, {x2} {y2})"

TRANSLATION = {
    "point": ogr.wkbPoint,
    "line": ogr.wkbLineString,
    "polygon": ogr.wkbPolygon,
    "multipoint": ogr.wkbMultiPoint,
    "multiline": ogr.wkbMultiLineString,
    "multiPolygon": ogr.wkbMultiPolygon,
}

SINGLE_TYPES = {
    6: 3,
    5: 2,
    4: 1,
    3: 3,
    2: 2,
    1: 1,
}  # polygon  # linestring  # point

MULTI_TYPES = {
    1: 4,
    2: 5,
    3: 6,
    4: 4,
    5: 5,
    6: 6,
}

SINGLE_TYPES_INVERT = dict(map(reversed, SINGLE_TYPES.items()))
SINGLE_TO_MULTIPLE = {1: [1, 4], 2: [2, 5], 3: [3, 6], 4: [4], 5: [5], 6: [6]}


class Geometry(ogr.Geometry):
    """
    Extension of an ogr geometry

    Copies the input of a geomtry, hence the pointer connection is lost
    and geometries must be set via set_feature

    Every function always leaves the original geometry untouched

    Geometry is fixed as much as possible

    """

    def __init__(self, geometry, geometry_type=ogr.wkbPoint):
        geometry, _ = fix(geometry)
        super().__init__(wkb=geometry.ExportToWkb())
        self.AssignSpatialReference(geometry.GetSpatialReference())

    def check_type(self, types):
        if not self.type in types:
            raise TypeError(f"Wrong ogr geom type {self.name} {self.type}")

    @property
    def area(self):
        return self.GetArea()

    @property
    def name(self):
        return self.GetGeometryName()

    @property
    def type(self):
        return self.GetGeometryType()

    @property
    def valid(self):
        return self.IsValid()

    @property
    def fixed(self):
        return fix(self)

    @property
    def points(self):
        return self.GetPoints()

    @property
    def envelope(self):
        return self.GetEnvelope()

    @property
    def wkt(self):
        return self.ExportToWkt()

    @property
    def wkb(self):
        return self.ExportToWkb()

    @property
    def wkb_size(self):
        return self.WkbSize()

    @property
    def point_on_surface(self):
        return self.PointOnSurface()

    @property
    def centroid(self):
        return Geometry(self.Centroid())

    @property
    def spatial_reference(self):
        return SpatialReference(sr=self.GetSpatialReference())
    
    @property
    def ogr(self):
        """ returns a pure ogr geometry"""
        return release(self)

    @spatial_reference.setter
    def spatial_reference(self, sr_input):
        """ takes an epsg or a spatial_reference input"""
        if type(sr_input) == int:
            sr_input = SpatialReference(epsg=sr_input)

        self.AssignSpatialReference(sr_input)

    def buffer(self, size):
        return Geometry(self.Buffer(size))

    def difference(self, geometry):
        return Geometry(self.Difference(geometry))

    def simplify(self, simplification):
        return Geometry(self.Simplify(simplification))

    def clip(self, mask):
        clipped = clip(self, mask, self.type)
        if clipped:
            return [Geometry(i) for i in clipped]
        else:
            return 
        
    def copy(self):
        return Geometry(geometry=self)

    def reproject(self, out_epsg):
        geometry = self.copy()
        transform = geometry.spatial_reference.transform(out_epsg)
        geometry.Transform(transform)
        return geometry

    def create_point(self, points, flatten=True):
        """ takes tuple points and creates an ogr point"""
        output_geom = ogr.Geometry(ogr.wkbPoint)
        output_geom.AddPoint(*points)
        if flatten:
            output_geom.FlattenTo2D()
        return output_geom

    def create_multipoint(self, points, flatten=True):
        """ takes list of tuple points and creates an ogr multipoint"""
        output_geom = ogr.Geometry(ogr.wkbMultiPoint)
        for point in points:
            point_geometry = ogr.Geometry(ogr.wkbPoint)
            point_geometry.AddPoint(*point)
            output_geom.AddGeometry(point_geometry)
        if flatten:
            output_geom.FlattenTo2D()
        return output_geom

    def create_line(self, points, flatten=True):
        """ takes list of tuple points and creates an ogr linestring"""
        output_geom = ogr.Geometry(ogr.wkbLineString)
        for point in points:
            output_geom.AddPoint(*point)
        if flatten:
            output_geom.FlattenTo2D()
        return output_geom

    def create_multiline(self, points, flatten=True):
        """ takes list of tuple points and creates an ogr multilinestring"""

        output_geom = ogr.Geometry(ogr.wkbMultiLineString)

        # check if input is a single linestring
        if type(points[0]) == tuple:
            points = [[point] for point in points]

        for point in points:
            line = ogr.Geometry(ogr.wkbLineString)
            for p in point:
                line.AddPoint(*p)
            output_geom.AddGeometry(line)
        if flatten:
            output_geom.FlattenTo2D()
        return output_geom
    
    def create_polygon(self, points, flatten=True, close=True):
        """ takes list of tuple points and creates an ogr polygon"""

        output_geom = ogr.Geometry(ogr.wkbPolygon)
          
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for point in points:
            ring.AddPoint(*point)
            
        output_geom.AddGeometry(ring)
        
        if close:
            output_geom.CloseRings()
            
        if flatten:
            output_geom.FlattenTo2D()
            
        if not output_geom.IsValid():
            
            logger.warning("""
                            Is it a self-intersection polygon?
                            Are the points in the form a ring? E.g., 
                            left-upper, left-lower, right-lower, right-upper""")
        
        return output_geom
    
def release(geometry:ogr.Geometry):
    """ releases the c pointer from the geometry"""
    return ogr.CreateGeometryFromWkb(geometry.ExportToWkb())

def convert_geometry(geometry, target_geom_type):
    """converts geometry to target type"""
    geom_type = geometry.GetGeometryType()
    if geom_type in [1, 2, 3, 4, 5, 6]:
        return geometry

    if geom_type in [
        ogr.wkbCurvePolygon,
        ogr.wkbCurvePolygonM,
        ogr.wkbCurvePolygonZ,
        ogr.wkbCurvePolygonZM,
    ]:
        geometry = geometry.GetLinearGeometry() # to polygon

    elif geom_type in [
        ogr.wkbMultiSurface,
        ogr.wkbMultiSurfaceM,
        ogr.wkbMultiSurfaceZ,
        ogr.wkbMultiSurfaceZM,
    ]:
        geometry = ogr.ForceToMultiPolygon(geometry) # multi
    elif geom_type in [
        ogr.wkbGeometryCollection,
        ogr.wkbGeometryCollection25D,
        ogr.wkbGeometryCollectionM,
        ogr.wkbGeometryCollectionZM
        ]:
        logger.debug("Found a geometry collection, setting to target geometry")
        for geom in geometry:   
            if geom.GetGeometryType() == target_geom_type:
                geometry = geom
                break
        
    return geometry


def fix(geometry, target_geom_type=None):
    """
    First converts a geometry to type 1,2,3,4,5,6
    Fixes a geometry to ogr geom types 1,2,3,4,5,6:
        1. pointcount for  linestrings
        2. self intersections for polygons
        3. 3D polygon
        
    if a geometry collection is given, it can convert to a geom_type by
    setting geom_type = something

    Params:
        geometry : ogr geometry
    Returns
        geometry: ogr geometry or None if no geometry is present
        bool: geometry validity


    """
    if geometry is None:
        return None, False
    
    
    if not target_geom_type:
        target_geom_type = geometry.GetGeometryType()
    
        
    geometry = convert_geometry(geometry, target_geom_type)

    if geometry.IsValid():
        return geometry, True
    
    # Transformsm multipolugon into geometry collection
    #geometry = geometry.MakeValid()
    #if geometry.IsValid():
        #return geometry, True

    geom_type = geometry.GetGeometryType()
    if geom_type == ogr.wkbPoint:
        pass
    elif geom_type == ogr.wkbLineString:
        if geometry.GetPointCount() == 1:
            logger.debug("Geometry point count of linestring = 1")
            return geometry, False

    elif geom_type == ogr.wkbPolygon:
        geometry = geometry.Buffer(0)

    elif geom_type == ogr.wkbMultiPoint:
        pass

    elif geom_type == ogr.wkbMultiLineString:
        pass

    elif geom_type == ogr.wkbMultiPolygon:
        geometry = geometry.Buffer(0)

    geom_type = geometry.GetGeometryType()
    geom_name = ogr.GeometryTypeToName(geom_type)

    if geometry.Is3D():
        geometry.FlattenTo2D()

    if not geometry.IsValid():
        logger.warning(
            f"Could not fix invalid ogr geometry type: {geom_name}, {geom_type}"
            )
    return geometry, geometry.IsValid()

def multipart_to_singlepart(geometry:ogr.Geometry):
    """ returns a list of geometries, if invalid none"""
    geometry, valid = fix(geometry)

    if not valid: 
        logger.debug("Invalid geometry")
        return 

    if "MULTI" in geometry.GetGeometryName():
        
    ## release geometry from pointer
        return [release(part) for part in geometry]
    else:
        return [geometry]

def clip(geometry: ogr.Geometry, mask: ogr.Geometry, output_type: int):
    """Clips a single geometry on a mask
       returns in valid geoms as none
       returns a geometry of the output type
       returns a list
    """
    geometry, valid = fix(geometry)
    if not valid: 
        logger.debug("Invalid geometry")
        return

    if geometry.Intersects(mask.Boundary()):
        intersect = geometry.Intersection(mask)
        intersect_type = intersect.GetGeometryType()
        if intersect_type not in SINGLE_TO_MULTIPLE[output_type]:
            logger.debug("Output has incorrect geometry type")
            return
        return multipart_to_singlepart(intersect)
    
    elif geometry.Within(mask):
        return [geometry]
    else:
        return  # outside


def difference(geometry: ogr.Geometry, mask: ogr.Geometry):
    """ checks if intersects or valid before doing difference"""
    geometry, valid = fix(geometry)
    if not valid:
        logger.debug("Invalid geometry")
        return

    if not geometry.Intersects(mask):
        return

    if geometry.Intersects(mask):
        geometry = geometry.Difference(mask)

    return geometry


def dissolve(multigeometry: ogr.Geometry):
    """ dissolves a multigeometry into a single geometry"""
    multigeometry, valid = fix(multigeometry)
    if not valid:
        logger.debug("Invalid geometry")
        return
    
    geometry_type = multigeometry.GetGeometryType()
    if geometry_type == ogr.wkbMultiPolygon:
        union = multigeometry.UnionCascaded()
    else:
        union = ogr.Geometry(geometry_type)
        for geometry in multigeometry:
            union = union.Union(geometry)
    return union

