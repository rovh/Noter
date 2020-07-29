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

from bpy.app.handlers import persistent

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
def draw_text(self, text):
    text_parts_list = text.split('\n')
    layout = self.layout
    box = layout.box()
    # column.separator(factor=.5)
    col = box.column(align = 1)
    for i in text_parts_list:
        row = col.row(align = 1)
        row.label(text = i)
        row.scale_y = 0


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
        else:
            header_note = True

        action = self.action
        file_name = bpy.context.window_manager.noter.file_name
        note_text_object = bpy.context.active_object.note_text_object
        note_text_scene = bpy.context.scene.note_text_scene

        if len(bpy.data.texts.values()) == 0:
            bpy.ops.text.new()
            text = "A new text file was created"
            war = "INFO"
            self.report({war}, text)
            # return {'FINISHED'}

        try:
            main_text = bpy.data.texts[file_name].as_string()
        except KeyError:
            text = "File was not found"
            war = "ERROR"
            self.report({war}, text)
            return {'FINISHED'}

        if action == 'object':
            if header_note == True:
                bpy.context.active_object.note_text_object = main_text
            else:
                item = self.item_object(context)
                item.text = main_text

        elif action == "object_get":
            bpy.data.texts[file_name].clear()
            if header_note == True:
                bpy.data.texts[file_name].write(note_text_object)
            else:
                item = self.item_object(context)
                bpy.data.texts[file_name].write(item.text)

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
            bpy.data.texts[file_name].clear()
            if header_note == True:
                bpy.data.texts[file_name].write(note_text_scene)
            else:
                item = self.item_scene(context)
                bpy.data.texts[file_name].write(item.text)

        elif action == 'scene_delete':
            pass


        bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1)
        print("Warning because of Noter")

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

class Note_Pop_Up_Operator(bpy.types.Operator):
    bl_idname = "window_manager.note_popup_operator"
    bl_label = "Warning Panel Operator"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event): 
        # bool_warning = bpy.data.scenes[bpy.context.scene.name_full].bool_warning
        # settings = bpy.context.preferences.addons[__name__].preferences
        # bool_warning_global = settings.bool_warning_global

        x = event.mouse_x
        y = event.mouse_y 

        # move_x = 0
        # move_y = 60

        bpy.context.window.cursor_warp(0 , 1000)

        # bpy.context.window.cursor_warp(x + move_x, y + move_y)


        invoke = context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self, width=700)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_props_popup(self, event)
        # return context.window_manager.invoke_confirm(self, event)

        bpy.context.window.cursor_warp(x , y)

        return invoke
    
        # return {'FINISHED'}


    def draw(self, context):
        layout = self.layout
        layout.label(text='Warning' , icon="ERROR")

class OBJECT_PT_note(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_label = ""
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        # layout = self.layout
        # box = layout.box()
        # box.label(text = 'qqqqqqqqqqqqqqqq')
        text = bpy.context.active_object.note_text_object
        draw_text(self, text)
        



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
    Note_Pop_Up_Operator,
    OBJECT_PT_note,
]

blender_classes = Notes_list_blender_classes + blender_classes

@persistent
def load_handler(dummy):
    # print("Load Handler:", bpy.data.filepath)
    bpy.ops.screen.animation_play()

def my_handler(scene):
    # print("Frame Change", scene.frame_current)

    bpy.ops.window_manager.note_popup_operator('INVOKE_DEFAULT')

    bpy.app.handlers.frame_change_post.remove(my_handler)
    bpy.app.handlers.load_post.remove(load_handler)
    bpy.ops.screen.animation_play()
    bpy.context.scene.frame_current = 1


def register():

    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)

    # if kc:
    #     km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    #     kmi = km.keymap_items.new('mesh.change_length', 'LEFTMOUSE', 'CLICK', shift=True)
        # Could pass settings to operator properties here
        # kmi.properties.mode = (False, True, False)

    # bpy.app.handlers.depsgraph_update_post.append(my_handler)
    # bpy.app.handlers.on_scene_update_pre.append(my_handler)

    bpy.app.handlers.frame_change_post.append(my_handler)
    bpy.app.handlers.load_post.append(load_handler)


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

    if my_handler in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(my_handler)

    if my_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_handler)

    del bpy.types.Object.note_text_object
    del bpy.types.Scene.note_text_scene

    del bpy.types.Object.notes_list_object
    del bpy.types.Object.notes_list_object_index

    del bpy.types.Scene.notes_list_scene
    del bpy.types.Scene.notes_list_scene_index


if __name__ == "__main__":
    register()