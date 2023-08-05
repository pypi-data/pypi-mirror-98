from enum import Enum


class GfxPrimitiveType(Enum):
    kPrimitiveTriangles = 0
    kPrimitiveTriangleStrip = 1
    kPrimitiveQuads = 2
    kPrimitiveLines = 3
    kPrimitiveLineStrip = 4
    kPrimitivePoints = 5