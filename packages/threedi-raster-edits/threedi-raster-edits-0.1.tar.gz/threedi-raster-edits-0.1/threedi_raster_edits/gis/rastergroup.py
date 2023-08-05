# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:02:45 2021

@author: chris.kerklaan

#TODO:
    1. Write checks
"""

# Third-party imports
import numpy as np
from osgeo import gdal

# local imports
from .raster import Raster


class RasterGroup(object):
    """input is list of Raster objects,
    Params:
        align_extent: if set to True, all will be alligned to the first raster

    Message:
        check if data is aligned, is it is not request to run data aligning
        align_data: if set to True, data/nodata will also be aligned

    Note:
        input has to be aligned to be able to do calculations

    """

    def __init__(
        self,
        rasters: list,
        epsg=28992,
        nodata=-9999,
        data_type=gdal.GDT_Float32,
        np_data_type="f4",
    ):
        self.rasters = rasters
        self.names = [raster.name for raster in self.rasters]
        self.nodata = nodata
        self.epsg = epsg
        self.data_type = data_type
        self.np_data_type = np_data_type

        for name, raster in zip(self.names, self.rasters):
            setattr(self, name, raster)

    def __iter__(self):
        for raster in self.rasters:
            yield raster

    def __getitem__(self, name):
        return self.rasters[self.names.index(name)]

    def __setitem__(self, name, value):
        """ without alignemnt"""
        self.rasters[self.names.index(name)] = value

    def check_alignment(self):
        return check_alignment(self.rasters)

    def align(self):
        align_raster = self.rasters[0]
        aligned_rasters = []
        for raster in self.rasters[1:]:
            aligned_rasters.append(
                raster.align(align_raster, nodata_align=False)
            )

        aligned_rasters.insert(0, align_raster)
        self.rasters = aligned_rasters

    def insert(self, raster: Raster):
        """ inserts a raster into the group"""
        align_raster = self.rasters[0]
        raster.align(align_raster, nodata_align=False)
        self.rasters.append(raster)


def check_alignment(raster_list):
    """  checks data/nodata alignemnt and extent alignment"""
    dem = raster_list[0]

    output = {"extent": {}, "counts": {}, "location": {}, "errors": []}
    for raster in raster_list:
        # extent
        if (raster.columns, raster.rows) != (dem.columns, dem.rows):
            msg = f"{raster.name} has unqual columns and rows "
            print(msg)
            output["errors"].append(("extent", msg))
        output["extent"][raster.name] = {
            "rows": raster.rows,
            "columns": raster.columns,
        }

        # data/nodata
        output["counts"][raster.name] = count_data_nodata(raster)

        # location
        if raster.geotransform != dem.geotransform:
            msg = f"{raster.name} has not a similar geotransform as the first raster"
            print(msg)
            output["errors"].append(("location", msg))

        output["location"][raster.name] = raster.geotransform

    for key, values in output["counts"].items():
        if values != output["counts"][dem.name]:
            msg = f"{key} pixel data/nodata count not equal"
            print(msg)
            output["errors"].append(("counts", msg))

    if len(output["errors"]) == 0:
        print("RasterGroup - Check alignment found no problems")
    return output


def count_data_nodata(raster):
    """ input array has np.nan as nodata"""
    count_data = 0
    count_nodata = 0
    for data in raster:
        arr = data.array
        total_size = arr.size
        add_cnt_nodata = np.count_nonzero(np.isnan(arr))
        add_cnt_data = total_size - add_cnt_nodata
        count_nodata += add_cnt_nodata
        count_data += add_cnt_data
        del arr
    return count_data, count_nodata


def max_template(rasters=[Raster, Raster], resolution=0.5):
    """ Takes a list of Raster objects and returns the largest template"""

    x_min = 1e31
    x_max = -1e31
    y_min = 1e31
    y_max = -1e31

    for raster in rasters:

        gtt = raster.geotransform
        # xmin
        if gtt[0] < x_min:
            x_min = gtt[0]

        # xmax
        if gtt[0] + (raster.rows * gtt[1]) > x_max:
            x_max = gtt[0] + (raster.rows * gtt[1])

        # ymax
        if gtt[3] > y_max:
            y_max = gtt[3]

        # ymin
        if gtt[3] + (raster.columns * gtt[5]) < y_min:
            y_min = gtt[3] + (raster.columns * gtt[5])

    rows = (y_max - y_min) / resolution
    columns = (x_max - x_min) / resolution
    template = Raster(np.zeros((int(columns), int(rows))))
    template.geotransform = (x_min, resolution, 0.0, y_max, 0.0, -resolution)
    template.nodata_value = -9999
    return template
