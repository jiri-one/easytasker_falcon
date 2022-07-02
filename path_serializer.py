from tinydb_serialization import Serializer
from pathlib import Path

class PathSerializer(Serializer):
    OBJ_CLASS = Path  # The class this serializer handles

    def encode(self, obj):
        return str(obj)

    def decode(self, s):
        return Path(s)
