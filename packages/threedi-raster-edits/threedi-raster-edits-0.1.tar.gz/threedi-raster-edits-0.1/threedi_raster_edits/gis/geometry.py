# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 13:49:48 2021

@author: chris.kerklaan

Wrapper for an ogr geometry


"""
# Third-party imports
from osgeo import ogr

# Local imports
from .spatial_reference import SpatialReference

# GLOBALS
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
        geometry, _ = fix_geometry(geometry)
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
        return fix_geometry(self)

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

    def copy(self):
        return Geometry(geometry=self)

    def reproject(self, out_epsg):
        geometry = self.copy()
        transform = geometry.spatial_reference.transform(out_epsg)
        geometry.Transform(transform)
        return geometry

    def create_point(self, points, flatten=True):
        output_geom = ogr.Geometry(ogr.wkbPoint)
        output_geom.AddPoint(*points)
        if flatten:
            output_geom.FlattenTo2D()
        return output_geom

    def create_multipoint(self, points, flatten=True):
        output_geom = ogr.Geometry(ogr.wkbMultiPoint)
        for point in points:
            point_geometry = ogr.Geometry(ogr.wkbPoint)
            point_geometry.AddPoint(*point)
            output_geom.AddGeometry(point_geometry)
        if flatten:
            output_geom.FlattenTo2D()
        return output_geom

    def create_line(self, points, flatten=True):
        output_geom = ogr.Geometry(self.type)
        for point in points:
            output_geom.AddPoint(*point)
        if flatten:
            output_geom.FlattenTo2D()
        return output_geom

    def create_multiline(self, points, flatten=True):
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


def convert_geometry(geometry):
    """converts geometry to 1 to 6"""
    geom_type = geometry.GetGeometryType()
    if geom_type in [1, 2, 3, 4, 5, 6]:
        return geometry

    if geom_type in [
        ogr.wkbCurvePolygon,
        ogr.wkbCurvePolygonM,
        ogr.wkbCurvePolygonZ,
        ogr.wkbCurvePolygonZM,
    ]:
        geometry = geometry.GetLinearGeometry()

    elif geom_type in [
        ogr.wkbMultiSurface,
        ogr.wkbMultiSurfaceM,
        ogr.wkbMultiSurfaceZ,
        ogr.wkbMultiSurfaceZM,
    ]:
        geometry = ogr.ForceToMultiPolygon(geometry)

    return geometry


def fix_geometry(geometry):
    """
    First converts a geometry to type 1,2,3,4,5,6
    Fixes a geometry to ogr geom types 1,2,3,4,5,6:
        1. pointcount for  linestrings
        2. self intersections for polygons
        3. 3D polygon

    Params:
        geometry : ogr geometry
    Returns
        geometry: ogr geometry or None if no geometry is present
        bool: geometry validity


    """
    if geometry is None:
        return None, False

    geometry = convert_geometry(geometry)
    if geometry.IsValid():
        return geometry, True

    geometry = geometry.MakeValid()
    if geometry.IsValid():
        return geometry, True

    geom_type = geometry.GetGeometryType()
    if geom_type == ogr.wkbPoint:
        pass
    elif geom_type == ogr.wkbLineString:
        if geometry.GetPointCount() == 1:
            print("Geometry point count of linestring = 1")
            return geometry, False

    elif geom_type == ogr.wkbPolygon:
        geometry = geometry.Buffer(0)

    elif geom_type == ogr.wkbMultiPoint:
        pass

    elif geom_type == ogr.wkbMultiLineString:
        pass

    elif geom_type == ogr.wkbMultiPolygon:
        pass

    geom_type = geometry.GetGeometryType()
    geom_name = ogr.GeometryTypeToName(geom_type)

    if "3D" in geom_name:
        geometry.FlattenTo2D()

    if not geometry.IsValid():
        print(
            f"Could not fix invalid ogr geometry type: {geom_name}, {geom_type}"
        )

    return geometry, geometry.IsValid()


def clip(geometry: ogr.Geometry, mask: ogr.Geometry, output_type: int):
    """clips a single geometry on a mask
    Checks for single and multiparts and leaves invalid geometries
    returns a list of clipped geometry or None
    """
    geometry, valid = fix_geometry(geometry)
    if not valid:
        return

    if geometry.Intersects(mask.Boundary()):
        intersect = geometry.Intersection(mask)
        intersect, valid = fix_geometry(intersect)
        if not valid:
            return

        intersect_type = intersect.GetGeometryType()
        if intersect_type != output_type:
            return

        if intersect_type > 3 or intersect_type < 0:  # multiparts
            geometries = []
            for geometry_part in intersect:
                geometry_part, valid = fix_geometry(geometry_part)
                if not valid:
                    return

                geometry_part_type = geometry_part.GetGeometryType()
                if geometry_part_type != output_type:
                    return

                geometries.append(geometry_part)
            return geometries

        else:
            return [intersect]

    elif geometry.Within(mask):
        return [geometry]
    else:
        return  # outside


def difference(geometry: ogr.Geometry, mask: ogr.Geometry):
    """ checks if intersects or valid before doing difference"""
    geometry, valid = fix_geometry(geometry)
    if not valid:
        return

    if not geometry.Intersects(mask):
        return

    if geometry.Intersects(mask):
        geometry = geometry.Difference(mask)

        geometry, valid = fix_geometry(geometry)
        if not valid:
            return
    return geometry


def dissolve(multigeometry: ogr.Geometry):
    """ dissolves a multigeometry into a single geometry"""
    multigeometry, valid = fix_geometry(multigeometry)

    if not valid:
        return
    geometry_type = multigeometry.GetGeometryType()
    if geometry_type == ogr.wkbMultiPolygon:
        union = multigeometry.UnionCascaded()
    else:
        union = ogr.Geometry(geometry_type)
        for geometry in multigeometry:
            union = union.Union(geometry)
    return union


if __name__ == "__main__":
    pass
