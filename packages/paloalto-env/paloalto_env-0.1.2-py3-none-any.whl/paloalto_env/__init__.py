try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)

from .paloalto_env import paloalto_api_key
from .paloalto_env import paloalto_panorama_ip
