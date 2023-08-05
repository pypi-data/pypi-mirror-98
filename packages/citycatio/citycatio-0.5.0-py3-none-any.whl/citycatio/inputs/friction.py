import geopandas as gpd
from ..utils import geoseries_to_string
import os


class Friction:
    """Areas with custom friction coefficients"""
    def __init__(self, data: gpd.GeoDataFrame):
        assert type(data) == gpd.GeoDataFrame
        self.data = data

    def write(self, path):
        with open(os.path.join(path, 'FrictionCoeffs.txt'), 'w') as f:
            f.write(geoseries_to_string(self.data.geometry, index=True, index_first=False))
