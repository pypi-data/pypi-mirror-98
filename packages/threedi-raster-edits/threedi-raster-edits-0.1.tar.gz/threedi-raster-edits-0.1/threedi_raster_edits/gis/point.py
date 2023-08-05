# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 14:13:51 2021

@author: chris.kerklaan
"""
# Third-party imports
from osgeo import ogr

# Local imports
from .geometry import Geometry

# Globals
POINT_COVERAGE = [
    ogr.wkbPoint,
    ogr.wkbPoint25D,
    ogr.wkbPointM,
    ogr.wkbPointZM,
]
MULTIPOINT_COVERAGE = [
    ogr.wkbMultiPoint,
    ogr.wkbMultiPoint25D,
    ogr.wkbMultiPointM,
    ogr.wkbMultiPointZM,
]


class Point(Geometry):
    ogr_coverage = POINT_COVERAGE

    def __init__(self, geometry: ogr.wkbPoint = None, point: tuple = None):
        if point:
            geometry = self.create_point(point)

        super().__init__(geometry)
        self.check_type(Point.ogr_coverage)

    @property
    def point(self):
        return self.points[0]


class MultiPoint(Geometry):
    ogr_coverage = MULTIPOINT_COVERAGE

    def __init__(self, geometry: ogr.wkbPoint):
        super().__init__(geometry)

        if type(geometry) in [list, tuple]:
            geometry = self.create_points(geometry)
            super().__init__(geometry)

        self.check_type(MultiPoint.ogr_coverage)
