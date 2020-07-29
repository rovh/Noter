import bpy

# from .__init__ import draw_text

from bpy.types import (
        Panel,
        PropertyGroup,
        Operator,
        UIList,
        )

from bpy.props import (
        FloatProperty,
        BoolProperty,
        PointerProperty,
        EnumProperty,
        StringProperty,
        IntProperty,
        CollectionProperty,
        )

from .Notes_list import Notes_list_blender_classes


bl_info = {
    "name" : "Noter",
    "author" : "Rovh",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

# print(44444444444444)

class TEXT_PT_noter(Panel):
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Noter"
    # bl_category = "Text"
    bl_label = "Noter"

    def draw(self, context):
        layout = self.layout
        layout.label(text = '11111111111')

class Noter_Props (bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.noter
    """
    file_name: StringProperty()

blender_classes = [
    TEXT_PT_noter,
    Noter_Props,
]

blender_classes = Notes_list_blender_classes + blender_classes

def register():

    # if kc:
    #     km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    #     kmi = km.keymap_items.new('mesh.change_length', 'LEFTMOUSE', 'CLICK', shift=True)
        # Could pass settings to operator properties here
        # kmi.properties.mode = (False, True, False)

    # bpy.app.handlers.depsgraph_update_post.append(my_handler)
    # bpy.app.handlers.on_scene_update_pre.append(my_handler)

    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)

    bpy.types.WindowManager.noter = PointerProperty(type=Noter_Props)

def unregister():

    for blender_class in blender_classes:
            bpy.utils.unregister_class(blender_class)


if __name__ == "__main__":
    register()