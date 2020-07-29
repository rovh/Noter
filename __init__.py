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

from .Notes_list import *


bl_info = {
    "name" : "Noter",
    "author" : "Rovh",
    "description" : "",
    "blender" : (2, 83, 0),
    "version" : (1, 0, 0),
    "location" : "",
    "warning" : "",
    "category" : "Interface"
}

# print(44444444444444)

class SetLength(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_length"
    bl_label = "Set Length " + name
    bl_description = 'You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut'
    # bl_options = {'REGISTER', 'UNDO'}
    bl_options = {'UNDO'}

    plus_length: bpy.props.IntProperty(options = {"SKIP_SAVE"}) 
    eyedropper: bpy.props.BoolProperty(options = {"SKIP_SAVE"})
    draw:       bpy.props.BoolProperty(options = {"SKIP_SAVE"})
    lengthbool_SKIP_SAVE: bpy.props.BoolProperty(options = {"SKIP_SAVE"})
    @classmethod
    def poll(cls, context):
        return context.active_object is not None\
            and context.active_object.mode in {'EDIT'}\
            and context.active_object.type == "MESH"

    @classmethod
    def description(cls, context, properties):
        if properties.plus_length == 1:
            return "Plus Length / Distance"
        elif properties.plus_length == -1:
            return "Minus Length / Distance"
        elif properties.eyedropper == True:
            return "Get Length / Distance"
        else:
            pass

    def execute(self, context):
        
        if self.draw == False:
            check(self) 

        # Set values
        length = bpy.context.window_manager.setprecisemesh.length
        data_block_2 = bpy.context.window_manager.setprecisemesh.data_block_2
        
        """Replace syntax"""
        data_block_2 = data_block_2.replace(',', '.')
        data_block_2 = data_block_2.replace('^', '**')
        data_block_2 = data_block_2.replace(':', '/')
        data_block_2 = data_block_2.replace('unit', str(length))
        data_block_2 = data_block_2.replace('u', str(length))
        # print(   re.search(r"\((\w+)\)", data_block_2)   )

        # data_block_2 = data_block_2.replace( 'psqrt(r(A-Za-z0-9)' , 'sqrt(r(A-Za-z0-9_])')


        script_input_2 = bpy.context.scene.script_input_2
        length_unit = bpy.context.scene.unit_settings.length_unit

class TEXT_PT_noter(Panel):
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Noter"
    # bl_category = "Text"
    bl_label = "Noter"

    

    def draw(self, context):
        noter = bpy.context.window_manager.noter
        
        layout = self.layout
        column = layout.column(align = 1)
        column.prop(noter, "file_name", text = '')

        column.separator(factor = 1)

        box = column.box()
        box.label(text = '11111111')

class Noter_Props (bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.noter
    """
    file_name: StringProperty(name = 'Name of the file',\
        default = 'Text')

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

    bpy.types.Object.notes_list_object = CollectionProperty(type=Notes_List_Collection)
    bpy.types.Object.notes_list_object_index = IntProperty()

    bpy.types.Scene.notes_list_object = CollectionProperty(type=Notes_List_Collection)
    bpy.types.Scene.notes_list_scene_index = IntProperty()
    

def unregister():

    for blender_class in blender_classes:
            bpy.utils.unregister_class(blender_class)

    del bpy.types.Object.notes_list_object
    del bpy.types.Object.notes_list_object_index
    del bpy.types.Scene.notes_list_object
    del bpy.types.Scene.notes_list_scene_index


if __name__ == "__main__":
    register()