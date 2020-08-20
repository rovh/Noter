import bpy
from bpy.types import NodeTree, Node, NodeSocket
# import itertools
from bpy.app.translations import pgettext_iface as iface_
# import time


class NodeOperators(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "node.noter_operator"
    bl_label = ""

    action: bpy.props.StringProperty()

    @classmethod
    def description(cls, context, properties):


        is_node = bool(  properties.action.count("*")  ) 

        if is_node == True:
            action = properties.action
            action = action.split("*")
            action = action[0]

            if action == 'node':
                return "Assign text to the current node"
            elif action == 'node_get':
                return "Get text from the current node"
            elif action == 'node_delete':
                return "Delete text in the current node"
        else:

            if properties.action == 'node':
                return "Assign text to the active node"
            elif properties.action == 'node_get':
                return "Get text from the active node"
            elif properties.action == 'node_delete':
                return "Delete text in the active node"

            elif properties.action == 'colour':
                return "Paint the nodes in the color of the active node"
            elif properties.action == 'colour_all':
                return "Paint selected node (nodes)"

            elif properties.action == 'label':
                return "Write label text from the label text of the active node"
            elif properties.action == 'label_all':
                return "Write label text in the selected node (nodes)"

        

    @classmethod
    def poll(cls, context):
        # space = False
        # for area in bpy.context.screen.areas:
        #     if area.type == ('NODE_EDITOR'):
        #         space = True
        #         break
        # return space
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):
        # space = None
        # for area in bpy.context.screen.areas:
        #     if area.type == ('NODE_EDITOR'):
        #         space = area
        #         print (space)
        #         break

        # space = context.space_data
        # return space.type == 'NODE_EDITOR'

        
        action = self.action
        space = context.space_data
        node_tree = space.node_tree
        node_active = context.active_node
        text_node = node_active.text
        node_selected = context.selected_nodes
        file_name = bpy.context.scene.file_name
        

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

        


        # print(node_active.text, 1111111111111)
        # print(len(node_active.internal_links))
        # print(node_active.inputs[0].is_linked)
        from_node = False

        if action.count("*"):
            action, from_node_name = action.split("*")[0], action.split("*")[1]
            from_node = True



        if action == 'node':
            if from_node == True:
                bpy.data.node_groups[node_tree.name].nodes[from_node_name].text = main_text
            else:
                node_active.text = main_text
        
        elif action == 'node_get':
            bpy.data.texts[file_name].clear()
            if from_node == True:
                text_node = bpy.data.node_groups[node_tree.name].nodes[from_node_name].text
                bpy.data.texts[file_name].write(text_node)
            else:
                bpy.data.texts[file_name].write(text_node)

        elif action == 'node_delete':
            if from_node == True:
                bpy.data.node_groups[node_tree.name].nodes[from_node_name].text = ''
            else:
                node_active.text = ""
  


        elif action == 'colour':

            if len(node_selected) == 0:
                text = "No selected nodes was found"
                war = "WARNING"
                self.report({war}, text)
                return {'FINISHED'}

            for i in node_selected:
                # node_selected.use_custom_color = bpy.data.node_groups[node_tree.name].nodes[from_node_name].use_custom_color
                i.use_custom_color = node_active.use_custom_color
                i.color = node_active.color

        elif action == 'colour_all':

            if len(node_selected) == 0:
                text = "No selected nodes was found"
                war = "WARNING"
                self.report({war}, text)
                return {'FINISHED'}

            for i in node_selected:
                i.use_custom_color = True
                i.color = bpy.context.scene.colorProperty




        elif action == "label":

            if len(node_selected) == 0:
                text = "No selected nodes was found"
                war = "WARNING"
                self.report({war}, text)
                return {'FINISHED'}

            for i in node_selected:
                # i.use_custom_color = node_active.use_custom_color
                i.label = node_active.label

        elif action == "label_all":

            if len(node_selected) == 0:
                text = "No selected nodes was found"
                war = "WARNING"
                self.report({war}, text)
                return {'FINISHED'}

            for i in node_selected:
                # i.use_custom_color = node_active.use_custom_color
                i.label = bpy.context.scene.label_node_text



        # now we have the context, perform a simple operation
        # if node_active in node_selected:
        #     node_selected.remove(node_active)
        # if len(node_selected) != 1:
        #     operator.report({'ERROR'}, "2 nodes must be selected")
        #     return

        # node_other, = node_selected

        # now we have 2 nodes to operate on
        # 
            # operaif not node_active.inputs:tor.report({'ERROR'}, "Active node has no inputs")
            # return

        # if not node_other.outputs:
        #     operator.report({'ERROR'}, "Selected node has no outputs")
        #     return

        # socket_in = node_active.inputs[0]
        # socket_out = node_other.outputs[0]

        # add a link between the two nodes
        # node_link = node_tree.links.new(socket_in, socket_out)
        return {'FINISHED'}

class Note_Node_Bool_Operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "node.noter_bool_operator"
    bl_label = ""
    bl_description = "Mute or unmute current node"

    # my_bool: bpy.props.FloatProperty()
    # my_bool: bpy.props.CollectionProperty(type = MyCustomNode)
    # name: bpy.props.PointerProperty(type = MyCustomTreeNode)
    # my_bool: bpy.props.StringProperty()
    name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        space = context.space_data
        node_tree = space.node_tree
        mute = bpy.data.node_groups[node_tree.name].nodes[self.name].mute
        
   
        if mute == True:
            bpy.data.node_groups[node_tree.name].nodes[self.name].mute = False
        else:
            bpy.data.node_groups[node_tree.name].nodes[self.name].mute = True
    

        

        return {'FINISHED'}

class Add_Nodes_Tree(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "node.noter_add_nodes_tree"
    bl_label = ""
    bl_description = "Mute or unmute current node"

    # my_bool: bpy.props.FloatProperty()
    # my_bool: bpy.props.CollectionProperty(type = MyCustomNode)
    # name: bpy.props.PointerProperty(type = MyCustomTreeNode)
    # my_bool: bpy.props.StringProperty()
    name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):


        context.space_data.node_tree = bpy.data.node_groups.new("", 'Noter_CustomTreeType')

        return {'FINISHED'}


# def iterSingleNodeItems():
    # for node in iterAnimationNodeClasses():
    #     if not node.onlySearchTags:
    #         yield SingleNodeInsertionItem(node.bl_idname, node.bl_label)
    #     for customSearch in node.getSearchTags():
    #         if isinstance(customSearch, tuple):
    #             yield SingleNodeInsertionItem(node.bl_idname, customSearch[0], customSearch[1])
    #         else:
    #             yield SingleNodeInsertionItem(node.bl_idname, customSearch)
    # for network in getSubprogramNetworks():
    #     yield SingleNodeInsertionItem("an_InvokeSubprogramNode", network.name,
    #         {"subprogramIdentifier" : repr(network.identifier)})
# itemsByIdentifier = {}
# class NodeSearch(bpy.types.Operator):
    # bl_idname = "an.node_search"
    # bl_label = "Node Search"
    # bl_options = {"REGISTER"}
    # bl_property = "item"

    # def getSearchItems(self, context):
    #     itemsByIdentifier.clear()
    #     items = []
    #     for item in itertools.chain(iterSingleNodeItems()):
    #         itemsByIdentifier[item.identifier] = item
    #         items.append((item.identifier, item.searchTag, ""))
    #     return items

    # item: bpy.props.EnumProperty(items = getSearchItems)

    # # @classmethod
    # # def poll(cls, context):
    # #     try: return context.space_data.node_tree.bl_idname == "an_AnimationNodeTree"
    # #     except: return False

    # def invoke(self, context, event):
    #     context.window_manager.invoke_search_popup(self)
    #     return {"CANCELLED"}

    # def execute(self, context):
    #     itemsByIdentifier[self.item].insert()
    #     return {"FINISHED"}




# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class MyCustomTree(NodeTree):
    # Description string
    bl_description = 'Notes Nodes'
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'Noter_CustomTreeType'
    # Label for nice name display
    bl_label = "Notes Tree"
    # Icon identifier
    bl_icon = 'FILE'

    # type = 'COMPOSITING'


# Custom socket type
class MyCustomSocket(NodeSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'Noter_CustomSocketType'
    # Label for nice name display
    bl_label = "Custom Node Socket"

    # Enum items list
    my_items = (
        ('DOWN', "Down", "Where your feet are"),
        ('UP', "Up", "Where your head should be"),
        ('LEFT', "Left", "Not right"),
        ('RIGHT', "Right", "Not left"),
    )

    my_enum_prop: bpy.props.EnumProperty(
        name="Direction",
        description="Just an example",
        items=my_items,
        default='UP',
    )

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        # if self.is_output or self.is_linked:
        #     layout.label(text=text)
        # else:
        #     layout.prop(self, "my_enum_prop", text=text)

        # layout.label(text="Text")
        # if len(node.inputs)
        # for i in range(0, len(node.inputs) ):
            # if i == 0: 
            # self.inputs.new('Noter_CustomSocketType', "")

        # text = node.text
        # if text.count("\n") == 0:
        #     layout.prop(node, "text", text = '')
        # else:
        #     text_parts_list = text.split('\n')
        #     box = layout.box()
        #     box = box.box()
        #     col = box.column(align = 1)
        #     for i in text_parts_list:
        #         row = col.row(align = 1)
        #         row.label(text = i)
        #         row.scale_y = 0
        #         # break
        pass

    # Socket color
    def draw_color(self, context, node):
        # return (1.0, 0.4, 0.216, 1)
        # return (1, 1, 0.035, .9)
        return (0.8, 0.8, 0.03, 1.000000)

class MyCustomSocket_2(NodeSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomSocketType_2'
    # Label for nice name display
    bl_label = "Custom Node Socket"

    my_bool: bpy.props.BoolProperty()


    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        # if self.is_output or self.is_linked:
        layout.prop(self, 'my_bool', text = '')
        # else:
        #     layout.prop(self, "my_enum_prop", text=text)
        pass

    # Socket color
    def draw_color(self, context, node):
        # return (1.0, 0.4, 0.216, 1)
        # return (1, 1, 0.035, .9)
        return (0.8, 0.8, 0.03, 1.000000)
# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class MyCustomTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'Noter_CustomTreeType'

# Derived from the Node base type.
class MyCustomNode(Node, MyCustomTreeNode):
    # === Basics ===
    # Description string
    '''A custom node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'Noter_CustomNodeType'
    # Label for nice name display
    bl_label = "Custom Node"
    # Icon identifier
    # bl_icon = 'SOUND'
    bl_width_default = 200


    # === Custom Properties ===
    # These work just like custom properties in ID data blocks
    # Extensive information can be found under
    # http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Properties
    text: bpy.props.StringProperty()
    my_bool: bpy.props.BoolProperty()
    draw_extra: bpy.props.StringProperty(default = "++")

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    # This is the most common place to create the sockets for a node, as shown below.
    # NOTE: this is not the same as the standard __init__ function in Python, which is
    #       a purely internal Python method and unknown to the node system!

    def draw_label(self):
        # def draw_color(self, context, node):
        # return (1.0, 0.4, 0.216, 1)
        # return (1, 1, 0.035, .9)
        # return (0.8, 0.8, 0.03, 1.000000)
        return " "
        # return "Press F2"
        # return self.my_bool

    def init(self, context):
        
        self.inputs.new('Noter_CustomSocketType', "")
        # self.inputs.new('CustomSocketType_2', "")
        # self.inputs[0].display_shape = 'DIAMOND'
        
        # self.inputs.new('NodeSocketFloat', "World")
        # self.inputs.new('NodeSocketVector', "!")
        # self.inputs.new('NodeSocketColor', "")

        # self.outputs.new('NodeSocketColor', "")
        self.outputs.new('Noter_CustomSocketType', "")
        # self.outputs.new('CustomSocketType_2', "")
        # self.outputs.new('NodeSocketColor', "are")
        # self.outputs.new('NodeSocketFloat', "you")

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        pass
        # print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        # print("Removing node ", self, ", Goodbye!")
        pass

    # Additional buttons displayed on the node.
    # def draw_buttons_ext(self, context, layout):
    def draw_buttons(self, context, layout):
        # layout.label(text="Text")
        # row_header = layout.row()

        # ic = 'CHECKMARK' if self.mute else 'BLANK1'

        # row = row_header.row()
        # row.operator("node.noter_bool_operator",  icon = ic, text = '', depress = self.mute).name = self.name
        # row.alignment = 'LEFT'
        # if self.mute == True:
        #     row.scale_y = 2
        #     row.scale_x = 2
        # else:
        #     row.scale_y = 1
        #     row.scale_x = 1

        # row = row_header.row()
        # row.operator("node.noter_operator",  icon = 'IMPORT', text = '').action = f"node*{self.name}"
        # row.operator("node.noter_operator",  icon = 'EXPORT', text = '').action = f"node_get*{self.name}"
        # row.operator("node.noter_operator",  icon = 'TRASH', text = '').action = f"node_delete*{self.name}"
        # row.alignment = 'RIGHT'
        # row.scale_y = 1.3
        # row.scale_x = 1.3

        

        

        # # self.inputs.new('Noter_CustomSocketType', "")

        text = self.text
        if text.count("\n") == 0:
            layout.separator(factor = 1)
            box = layout.box()
            box.prop(self, "text", text = '')
        else:
            text_parts_list = text.split('\n')
            layout.separator(factor = .5)
            box = layout.box()
            box = box.box()
            col = box.column(align = 1)
            for i in text_parts_list:
                row = col.row(align = 1)
                row.label(text = i)
                row.scale_y = 0

        draw_extra_count = self.draw_extra.count("+")

        if draw_extra_count >= 1:

            layout.separator(factor = 2)

            row_header = layout.row()

            ic = 'CHECKMARK' if self.mute else 'BLANK1'

            row = row_header.row()
            row.operator("node.noter_bool_operator",  icon = ic, text = '', depress = self.mute).name = self.name
            row.alignment = 'LEFT'
            if self.mute == True:
                row.scale_y = 2.5
                row.scale_x = 2.5
            else:
                row.scale_y = 1
                row.scale_x = 1

            if draw_extra_count >= 2:

                row = row_header.row()
                row.operator("node.noter_operator",  icon = 'IMPORT', text = '').action = f"node*{self.name}"
                row.operator("node.noter_operator",  icon = 'EXPORT', text = '').action = f"node_get*{self.name}"
                row.operator("node.noter_operator",  icon = 'TRASH', text = '').action = f"node_delete*{self.name}"
                row.alignment = 'RIGHT'
                row.scale_y = 1.6
                row.scale_x = 1.6

        # col = layout.column(align = 1)
        # col.operator("node.noter_operator", text = '', icon = "IMPORT").action = 'node'
        # col.operator("node.noter_operator", text = '', icon = "EXPORT").action = 'node_get'
        # col.operator("node.noter_operator", text = '', icon = "TRASH").action = 'node_delete'

        # col.operator("window_manager.export_note_text", text = 'Node', icon = 'IMPORT').action = "node"
        # col.operator("window_manager.export_note_text", text = '', icon = 'EXPORT').action = "node_get"
        # col.operator("window_manager.export_note_text", text = '', icon = 'TRASH').action = "node_delete"
        # pass

    def update(self):

        count = 0
        for i in self.inputs:
            if i.is_linked == True:
                count += 1
        free_inputs = len(self.inputs) - count


        if free_inputs == 0:
            self.inputs.new('Noter_CustomSocketType', "")
            # self.inputs.new('CustomSocketType_2', "")
        elif free_inputs > 1:

            for i in self.inputs:

                if i.is_linked == False and free_inputs > 1:
                    self.inputs.remove(i)
                    free_inputs -= 1
                elif i.is_linked == True:
                    pass
                else:
                    break
    

    # def insert_link(self, link):
    #     count = 0
    #     for i in self.inputs:
    #         if i.is_linked == True:
    #             count += 1
    #     free_inputs = len(self.inputs) - count



    #     if free_inputs == 0:
    #         self.inputs.new('Noter_CustomSocketType', "")
    #         # self.inputs.new('CustomSocketType_2', "")

    #     elif free_inputs > 1:

    #         for i in self.inputs:

    #             if i.is_linked == False and free_inputs > 1:
    #                 self.inputs.remove(i)
    #                 free_inputs -= 1
    #             elif i.is_linked == True:
    #                 pass
    #             else:
    #                 break




    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    # def draw_buttons_ext(self, context, layout):
    #     layout.prop(self, "my_float_prop")
    #     # my_string_prop button will only be visible in the sidebar
    #     layout.prop(self, "my_string_prop")

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
  

### Node Categories ###
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.
# For more examples see release/scripts/startup/nodeitems_builtins.py

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type


class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'Noter_CustomTreeType'

class NODE_PT_active_node_generic(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Noter"
    bl_label = "Noter"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'Noter_CustomTreeType'
    
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(context.scene, "file_name", text = '')
        row.scale_y = 1.3


        box = layout.box()
        column = box.column(align = 1)
        column.scale_y = 1.3
        column.operator("node.noter_operator", text = '', icon = "IMPORT").action = 'node'
        column.operator("node.noter_operator", text = '', icon = "EXPORT").action = 'node_get'
        column.operator("node.noter_operator", text = '', icon = "TRASH").action = 'node_delete'

        column.separator(factor = 2)
        # column.template_columnor_picker(self, "columnorProperty", value_slider = True)
        # column.prop(self, "columnorProperty")
        

        column.operator("node.noter_operator", text = 'Copy-Paste', icon = "BRUSH_DATA").action = 'colour'
        column.operator("node.noter_operator", text = 'Copy-Paste', icon = "TOPBAR").action = 'label'
        
        column.separator(factor = 2)

        row = column.row(align = 1)
        row_row = row.row(align = 1)
        row_row.operator("node.noter_operator", text = 'Paint', icon = "BRUSH_DATA").action = 'colour_all'
        
        row_row = row.row(align = 1)
        row_row.scale_x = .6
        row_row.prop(bpy.context.scene, "colorProperty", text = "")

        column.separator(factor = 2)

        column.operator("node.noter_operator", text = 'Write Label', icon = "TOPBAR").action = 'label_all'
        column.prop(bpy.context.scene, "label_node_text", text = "")

        column.separator(factor = 1)
        
        # row_row = row.row(align = 1)
        # row_row.scale_x = 2

class NODE_PT_active_node_color_2 (bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Noter"
    bl_label = "Node Color"
    # bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'NODE_PT_active_node_generic'

    @classmethod
    def poll(cls, context):
        return context.active_node is not None

    def draw_header(self, context):
        node = context.active_node
        self.layout.prop(node, "use_custom_color", text="")

    def draw_header_preset(self, _context):
        bpy.types.NODE_PT_node_color_presets.draw_panel_header(self.layout)

    def draw(self, context):
        layout = self.layout
        node = context.active_node

        layout.enabled = node.use_custom_color

        row = layout.row()
        row.prop(node, "color", text="")
        row.menu("NODE_MT_node_color_context_menu", text="", icon='DOWNARROW_HLT')

class NODE_SPACE_PT_AnnotationDataPanel_2(bpy.types.Panel):
    bl_label = "Annotations"
    bl_region_type = 'UI'
    bl_space_type = 'NODE_EDITOR'
    bl_category = "Noter"
    # bl_parent_id = 'NODE_PT_active_node_generic'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        # Show this panel as long as someone that might own this exists
        # AND the owner isn't an object (e.g. GP Object)
        if context.space_data.tree_type == 'Noter_CustomTreeType':
            if context.annotation_data_owner is None:
                return False
            elif type(context.annotation_data_owner) is bpy.types.Object:
                return False
            else:
                return True

    def draw_header(self, context):
        if context.space_data.type not in {'VIEW_3D', 'TOPBAR'}:
            self.layout.prop(context.space_data, "show_annotation", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_decorate = False

        # Grease Pencil owner.
        gpd_owner = context.annotation_data_owner
        gpd = context.annotation_data

        # Owner selector.
        if context.space_data.type == 'CLIP_EDITOR':
            layout.row().prop(context.space_data, "annotation_source", expand=True)

        layout.template_ID(gpd_owner, "grease_pencil", new="gpencil.annotation_add", unlink="gpencil.data_unlink")

        # List of layers/notes.
        if gpd and gpd.layers:
            self.draw_layers(context, layout, gpd)

    def draw_layers(self, context, layout, gpd):
        row = layout.row()

        col = row.column()
        if len(gpd.layers) >= 2:
            layer_rows = 5
        else:
            layer_rows = 3
        col.template_list("GPENCIL_UL_annotation_layer", "", gpd, "layers", gpd.layers, "active_index",
                          rows=layer_rows, sort_reverse=True, sort_lock=True)

        col = row.column()

        sub = col.column(align=True)
        sub.operator("gpencil.layer_annotation_add", icon='ADD', text="")
        sub.operator("gpencil.layer_annotation_remove", icon='REMOVE', text="")

        gpl = context.active_annotation_layer
        if gpl:
            if len(gpd.layers) > 1:
                col.separator()

                sub = col.column(align=True)
                sub.operator("gpencil.layer_annotation_move", icon='TRIA_UP', text="").type = 'UP'
                sub.operator("gpencil.layer_annotation_move", icon='TRIA_DOWN', text="").type = 'DOWN'

        tool_settings = context.tool_settings
        if gpd and gpl:
            layout.prop(gpl, "thickness")
        else:
            layout.prop(tool_settings, "annotation_thickness", text="Thickness")

        if gpl:
            # Full-Row - Frame Locking (and Delete Frame)
            row = layout.row(align=True)
            row.active = not gpl.lock

            if gpl.active_frame:
                lock_status = iface_("Locked") if gpl.lock_frame else iface_("Unlocked")
                lock_label = iface_("Frame: %d (%s)") % (gpl.active_frame.frame_number, lock_status)
            else:
                lock_label = iface_("Lock Frame")
            row.prop(gpl, "lock_frame", text=lock_label, icon='UNLOCKED')
            row.operator("gpencil.annotation_active_frame_delete", text="", icon='X')



def insertNode(layout, type, text, settings = {}, icon = "NONE"):
    operator = layout.operator("node.add_node", text = text, icon = icon)
    operator.type = type
    operator.use_transform = True
    for name, value in settings.items():
        item = operator.settings.add()
        item.name = name
        item.value = value
    return operator

class NODE_MT_add_menu_notes(bpy.types.Menu):
    bl_label = "Note"

    def draw(self, context):
        layout = self.layout
        
        props = layout.operator("node.add_node", text = "Note Node", icon = 'FILE')
        props.use_transform = True
        props.type = "Noter_CustomNodeType"

class NODE_MT_add_menu_layout(bpy.types.Menu):
    bl_label = "Layout"

    def draw(self, context):
        layout = self.layout

        # layout.operator_context = 'INVOKE_AREA'
        
        props = layout.operator("node.add_node", text = "Reroute", icon = 'REC')
        props.use_transform = True
        props.type = "NodeReroute"
        
        props = layout.operator("node.add_node", text = "Frame", icon = 'MATPLANE')
        props.use_transform = True
        props.type = "NodeFrame"

class NODE_MT_add_menu_othernotes(bpy.types.Menu):
    bl_label = "Other Notes"

    def draw(self, context):
        layout = self.layout

        insertNode(layout, "Noter_CustomNodeType", "Without extra buttons", {"draw_extra" : repr("+")}, 'OUTLINER_DATA_POINTCLOUD')
        
        insertNode(layout, "Noter_CustomNodeType", "Without extra buttons +", {"draw_extra" : repr("")}, 'LAYER_USED')

def add_to_add_menu(self, context):
    if context.space_data.tree_type == 'Noter_CustomTreeType':
        layout = self.layout


        if bool(context.space_data.edit_tree) ==  True:

            factor = .5

            # layout.operator('node.add_search', text = "Search...", icon = 'VIEWZOOM').use_transform = True

            layout.separator(factor = 1)

            layout.menu("NODE_MT_add_menu_notes", text = "Note", icon = "FILE")

            layout.separator(factor = factor)

            layout.menu("NODE_MT_add_menu_othernotes", text = "Other Notes", icon = 'DOCUMENTS')

            layout.separator(factor = factor)

            layout.menu("NODE_MT_add_menu_layout", text = "Layout", icon = 'SEQ_STRIP_META')

            layout.separator(factor = 1)

        else:
            row = layout.row()
            row.scale_y = 2
            row.operator('node.noter_add_nodes_tree', text = "Create New Node Tree", icon = 'ADD')

            layout.separator(factor = 1)



# all categories in a list
node_categories = [

    # identifier, label, items list
    # # MyNodeCategory('SOMENODES', "Some Nodes", NodeItem("Noter_CustomNodeType") ),

    # # NodeItem("Noter_CustomNodeType"),

    # MyNodeCategory('SOMENODES', "", items=[
    #     # our basic node
    # NodeItem("Noter_CustomNodeType", label = 'Note Node'),
    # ]),

    # # MyNodeCategory("Noter_CustomNodeType"),

    # MyNodeCategory('OTHERNODES', "Other Notes", items=[
    #     # the node item can have additional settings,
    #     # which are applied to new nodes
    #     # NB: settings values are stored as string expressions,
    #     # for this reason they should be converted to strings using repr()
    #     NodeItem("Noter_CustomNodeType", label="Without extra buttons", settings={
    #         "draw_extra": repr("+"),
    #     }),

    #     NodeItem("Noter_CustomNodeType", label="Without extra buttons +", settings={
    #         "draw_extra": repr(""),
    #     }),
    # ]),

    MyNodeCategory('OTHERNODES', "", items=[
        
        NodeItem("Noter_CustomNodeType", label="Note Nodes"
        ),
        
        NodeItem("Noter_CustomNodeType", label="Without extra buttons", settings={
            "draw_extra": repr("+"),
        }),

        NodeItem("Noter_CustomNodeType", label="Without extra buttons +", settings={
            "draw_extra": repr(""),
        }),
    

    ]
    ),

]

Nodes_blender_classes = (
    # MyNodeCategory,
    MyCustomTree,
    MyCustomSocket,
    MyCustomNode,
    NodeOperators,
    NODE_PT_active_node_generic,
    NODE_PT_active_node_color_2,
    NODE_SPACE_PT_AnnotationDataPanel_2,
    MyCustomSocket_2,
    Note_Node_Bool_Operator,
    Add_Nodes_Tree,


    NODE_MT_add_menu_layout,
    NODE_MT_add_menu_othernotes,
    NODE_MT_add_menu_notes,
    
)





# def register():
#     from bpy.utils import register_class
#     for cls in classes:
#         register_class(cls)

#     nodeitems_utils.register_node_categories('CUSTOM_NODES', node_categories)


# def unregister():
#     nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

#     from bpy.utils import unregister_class
#     for cls in reversed(classes):
#         unregister_class(cls)


if __name__ == "__main__":
    register()
