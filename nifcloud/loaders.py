"""NIFCLOUD data loader configuration.

Configures botocore's data loader to use NIFCLOUD-specific
service model data path.
"""

import os

from botocore import loaders

loaders.Loader.BUILTIN_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
