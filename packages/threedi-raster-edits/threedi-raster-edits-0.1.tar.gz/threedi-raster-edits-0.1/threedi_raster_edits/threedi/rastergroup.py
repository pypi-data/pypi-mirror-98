# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 16:40:16 2021

@author: chris.kerklaan


ThreediRasterGroup class checks for 3Di properties, alignment etc. 

Input:
    1. Raster dictionary with standardized names 
    2. Optional panden
    
Checks:
    1. Check alignemnt --> ALready included in rastergroups
    2. Check 3Di properties  --> Done!

Functions
    1. Convert input based on csv conversion tables
    2. Create based interception raster from panden

TODO:
    1. Finish ThreediRaster generation
    2. Write Checks
    3. 
    
Notes:
    1. Memory loading speeds up raster analysis, however is costly in memory
       Not all rasters are loaded into memory, e.g., it is not usefull to load
       a dem into memory since it is not used in conversion. 
    
"""
# First-party imports
import csv

# Third-party imports
import numpy as np
from osgeo import gdal

# local imports
from threedi_raster_edits.gis.rastergroup import RasterGroup
from threedi_raster_edits.gis.raster import Raster
from threedi_raster_edits.gis.vector import Vector
from threedi_raster_edits.utils.project import Progress


class ThreediRasterGroup(RasterGroup):
    def __init__(
        self,
        dem_path,
        landuse_path=None,
        soil_path=None,
        interception_path=None,
        friction_path=None,
        infiltration_path=None,
        buildings: Vector = None,
        epsg=28992,
        nodata_value=-9999,
        data_type=gdal.GDT_Float32,
        np_data_type="f4",
    ):

        rasters = [Raster(dem_path, name="dem")]

        if landuse_path:
            landuse = Raster(landuse_path, name="landuse")
            landuse.load_to_memory()
            rasters.append(landuse)

        if soil_path:
            soil = Raster(soil_path, name="soil")
            soil.load_to_memory()
            rasters.append(soil)

        if interception_path:
            interception = Raster(interception_path, name="interception")
            rasters.append(interception)

        if friction_path:
            friction = Raster(friction_path, name="friction")
            rasters.append(friction)

        if soil_path:
            soil = Raster(soil_path, name="soil")
            rasters.append(soil)

        if infiltration_path:
            infiltration = Raster(infiltration_path, name="infiltration")
            rasters.append(infiltration)

        RasterGroup.__init__(self, rasters)

        if buildings:
            self.buildings = buildings

        self.epsg = epsg
        self.data_type = data_type
        self.no_data_type = np_data_type
        self.nodata_value = nodata_value

    @property
    def check_tables(self):
        if not hasattr(self, "ct_soil"):
            raise AttributeError(
                """
                                 Please load soil csv using 
                                 'load_soil_conversion_table'"""
            )

        if not hasattr(self, "ct_lu"):
            raise AttributeError(
                """
                                 Please load landuse csv using 
                                 'load_landuse_conversion_table'"""
            )

    def check_properties(self):
        return check_properties(
            self.rasters,
            nodata=self.nodata,
            projection=self.epsg,
            data_type=self.data_type,
        )

    def null_raster(self):
        copy = self.dem.empty_copy()
        null_array = np.zeros((int(copy.rows), int(copy.columns)))
        null_array[~self.dem.mask] = np.nan
        copy.array = null_array
        return copy

    def load_soil_conversion_table(self, csv_soil_path):
        self.ct_soil, self.ct_soil_info = load_csv_file(csv_soil_path, "soil")

    def load_landuse_conversion_table(self, csv_lu_path):
        self.ct_lu, self.ct_lu_info = load_csv_file(csv_lu_path, "landuse")

    def generate_friction(self):
        self.friction = classify(self.landuse, "Friction", self.ct_lu)
        self.rasters.append(self.friction)

    def generate_permeability(self):
        self.permeability = classify(self.landuse, "Permeability", self.ct_lu)
        self.rasters.append(self.permeability)

    def generate_interception(self):
        self.interception = classify(self.landuse, "Interception", self.ct_lu)
        self.rasters.append(self.interception)

    def generate_crop_type(self):
        self.crop_type = classify(self.landuse, "Crop_type", self.ct_lu)
        self.rasters.append(self.crop_type)

    def generate_max_infiltration(self):
        self.max_infiltration = classify(
            self.soil, "Max_infiltration_rate", self.ct_soil
        )
        self.rasters.append(self.max_infiltration)

    def generate_infiltration(self):
        if not hasattr(self, "permeability"):
            self.generate_permeability()

        if not hasattr(self, "max_infiltration"):
            self.generate_max_infiltration()

        permeability = self.permeability.array
        max_infiltration = self.max_infiltration.array

        # calculate infiltration
        infiltration_array = np.where(
            np.logical_and(
                permeability != self.nodata_value,
                max_infiltration != self.nodata_value,
            ),
            permeability * max_infiltration,
            self.nodata_value,
        ).astype(self.np_data_type)

        empty_raster = self.null_raster()
        empty_raster.array = infiltration_array
        self.infiltration = empty_raster
        self.infiltration.name = "Infiltration"
        self.rasters.append(self.infiltration)

    def generate_hydraulic_conductivity(self):
        self.hydraulic_conductivity = classify(
            self.soil, "Hydraulic_conductivity", self.ct_soil
        )
        self.rasters.append(self.hydraulic_conductivity)

    def generate_building_interception(self, value):
        null = self.null_raster()
        value_raster = null.push_vector(self.buildings, value=value)
        self.interception = value_raster.align(
            self.dem, nodata_align=True, fill_value=0
        )
        self.interception.name = "Interception"
        self.rasters.append(self.interception)


def check_properties(
    raster_list,
    nodata=-9999,
    projection=28992,
    max_pixel_allow=1000000000,
    data_type=gdal.GDT_Float32,
    unit="metre",
    min_allow=-1000,
    max_allow=1000,
):

    # Has the raster the nodata value of -9999?
    output = {
        "nodata": {},
        "unit": {},
        "projection": {},
        "data_type": {},
        "resolution": {},
        "square_pixels": {},
        "min_max": {},
        "total_pixels": 0,
        "errors": [],
    }

    total_pixels = 0
    for raster in raster_list:

        # nodata value check
        if raster.nodata_value != nodata:
            msg = f"{raster.name} has a nodata value of {raster.nodata_value}"
            print(msg)
            output["errors"].append(("nodata_value", msg))
        output["nodata"][raster.name] = raster.nodata_value

        # unit check
        if raster.spatial_reference.unit != unit:
            msg = f"{raster.name} has not unit {unit}"
            print(msg)
            output["errors"].append(("unit", msg))
        output["unit"][raster.name] = raster.spatial_reference.unit

        # projection check
        if raster.spatial_reference.epsg != projection:
            msg = f"{raster.name} has not epsg {projection}"
            print(msg)
            output["errors"].append(("projection", msg))
        output["projection"][raster.name] = raster.spatial_reference.epsg

        # data type checl
        if raster.data_type != data_type:
            msg = f"{raster.name} is not a {gdal.GetDataTypeName(data_type)}"
            print(msg)
            output["errors"].append(("data_type", msg))
        output["data_type"][raster.name] = gdal.GetDataTypeName(data_type)

        # square pixel check
        if abs(raster.resolution["width"]) != abs(raster.resolution["height"]):
            msg = f"{raster.name} has not a square pixel"
            output["errors"].append(("width/height", msg))
        output["square_pixels"][raster.name] = raster.resolution

        # extreme value check
        _max, _min = np.nanmax(raster.array), np.nanmin(raster.array)
        if not (min_allow < _max < max_allow and min_allow < _min < max_allow):
            msg = f"{raster.name} has extreme values < {min_allow}, > {max_allow} "
            print(msg)
            output["errors"].append(("extreme_values", msg))
        output["min_max"][raster.name] = {"min": _min, "max": _max}

        total_pixels += raster.pixels

    # max pixel allowed check
    if total_pixels > max_pixel_allow:
        msg = f"Rasters combined pixels are larger than {max_pixel_allow}"
        print(msg)
        output["errors"].append(("maximum_allowed_pixels", msg))

    output["total_pixels"] = total_pixels

    if len(output["errors"]) == 0:
        print("ThreediRasterGroup - Check properties found no problems")
    return output


def load_csv_file(csv_path, csv_type="landuse"):
    csv_data = {}
    csv_info = {}
    if csv_type == "landuse":
        csv_structure = {
            1: "description",
            2: "unit",
            3: "range",
            4: "type",
        }
        meta_list = [1, 2, 3, 4]
    elif csv_type == "soil":
        csv_structure = {
            1: "description",
            2: "source",
            3: "unit",
            4: "range",
            5: "type",
        }
        meta_list = [1, 2, 3, 4, 5]

    with open(csv_path) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=";")
        for i, line in enumerate(csv_reader):

            # headers
            if i == 0:
                headers = line
                for column_value in line:
                    csv_data[column_value] = []
                    csv_info[column_value] = {}

            # units, descriptions, ranges etc.
            elif i in meta_list:

                for column_index, column_value in enumerate(line):
                    field = csv_structure[i]
                    csv_info[headers[column_index]][field] = column_value
            # csv data
            else:
                for column_index, column_value in enumerate(line):
                    column = headers[column_index]
                    column_type = csv_info[column]["type"]

                    if column_value == "":
                        csv_data[column].append(None)
                    else:
                        if column_type == "Integer":
                            column_value = int(column_value)
                        elif column_type == "Double" or column_type == "Real":
                            column_value = float(column_value)
                        elif column_type == "String":
                            column_value = str(column_value)
                        csv_data[column].append(column_value)

        return csv_data, csv_info


def classify(raster: Raster, table: str, ct: dict):
    """input is a table to classify,
    raster is the template raster,
    ct is the conversion table
    returns a dictionary of classified rasters"""

    tiles = []
    ct_codes = ct["Code"]
    pbar = Progress(raster.__len__(), f"classifying {table}")

    for tile in raster:
        array = tile.array

        # stop if nodata in array
        if np.isnan(array).all():
            tiles.append(tile)
            continue

        # Get all codes in tile
        codes = np.unique(array[~np.isnan(array)])

        # Classify tile
        output_array = np.copy(array)
        for code in codes:
            output_array[array == code] = ct[table][ct_codes.index(code)]

        # Save and append
        tile.array = output_array
        tiles.append(tile)

        # Delete array
        del array
        del output_array

        pbar.update(False)
    output = raster.merge([tile.ds for tile in tiles])
    output.name = table
    return output
