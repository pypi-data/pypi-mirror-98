import functools
import os
import numpy as np

from .load_cpt import load_cpt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm


LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def _get_cloud_tops_palette():
    filepath = os.path.join(LOCAL_BASE_PATH, 'smn_topes.cpt')
    cpt = load_cpt(filepath)
    return LinearSegmentedColormap('cpt', cpt)


def cmap(c_map, rgb_order=False):
    """
    Extract colormap color information as a LUT compatible with cv2.applyColormap().
    Default channel order is BGR.

    Args:
        cmap_name: string, name of the colormap.
        rgb_order: boolean, if false or not set, the returned array will be in
                   BGR order (standard OpenCV format). If true, the order
                   will be RGB.

    Returns:
        A numpy array of type uint8 containing the colormap.
    """

    rgba_data = cm.ScalarMappable(cmap=c_map).to_rgba(
        np.arange(0, 1.0, 1.0 / 256.0), bytes=True
    )
    rgba_data = rgba_data[:, 0:-1].reshape((256, 1, 3))

    # Convert to BGR (or RGB), uint8, for OpenCV.
    cmap = np.zeros((256, 1, 3), np.uint8)

    if not rgb_order:
        cmap[:, :, :] = rgba_data[:, :, ::-1]
    else:
        cmap[:, :, :] = rgba_data[:, :, :]

    return cmap


cmap = functools.lru_cache(maxsize=200)(cmap)

CLOUD_TOPS_PALETTE = _get_cloud_tops_palette()
CV2_CLOUD_TOPS_PALETTE = cmap(CLOUD_TOPS_PALETTE)



