try:
    from importlib import metadata
except (ImportError, ModuleNotFoundError):
    import importlib_metadata as metadata

help = "Show current postal version"

def arguments(parser):
    pass

def main(args=None):
    print(metadata.version('docker-postal'))
