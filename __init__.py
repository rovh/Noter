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
from .Nodes import *

import random

# from . import Image


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

    @classmethod
    def description(cls, context, properties):
        if properties.action == 'object':
            return "Plus Length / Distance"
        elif properties.action == 'object_get':
            return "Minus Length / Distance"
        elif properties.action == 'object_delete':
            return "Get Length / Distance"


        elif properties.action == 'scene':
            return "Get Length / Distance"
        elif properties.action == 'scene_delete':
            return "Get Length / Distance"
        elif properties.action == 'scene_delete':
            return "Get Length / Distance"


        elif properties.action == 'blender':
            return "Get Length / Distance"
        elif properties.action == 'blender_get':
            return "Get Length / Distance"
        elif properties.action == 'blender_delete':
            return "Get Length / Distance"


        elif properties.action == 'splash_screen':
            return "Get Length / Distance"
        elif properties.action == 'splash_screen_get':
            return "Get Length / Distance"
        elif properties.action == 'splash_screen_delete':
            return "Get Length / Distance"
        else:
            pass
 
    def execute(self, context):       

        action = self.action
        header_note = self.header_note

        # if action == 'object_get*' or\
        #     action == 'scene_get*' or\
        #     action == 'object*' or\
        #     action == 'scene*':
        #     self.window(context)

        if action.count("*") != 0:
            action = self.action.replace("*", "")
            header_note = False
        else:
            header_note = True

       

        if (action == 'object' or\
            action == 'object_get' or\
            action == 'object_delete') and\
            context.active_object is None:
            # len(bpy.context.selected_objects) != 0 and\
                # pass
        # else:
                text = "No Object was found"
                war = "ERROR"
                self.report({war}, text)
                return {'FINISHED'}


        
        # else:
        #     text = "No Object was found"
        #     war = "ERROR"
        #     self.report({war}, text)
        #     return {'FINISHED'}

        file_name = bpy.context.window_manager.noter.file_name
        note_text_object = bpy.context.active_object.note_text_object
        note_text_scene = bpy.context.scene.note_text_scene
        note_text_blender = bpy.context.scene.note_text_blender
        note_text_splash_screen = bpy.context.scene.note_text_splash_screen

        # bpy.data.texts.tag(bpy.context.space_data)
        # bpy.data.texts.find()
        # bpy.context.space_data.text.name = file_name
        # if bpy.context.space_data.text.name != file_name:
        #     for i in bpy.context.space_data.text.name:
        #         if i == file_name:
        #             # bpy.context.space_data.text = i
        #             # bpy.data.texts[i].name = i
        #             bpy.data.texts.get(bpy.context.space_data)
        #             # print(i, 111111111111111)
        #             break

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
                print(11111111111111111111111111111111)
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
                bpy.context.scene.note_text_scene = main_text
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
            if header_note == True:
                bpy.context.scene.note_text_scene = ""
            else:
                item = self.item_scene(context)
                item.text = ""



        elif action == 'blender':
            if header_note == True:
                for i in bpy.data.scenes:
                    i.note_text_blender = main_text
            else:
                item = self.item_object(context)
                item.text = main_text

        elif action == "blender_get":
            bpy.data.texts[file_name].clear()
            if header_note == True:
                bpy.data.texts[file_name].write(note_text_blender)
            else:
                item = self.item_object(context)
                bpy.data.texts[file_name].write(item.text)

        elif action == "blender_delete":
            if header_note == True:
                for i in bpy.data.scenes:
                    i.note_text_blender = ""
            else:
                item = self.item_object(context)
                item.text = ""


        
        elif action == 'splash_screen':
            if header_note == True:
                for i in bpy.data.scenes:
                    i.note_text_splash_screen = main_text   
            else:
                item = self.item_object(context)
                item.text = main_text

        elif action == "splash_screen_get":
            bpy.data.texts[file_name].clear()
            if header_note == True:
                bpy.data.texts[file_name].write(note_text_splash_screen)
            else:
                item = self.item_object(context)
                bpy.data.texts[file_name].write(item.text)

        elif action == "splash_screen_delete":
            if header_note == True:
                for i in bpy.data.scenes:
                    i.note_text_splash_screen = ""  
            else:
                item = self.item_object(context)
                item.text = ""



        # elif action == 'node':
        #     if header_note == True:
        #         bpy.context.active_object.note_text_object = main_text
        #     else:
        #         print(11111111111111111111111111111111)
        #         item = self.item_object(context)
        #         item.text = main_text

        # elif action == "node_get":
        #     bpy.data.texts[file_name].clear()
        #     if header_note == True:
        #         bpy.data.texts[file_name].write(note_text_object)
        #     else:
        #         item = self.item_object(context)
        #         bpy.data.texts[file_name].write(item.text)
                
        # elif action == "node_delete":
        #     if header_note == True:
        #         bpy.context.active_object.note_text_object = ""
        #     else:
        #         item = self.item_object(context)
        #         item.text = ""


        bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1)
        print("Warning because of Noter")

        return {'FINISHED'}
       


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

    def window(self, context):
        # Call user prefs window
        # bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        # # Change area type
        # area = bpy.context.window_manager.windows[-1].screen.areas[0]
        # area.type = 'TEXT_EDITOR'
            
        # Copy context member
        context = bpy.context.copy()
        # context = bpy.context.window.workspace.copy()
        # context = bpy.data.screens['Default'].copy()
        # context =  bpy.context.window.workspace
        # context = bpy.data.workspaces['Scripting'].copy()
        # print(bpy.context.window.screen.areas.data)

        stop_space = False
        # # Iterate through the areas
        for area in bpy.context.screen.areas:
            if area.type == ('TEXT_EDITOR'):
                stop_space = True
                break
        # for area in bpy.context.window.screen.areas:
        #     if area.type == ('TEXT_EDITOR'):
        #         stop_space = True
        #         break
            

        if stop_space == False:
            for area in bpy.context.screen.areas:
                    # if area.type in ('IMAGE_EDITOR', 'VIEW_3D', 'NODE_EDITOR'):
                if area.type in ('PROPERTIES', 'EMPTY' 'VIEW_3D', 'NODE_EDITOR'):
                    
                    old_area = area.type        # Store current area type
                    area.type = 'TEXT_EDITOR'  # Set the area to the Image editor
                    # context['area'] = area      # Override the area member
                    context['area'] = area
                    bpy.ops.screen.area_dupli(context, 'INVOKE_DEFAULT')
                    # bpy.ops.wm.window_duplicate(context, 'INVOKE_DEFAULT')
                    area.type = old_area        # Restore the old area
                    break 

        # bpy.context.area.spaces.active.type = 'IMAGE_EDITOR'

class TEXT_PT_noter(Panel):
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Noter"
    bl_label = "Noter"

    def draw(self, context):
        noter = bpy.context.window_manager.noter
        
        layout = self.layout
        column = layout.column(align = 1)
        column.prop(noter, "file_name", text = '')

        column.separator(factor = 1)

        box = column.box()
        box.label(text = "Header Note", icon = 'TOPBAR')

        box = column.box()
        col = box.column(align = 1)
        col.operator("window_manager.export_note_text", text = 'Object', icon = 'OBJECT_DATAMODE').action = "object"
        col.operator("window_manager.export_note_text", text = '', icon = 'FILE_TICK').action = "object_get"
        col.operator("window_manager.export_note_text", text = '', icon = 'TRASH').action = "object_delete"

        box = column.box()
        col = box.column(align = 1)
        col.operator("window_manager.export_note_text", text = 'Scene', icon = 'SCENE_DATA').action = "scene"
        col.operator("window_manager.export_note_text", text = '', icon = 'FILE_TICK').action = "scene_get"
        col.operator("window_manager.export_note_text", text = '', icon = 'TRASH').action = "scene_delete"

        box = column.box()
        col = box.column(align = 1)
        col.operator("window_manager.export_note_text", text = 'File (.blend)', icon = 'BLENDER').action = "blender"
        col.operator("window_manager.export_note_text", text = '', icon = 'FILE_TICK').action = "blender_get"
        col.operator("window_manager.export_note_text", text = '', icon = 'TRASH').action = "blender_delete"

        # box = column.box()
        # col = box.column(align = 1)
        # col.operator("node.noter_operator", text = 'Node', icon = 'NODE').action = "node"
        # col.operator("node.noter_operator", text = '', icon = 'FILE_TICK').action = "node_get"
        # col.operator("node.noter_operator", text = '', icon = 'TRASH').action = "node_delete"


        box = column.box()
        col = box.column(align = 1)
    
        # settings = bpy.context.preferences.addons[__name__].preferences
        # col.prop (bpy.context.space_data, 'splash_screen', text = 'Show Splash Screen')
        # col.prop (settings, 'splash_screen', text = 'Show Splash Screen')
        # col.prop (bpy.context.scene, 'splash_screen', text = 'Show Splash Screen')
        # if bpy.context.space_data.splash_screen == True:
        col.separator(factor = 1)
        
        row = col.row(align = 1)
        find = False
        for i in bpy.data.scenes:
            if i.splash_screen == True:
                find = True
                break
        row.operator("window_manager.global_bool", text = 'Splash Screen', icon = 'WINDOW', depress= find)
        row.alignment = 'RIGHT'
        row.scale_x = .5

        col.separator(factor = 1)
        if bpy.context.scene.splash_screen == True:
            col.operator("window_manager.export_note_text", text = 'Splash Screen', icon = 'WINDOW').action = "splash_screen"
            col.operator("window_manager.export_note_text", text = '', icon = 'FILE_TICK').action = "splash_screen_get"
            col.operator("window_manager.export_note_text", text = '', icon = 'TRASH').action = "splash_screen_delete"

class Global_Bool(Operator):
    """Tooltip"""
    bl_idname = "window_manager.global_bool"
    bl_label = "111"
    bl_description = 'You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut'
    # bl_options = {'REGISTER', 'UNDO'}
    bl_options = {'UNDO'}

    
    def execute(self, context):
        
        if bpy.context.scene.splash_screen == True:
            for i in bpy.data.scenes:
                i.splash_screen = False
        else:
            for i in bpy.data.scenes:
                i.splash_screen = True

            # print(i.name_full)
        return {'FINISHED'}



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

class Note_Pop_Up_Operator(Operator):
    bl_idname = "window_manager.note_popup_operator"
    bl_label = "Noter Splash Screen"

    location_cursor: BoolProperty(default = True, options = {"SKIP_SAVE"})

    @classmethod
    def poll(cls, context):
        find = False
        for i in bpy.data.scenes:
            if i.splash_screen == True:
                find = True
                break

        return find


    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text='' , icon="MOUSE_LMB_DRAG")
        row.alignment = 'RIGHT'

        row_text = layout.row(align = 1)
        # row_text.scale_y = 0.2
        row_text.scale_x = 0.6

        ic = ['MATCUBE',
            'ANTIALIASED',
            'COLLAPSEMENU',
            'OUTLINER_DATA_LIGHTPROBE',
            'MESH_CYLINDER',
            'META_PLANE',
            'SOLO_ON',
            'FILE_BLEND',
            'OUTLINER_OB_POINTCLOUD',
            'SEQ_CHROMA_SCOPE',
            'MATSPHERE',
            'AUTO',
            'FREEZE',
            'FUND',
            'COLORSET_02_VEC',
            'MONKEY',
            'SHADING_SOLID',
            'BRUSH_TEXFILL',
        ]

        ic = random.choice(ic)

        def label_draw(length):
            for i in range(0, length):
                column_text.label(icon = ic)


        column_text = row_text.column(align = 1)
        column_text.separator(factor = 1.7)
        column_text.scale_y = .6
        label_draw(4)


        column_text = row_text.column(align = 1)
        column_text.scale_x = .8
        column_text.separator(factor = 1.8)
        label_draw(1)

        column_text = row_text.column(align = 1)
        column_text.scale_x = .8
        column_text.separator(factor = 3)
        label_draw(1)

        column_text = row_text.column(align = 1)
        column_text.scale_x = .8
        column_text.separator(factor = 5)
        label_draw(1)


        column_text = row_text.column(align = 1)
        column_text.scale_y = .6
        column_text.separator(factor = 1.7)
        label_draw(4)



        row_text.separator(factor = 7)


        column_text = row_text.column(align = 1)
        column_text.scale_y = .5
        column_text.scale_x = .8
        column_text.separator(factor = 5)
        label_draw(3)

        column_text = row_text.column(align = 1)
        label_draw(1)
        column_text.separator(factor = 3.5)
        label_draw(1)

        column_text = row_text.column(align = 1)
        label_draw(1)
        column_text.separator(factor = 3.5)
        label_draw(1)

        column_text = row_text.column(align = 1)
        column_text.scale_y = .5
        column_text.separator(factor = 5)
        label_draw(3)



        row_text.separator(factor = 5)



        column_text = row_text.column(align = 1)
        label_draw(1)

        column_text = row_text.column(align = 1)
        label_draw(1)

        column_text = row_text.column(align = 1)
        column_text.separator(factor = .9)
        column_text.scale_y = .7
        label_draw(4)

        column_text = row_text.column(align = 1)
        label_draw(1)

        column_text = row_text.column(align = 1)
        label_draw(1)



        row_text.separator(factor = 6)


        column_text = row_text.column(align = 1)
        column_text.scale_y = .51
        column_text.separator(factor = 2 )
        label_draw(5)

        column_text = row_text.column(align = 1)
        column_text.scale_y = 1
        label_draw(3)

        column_text = row_text.column(align = 1)
        column_text.scale_y = 1
        label_draw(3)


        # col_f = layout.column_flow(columns=3, align=False)
        # col_f = layout.grid_flow(row_major=1, columns=1, even_columns=False, even_rows=0, align=1)
        # for i in range(0, 10):
            # col_f.label(icon = 'SHADING_SOLID')
        # col_f.label(icon = 'SHADING_SOLID')



        # materials = [mat for mat in bpy.data.materials]
        # tex = bpy.data.textures['.hidden']
        # tex = img.jpg
        # layout.template_preview(tex)

        # text = bpy.context.window_manager.noter.note_text_blender
        for i in bpy.data.scenes:
            if bool(i.note_text_splash_screen) == True:
                find = i.note_text_splash_screen
                break

        text = find
        if bool(text) == True:
            draw_text(self, text)

    def invoke(self, context, event): 
        # bool_warning = bpy.data.scenes[bpy.context.scene.name_full].bool_warning
        # settings = bpy.context.preferences.addons[__name__].preferences
        # bool_warning_global = settings.bool_warning_global
        height = bpy.context.area.spaces.data.height
        width = bpy.context.area.spaces.data.width

        self.location_cursor = False
        if self.location_cursor == True:
            return context.window_manager.invoke_props_dialog(self)
        else:
            x = event.mouse_x
            y = event.mouse_y 

            # location_x = height / 100 * 50
            # location_y = width / 100 * 40
            location_x = 300
            location_y = 550

            bpy.context.window.cursor_warp(location_x , location_y)

            # bpy.context.window.cursor_warp(x + move_x, y + move_y)


            invoke = context.window_manager.invoke_props_dialog(self)
            # return context.window_manager.invoke_popup(self, width=700)
            # return context.window_manager.invoke_popup(self)
            # return context.window_manager.invoke_props_popup(self, event)
            # return context.window_manager.invoke_confirm(self, event)

            bpy.context.window.cursor_warp(x , y)

            return invoke

        # return {'FINISHED'}

class Note_Pop_Up_Operator_2 (Operator):
    bl_idname = "window_manager.note_popup_operator_2"
    bl_label = "Noter Pop-up Menu"

    location_cursor: BoolProperty(default = True, options = {"SKIP_SAVE"})

    @classmethod
    def poll(cls, context):
        find = False
        for i in bpy.data.scenes:
            if bool(i.note_text_blender) == True:
                find = True
                break

        return find

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        for i in bpy.data.scenes:
            if bool(i.note_text_blender) == True:
                find = i.note_text_blender
                break

        text = find
        # text = bpy.context.scene.note_text_blender
        if bool(text) == True:
            draw_text(self, text)

    def invoke(self, context, event): 
        # bool_warning = bpy.data.scenes[bpy.context.scene.name_full].bool_warning
        # settings = bpy.context.preferences.addons[__name__].preferences
        # bool_warning_global = settings.bool_warning_global
        # height = bpy.context.area.spaces.data.height
        # width = bpy.context.area.spaces.data.width

        self.location_cursor = True
        if self.location_cursor == True:
            return context.window_manager.invoke_props_dialog(self)
            # return context.window_manager.invoke_popup(self)
        else:
            x = event.mouse_x
            y = event.mouse_y 

            # location_x = height / 100 * 50
            # location_y = width / 100 * 40
            location_x = 300
            location_y = 550

            bpy.context.window.cursor_warp(location_x , location_y)

            # bpy.context.window.cursor_warp(x + move_x, y + move_y)


            # invoke = context.window_manager.invoke_props_dialog(self)
            invoke = context.window_manager.invoke_popup(self, width=250)
            # return context.window_manager.invoke_popup(self)
            # return context.window_manager.invoke_props_popup(self, event)
            # return context.window_manager.invoke_confirm(self, event)

            bpy.context.window.cursor_warp(x , y)

            return invoke

        # return {'FINISHED'}

class OBJECT_PT_note(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_label = ""
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        text = bpy.context.active_object.note_text_object
        if bool(text) == True:
            draw_text(self, text)

class SCENE_PT_note(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_label = ""
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        text = bpy.context.scene.note_text_scene
        if bool(text) == True:
            draw_text(self, text)



class Noter_Props (bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.noter
    """
    file_name: StringProperty(name = 'Name of the file',\
        default = 'Text')

    note_text_blender: StringProperty()

    note_text_splash_screen: StringProperty()

class Noter_Preferences (bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    splash_screen: BoolProperty(
            name="bool",
            description="",
            default=False,
            )

blender_classes = [
    TEXT_PT_noter,
    Noter_Props,
    Note_Actions,
    Note_Pop_Up_Operator,
    Note_Pop_Up_Operator_2,
    OBJECT_PT_note,
    SCENE_PT_note,
    Noter_Preferences,
    Global_Bool
]

blender_classes = Notes_list_blender_classes + blender_classes

# blender_classes = Nodes_blender_classes + blender_classes

@persistent
def load_handler(dummy):
    # print("Load Handler:", bpy.data.filepath)
    # if bpy.context.window_manager.noter.splash_screen == True: 
    # if bpy.context.space_data.splash_screen == True:

    # if bpy.context.scene.splash_screen == True:
    bpy.ops.window_manager.note_popup_operator('INVOKE_DEFAULT', location_cursor = False)
    # bpy.ops.window_manager.note_popup_operator('INVOKE_DEFAULT')
    # bpy.ops.screen.animation_play()
    # bpy.app.handlers.load_post.remove(load_handler)
    # bpy.app.handlers.load_post.remove(load_handler)

@persistent
def my_handler(scene):
    # print("Frame Change", scene.frame_current)

    # if bpy.context.window_manager.noter.splash_screen == True:
    # bpy.ops.window_manager.note_popup_operator('INVOKE_DEFAULT', location_cursor = False)
    bpy.ops.window_manager.note_popup_operator('INVOKE_DEFAULT')

    bpy.app.handlers.frame_change_post.remove(my_handler)
    bpy.app.handlers.load_post.remove(load_handler)
    bpy.ops.screen.animation_play()
    bpy.context.scene.frame_current = 1


def extra_draw_menu(self, context):
    layout = self.layout

    layout.separator()

    layout.operator("node.noter_operator", text="Set Color").action = 'colour'
    layout.operator("node.noter_operator", text="Set Label name").action = 'label'

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

    # bpy.app.handlers.frame_change_post.append(my_handler)
    bpy.app.handlers.load_post.append(load_handler)

    # bpy.types.WindowManager.splash_screen = BoolProperty()
    bpy.types.Scene.splash_screen = BoolProperty()


    bpy.types.Object.note_text_object = StringProperty()
    bpy.types.Scene.note_text_scene = StringProperty()
    bpy.types.Scene.note_text_blender = StringProperty()
    bpy.types.Scene.note_text_splash_screen = StringProperty()

    bpy.types.WindowManager.noter = PointerProperty(type=Noter_Props)

    bpy.types.Object.notes_list_object = CollectionProperty(type=Notes_List_Collection)
    bpy.types.Object.notes_list_object_index = IntProperty()

    bpy.types.Scene.notes_list_scene = CollectionProperty(type=Notes_List_Collection)
    bpy.types.Scene.notes_list_scene_index = IntProperty()

    from bpy.utils import register_class
    for cls in Nodes_blender_classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('CUSTOM_NODES', node_categories)

    bpy.types.NODE_MT_node.append(extra_draw_menu)

    bpy.types.Scene.colorProperty =  bpy.props.FloatVectorProperty(
        default = [1, 1, 1], subtype = "COLOR",
        soft_min = 0.0, soft_max = 1.0)

    bpy.types.Scene.label_node_text = bpy.props.StringProperty()

    
def unregister():

    bpy.types.NODE_MT_node.remove(extra_draw_menu)

    nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(Nodes_blender_classes):
        unregister_class(cls)


    # if my_handler in bpy.app.handlers.frame_change_post:
    #     bpy.app.handlers.frame_change_post.remove(my_handler)

    if my_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_handler)

    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)

    del bpy.types.Scene.colorProperty
    del bpy.types.Scene.label_node_text

    del bpy.types.Scene.splash_screen


    del bpy.types.Object.note_text_object
    del bpy.types.Scene.note_text_scene
    del bpy.types.Scene.note_text_blender
    del bpy.types.Scene.note_text_splash_screen

    del bpy.types.Object.notes_list_object
    del bpy.types.Object.notes_list_object_index

    del bpy.types.Scene.notes_list_scene
    del bpy.types.Scene.notes_list_scene_index
    


if __name__ == "__main__":
    register()