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

class Note_Actions(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "window_manager.export_note_text"
    bl_label = "note text actions"
    bl_description = 'You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut'
    # bl_options = {'REGISTER', 'UNDO'}
    bl_options = {'UNDO'}

    action: StringProperty(options = {"SKIP_SAVE"})
    header_note: BoolProperty(options = {"SKIP_SAVE"}, default = True)
    # draw:       bpy.props.BoolProperty(options = {"SKIP_SAVE"})
    # lengthbool_SKIP_SAVE: bpy.props.BoolProperty(options = {"SKIP_SAVE"})
    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None\
    #         and context.active_object.mode in {'EDIT'}\
            # and context.active_object.type == "MESH"

    # @classmethod
    # def description(cls, context, properties):
    #     if properties.plus_length == 1:
    #         return "Plus Length / Distance"
    #     elif properties.plus_length == -1:
    #         return "Minus Length / Distance"
    #     elif properties.eyedropper == True:
    #         return "Get Length / Distance"
    #     else:
    #         pass

    def item_object(self, context):
        act_obj = context.active_object
        idx = act_obj.notes_list_object_index

        try:
            item = act_obj.notes_list_object[idx]
        except IndexError:
            pass
        return item

    def item_scene(self, context):
        scene = context.scene
        idx = scene.notes_list_scene_index

        try:
            item = scene.notes_list_scene[idx]
        except IndexError:
            pass

        return item


    def execute(self, context):

        if self.action.count("*") != 0:
            self.action = self.action.replace("*", "")
            header_note = False

        action = self.action
        note_text_object = bpy.context.active_object.note_text_object
        note_text_scene = bpy.context.scene.note_text_scene

        main_text = bpy.data.texts['Text'].as_string()

        # action = 'object'

        if action == 'object':
            if header_note == True:
                bpy.context.active_object.note_text_object = main_text
            else:
                item = self.item_object(context)
                item.text = main_text

        elif action == "object_get":
            bpy.data.texts['Text'].clear()
            if header_note == True:
                bpy.data.texts['Text'].write(note_text_object)
            else:
                item = self.item_object(context)
                bpy.data.texts['Text'].write(item.text)

        elif action == "object_delete":
            if header_note == True:
                bpy.context.active_object.note_text_object = ""
            else:
                item = self.item_object(context)
                item.text = ""



        elif action == 'scene':
            if header_note == True:
                bpy.context.active_object.note_text_object = main_text
            else:
                item = self.item_scene(context)
                item.text = main_text

        elif action == 'scene_get':
            pass

        elif action == 'scene_delete':
            pass



        return {'FINISHED'}
        

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
        col = box.column(align = 1)
        col.operator("window_manager.export_note_text", text = 'Object', icon = 'OBJECT_DATAMODE').action = "object"
        col.operator("window_manager.export_note_text", text = '', icon = 'FILE_TICK').action = "object_get"
        col.operator("window_manager.export_note_text", text = '', icon = 'TRASH').action = "object_delete"

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
    Note_Actions,
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

    bpy.types.Object.note_text_object = StringProperty()
    bpy.types.Scene.note_text_scene = StringProperty()

    bpy.types.WindowManager.noter = PointerProperty(type=Noter_Props)

    bpy.types.Object.notes_list_object = CollectionProperty(type=Notes_List_Collection)
    bpy.types.Object.notes_list_object_index = IntProperty()

    bpy.types.Scene.notes_list_scene = CollectionProperty(type=Notes_List_Collection)
    bpy.types.Scene.notes_list_scene_index = IntProperty()
    
def unregister():

    for blender_class in blender_classes:
            bpy.utils.unregister_class(blender_class)

    del bpy.types.Object.note_text_object
    del bpy.types.Scene.note_text_scene

    del bpy.types.Object.notes_list_object
    del bpy.types.Object.notes_list_object_index
    del bpy.types.Scene.notes_list_object
    del bpy.types.Scene.notes_list_scene_index


if __name__ == "__main__":
    register()