# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 13:05:21 2021

@author: chris.kerklaan

Note:
    Spatial references can be either projected, geographic or local
    
BUG:
    cannot set the spatial reference somehow
"""
from osgeo import osr


class SpatialReference(osr.SpatialReference):
    def __init__(self, wkt=None, standard=4326):

        if not wkt:
            print(f"No spatial reference assigned, assigning epsg {standard}")
            wkt = self.epsg_to_wkt(standard)

        if type(wkt) == int:
            print("please use SpatialReference.from_epsg")
        elif type(wkt) == osr.SpatialReference:
            print("please use SpatialReference.from_sr")

        super().__init__(wkt=wkt)

    @classmethod
    def from_epsg(cls, epsg, **kwargs):
        return cls(SpatialReference.epsg_to_wkt(epsg), **kwargs)

    @classmethod
    def from_sr(cls, sr, **kwargs):
        wkt = sr.ExportToWkt()
        return cls(wkt, **kwargs)

    @staticmethod
    def epsg_to_wkt(epsg):
        sr = osr.SpatialReference()
        sr.ImportFromEPSG(epsg)
        return sr.ExportToWkt()

    def __getitem__(self, item):
        return self.GetAttrValue(item)

    def __str__(self):
        return self.ExportToPrettyWkt()

    @property
    def wkt(self):
        return self.ExportToWkt()

    @property
    def unit(self):
        return self["UNIT"]

    @property
    def type(self):
        if self.IsProjected:
            return "PROJCS"
        elif self.IsGeographic:
            return "GEOGCS"
        elif self.IsLocal:
            return "LOCAL"
        else:
            return None

    @property
    def epsg(self):
        if self.GetAuthorityName(self.type) == "EPSG":
            return int(self.GetAuthorityCode(self.type))
        else:
            self.AutoIdentifyEPSG()
            return int(self.GetAttrValue("AUTHORITY", 1))

    def transform(self, epsg=28992):
        """ returns a transform between current projection and out_epsg"""
        return osr.CoordinateTransformation(self, SpatialReference(epsg=epsg))


if __name__ == "__main__":
    sr = SpatialReference(28992)
