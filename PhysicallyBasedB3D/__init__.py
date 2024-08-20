"""
TODO: Subsurf handling
TODO: 
"""

from typing import Any
import bpy
from bpy.types import ShaderNodeBsdfPrincipled
from mathutils import Color

from . import ui

def assign_principled_values(node: ShaderNodeBsdfPrincipled, values: dict[str, Any]):
    """
    TODO: Check whether color is linear or sRGB
    TODO: Determine appropriate value for specular
    TODO: What about subsurf?
    """
    base_color = Color(values.get("color", (0, 0, 0)))
    node.inputs["Base Color"].default_value = tuple(base_color) + (1,) 
    node.inputs["Metallic"].default_value = values.get("metalness", 0)
    node.inputs["Roughness"].default_value = values.get("roughness", 0.5)
    node.inputs["IOR"].default_value = values.get("ior", 0.5)
    node.inputs["Transmission"].default_value = values.get("transmission", 0.0)

    # specular_color = values.get("specularColor", (1, 1, 1))
    # complex_ior = values.get("complexIor", (1,) * 6)


registered = (ui,)


def register():
    pass


def unregister():
    pass


if __name__ == "__main__":
    testfunc()
