# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 16:52:22 2021

@author: chris.kerklaan
"""

# system imports

# Third-party imports

# Local imports
from .fields import Fields, GeometryFields
from .geometries import convert_geometry


class Feature:
    """wrapper of ogr feature

    Edits to geometry and fields are never set, just do object['field']
    to set the field
    """

    def __init__(self, feature, layer=None, set_feature=True):
        self.ptr = feature

        if feature:
            self.exists = True
        else:
            self.exists = False
            raise IndexError("Feature does not exsist, try Vector.fids")
        self.set_feature = set_feature

        if layer:
            self.layer = layer
            self.layer_defn = self.layer.GetLayerDefn()
            self.fields = Fields(self.layer)

    def __setitem__(self, key, value):
        self.ptr.SetField(key, value)
        if hasattr(self, "layer") and self.set_feature:
            self.layer.SetFeature(self)

    def __getitem__(self, key):
        return self.ptr.GetField(key)

    def copy(self):
        return Feature(self.ptr.Clone())

    @property
    def fid(self):
        return self.ptr.GetFID()

    @fid.setter
    def fid(self, value):
        self.ptr.SetFID(value)

    @property
    def geometry(self):
        geom = self.ptr.geometry()
        if geom:
            return convert_geometry(geom)

        geom = self.ptr.GetGeomFieldRef(1)
        if geom:
            return convert_geometry(geom)

    @geometry.setter
    def geometry(self, value):
        self.ptr.SetGeometry(value)

    @property
    def items(self):
        return self.ptr.items()

    @property
    def id(self):
        return self.fid

    @property
    def spatial_reference(self):
        return self.geometry.spatial_reference

    @property
    def geometry_fields(self):
        return GeometryFields(self.ptr)

    def simplify(self, wkb_threshold, start=10000000, quiet=False):
        """ simplifying a geometry to a wkb size threshold"""
        geometry = self.geometry
        while geometry.WkbSize() > wkb_threshold:
            geometry = geometry.simply(1 / start)
            start = start / 10
        return geometry

    def reproject(self, out_epsg):
        return self.geometry.reproject(out_epsg)
