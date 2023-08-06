# Reference:
# https://kavigupta.org/2019/05/18/Setting-the-size-of-figures-in-matplotlib/
from matplotlib.image import imread
from tempfile import NamedTemporaryFile
from .data_types import FigureSizeInches


def _get_size(fig, dpi=100):
    with NamedTemporaryFile(suffix='.png') as f:
        fig.savefig(f.name, bbox_inches='tight', pad_inches=0, dpi=dpi)
        height, width, _channels = imread(f.name).shape
        return width / dpi, height / dpi


def get_figure_size(fig, size, dpi=100, eps=1e-2, give_up=2, min_size_px=10):
    target_width, target_height = size
    set_width, set_height = target_width, target_height  # reasonable starting point
    deltas = []  # how far we have

    while True:
        fig.set_size_inches([set_width, set_height])
        print([set_width, set_height], [target_width, target_height])
        actual_width, actual_height = _get_size(fig, dpi=dpi)
        deltas.append(abs(actual_width - target_width) + abs(actual_height - target_height))
        if deltas[-1] < eps:
            return FigureSizeInches(
                width=set_width,
                height=set_height,
                dpi=dpi,
                pixels_width=actual_width * dpi,
                pixels_height=actual_height * dpi)

        if len(deltas) > give_up and sorted(deltas[-give_up:]) == deltas[-give_up:]:
            raise Exception('Cannot get size')
        set_width *= target_width / actual_width
        set_height *= target_height / actual_height
        if set_width * dpi < min_size_px or set_height * dpi < min_size_px:
            raise Exception('Cannot get size')
