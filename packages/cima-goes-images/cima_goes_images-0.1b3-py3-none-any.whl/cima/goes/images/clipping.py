import json
import numpy as np
from typing import Dict, Tuple, Any
from .data_types import LatLonRegion, TilesInfo, TileInfo

TilesDict = Dict[Tuple[int, int], Any]


def expand_region(region: LatLonRegion, lat, lon):
    return LatLonRegion(
        lat_south=region.lat_south - lat,
        lat_north=region.lat_north + lat,
        lon_west=region.lon_west - lon,
        lon_east=region.lon_east + lon,
    )


def get_width_height_pixels(
        original_width,
        original_height,
        source_region: LatLonRegion,
        clipping_region: LatLonRegion):
    original_width_lat = abs(source_region.lat_south-source_region.lat_north)
    original_height_lon = abs(source_region.lon_east-source_region.lon_west)
    clipping_width_lat = abs(clipping_region.lat_south-clipping_region.lat_north)
    clipping_height_lon = abs(clipping_region.lon_east-clipping_region.lon_west)
    width_factor = (original_width_lat - clipping_width_lat) / original_width_lat
    height_factor = (original_height_lon - clipping_height_lon) / original_height_lon
    return int(original_width * width_factor), int(original_height * height_factor)


def get_tiles(region: LatLonRegion,
              lat_step: float,
              lon_step: float,
              lat_extends: float,
              lon_extends: float,
              width: int,
              height: int,
              ) -> TilesInfo:
    tile_lat_grades = lat_step + 2 * lat_extends
    tile_lon_grades = lon_step + 2 * lon_extends
    lat_grades = abs((region.lat_south - (2 * lat_extends)) - region.lat_north)
    lon_grades = abs((region.lon_east + (2 * lon_extends)) - region.lon_west)
    pixels_lat_grade = (height / lat_grades)
    pixels_lon_grade = (width / lon_grades)

    tile_height = int(np.ceil(pixels_lat_grade * tile_lat_grades))
    tile_width = int(np.ceil(pixels_lon_grade * tile_lon_grades))

    lat_0 = region.lat_north + lat_extends
    lon_0 = region.lon_west - lon_extends

    lat_step = -lat_step
    lats = [x for x in np.arange(region.lat_north, region.lat_south, lat_step)]
    lons = [x for x in np.arange(region.lon_west, region.lon_east, lon_step)]

    tiles = []
    tiles_info = TilesInfo(
        pixels_per_lat=pixels_lat_grade,
        pixels_per_lon=pixels_lon_grade,
        image_height=height,
        image_width=width,
        tile_height=tile_height,
        tile_width=tile_width,
        tiles=tiles)

    for lat_index, lat in enumerate(lats):
        for lon_index, lon in enumerate(lons):
            north = lat + lat_extends
            west = lon - lon_extends
            y0 = int(abs(lat_0-north) * pixels_lat_grade)
            x0 = int(abs(lon_0-west) * pixels_lon_grade)
            x1 = x0 + tiles_info.tile_width
            y1 = y0 + tiles_info.tile_height
            tiles.append(TileInfo(
                lat_index=lat_index,
                lon_index=lon_index,
                north=north,
                west=west,
                x0=x0,
                y0=y0,
                x1=x1,
                y1=y1)
            )
    return tiles_info


if __name__ == '__main__':
    pass
