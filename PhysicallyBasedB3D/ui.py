# from itertools import count
# import bpy
# from bpy.types import Context


try:
    from . import pbreader
except:
    import pbreader


def _create_data_enum(self, ctx, datatype: str = "materials"):
    enum = []
    # Read data and format relevant fields in enum
    data = pbreader.load_cached_data(datatype)
    for item in data:
        for category in item["category"]:
            value = f"{category}/{item.get('name')}"
            name = value
            description = item.get("description", "")
            enum.append([value, name, description])

    # Sort by name and add index
    enum = sorted(enum, key=lambda i: i[0])
    for i, item in enumerate(enum):
        item.append(i)

    return enum


def register():
    pass


def unregister():
    pass


if __name__ == "__main__":
    material_enum = _create_data_enum(None, None)
    for mat in material_enum:
        print(mat)

