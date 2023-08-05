try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

_VERSION = metadata.version('actomyosin-analyser')
__version__ = _VERSION
