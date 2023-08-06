# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 14:14:38 2021

@author: chris.kerklaan
"""

# Third-party imports
from osgeo import ogr

# Local imports
from .geometry import Geometry


POLYGON_COVERAGE = [
    ogr.wkbPolygon,
    ogr.wkbPolygon25D,
    ogr.wkbPolygonM,
    ogr.wkbPolygonZM,
    ogr.wkbCurvePolygon,
    ogr.wkbCurvePolygonM,
    ogr.wkbCurvePolygonZ,
    ogr.wkbCurvePolygonZM,
]

MULTIPOLYGON_COVERAGE = [
    ogr.wkbMultiPolygon,
    ogr.wkbMultiPolygon25D,
    ogr.wkbMultiPolygonM,
    ogr.wkbMultiPolygonZM,
    ogr.wkbMultiSurface,
    ogr.wkbMultiSurface,
    ogr.wkbMultiSurfaceM,
    ogr.wkbMultiSurfaceZ,
    ogr.wkbMultiSurfaceZM,
]


class Polygon(Geometry):
    ogr_coverage = POLYGON_COVERAGE

    def __init__(self, geometry: ogr.wkbPolygon = None, points: list = None):
        if points:
            geometry = self.create_polygon(points)

        super().__init__(geometry)
        self.check_type(Polygon.ogr_coverage)


class MultiPolygon(Geometry):
    ogr_coverage = MULTIPOLYGON_COVERAGE

    def __init__(self, geometry: ogr.wkbMultiPolygon = None, points: list = None):

        if points:
            geometry = self.create_multipolygon(points)
        super().__init__(geometry)
        self.check_type(MultiPolygon.ogr_coverage)


def union(geometries, geom_type=ogr.wkbMultiPolygon):
    """ create an union for multiple polygons"""

    multi = ogr.Geometry(geom_type)
    for geometry in geometries:
        multi.AddGeometryDirectly(geometry)
    return ogr.ForceTo(multi.UnionCascaded().Clone(), 3)
