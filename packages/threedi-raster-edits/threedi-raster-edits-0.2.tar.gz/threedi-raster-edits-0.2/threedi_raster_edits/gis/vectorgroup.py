# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 16:45:07 2021

@author: chris.kerklaan
"""

# First-party imports
import os
import pathlib

# Third-party imports
from osgeo import ogr

# Local imports
from .vector import Vector, mem_ds, driver_extension_mapping


# globals
OGR_MEM_DRIVER = ogr.GetDriverByName("Memory")


class VectorGroup:
    def __init__(
        self,
        path=None,
        ogr_ds=None,
        dictionary=None,
        options={},
        memory=True,
        write=False,
    ):
        """ vector groups, if write == True, object gets loaded in memory"""

        if path:
            self.ext = pathlib.Path(path).suffix
            self.ds = ogr.Open(path, write, **options)
        elif dictionary:
            self.ds = ogr.Open(pg_string(**dictionary), write)
        elif ogr_ds:
            self.ds = ogr_ds
        else:
            self.ds = mem_ds()

        if memory:
            self.ds = self.load_to_memory(self.ds)

    def __getitem__(self, i):
        return Vector(ogr_ds=self.ds, layer_name=i)

    @property
    def layers(self):
        return [layer.GetName() for layer in self.ds]

    @property
    def drivers(self):
        return driver_extension_mapping()

    def add(self, vector, name):
        new_layer = self.ds.CopyLayer(vector.layer, name)
        new_layer = None

    def add_styling(self, vector, name="layer_styles"):
        """ add styling to the gpkg by adding the layer_styles column"""
        self.add(vector, name)

    def clear(self):
        for table in self:
            table.delete_all()

    def load_to_memory(self, ds):
        new_ds = OGR_MEM_DRIVER.CopyDataSource(ds, "")
        ds = None
        return new_ds

    def write(self, path):
        driver_name = self.drivers[os.path.splitext(path)[-1]]
        driver = ogr.GetDriverByName(driver_name)
        out_db = driver.CopyDataSource(self.ds, path)
        out_db.Destroy()


def pg_string(host, port, user, password, dbname):
    return ("PG:host={} port={} user='{}'" "password='{}' dbname='{}'").format(
        host, port, user, password, dbname
    )
