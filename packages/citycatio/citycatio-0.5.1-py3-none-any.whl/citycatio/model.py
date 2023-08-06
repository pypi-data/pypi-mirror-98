from . import inputs
import rasterio as rio
import geopandas as gpd
import pandas as pd
from typing import Optional
import os
import shutil


class Model:
    """Combines input data to create a complete CityCAT model

    Args:
        dem: Digital Elevation Model
        rainfall: Rainfall time series
        rainfall_polygons: Areas corresponding to rainfall series
        buildings: Areas representing buildings which are extracted from the domain
        green_areas: Areas representing permeable land cover
        friction: Areas with custom friction coefficients
        open_boundaries: Areas where the domain boundary should be open
        **kwargs: Options to pass to :class:`.inputs.Configuration`

    Attributes:
        dem (inputs.Dem)
        rainfall (inputs.Rainfall)
        configuration (inputs.Configuration)
        rainfall_polygons (inputs.RainfallPolygons)
        green_areas (inputs.GreenAreas)
        friction (inputs.Friction)
        open_boundaries (inputs.OpenBoundaries)
    """
    def __init__(
            self,
            dem: rio.MemoryFile,
            rainfall: pd.DataFrame,
            rainfall_polygons: Optional[gpd.GeoSeries] = None,
            buildings: Optional[gpd.GeoDataFrame] = None,
            green_areas: Optional[gpd.GeoDataFrame] = None,
            friction: Optional[gpd.GeoDataFrame] = None,
            open_boundaries: Optional[gpd.GeoDataFrame] = None,
            **kwargs
    ):
        self.dem = inputs.Dem(dem)
        spatial_rainfall = rainfall_polygons is not None
        if len(rainfall.columns) > 1:
            assert spatial_rainfall, 'if len(rainfall.columns) > 1, rainfall_polygons must be provided'
        if spatial_rainfall:
            assert len(rainfall.columns) == len(rainfall_polygons)
        self.rainfall = inputs.Rainfall(rainfall, spatial=spatial_rainfall)

        self.configuration = inputs.Configuration(
            **{**dict(duration=rainfall.index[-1], rainfall_zones=len(rainfall.columns),
                      spatial_rainfall=spatial_rainfall), **kwargs})

        self.rainfall_polygons = inputs.RainfallPolygons(rainfall_polygons) if rainfall_polygons is not None else None
        self.buildings = inputs.Buildings(buildings) if buildings is not None else None
        self.green_areas = inputs.GreenAreas(green_areas) if green_areas is not None else None
        self.friction = inputs.Friction(friction) if friction is not None else None
        self.open_boundaries = inputs.OpenBoundaries(open_boundaries) if open_boundaries is not None else None

    def write(self, path: str):
        """Creates all input files in the directory given by path

        Args:
            path: Directory in which to create input files, will be created if it does not exists
        """
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        self.dem.write(path)
        self.rainfall.write(path)
        self.configuration.write(path)
        if self.rainfall_polygons is not None:
            self.rainfall_polygons.write(path)
        if self.buildings is not None:
            self.buildings.write(path)
        if self.green_areas is not None:
            self.green_areas.write(path)
        if self.friction is not None:
            self.friction.write(path)
        if self.open_boundaries is not None:
            self.open_boundaries.write(path)
