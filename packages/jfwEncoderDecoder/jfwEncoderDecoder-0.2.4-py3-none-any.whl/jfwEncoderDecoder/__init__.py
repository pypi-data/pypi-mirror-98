# __init__.py
try:
    from .jfw_generator import *
    from .jfw_structs import *
    from .jfw_deserializer import deserializer
    from .jfw_serializer import serializer
except ModuleNotFoundError as err:
    print(err)

# Version of the jfw-encoder-decoder package
__version__ = "0.2.4"