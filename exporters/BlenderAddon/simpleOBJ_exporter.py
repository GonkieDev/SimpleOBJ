"""
---------------------------------------------------------------------------------------------------------------
                                                Meta Info
---------------------------------------------------------------------------------------------------------------
"""
bl_info = {
    "name" : "Simple OBJ Exporter",
    "author" : "gsp, Goncalo Pestana",
    "description" : "Blender exporter for a simple file format called 'SimpleOBJ'.",
    "blender" : (3, 6, 4),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Import-Export",
    "location": "File > Export > SimpleOBJ Exporter",
}


"""
---------------------------------------------------------------------------------------------------------------
                                                Main
---------------------------------------------------------------------------------------------------------------
"""
import bpy

class SimpleOBJExportSettings:
    file_ext = ".sobj"


def SimpleOBJExporterMain(context, filepath, sobj_settings):
    print("running write_some_data...")
    print(f"OBJ NAME: {sobj_settings.object}")
    # f = open(filepath, 'w', encoding='utf-8')
    # f.write("Hello World %s" % use_some_setting)
    # f.close()

    return {'FINISHED'}


"""
---------------------------------------------------------------------------------------------------------------
                                                Menus
---------------------------------------------------------------------------------------------------------------
"""

from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       CollectionProperty)
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper


class SimpleOBJExporter(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    # important since its how bpy.ops.simpoleobj.export is constructed
    # NOTE(gsp): cannot have capital characters apparrently
    bl_idname = "simpleobj.export"  
    bl_label = "SimpleOBJ Export"

    filename_ext = SimpleOBJExportSettings.file_ext

    filter_glob: StringProperty(
        default="*" + filename_ext,
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    use_setting: BoolProperty(
        name="Test b ool",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    objectName: EnumProperty(
        name="Object",
        description="Object to export",
        items= tuple((i.name, i.name, '') for i in bpy.context.selectable_objects if i.type == 'MESH'),
    )

    def execute(self, context):
        sobj_settings = {
            "object": bpy.data.objects[self.objectName]
        }
        print(sobj_settings["object"].name)
        return SimpleOBJExporterMain(context, self.filepath, sobj_settings)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(SimpleOBJExporter.bl_idname, text="Text Export Operator")


# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(SimpleOBJExporter)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(SimpleOBJExporter)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.simpleobj.export('INVOKE_DEFAULT')
