import json
from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class FigureSizeInches:
    width: float
    height: float
    dpi: int
    pixels_width: int
    pixels_height: int


@dataclass
class RegionIndexes:
    x_min: int = None
    x_max: int = None
    y_min: int = None
    y_max: int = None


@dataclass
class ImageResolution:
    dpi: int
    x: float
    y: float


@dataclass
class LatLonRegion:
    lat_north: float
    lat_south: float
    lon_west: float
    lon_east: float


@dataclass
class SatBandKey:
    sat_height: float
    sat_lon: float
    sat_sweep: float


@dataclass
class TileInfo:
    lat_index: int
    lon_index: int
    north: float
    west: float
    x0: int
    y0: int
    x1: int
    y1: int


@dataclass
class TilesInfo:
    pixels_per_lat: float
    pixels_per_lon: float
    image_height: int
    image_width: int
    tile_height: int
    tile_width: int
    tiles: List[TileInfo]

    def json_for_images(self):
        data = {
            'pixels_per_lat': self.pixels_per_lat,
            'pixels_per_lon': self.pixels_per_lon,
            'tile_height': self.tile_height,
            'tile_width': self.tile_width,
            'tiles': {f'{x.lon_index}_{x.lat_index}': {'north': x.north, 'west': x.west} for x in self.tiles}
        }
        return json.dumps(data, indent=2)


class Color(Enum):
    ALICEBLUE = 'aliceblue',
    ANTIQUEWHITE = 'antiquewhite',
    AQUA = 'aqua',
    AQUAMARINE = 'aquamarine',
    AZURE = 'azure',
    BEIGE = 'beige',
    BISQUE = 'bisque',
    BLACK = 'black',
    BLANCHEDALMOND = 'blanchedalmond',
    BLUE = 'blue',
    BLUEVIOLET = 'blueviolet',
    BROWN = 'brown',
    BURLYWOOD = 'burlywood',
    CADETBLUE = 'cadetblue',
    CHARTREUSE = 'chartreuse',
    CHOCOLATE = 'chocolate',
    CORAL = 'coral',
    CORNFLOWERBLUE = 'cornflowerblue',
    CORNSILK = 'cornsilk',
    CRIMSON = 'crimson',
    CYAN = 'cyan',
    DARKBLUE = 'darkblue',
    DARKCYAN = 'darkcyan',
    DARKGOLDENROD = 'darkgoldenrod',
    DARKGRAY = 'darkgray',
    DARKGREEN = 'darkgreen',
    DARKGREY = 'darkgrey',
    DARKKHAKI = 'darkkhaki',
    DARKMAGENTA = 'darkmagenta',
    DARKOLIVEGREEN = 'darkolivegreen',
    DARKORANGE = 'darkorange',
    DARKORCHID = 'darkorchid',
    DARKRED = 'darkred',
    DARKSALMON = 'darksalmon',
    DARKSEAGREEN = 'darkseagreen',
    DARKSLATEBLUE = 'darkslateblue',
    DARKSLATEGRAY = 'darkslategray',
    DARKSLATEGREY = 'darkslategrey',
    DARKTURQUOISE = 'darkturquoise',
    DARKVIOLET = 'darkviolet',
    DEEPPINK = 'deeppink',
    DEEPSKYBLUE = 'deepskyblue',
    DIMGRAY = 'dimgray',
    DIMGREY = 'dimgrey',
    DODGERBLUE = 'dodgerblue',
    FIREBRICK = 'firebrick',
    FLORALWHITE = 'floralwhite',
    FORESTGREEN = 'forestgreen',
    FUCHSIA = 'fuchsia',
    GAINSBORO = 'gainsboro',
    GHOSTWHITE = 'ghostwhite',
    GOLD = 'gold',
    GOLDENROD = 'goldenrod',
    GRAY = 'gray',
    GREEN = 'green',
    GREENYELLOW = 'greenyellow',
    GREY = 'grey',
    HONEYDEW = 'honeydew',
    HOTPINK = 'hotpink',
    INDIANRED = 'indianred',
    INDIGO = 'indigo',
    IVORY = 'ivory',
    KHAKI = 'khaki',
    LAVENDER = 'lavender',
    LAVENDERBLUSH = 'lavenderblush',
    LAWNGREEN = 'lawngreen',
    LEMONCHIFFON = 'lemonchiffon',
    LIGHTBLUE = 'lightblue',
    LIGHTCORAL = 'lightcoral',
    LIGHTCYAN = 'lightcyan',
    LIGHTGOLDENRODYELL = 'lightgoldenrodyell'
    LIGHTGRAY = 'lightgray',
    LIGHTGREEN = 'lightgreen',
    LIGHTGREY = 'lightgrey',
    LIGHTPINK = 'lightpink',
    LIGHTSALMON = 'lightsalmon',
    LIGHTSEAGREEN = 'lightseagreen',
    LIGHTSKYBLUE = 'lightskyblue',
    LIGHTSLATEGRAY = 'lightslategray',
    LIGHTSLATEGREY = 'lightslategrey',
    LIGHTSTEELBLUE = 'lightsteelblue',
    LIGHTYELLOW = 'lightyellow',
    LIME = 'lime',
    LIMEGREEN = 'limegreen',
    LINEN = 'linen',
    MAGENTA = 'magenta',
    MAROON = 'maroon',
    MEDIUMAQUAMARINE = 'mediumaquamarine',
    MEDIUMBLUE = 'mediumblue',
    MEDIUMORCHID = 'mediumorchid',
    MEDIUMPURPLE = 'mediumpurple',
    MEDIUMSEAGREEN = 'mediumseagreen',
    MEDIUMSLATEBLUE = 'mediumslateblue',
    MEDIUMSPRINGGREEN = 'mediumspringgreen',
    MEDIUMTURQUOISE = 'mediumturquoise',
    MEDIUMVIOLETRED = 'mediumvioletred',
    MIDNIGHTBLUE = 'midnightblue',
    MINTCREAM = 'mintcream',
    MISTYROSE = 'mistyrose',
    MOCCASIN = 'moccasin',
    NAVAJOWHITE = 'navajowhite',
    NAVY = 'navy',
    OLDLACE = 'oldlace',
    OLIVE = 'olive',
    OLIVEDRAB = 'olivedrab',
    ORANGE = 'orange',
    ORANGERED = 'orangered',
    ORCHID = 'orchid',
    PALEGOLDENROD = 'palegoldenrod',
    PALEGREEN = 'palegreen',
    PALETURQUOISE = 'paleturquoise',
    PALEVIOLETRED = 'palevioletred',
    PAPAYAWHIP = 'papayawhip',
    PEACHPUFF = 'peachpuff',
    PERU = 'peru',
    PINK = 'pink',
    PLUM = 'plum',
    POWDERBLUE = 'powderblue',
    PURPLE = 'purple',
    REBECCAPURPLE = 'rebeccapurple',
    RED = 'red',
    ROSYBROWN = 'rosybrown',
    ROYALBLUE = 'royalblue',
    SADDLEBROWN = 'saddlebrown',
    SALMON = 'salmon',
    SANDYBROWN = 'sandybrown',
    SEAGREEN = 'seagreen',
    SEASHELL = 'seashell',
    SIENNA = 'sienna',
    SILVER = 'silver',
    SKYBLUE = 'skyblue',
    SLATEBLUE = 'slateblue',
    SLATEGRAY = 'slategray',
    SLATEGREY = 'slategrey',
    SNOW = 'snow',
    SPRINGGREEN = 'springgreen',
    STEELBLUE = 'steelblue',
    TAN = 'tan',
    TEAL = 'teal',
    THISTLE = 'thistle',
    TOMATO = 'tomato',
    TURQUOISE = 'turquoise',
    VIOLET = 'violet',
    WHEAT = 'wheat',
    WHITE = 'white',
    WHITESMOKE = 'whitesmoke',
    YELLOW = 'yellow',
    YELLOWGREEN = 'yellowgreen'


class LineStyle(Enum):
    SOLID = 'solid',
    DASHED = 'dashed',
    DASHDOT = 'dashdot',
    DOTTED = 'dotted'


@dataclass
class Grid:
    step: float = 1
    color: Color = Color.BLACK
    linestyle: LineStyle = LineStyle.SOLID
    linewidth: float = 0.1
    draw_labels: bool = False
    top_labels: bool = False
    right_labels: bool = False


@dataclass
class Cultural:
    color: Color = Color.WHITE
    linestyle: LineStyle = LineStyle.SOLID
    linewidth: float = 0.1


