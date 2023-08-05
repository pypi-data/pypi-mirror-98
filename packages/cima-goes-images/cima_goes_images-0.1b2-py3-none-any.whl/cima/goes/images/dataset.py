import netCDF4
import numpy as np
import pyproj
from .data_types import RegionIndexes, SatBandKey


def to_albedo(data):
    new_data = (data * np.pi * 0.3) / 663.274497
    new_data = np.clip(new_data, 0, 1)
    return np.power(new_data, 1.5)


def get_dataset_from_file(filepath: str) -> netCDF4.Dataset:
    with open(filepath, mode='rb') as f:
        data = f.read()
    return netCDF4.Dataset("in_memory_file", memory=data)


def get_data(dataset: netCDF4.Dataset, indexes: RegionIndexes = None, variable: str = None):
    if variable is None:
        if 'CMI' in dataset.variables:
            variable = 'CMI'
        elif 'Rad' in dataset.variables:
            variable = 'Rad'
    if indexes is None:
        data = dataset.variables[variable][:, :]
    else:
        data = dataset.variables[variable][indexes.y_min: indexes.y_max, indexes.x_min: indexes.x_max]
    data.units = dataset.variables[variable].units
    data.long_name = dataset.variables[variable].long_name
    data.name = variable
    return data


def get_dataset_key(dataset: netCDF4.Dataset) -> SatBandKey:
    imager_projection = dataset['goes_imager_projection']
    sat_height = imager_projection.perspective_point_height
    sat_lon = imager_projection.longitude_of_projection_origin
    sat_sweep = imager_projection.sweep_angle_axis
    return SatBandKey(
        sat_height=sat_height,
        sat_lon=sat_lon,
        sat_sweep=sat_sweep,
    )


def get_lats_lons(dataset: netCDF4.Dataset, indexes: RegionIndexes = None):
    dataset_key = get_dataset_key(dataset)
    if indexes is None:
        x = dataset['x'][:] * dataset_key.sat_height
        y = dataset['y'][:] * dataset_key.sat_height
    else:
        x = dataset['x'][indexes.x_min: indexes.x_max] * dataset_key.sat_height
        y = dataset['y'][indexes.y_min: indexes.y_max] * dataset_key.sat_height
    XX, YY = np.meshgrid(np.array(x), np.array(y))
    projection = pyproj.Proj(proj='geos', h=dataset_key.sat_height, lon_0=dataset_key.sat_lon,
                             sweep=dataset_key.sat_sweep)
    lons, lats = projection(XX, YY, inverse=True)
    return np.array(lats), np.array(lons)


