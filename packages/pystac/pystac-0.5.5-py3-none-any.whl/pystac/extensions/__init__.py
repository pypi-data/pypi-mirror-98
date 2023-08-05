# flake8: noqa
from enum import Enum


class ExtensionError(Exception):
    """An error related to the construction of extensions.
    """
    pass


class Extensions(str, Enum):
    """Enumerates the IDs of common extensions."""
    def __str__(self):
        return str(self.value)

    CHECKSUM = 'checksum'
    COLLECTION_ASSETS = 'collection-assets'
    DATACUBE = 'datacube'
    EO = 'eo'
    ITEM_ASSETS = 'item-assets'
    LABEL = 'label'
    POINTCLOUD = 'pointcloud'
    PROJECTION = 'projection'
    SAR = 'sar'
    SAT = 'sat'
    SCIENTIFIC = 'scientific'
    SINGLE_FILE_STAC = 'single-file-stac'
    TILED_ASSETS = 'tiled-assets'
    TIMESTAMPS = 'timestamps'
    VERSION = 'version'
    VIEW = 'view'
    FILE = 'file'
