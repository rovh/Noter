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

# def draw_text(text_parts_list):
#     # col = column
#     for i in text_parts_list:
#         row = col.row(align = 1)
#         row.label(text = i)
#         row.scale_y = 0

class Notes_List_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "notes_list_object.list_action"
    bl_label = ""
    bl_description = "Move items up and down or remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            # ('ADD', "Add", "") 
            ))

    @classmethod
    def description(cls, context, properties):
        if properties.action == 'REMOVE':
            return "Remove"
        elif properties.action == 'UP':
            return "Up"
        elif properties.action == 'DOWN':
            return "Down"

    def invoke(self, context, event):

        act_obj = context.active_object
        idx = act_obj.notes_list_object_index

        try:
            item = act_obj.notes_list_object[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(act_obj.notes_list_object) - 1:
                act_obj.notes_list_object.move(idx, idx+1)
                act_obj.notes_list_object_index += 1

            elif self.action == 'UP' and idx >= 1:
                act_obj.notes_list_object.move(idx, idx-1)
                act_obj.notes_list_object_index -= 1
                
            elif self.action == 'REMOVE':
                if idx == 0:
                    act_obj.notes_list_object_index = 0
                else:
                    act_obj.notes_list_object_index -= 1
                act_obj.notes_list_object.remove(idx)

        return {"FINISHED"}
class Notes_List_actions_add(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "notes_list_object.list_action_add"
    bl_label = "Add"
    bl_description = "Add item"
    bl_options = {'REGISTER'}
    # bl_options = {'BLOCKING'}
    # bl_options = {'INTERNAL'}

    # def draw(self, context):
    #     layout = self.layout

    #     layout.prop(self, "text_input", text = "Name")

    # def invoke(self, context, event):
    #     self.unit_input = bpy.context.window_manager.setprecisemesh.length
    #     return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        act_obj = context.active_object
        idx = act_obj.notes_list_object_index

        try:
            item = act_obj.notes_list_object[idx]
        except IndexError:
            pass

        item = act_obj.notes_list_object.add()

        act_obj.notes_list_object_index = len(act_obj.notes_list_object) - 1

        return {"FINISHED"}
class Notes_List_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "notes_list_object.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.active_object.notes_list_object)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.active_object.notes_list_object):
            context.active_object.notes_list_object.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}
class Notes_actions_bool(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "notes_list_object.list_action_bool"
    bl_label = ""
    bl_description = "Checkmark"
    bl_options = {'REGISTER'}

    my_index: IntProperty()


    def execute(self, context):

        # bpy.context.active_object.notes_list_object_index = self.my_index

        act_obj = context.active_object
        # idx = act_obj.notes_list_object_index
        idx = self.my_index

        try:
            item = act_obj.notes_list_object[idx]
        except IndexError:
            pass

        
        if act_obj.notes_list_object[idx].bool == True:
            act_obj.notes_list_object[idx].bool = False
            if len(act_obj.notes_list_object)>1:
                act_obj.notes_list_object.move(idx, 0)
        else:
            act_obj.notes_list_object[idx].bool = True
            act_obj.notes_list_object.move(idx, len(act_obj.notes_list_object) - 1)

        # if bpy.context.active_object:
    
            # bpy.context.window_manager.setprecisemesh.length = item.unit

            # bpy.context.region.tag_redraw()
            # context.area.tag_redraw()
            # bpy.context.scene.update()

            # for region in context.area.regions:
            #     if region.type == "UI":
            #         region.tag_redraw()

            # bpy.data.scenes.update()

            
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1)
            # print("Warning because of Set Precise Mesh")



            # bpy.ops.wm.redraw_timer(type = "UNDO", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_SWAP", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW", iterations = 1, time_limit = 0.0)

        # else:
            # self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}


class Notes_List_actions_scene(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "notes_list_scene.list_action"
    bl_label = ""
    bl_description = "Move items up and down or remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            # ('ADD', "Add", "") 
            ))

    @classmethod
    def description(cls, context, properties):
        if properties.action == 'REMOVE':
            return "Remove"
        elif properties.action == 'UP':
            return "Up"
        elif properties.action == 'DOWN':
            return "Down"

    def invoke(self, context, event):

        scene = context.scene
        idx = scene.notes_list_scene_index

        try:
            item = scene.notes_list_scene[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scene.notes_list_scene) - 1:
                scene.notes_list_scene.move(idx, idx+1)
                scene.notes_list_scene_index += 1

            elif self.action == 'UP' and idx >= 1:
                scene.notes_list_scene.move(idx, idx-1)
                scene.notes_list_scene_index -= 1
                
            elif self.action == 'REMOVE':
                if idx == 0:
                    scene.notes_list_scene_index = 0
                else:
                    scene.notes_list_scene_index -= 1
                
                scene.notes_list_scene.remove(idx)

        return {"FINISHED"}
class Notes_List_actions_add_scene(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "notes_list_scene.list_action_add"
    bl_label = "Add"
    bl_description = "Add item"
    bl_options = {'REGISTER'}
    # bl_options = {'BLOCKING'}
    # bl_options = {'INTERNAL'}

    # def draw(self, context):
    #     layout = self.layout

    #     layout.prop(self, "text_input", text = "Name")

    # def invoke(self, context, event):
    #     self.unit_input = bpy.context.window_manager.setprecisemesh.length
    #     return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        scene = context.scene
        idx = scene.notes_list_scene_index

        try:
            item = scene.notes_list_scene[idx]
        except IndexError:
            pass

        item = scene.notes_list_scene.add()

        scene.notes_list_scene_index = len(scene.notes_list_scene) - 1

        return {"FINISHED"}
class Notes_List_clearList_scene(Operator):
    """Clear all items of the list"""
    bl_idname = "notes_list_scene.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.notes_list_scene)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.notes_list_scene):
            context.scene.notes_list_scene.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}
class Notes_actions_bool_scene(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "notes_list_scene.list_action_bool"
    bl_label = ""
    bl_description = "Checkmark"
    bl_options = {'REGISTER'}

    my_index: IntProperty()

    def execute(self, context):

        # bpy.context.scene.notes_list_scene_index = self.my_index

        scene = context.scene
        # idx = scene.notes_list_scene_index
        idx = self.my_index

        try:
            item = scene.notes_list_scene[idx]
        except IndexError:
            pass

        
        if scene.notes_list_scene[idx].bool == True:
            scene.notes_list_scene[idx].bool = False
            if len(scene.notes_list_scene) > 1:
                scene.notes_list_scene.move(idx, 0)
        else:
            scene.notes_list_scene[idx].bool = True
            scene.notes_list_scene.move(idx, len(scene.notes_list_scene) - 1)


        return {"FINISHED"}



class NOTES_LIST_UL_items_scene(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        # draw_text(self)

        scene = context.scene
        idx = scene.notes_list_scene_index

        try:
            item = scene.notes_list_scene[index]
        except IndexError:
            pass


        column_main = layout.column(align = 1)
        box = column_main.box()
        column = box.column(align = 1)
        row_header = column.row(align = 1)
        row_header.scale_y = .7


        if bpy.context.scene.notes_list_scene[index].bool == True:
            row_info = row_header.row(align = 1)
            row_info.operator("notes_list_scene.list_action_bool", text = "", icon = "CHECKBOX_DEHLT", emboss = 0).my_index = index
            row_info.alignment = 'RIGHT'

            # row_info = row_header.row(align = 1)
            # row_info.operator("notes_list_scene.list_action_bool", text = "", icon = "SHADING_SOLID", emboss = 0).my_index = index
            # row_info.alignment = 'CENTER'
        else:
            row_info = row_header.row(align = 1)
            row_info.operator("notes_list_scene.list_action_bool", text = "", icon = "BOOKMARKS", emboss = 0).my_index = index
            row_info.alignment = 'LEFT'

        if item.text.count("\n") > 0:
            multiple_strokes = True
        else:
            multiple_strokes = False


        if multiple_strokes == True:
            text_parts_list = item.text.split('\n')
            # self.draw_text(text_parts_list)
            column.separator(factor=.5)
            col = column
            for i in text_parts_list:
                row = col.row(align = 1)
                row.label(text = i)
                row.scale_y = 0
        else:
            column.separator(factor=.6)
            column.prop(item, "text", emboss=1, text = "")
        
        column_main.separator(factor=1.1)
class Notes_List_PT_scene(Panel):
    """Adds a custom panel to the TEXT_EDITOR"""

    bl_idname = 'SCENE_PT_presets'
    bl_label = " "
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    # bl_context = "object"
    # bl_context = "mesh_edit"
    bl_order = -1

    @classmethod
    def poll(cls, context):
        return bpy.context.scene != None\
            # and bpy.context.scene.mode in {'EDIT'}

    def draw_header(self, context):
        layout = self.layout
        layout.label(text = 'Notes List', icon = 'FILE')
        # layout.label(icon = 'LINENUMBERS_ON')

    def draw(self, context):
        # if bpy.context.scene != None:
            # if bpy.context.scene.mode in {'EDIT'}:
            
        layout = self.layout
        scene = bpy.context.scene

        rows = 3
        row = layout.row()
        row.template_list("NOTES_LIST_UL_items_scene", "", scene, "notes_list_scene", scene, "notes_list_scene_index", rows=rows)

        col = row.column(align=True)
        col.scale_x = 1.1
        col.scale_y = 1.2

        col.operator("notes_list_scene.list_action_add", icon='ADD', text="")
        # col.operator("window_manager.export_note_text", icon='ADD', text="").type = "object*"
        # col.operator("window_manager.export_note_text", icon='REMOVE', text="").type = "scene_delete*"
        col.operator("notes_list_scene.list_action", icon='REMOVE', text="").action = 'REMOVE'
        
        col.separator(factor = 0.4)

        col.operator("notes_list_scene.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("notes_list_scene.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        col.separator(factor = 0.4)

        col.operator('window_manager.export_note_text', text = '', icon = 'IMPORT').action = 'scene*'

        col.separator(factor = 0.4)

        col.operator('window_manager.export_note_text', text = '', icon = 'EXPORT').action = 'scene_get*'

        col.separator(factor = 0.4)

        col.operator("notes_list_scene.clear_list", icon="TRASH", text = "")
        # row = layout.row()
        # col = row.column(align=True)
        # row = col.row(align=True)
        # row.operator("presets_angle.remove_duplicates", icon="GHOST_ENABLED")



class NOTES_LIST_UL_items(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        # draw_text(self)

        act_obj = context.active_object
        idx = act_obj.notes_list_object_index

        try:
            item = act_obj.notes_list_object[index]
        except IndexError:
            pass


        column_main = layout.column(align = 1)
        box = column_main.box()
        column = box.column(align = 1)
        row_header = column.row(align = 1)
        row_header.scale_y = .7


        if bpy.context.object.notes_list_object[index].bool == True:
            row_info = row_header.row(align = 1)
            row_info.operator("notes_list_object.list_action_bool", text = "", icon = "CHECKBOX_DEHLT", emboss = 0).my_index = index
            row_info.alignment = 'RIGHT'

            # row_info = row_header.row(align = 1)
            # row_info.operator("notes_list_object.list_action_bool", text = "", icon = "SHADING_SOLID", emboss = 0).my_index = index
            # row_info.alignment = 'CENTER'
        else:
            row_info = row_header.row(align = 1)
            row_info.operator("notes_list_object.list_action_bool", text = "", icon = "BOOKMARKS", emboss = 0).my_index = index
            row_info.alignment = 'LEFT'

        if item.text.count("\n") > 0:
            multiple_strokes = True
        else:
            multiple_strokes = False


        if multiple_strokes == True:
            text_parts_list = item.text.split('\n')
            # self.draw_text(text_parts_list)
            column.separator(factor=.5)
            col = column
            for i in text_parts_list:
                row = col.row(align = 1)
                row.label(text = i)
                row.scale_y = 0
        else:
            column.separator(factor=.6)
            column.prop(item, "text", emboss=1, text = "")
        
        column_main.separator(factor=1.1)


        # space = column_main.label(text = "")
        # space.scale_y = 1
        # row = column.row()
        # row.label(text = '')
        # row.scale_y = .75

        # row = row_header.row(align = 1)
        # row.alignment = 'RIGHT'
        # row.prop(item, "bool", emboss=1, text = "", expand = 1)


        # column.operator()


        # column.separator(factor=1.0)
        # separator_spacer()

        # box = layout.box()
        # col = box.column(align = 0)
        # row = box.row(align = 1)
        # row.label(text = 'Select')
        # row.scale_y = 0

        # col.prop(item, "bool", emboss=1, text = "", expand = 1)
        # col.prop(item, "bool", emboss=1, text = "", expand = 1)
        # col.prop(item, "text", emboss=1, text = "")
        # col.prop(item, "text", emboss=1, text = "")

        # row.operator("presets_angle.list_action_refresh", text = item.name, emboss = 0, depress=0).my_index = index
        # row.prop(item, "unit", emboss=0, text = "", expand = 1)

        # row.operator("presets_angle.rename", text = "", icon = "SORTALPHA", emboss = 0).my_index = index

        # template_input_status()

    # def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
    #     act_obj = context.active_object
    #     idx = act_obj.notes_list_object_index

        # if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # split = layout.split(factor=0.3)
            # split.label(text="Index: %d" % (index))
            # custom_icon = "OUTLINER_OB_%s" % item.obj_type
            #split.prop(item, "name", text="", emboss=False, translate=False, icon=custom_icon)
        # row = layout.row(align = 0)

        # row.scale_y = 1.1
        # row.scale_x = 1.1
        # row.label(text=item.name, icon=custom_icon) # avoids renaming the item by accident
class Notes_List_PT(Panel):
    """Adds a custom panel to the TEXT_EDITOR"""

    bl_idname = 'OBJECT_PT_presets'
    bl_label = " "
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    # bl_context = "scene"
    bl_context = "object"
    # bl_context = "mesh_edit"
    bl_order = -1

    @classmethod
    def poll(cls, context):
        return bpy.context.active_object != None\
            # and bpy.context.active_object.mode in {'EDIT'}


    def draw_header(self, context):
        layout = self.layout
        layout.label(text = 'Notes List', icon = 'FILE')

    def draw(self, context):
        # if bpy.context.active_object != None:
            # if bpy.context.active_object.mode in {'EDIT'}:
            
        layout = self.layout
        act_obj = bpy.context.active_object

        rows = 3
        row = layout.row()
        row.template_list("NOTES_LIST_UL_items", "", act_obj, "notes_list_object", act_obj, "notes_list_object_index", rows=rows)

        col = row.column(align=True)
        col.scale_x = 1.1
        col.scale_y = 1.2

        col.operator("notes_list_object.list_action_add", icon='ADD', text="")
        # col.operator("window_manager.export_note_text", icon='ADD', text="").type = "object*"
        # col.operator("window_manager.export_note_text", icon='REMOVE', text="").action = "object_delete*"
        col.operator("notes_list_object.list_action", icon='REMOVE', text="").action = 'REMOVE'
        
        col.separator(factor = 0.4)

        col.operator("notes_list_object.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("notes_list_object.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        col.separator(factor = 0.4)

        col.operator('window_manager.export_note_text', text = '', icon = 'IMPORT').action = 'object*'

        col.separator(factor = 0.4)

        col.operator('window_manager.export_note_text', text = '', icon = 'EXPORT').action = 'object_get*'

        col.separator(factor = 0.4)

        col.operator("notes_list_object.clear_list", icon="TRASH", text = "")

        # row = layout.row()
        # col = row.column(align=True)
        # row = col.row(align=True)
        # row.operator("presets_angle.remove_duplicates", icon="GHOST_ENABLED")


class Notes_List_Collection(PropertyGroup):

    unit: FloatProperty(
        name="Angle",
        description="Angle",
        min=-360.0, max=360.0,
        default=0.0,
        step = 100.0,
        unit="ROTATION",
        precision = 6,)
    text: StringProperty()
    bool: BoolProperty()


Notes_list_blender_classes = [
    Notes_List_Collection,
    
    Notes_List_actions,
    Notes_List_actions_add,
    NOTES_LIST_UL_items,
    Notes_List_PT,
    Notes_actions_bool,
    Notes_List_clearList,

    Notes_List_actions_scene,
    Notes_List_actions_add_scene,
    Notes_List_clearList_scene,
    Notes_actions_bool_scene,
    NOTES_LIST_UL_items_scene,
    Notes_List_PT_scene,
]

if __name__ == "__main__":
    register()