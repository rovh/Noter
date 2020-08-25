import bpy
import json
import os
import pathlib
import nodeitems_utils
# import time

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
    "description" : "Noter is an add-on created to increase productivity in Blender by organizing the workflow.",
    "blender" : (2, 83, 0),
    "version" : (1, 1, 0),
    "location" : "Text Editor > Sidebar > Noter Tab",
    "warning" : "",
    "category" : "System",
    "wiki_url": "https://github.com/rovh/Noter#noter",
    "tracker_url": "https://github.com/rovh/Noter/issues",
}

custom_scene_name = ".Noter"

class Noter_Actions(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "window_manager.export_note_text"
    bl_label = ""
    bl_description = 'You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut'
    # bl_options = {'REGISTER', 'UNDO'}
    bl_options = {'UNDO'}

    action: StringProperty(options = {"SKIP_SAVE"})
    header_note: BoolProperty(options = {"SKIP_SAVE"}, default = True)

    @classmethod
    def description(cls, context, properties):

        if properties.action == 'object':
            return "Assign text to the active object"
        elif properties.action == 'object_get':
            return "Get text from the active object"
        elif properties.action == 'object_delete':
            return "Delete text in the active object"

        elif properties.action == 'object*':
            return "Import text to the active object list"
        elif properties.action == 'object_get*':
            return "Export text from the active object list"
        


        elif properties.action == 'scene':
            return "Assign text to the active scene"
        elif properties.action == 'scene_get':
            return "Get text from the active scene"
        elif properties.action == 'scene_delete':
            return "Delete text in the active scene"

        elif properties.action == 'scene*':
            return "Import text to the scene list"
        elif properties.action == 'scene_get*':
            return "Export text from the scene list"


        elif properties.action == 'blender_file':
            return "Assign text to the .blend file"
        elif properties.action == 'blender_file_get':
            return "Get text from the .blend file"
        elif properties.action == 'blender_file_delete':
            return "Delete text in the .blend file"


        elif properties.action == 'blender':
            return "Assign text to Blender (Noter)"
        elif properties.action == 'blender_get':
            return "Get text from Blender (Noter)"
        elif properties.action == 'blender_delete':
            return "Delete text in Blender (Noter)"


        elif properties.action == 'splash_screen':
            return "Assign text to the Noter Splash Screen"
        elif properties.action == 'splash_screen_get':
            return "Get text from the Noter Splash Screen"
        elif properties.action == 'splash_screen_delete':
            return "Delete text in the Noter Splash Screen"
 
    def execute(self, context):    

        # t1 = time.perf_counter()
        # t1 = time.perf_counter()


        action = self.action
        header_note = self.header_note

        

        if action.count("*") != 0:
            action = self.action.replace("*", "")
            header_note = False
        else:
            header_note = True

        action_type = action.split("_")
        action_type = action_type[0]

        if header_note == True:
            pass
        else:
            if len(bpy.context.active_object.notes_list_object) == 0 and action_type == 'object':
                bpy.context.active_object.notes_list_object.add()

            elif len(bpy.context.scene.notes_list_scene) == 0 and action_type == 'scene':
                bpy.context.scene.notes_list_scene.add()

        if (action == 'object' or\
            action == 'object_get' or\
            action == 'object_delete') and\
            bpy.context.active_object is None:

                text = "No Active Object was found"
                war = "ERROR"
                self.report({war}, text)
                return {'FINISHED'}


        if len(bpy.data.texts.values()) == 0 and header_note == True:
            bpy.ops.text.new()
            try:
                bpy.data.texts[bpy.context.space_data.text.name].name = bpy.context.scene.file_name
            except AttributeError:
                pass

            text = f'A new text file " {bpy.context.scene.file_name} " was created'
            war = "INFO"
            self.report({war}, text)
            # return {'FINISHED'}



    #object
        try:
            note_text_object = bpy.context.active_object.note_text_object
        except AttributeError:
            pass
        
    #scene
        note_text_scene = bpy.context.scene.note_text_scene
        
    #blender_file

        # note_text_blender_file = ""
        # for i in bpy.data.scenes:
        #     if bool(i.note_text_blender_file) == True:
        #         note_text_blender_file = i.note_text_blender_file
        #         break

    #splash_screen

        # note_text_splash_screen = ""
        # for i in bpy.data.scenes:
        #     if i.splash_screen == True:
        #         note_text_splash_screen = i.note_text_splash_screen
        #         break
    #
        
        use_file_path = bpy.context.preferences.addons[__name__].preferences.use_file_path
        if use_file_path == 'OPENED':
            try:
                # for i in bpy.context.workspace:
                #     file_name = i.text.name

                file_name = bpy.data.screens['Scripting'].areas.data.text.name
            except AttributeError:
                pass
        else:

            file_name = bpy.context.scene.file_name
            try:
                if bpy.context.space_data.text.name != file_name:
                    if action.count('get'):
                        if bpy.data.texts.find(file_name) != -1:
                            bpy.context.space_data.text = bpy.data.texts[file_name]
                            text = f'File was changed to " {file_name} " '
                            war = "INFO"
                            self.report({war}, text)
                        else:
                            bpy.ops.text.new()
                            bpy.data.texts[bpy.context.space_data.text.name].name = file_name
                            text = f'A new text file " {file_name} " was created'
                            war = "INFO"
                            self.report({war}, text)

                    elif action.count('get') == 0 and action.count('delete') == 0:
                        text = 'The name of the open file does not match the name of the files used by "Noter"'
                        war = "WARNING"
                        self.report({war}, text)
                        # file_name = bpy.context.space_data.text.name
            except AttributeError:
                pass



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



        elif action == 'blender_file':
            if bpy.data.scenes.find(custom_scene_name) == -1:
                bpy.data.scenes.new(custom_scene_name)

            if header_note == True:
                bpy.data.scenes[custom_scene_name].note_text_blender_file = main_text

                # for i in bpy.data.scenes:
                #     i.note_text_blender_file = main_text
            else:
                item = self.item_blender_file(context)
                item.text = main_text

        elif action == "blender_file_get":
            bpy.data.texts[file_name].clear()

            if bpy.data.scenes.find(custom_scene_name) == -1:
                bpy.data.scenes.new(custom_scene_name)

            if header_note == True:
                note_text_blender_file = bpy.data.scenes[custom_scene_name].note_text_blender_file

                bpy.data.texts[file_name].write(note_text_blender_file)
            else:
                item = self.item_blender_file(context)
                bpy.data.texts[file_name].write(item.text)

        elif action == "blender_file_delete":
            if header_note == True:
                if bpy.data.scenes.find(custom_scene_name) == -1:
                    bpy.data.scenes.new(custom_scene_name)

                bpy.data.scenes[custom_scene_name].note_text_blender_file = ""
                
                # for i in bpy.data.scenes:
                #     i.note_text_blender_file = ""
            else:
                item = self.item_object(context)
                item.text = ""



        elif action == 'blender':
            if header_note == True:
                file_folder_path = pathlib.Path(__file__).parent.absolute()
                file_folder_path = os.path.join(file_folder_path, 'note_text_blender.json')

                with open(file_folder_path, "w", encoding='utf-8') as data_file:
                    json.dump(main_text, data_file)

                # bpy.context.preferences.addons[__name__].preferences.note_text_blender = main_text
                # bpy.context.preferences.use_preferences_save
            else:
                item = self.item_scene(context)
                item.text = main_text

        elif action == 'blender_get':
            bpy.data.texts[file_name].clear()
            if header_note == True:
                file_folder_path = pathlib.Path(__file__).parent.absolute()
                file_folder_path = os.path.join(file_folder_path, 'note_text_blender.json')

                with open(file_folder_path, encoding='utf-8') as f:
                    note_text_blender_json = json.load(f)
                bpy.data.texts[file_name].write(note_text_blender_json)
            else:
                item = self.item_scene(context)
                bpy.data.texts[file_name].write(item.text)

        elif action == 'blender_delete':
            if header_note == True:
                file_folder_path = pathlib.Path(__file__).parent.absolute()
                file_folder_path = os.path.join(file_folder_path, 'note_text_blender.json')

                with open(file_folder_path, 'w', encoding ='utf-8') as f:
                    json.dump('', f)
                # bpy.context.preferences.addons[__name__].preferences.note_text_blender = ""
            else:
                item = self.item_scene(context)
                item.text = ""



        elif action == 'splash_screen':
            if header_note == True:

                if bpy.data.scenes.find(custom_scene_name) == -1:
                    bpy.data.scenes.new(custom_scene_name)

                bpy.data.scenes[custom_scene_name].note_text_splash_screen = main_text

                # for i in bpy.data.scenes:
                #     i.note_text_splash_screen = main_text   
            else:
                item = self.item_object(context)
                item.text = main_text

        elif action == "splash_screen_get":
            bpy.data.texts[file_name].clear()
            if header_note == True:
                if bpy.data.scenes.find(custom_scene_name) == -1:
                    bpy.data.scenes.new(custom_scene_name)

                note_text_splash_screen = bpy.data.scenes[custom_scene_name].note_text_splash_screen
                
                bpy.data.texts[file_name].write(note_text_splash_screen)
            else:
                item = self.item_object(context)
                bpy.data.texts[file_name].write(item.text)

        elif action == "splash_screen_delete":
            if header_note == True:
                if bpy.data.scenes.find(custom_scene_name) == -1:
                    bpy.data.scenes.new(custom_scene_name)

                bpy.data.scenes[custom_scene_name].note_text_splash_screen = ''

                # for i in bpy.data.scenes:
                #     i.note_text_splash_screen = ""  
            else:
                item = self.item_object(context)
                item.text = ""


        # t2 = time.perf_counter()
        # t2 = time.perf_counter()

        # print(f"\nProgramm Time:{t2 - t1}\n")

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

    def item_blender_file(self, context):
        scene = bpy.data.scenes[custom_scene_name]
        idx = scene.notes_list_blender_file_index

        try:
            item = scene.notes_list_blender_file[idx]
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
        # noter = bpy.context.window_manager.noter
        scene = bpy.context.scene
        # preferences = bpy.context.preferences.addons[__name__].preferences
        
        
        layout = self.layout
        column = layout.column(align = 1)
        column.scale_y = 1.3

        column.prop(scene, "file_name", text = '')
        

        column.separator(factor = 1)

        # box = column.box()
        # box.label(text = "Header Note", icon = 'TOPBAR')


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
        col.operator("window_manager.export_note_text", text = 'File (.blend)', icon = 'FILE_FOLDER').action = "blender_file"
        col.operator("window_manager.export_note_text", text = '', icon = 'FILE_TICK').action = "blender_file_get"
        col.operator("window_manager.export_note_text", text = '', icon = 'TRASH').action = "blender_file_delete"


        box = column.box()
        col = box.column(align = 1)
        col.operator("window_manager.export_note_text", text = 'Blender (Noter)', icon = 'BLENDER').action = "blender"
        col.operator("window_manager.export_note_text", text = '', icon = 'FILE_TICK').action = "blender_get"
        col.operator("window_manager.export_note_text", text = '', icon = 'TRASH').action = "blender_delete"


        box = column.box()
        col = box.column(align = 1)
        col.separator(factor = 1)
        row = col.row(align = 1)
        

        find = False
        try:
            find = bpy.data.scenes[custom_scene_name].splash_screen
        except KeyError:
            pass
        
        # find = False
        # for i in bpy.data.scenes:
        #     if i.splash_screen == True:
        #         find = True
        #         break


        row.operator("window_manager.global_bool", text = 'Splash Screen', icon = 'WINDOW', depress= find)
        row.alignment = 'RIGHT'
        row.scale_x = .5

        col.separator(factor = 1)
        if find == True:
            col.operator("window_manager.export_note_text", text = 'Splash Screen', icon = 'WINDOW').action = "splash_screen"
            col.operator("window_manager.export_note_text", text = '', icon = 'FILE_TICK').action = "splash_screen_get"
            col.operator("window_manager.export_note_text", text = '', icon = 'TRASH').action = "splash_screen_delete"

class Noter_Splash_Screen_Switch(Operator):
    """Tooltip"""
    bl_idname = "window_manager.global_bool"
    bl_label = ""
    bl_description = 'Display Noter splash screen on startup \n\n You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut'
    # bl_options = {'REGISTER', 'UNDO'}
    bl_options = {'UNDO'}

    
    def execute(self, context):

        if bpy.data.scenes.find(custom_scene_name) == -1:
            bpy.data.scenes.new(custom_scene_name)


        if bpy.data.scenes[custom_scene_name].splash_screen == True:
            bpy.data.scenes[custom_scene_name].splash_screen = False
        else:
            bpy.data.scenes[custom_scene_name].splash_screen = True

            
                
        
        # if bpy.context.scene.splash_screen == True:
        #     for i in bpy.data.scenes:
        #         i.splash_screen = False
        # else:
        #     for i in bpy.data.scenes:
        #         i.splash_screen = True

        return {'FINISHED'}

class Noter_Text_Lines_Create(Operator):
    """Tooltip"""
    bl_idname = "window_manager.text_lines_create"
    bl_label = "Create Text Lines"
    bl_description = 'Line text \n\n You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut'
    # bl_options = {'REGISTER', 'UNDO'}
    # bl_options = {'UNDO'}

    
    def execute(self, context):
        file_name = bpy.context.scene.file_name
        line_width_characters = bpy.context.scene.line_width_characters
        try:
            main_text = bpy.data.texts[file_name].as_string()
        except KeyError:

            text = "File was not found"
            war = "ERROR"
            self.report({war}, text)
            return {'FINISHED'}




        line_width_characters = line_width_characters
        new_main_text = ""
        new_main_text_split = ""

        main_text = main_text.replace("\n", " ")
        main_text_split_list = main_text.split(" ")

        for index, split in enumerate(main_text_split_list):
            if len(new_main_text_split) == 0:
                new_main_text_split = new_main_text_split + split
            else:
                new_main_text_split = new_main_text_split + " " + split

            if len(new_main_text_split) > line_width_characters:
                new_main_text += new_main_text_split + "\n"
                new_main_text_split = ""

        new_main_text +=  new_main_text_split


        bpy.data.texts[file_name].from_string(new_main_text)
            

        # line_width_characters = 40
        # text = "\n"
        # line = 1
        # index = 1
        # new_main_text = ""
        # new_main_text_part = ""



        # for character in main_text:

        #     if character == " " and index > line_width_characters:

        #         bpy.data.texts[file_name].cursor_set(line, character=index, select=False)

        #         line += 1

        #         index = 1

        #         bpy.data.texts[file_name].write(text)

        #     index += 1
         

        #     print (index, 'index','|', character, 'character')
        
        # print ()




        # text = '123123123123'
        # line_start = 2
        # char_start = 0

        # line_end = 30
        # char_end = 100

        # t = bpy.data.texts['Text'].cursor_set(line, character=10, select=False)
        
        # t = bpy.data.texts['Text'].select_set(line_start, char_start, line_end, char_end)
        
        # t = bpy.data.texts['Text'].write(text)

        # t = bpy.data.texts['Text'].as_string()

        # t = bpy.data.texts['Text'].from_string(text)


            
        return {'FINISHED'}




def draw_text(self, text):
    text_parts_list = text.split('\n')
    layout = self.layout
    box = layout.box()
    row = box.row(align = 1)
    row.scale_x = 2.7
    row.alignment = 'CENTER'
    # column.separator(factor=.5)
    col = row.column(align = 1)
    for i in text_parts_list:
        row = col.row(align = 0)
        row.label(text = i)
        row.scale_y = 0

def calculate_width_menu(self, text):

    # from matplotlib.afm import AFM
    # afm = AFM(open(afm_filename, "rb"))
    # AFM.string_width_height('What the heck?')


    text_parts_list = text.split('\n')
    length = 25
    for row in text_parts_list:
        row = len(row)
        if row > length:
            length = row
    # 450 pixels = 50 symbols > 1 symbol = 9 pixels 
    # 550 pixels = 50 symbols > 1 symbol = 11 pixels 
    width_menu = length * 12


    return width_menu


class Note_Pop_Up_Operator(Operator):
    bl_idname = "window_manager.note_popup_operator"
    bl_label = "Noter Splash Screen"

    location_cursor: BoolProperty(default = True, options = {"SKIP_SAVE"})

    @classmethod
    def poll(cls, context):

        find = False
        try:
            find = bpy.data.scenes[custom_scene_name].splash_screen
        except KeyError:
            pass

            # find = False
        # find = False
        # for i in bpy.data.scenes:
        #     if i.splash_screen == True:
        #         find = True
        #         break

        return find

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        # row.label(text='' , icon="MOUSE_LMB_DRAG")
        row.operator("window_manager.note_popup_operator_2",text='' , icon="MOUSE_LMB_DRAG").action = 'drag'
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
            for _ in range(0, length):
                column_text.label(icon = ic)


        row_text.separator(factor = 2)


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

        row_text.separator(factor = 5)



        # materials = [mat for mat in bpy.data.materials]
        # tex = bpy.data.textures['.hidden']
        # tex = img.jpg
        # layout.template_preview(tex)



        # text = bpy.context.window_manager.noter.note_text_blender_file
        # find = None
        # for i in bpy.data.scenes:
        #     if bool(i.note_text_splash_screen) == True:
        #         find = i.note_text_splash_screen
        #         break

        # find = None
        # for i in bpy.data.scenes:
        #     if i.splash_screen == True:
        #         find = i.note_text_splash_screen
        #         break

        # text = ""
        text = bpy.data.scenes[custom_scene_name].note_text_splash_screen
        if bool(text) == True:
            draw_text(self, text)

    def invoke(self, context, event): 
        # bool_warning = bpy.data.scenes[bpy.context.scene.name_full].bool_warning
        preferences = bpy.context.preferences.addons[__name__].preferences
        # bool_warning_global = settings.bool_warning_global
        # height = bpy.context.area.spaces.data.height
        # width = bpy.context.area.spaces.data.width
        height = bpy.context.window.height
        width = bpy.context.window.width

        if bpy.data.scenes.find(custom_scene_name) == -1:
            bpy.data.scenes.new(custom_scene_name)

        text = bpy.data.scenes[custom_scene_name].note_text_splash_screen
        width_menu = calculate_width_menu(self, text)
        

        self.location_cursor = False
        if self.location_cursor == True:
            return context.window_manager.invoke_props_dialog(self)
        else:
            x = event.mouse_x
            y = event.mouse_y 


            
            # location_x = width  * .5
            # location_y = height * .9
            location_x = width  * preferences.splash_screen_location_x
            location_y = height * preferences.splash_screen_location_y

            bpy.context.window.cursor_warp(location_x , location_y)


            invoke = context.window_manager.invoke_props_dialog(self, width=width_menu)
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

    action: StringProperty()
    location_cursor: BoolProperty(default = False, options = {"SKIP_SAVE"})

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        action = self.action
        layout = self.layout

        if action == 'drag':
            layout.label(text = 'You can drag this menu by clicking on its upper part', icon = 'INFO')
        else:
            row = layout.row()
            # row.label(text='' , icon="MOUSE_LMB_DRAG")
            row.operator("window_manager.note_popup_operator_2",text='' , icon="MOUSE_LMB_DRAG").action = 'drag'
            row.alignment = 'RIGHT'

        if action == 'blender':
            file_folder_path = pathlib.Path(__file__).parent.absolute()
            file_folder_path = os.path.join(file_folder_path, 'note_text_blender.json')

            with open(file_folder_path, encoding='utf-8') as f:
                note_text_blender_json = json.load(f)

            draw_text(self, note_text_blender_json)

        elif action == 'blender_file':

            if bpy.data.scenes.find(custom_scene_name) == -1:
                bpy.data.scenes.new(custom_scene_name)

            note_text_blender_file = bpy.data.scenes[custom_scene_name].note_text_blender_file


            # note_text_blender_file = ""
            # for i in bpy.data.scenes:
            #     if bool(i.note_text_blender_file) == True:
            #         note_text_blender_file = i.note_text_blender_file
            #         break


            draw_text(self, note_text_blender_file)

    def invoke(self, context, event): 
        # bool_warning = bpy.data.scenes[bpy.context.scene.name_full].bool_warning
        # settings = bpy.context.preferences.addons[__name__].preferences
        # bool_warning_global = settings.bool_warning_global
        # height = bpy.context.area.spaces.data.height
        # width = bpy.context.area.spaces.data.width
        height = bpy.context.window.height
        width = bpy.context.window.width


        if self.action == 'blender':
            file_folder_path = pathlib.Path(__file__).parent.absolute()
            file_folder_path = os.path.join(file_folder_path, 'note_text_blender.json')

            with open(file_folder_path, encoding='utf-8') as f:
                text = json.load(f)

        elif self.action == 'blender_file':

            if bpy.data.scenes.find(custom_scene_name) == -1:
                bpy.data.scenes.new(custom_scene_name)

            text = bpy.data.scenes[custom_scene_name].note_text_blender_file

        try:
            width_menu = calculate_width_menu(self, text)
        except UnboundLocalError:
            width_menu = 300


        self.location_cursor = True if self.action == 'drag' else False
        location_cursor = self.location_cursor

        if location_cursor == True:
            return context.window_manager.invoke_props_dialog(self, width = width_menu)
        else:
            x = event.mouse_x
            y = event.mouse_y 

            location_x = width * .5
            location_y = height * .75
            # location_x = 300
            # location_y = 550

            bpy.context.window.cursor_warp(location_x , location_y)

            # bpy.context.window.cursor_warp(x + move_x, y + move_y)


            invoke = context.window_manager.invoke_props_dialog(self, width = width_menu)
            # invoke = context.window_manager.invoke_popup(self, width=250)
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

class TEXT_PT_list_text(Panel):
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Text"
    bl_label = "Line Text"
    # bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        scene = context.scene
        
        layout = self.layout

        layout.operator('window_manager.text_lines_create', text = 'List Text')

        layout.prop(scene, "line_width_characters", text = '')

# class Noter_Props (bpy.types.PropertyGroup):
    # """
    # Fake module like class
    # bpy.context.window_manager.noter
    # """
    # file_name: StringProperty(name = 'Name of the file',\
    #     default = 'Text')

    # note_text_blender_file: StringProperty()

    # note_text_splash_screen: StringProperty()


class Noter_Preferences (bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    note_text_blender: StringProperty()

    splash_screen: BoolProperty(
            name="bool",
            description="",
            default=False,
            )

    splash_screen_location_x: FloatProperty(name="123", default = 0.5, precision = 6, \
        min = 0, max = 1.0, description = "123")

    splash_screen_location_y: FloatProperty(name="123", default = 0.9, precision = 6, \
        min = 0, max = 1.0, description = "123")

    use_file_path: bpy.props.EnumProperty(
        items=(
            ('OPENED', "Opened", ""),
            ('NAME', "Name", "")),
        default = 'NAME')

    preference_type: bpy.props.EnumProperty(
        items=(
            ('SPLASH_SCREEN', "Splash Screen", ""),
            ('INTERFACE', "Interface", "")),
        default = 'SPLASH_SCREEN')

    add_custom_menu_to_header_bar_menu: bpy.props.BoolProperty(
        name="bool",
        description="",
        default=False,
        )
    
    add_elements_to_menus: bpy.props.BoolProperty(
        name="bool",
        description="",
        default=True,
        )



    # use_opened_file_path: BoolProperty(
            # name="bool",
            # description="",
            # default=False,
            # )

    def draw(self, context):
        layout = self.layout
        layout.separator(factor = .5)

        column = layout.column(align = True)
        
        row = column.row(align = True)
        row.prop(self, 'preference_type', expand = True)
        row.scale_y = 1.2

        box = column.box()


        if self.preference_type == "SPLASH_SCREEN":

            box.label(text = 'Splash Screen Position')


            row_main = box.row(align = 0)

            col_1 = row_main.column(align = 1)
            col_1.separator(factor = 4)

            row = col_1.row(align = 1)

            row.label(icon = 'BACK')
            row.label(icon = 'TOPBAR')
            row.label(icon = 'FORWARD')
            row.alignment = 'CENTER'

            col_1.separator(factor = 2.7)

            col_1.prop(self, 'splash_screen_location_x', text = 'X')



            row_main.separator(factor = 3)



            col_2 = row_main.column(align = 1)
            row = col_2.row(align = 1)
            row.alignment = 'CENTER'

            col_sub = row.column(align = 1)
            col_sub.label(icon = 'SORT_DESC')
            col_sub.label(icon = 'TOPBAR')
            col_sub.label(icon = 'SORT_ASC')
            
            col_2.prop(self, 'splash_screen_location_y', text = 'Y')

            box.separator(factor = .1)

        elif self.preference_type == "INTERFACE":
            box.label(text = 'Interface')

            row = box.row(align = False)
            row = row.row(align = True)

            row.prop(self, 'add_custom_menu_to_header_bar_menu', text = 'Add a new custom header menu to the topbar', toggle=True)
            row.prop(self, 'add_elements_to_menus', text = 'Add buttons to the existing topbar menus', toggle=True)
            row.alignment = 'LEFT'
            row.scale_x = 1.5

            box.separator(factor = .1)



        layout.separator(factor = 2)
        

@persistent
def load_handler(dummy):

    # action = False
    # try:
    #     action = bpy.data.scenes[custom_scene_name].splash_screen
    # except KeyError:
    #     pass
    # print("Load Handler:", bpy.data.filepath)
    # if bpy.context.window_manager.noter.splash_screen == True: 
    # if bpy.context.space_data.splash_screen == True:
    # bpy.ops.window_manager.note_popup_operator('INVOKE_DEFAULT', location_cursor = False)
    # if action == True:
    try:
        bpy.ops.window_manager.note_popup_operator('INVOKE_DEFAULT')
    except RuntimeError:
        pass
    # bpy.ops.screen.animation_play()
    # bpy.app.handlers.load_post.remove(load_handler)
    # bpy.app.handlers.load_post.remove(load_handler)

def my_extra_draw_menu(self, context):
    layout = self.layout

    layout.separator()

    layout.operator("node.noter_operator", text="Set Color").action = 'colour'
    layout.operator("node.noter_operator", text="Set Label name").action = 'label'

def my_extra_draw_menu_2(self, context, mode = "normal_location"):
    preferences = bpy.context.preferences.addons[__name__].preferences
    if preferences.add_elements_to_menus == True:

        if type(self) == bpy.types.TOPBAR_MT_window:
            text = "Note (File)"
            icon = 'FILE'

        elif mode == "normal_location":
            text = "Note"
            icon = 'FILE'

        elif mode == "custom_menu_location":
            text = "Blender (Noter)"
            icon = 'BLENDER'
        

        layout = self.layout


        file_folder_path = pathlib.Path(__file__).parent.absolute()
        file_folder_path = os.path.join(file_folder_path, 'note_text_blender.json')

        with open(file_folder_path, encoding='utf-8') as f:
            note_text_blender_json = json.load(f)
        note_text_blender_json = bool(note_text_blender_json)



        find = False
        try:
            find = bpy.data.scenes[custom_scene_name].splash_screen
        except KeyError:
            pass
        # find = False
        # for i in bpy.data.scenes:
        #     if i.splash_screen == True:
        #         find = True
        #         break

        if note_text_blender_json == True:

            layout.separator()

            layout.operator("window_manager.note_popup_operator_2", text=text, icon = icon).action = 'blender'

        if find == True:
            layout.separator()

            layout.operator("window_manager.note_popup_operator", text="Noter Splash Screen", icon = 'WINDOW')

def my_extra_draw_menu_3(self, context, mode = "normal_location"):
    preferences = bpy.context.preferences.addons[__name__].preferences
    if preferences.add_elements_to_menus == True:

        if mode == "normal_location":
            text = "Note"
            icon = 'FILE'
            separator_factor = 2
            
        elif mode == "custom_menu_location":
            text = "File"
            icon = 'FILE_FOLDER'
            separator_factor = 1


        find = False
        try:
            find = bpy.data.scenes[custom_scene_name].note_text_blender_file
            find = bool(find)
        except KeyError:
            pass
        

        # find = False
        # for i in bpy.data.scenes:
        #     if bool(i.note_text_blender_file) == True:
        #         find = True
        #         break

        if find == True:

            layout = self.layout

            layout.separator(factor = separator_factor)

            layout.operator("window_manager.note_popup_operator_2", text=text, icon = icon).action = 'blender_file'

            # layout.separator()        

class TOPBAR_MT_notes(bpy.types.Menu):
    bl_label = "Notes"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_AREA'
        my_extra_draw_menu_3(self, context, "custom_menu_location")
        my_extra_draw_menu_2(self, context, "custom_menu_location")

def add_to_the_topbar(self, context):
    preferences = bpy.context.preferences.addons[__name__].preferences

    if preferences.add_custom_menu_to_header_bar_menu == True:
        layout = self.layout
        layout.menu("TOPBAR_MT_notes", text = "", icon = "FILE")



blender_classes = [
    TEXT_PT_noter,
    # Noter_Props,
    Noter_Actions,
    Note_Pop_Up_Operator,
    Note_Pop_Up_Operator_2,
    Noter_Text_Lines_Create,
    OBJECT_PT_note,
    SCENE_PT_note,
    Noter_Preferences,
    Noter_Splash_Screen_Switch,
    TOPBAR_MT_notes,
    TEXT_PT_list_text,

    

    ]

blender_classes = Notes_list_blender_classes + blender_classes


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

    # bpy.types.WindowManager.splash_screen = BoolProperty()

    bpy.types.Scene.splash_screen = BoolProperty()
    bpy.app.handlers.load_post.append(load_handler)


    bpy.types.Scene.file_name = StringProperty(name = 'Name of the file',default = 'Text', description = "Name of the file from which the text will be taken or where the text will be displayed")
    bpy.types.Scene.line_width_characters = IntProperty(name = 'Number', default = 60, description = "Name of the file from which the text will be taken or where the text will be displayed")

    bpy.types.Object.note_text_object = StringProperty()
    bpy.types.Scene.note_text_scene = StringProperty()
    bpy.types.Scene.note_text_blender_file = StringProperty()
    bpy.types.Scene.note_text_splash_screen = StringProperty()

    # bpy.types.WindowManager.noter = PointerProperty(type=Noter_Props)

    bpy.types.Object.notes_list_object = CollectionProperty(type=Notes_List_Collection)
    bpy.types.Object.notes_list_object_index = IntProperty()

    bpy.types.Scene.notes_list_scene = CollectionProperty(type=Notes_List_Collection)
    bpy.types.Scene.notes_list_scene_index = IntProperty()

    bpy.types.Scene.notes_list_blender_file = CollectionProperty(type=Notes_List_Collection)
    bpy.types.Scene.notes_list_blender_file_index = IntProperty()

    from bpy.utils import register_class
    for cls in Nodes_blender_classes:
        register_class(cls)

    bpy.types.NODE_MT_add.prepend(add_to_add_menu)


    bpy.types.Scene.colorProperty =  bpy.props.FloatVectorProperty(
        default = [1, 1, 1], subtype = "COLOR",
        soft_min = 0.0, soft_max = 1.0)

    bpy.types.Scene.label_node_text = bpy.props.StringProperty()

    nodeitems_utils.register_node_categories('NOTER_CUSTOM_NODES', node_categories)

    bpy.types.NODE_MT_node.append(my_extra_draw_menu)
    try:
        bpy.types.TOPBAR_MT_app.append(my_extra_draw_menu_2)
    except AttributeError:
        bpy.types.TOPBAR_MT_window.append(my_extra_draw_menu_2)

    bpy.types.TOPBAR_MT_file.append(my_extra_draw_menu_3)

    bpy.types.TOPBAR_MT_editor_menus.append(add_to_the_topbar)

def unregister():


    bpy.types.NODE_MT_node.remove(my_extra_draw_menu)
    try:
        bpy.types.TOPBAR_MT_app.remove(my_extra_draw_menu_2)
    except AttributeError:
        bpy.types.TOPBAR_MT_window.remove(my_extra_draw_menu_2)

    bpy.types.TOPBAR_MT_file.remove(my_extra_draw_menu_3)

    bpy.types.TOPBAR_MT_editor_menus.remove(add_to_the_topbar)

    bpy.types.NODE_MT_add.remove(add_to_add_menu)


    nodeitems_utils.unregister_node_categories('NOTER_CUSTOM_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(Nodes_blender_classes):
        unregister_class(cls)


    # if my_handler in bpy.app.handlers.frame_change_post:
    #     bpy.app.handlers.frame_change_post.remove(my_handler)

    # if my_handler in bpy.app.handlers.load_post:
    #     bpy.app.handlers.load_post.remove(load_handler)

    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)

    del bpy.types.Scene.colorProperty
    del bpy.types.Scene.label_node_text

    del bpy.types.Scene.file_name
    del bpy.types.Scene.line_width_characters

    del bpy.types.Scene.splash_screen


    del bpy.types.Object.note_text_object
    del bpy.types.Scene.note_text_scene
    del bpy.types.Scene.note_text_blender_file
    del bpy.types.Scene.note_text_splash_screen

    del bpy.types.Object.notes_list_object
    del bpy.types.Object.notes_list_object_index

    del bpy.types.Scene.notes_list_scene
    del bpy.types.Scene.notes_list_scene_index
    
    del bpy.types.Scene.notes_list_blender_file
    del bpy.types.Scene.notes_list_blender_file_index


if __name__ == "__main__":
    register()