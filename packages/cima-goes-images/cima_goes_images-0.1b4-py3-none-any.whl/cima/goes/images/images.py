import io
import os
import gc
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import matplotlib.ticker as mticker
import matplotlib.cm as cm
import cartopy
import cartopy.crs as ccrs
import numpy as np
from PIL import Image
from typing import Union
import cv2

from .data_types import ImageResolution, LatLonRegion, Grid, FigureSizeInches, Cultural
from .figure_sizing import get_figure_size


Image.MAX_IMAGE_PIXELS = 670716416

SAVE_DPI = 100


def get_image_inches(shape):
    y, x = shape
    return ImageResolution(dpi=SAVE_DPI, x=x/SAVE_DPI, y=y/SAVE_DPI)


def add_cultural(ax, cultural: Cultural):
    states_provinces = cartopy.feature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none')

    countries = cartopy.feature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_countries',
        scale='10m',
        facecolor='none')

    ax.coastlines(resolution='10m', color=cultural.color.value, linewidth=cultural.linewidth)
    ax.add_feature(countries, edgecolor=cultural.color.value, linewidth=cultural.linewidth)
    ax.add_feature(states_provinces, edgecolor=cultural.color.value, linewidth=cultural.linewidth)


def get_tile_extent(region: LatLonRegion, trim_excess=0) -> tuple:
    # (left, right, bottom, top)
    return (
        region.lon_west + trim_excess,
        region.lon_east - trim_excess,
        region.lat_south + trim_excess,
        region.lat_north - trim_excess
    )


def set_extent(ax: Axes, lonlat_region: LatLonRegion, trim_excess=0, projection=ccrs.PlateCarree()):
    extent = get_tile_extent(lonlat_region, trim_excess=trim_excess)
    ax.set_extent(extent, crs=projection)


def add_grid(ax, crs=None, grid: Grid = None):
    if crs is None:
        crs = ccrs.PlateCarree()
    grid = grid.__dict__ if grid is not None else Grid()
    step = grid.pop('step')
    top_labels = grid.pop('top_labels')
    right_labels = grid.pop('right_labels')
    grid['color'] = grid['color'].value
    grid['linestyle'] = grid['linestyle'].value
    gl = ax.gridlines(crs=crs, **grid)
    gl.xlocator = mticker.FixedLocator([x for x in range(-180, 180, step)])
    gl.ylocator = mticker.FixedLocator([x for x in range(-180, 180, step)])
    gl.top_labels = top_labels
    gl.right_labels = right_labels


def interpolate_invalid(data):
    data = np.ma.masked_invalid(data)
    data = data.filled(np.nan)
    nans = np.isnan(data)
    nz = lambda x: x.nonzero()[0]
    data[nans] = np.interp(nz(nans), nz(~nans), data[~nans])
    return data


def make_color_tuple(rgb):
    """
    Convert an 3D RGB array into an color tuple list suitable for plotting with
    pcolormesh.
    Input:
        rgb - a three dimensional array of RGB values from np.dstack([R, G, B])
    """
    # Don't use the last column of the RGB array or else the image will be scrambled!
    # This is the strange nature of pcolormesh.
    rgb = rgb[:, :-1, :]

    # Flatten the array, because that's what pcolormesh wants.
    color_tuple = rgb.reshape((rgb.shape[0] * rgb.shape[1]), 3)

    # Adding an alpha channel will plot faster, according to Stack Overflow. Not sure why.
    color_tuple = np.insert(color_tuple, 3, 1.0, axis=1)

    return color_tuple


def pcolormesh(ax: Axes, image, lons, lats, cmap='gray', vmin=None, vmax=None):
    if len(image.shape) == 3:
        color_tuple = make_color_tuple(image)
        # ax.pcolormesh(lons, lats, np.zeros_like(lons),
        #               color=color_tuple, linewidth=0)
        ax.pcolormesh(lons, lats, image[:, :, 0], color=color_tuple)
    else:
        ax.pcolormesh(lons, lats, image, cmap=cmap, vmin=vmin, vmax=vmax) # shading='gouraud'


def plot_dataset(data,
                 filepath,
                 figure_size_inches: FigureSizeInches = None,
                 shape=None,
                 cmap=None,
                 vmin=None,
                 vmax=None,
                 ):
    fig, ax = plt.subplots()
    try:
        ax.set_axis_off()
        ax.imshow(data, extent=(0, data.shape[1], 0, data.shape[0]), origin='upper', cmap=cmap, vmin=vmin, vmax=vmax)
        if figure_size_inches is None:
            if shape is None:
                shape = data.shape[:2]
            figure_size_inches = get_figure_size(
                fig, (shape[1]/SAVE_DPI, shape[0]/SAVE_DPI), dpi=SAVE_DPI, eps=0.1)
            print(figure_size_inches.__dict__)
        fig.set_size_inches([figure_size_inches.width, figure_size_inches.height])
        plt.savefig(filepath, bbox_inches='tight', pad_inches=0, dpi=figure_size_inches.dpi)
    finally:
        fig.clear()
        plt.close()
        gc.collect()


def save_figure(
        data,
        lats,
        lons,
        file: Union[str, io.BytesIO],
        region: LatLonRegion = None,
        figure_size_inches: FigureSizeInches = None,
        projection=ccrs.PlateCarree(),
        shape=None,
        cmap=None,
        vmin=None,
        vmax=None,
        format='png',
        cultural: Cultural = None,
        grid: Grid = None,
        title: str = None,
        trim_excess=0):

    # fig = plt.figure(frameon=False, dpi=SAVE_DPI)
    fig = plt.figure()
    try:
        # Interpolate invalid values to fix pcolormesh errors
        lats = interpolate_invalid(lats)
        lons = interpolate_invalid(lons)

        if projection is not None:
            ax = fig.add_subplot(1, 1, 1, projection=projection)
            if region is not None:
                set_extent(ax, region, trim_excess, projection=projection)
        else:
            ax = fig.add_subplot(1, 1, 1)

        ax.set_axis_off()

        if cultural is not None:
            add_cultural(ax, cultural)
        if grid is not None:
            add_grid(ax, crs=projection, grid=grid)
        if title is not None:
            ax.title.set_text(title)
        ax.axis('off')

        pcolormesh(ax, data, lons, lats, cmap=cmap, vmin=vmin, vmax=vmax)

        if projection is not None:
            fig.add_axes(ax, projection=projection)
        else:
            fig.add_axes(ax)

        if figure_size_inches is None:
            if shape is None:
                shape = data.shape[:2]
            figure_size_inches = get_figure_size(
                fig, (shape[1]/SAVE_DPI, shape[0]/SAVE_DPI), dpi=SAVE_DPI, eps=0.1)
            print(figure_size_inches.__dict__)
        fig.set_size_inches([figure_size_inches.width, figure_size_inches.height])
        plt.savefig(file, bbox_inches='tight', pad_inches=0, dpi=figure_size_inches.dpi)
    finally:
        fig.clear()
        plt.close()
        gc.collect()


def get_figure_stream(
        data,
        lats,
        lons,
        region: LatLonRegion = None,
        figure_size_inches: FigureSizeInches = None,
        projection=ccrs.PlateCarree(),
        format='png',
        shape=None,
        cmap=None,
        vmin=None,
        vmax=None,
        cultural: Cultural = None,
        grid: Grid = None,
        trim_excess=0):
    buffer = io.BytesIO()
    save_figure(
        data=data,
        lats=lats,
        lons=lons,
        file=buffer,
        region=region,
        figure_size_inches=figure_size_inches,
        projection=projection,
        format=format,
        shape=shape,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        cultural=cultural,
        grid=grid,
        trim_excess=trim_excess)
    buffer.seek(0)
    return buffer


def upload_stream(stream, filepath):
    directory = os.path.dirname(filepath)
    if not directory:
        directory = './'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filepath, mode='w+b') as f:
        f.write(stream.read())


def save_image(data,
               filepath: str,
               lats, lons,
               lonlat_region: LatLonRegion = None,
               format=None,
               upload_stream=upload_stream,
               cmap=None,
               vmin=None,
               vmax=None,
               draw_cultural=False,
               grid: Grid = None,
               trim_excess=0):
    if format is None:
        format = 'png'
        _, file_extension = os.path.splitext(filepath)
        if file_extension[0] == '.':
            format = file_extension[1:]
    figure = get_figure_stream(data, lats, lons, lonlat_region, format=format, cmap=cmap, vmin=vmin, vmax=vmax,
                               draw_cultural=draw_cultural, grid=grid, trim_excess=trim_excess)
    upload_stream(figure, filepath)
    figure.seek(0)
    return figure


def get_pil_image(
        image,
        lats,
        lons,
        region: LatLonRegion,
        cmap=None,
        vmin=None,
        vmax=None,
        draw_cultural=False,
        draw_grid=False,
        trim_excess=0):
    image_stream = get_figure_stream(image,
                                     lats=lats,
                                     lons=lons,
                                     region=region,
                                     cmap=cmap,
                                     vmin=vmin,
                                     vmax=vmax,
                                     draw_cultural=draw_cultural,
                                     draw_grid=draw_grid,
                                     trim_excess=trim_excess)
    return Image.open(image_stream)


def pil2cv(pil_image: Image):
    return np.array(pil_image.convert('RGB'))[:, :, ::-1].copy()
    # return np.array(pil_image)[:, :, ::-1].copy()


def cv2pil(cv_image: Image):
    img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)


def pil2stream(pil_image):
    stream = io.BytesIO()
    pil_image.save(stream, 'PNG')
    stream.seek(0)
    return stream


def stream2cv(image_stream, flags=cv2.IMREAD_COLOR):
    image_stream.seek(0)
    np_image = np.asarray(bytearray(image_stream.read()), dtype="uint8")
    return cv2.imdecode(np_image, flags)


def cv2stream(cv_image):
    pil_image = cv2pil(cv_image)
    return pil2stream(pil_image)


def stream2pil(image_stream) -> Image:
    image_stream.seek(0)
    return Image.open(image_stream).convert('RGB')


def contrast_correction(color, contrast):
    """
    Modify the contrast of an R, G, or B color channel
    See: #www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-5-contrast-adjustment/
    Input:
        C - contrast level
    """
    F = (259 * (contrast + 255)) / (255. * 259 - contrast)
    COLOR = F * (color - .5) + .5
    COLOR = np.minimum(COLOR, 1)
    COLOR = np.maximum(COLOR, 0)
    return COLOR


def get_true_colors(red, veggie, blue):
    # Turn empty values into nans
    red[red == -1] = np.nan
    veggie[veggie == -1] = np.nan
    blue[blue == -1] = np.nan

    R = np.maximum(red, 0)
    R = np.minimum(R, 1)
    G = np.maximum(veggie, 0)
    G = np.minimum(G, 1)
    B = np.maximum(blue, 0)
    B = np.minimum(B, 1)

    gamma = 0.4
    R = np.power(R, gamma)
    G = np.power(G, gamma)
    B = np.power(B, gamma)

    G_true = 0.48358168 * R + 0.45706946 * B + 0.06038137 * G
    G_true = np.maximum(G_true, 0)
    G_true = np.minimum(G_true, 1)

    contrast = 125
    return contrast_correction(np.dstack([R, G_true, B]), contrast)


def plot_colormap(colormap):
    a = np.outer(np.arange(0, 1, 0.01), np.ones(10))
    fig = plt.figure(figsize=(10, 5))
    fig.subplots_adjust(top=0.8, bottom=0.05, left=0.01, right=0.99)
    # maps = [m for m in cm.datad if not m.endswith("_r")]
    maps = [colormap]
    maps.sort()
    l = len(maps) + 1
    for i, m in enumerate(maps):
        ax = plt.subplot(1, l, i+1)
        ax.axis("off")
        ax.imshow(a, aspect='auto', cmap=cm.get_cmap(m), origin="lower")
    plt.savefig("colormaps.png", dpi=100, facecolor='gray')