import bpy
from bpy.types import NodeTree, Node, NodeSocket


class NodeOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "node.noter_operator"
    bl_label = ""

    action: bpy.props.StringProperty()

    @classmethod
    def description(cls, context, properties):
        if properties.action == 'node':
            return "Assign text to the node (or active node)"
        elif properties.action == 'node_get':
            return "Get text from the node (or active node)"
        elif properties.action == 'node_delete':
            return "Delete text in the node (or active node)"

        elif properties.action == 'colour':
            return "Paint the nodes in the color of the active node"
        elif properties.action == 'colour_all':
            return "Paint selected node (nodes)"

        elif properties.action == 'label':
            return "Write label text in the label text of the active node"
        elif properties.action == 'label_all':
            return "Write label text in the node (or active node)"

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

            for i in node_selected:
                # node_selected.use_custom_color = bpy.data.node_groups[node_tree.name].nodes[from_node_name].use_custom_color
                i.use_custom_color = node_active.use_custom_color
                i.color = node_active.color

        elif action == 'colour_all':
            for i in node_selected:
                i.use_custom_color = True
                i.color = bpy.context.scene.colorProperty




        elif action == "label":
            for i in node_selected:
                # i.use_custom_color = node_active.use_custom_color
                i.label = node_active.label

        elif action == "label_all":
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

  
class Node_Bool_Operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "node.noter_bool_operator"
    bl_label = "Simple Node Operator"

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


# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class MyCustomTree(NodeTree):
    # Description string
    bl_description = 'Notes Nodes'
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomTreeType'
    # Label for nice name display
    bl_label = "Notes"
    # Icon identifier
    bl_icon = 'FILE'

    # type = 'COMPOSITING'


# Custom socket type
class MyCustomSocket(NodeSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomSocketType'
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
            # self.inputs.new('CustomSocketType', "")

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
        return ntree.bl_idname == 'CustomTreeType'

# Derived from the Node base type.
class MyCustomNode(Node, MyCustomTreeNode):
    # === Basics ===
    # Description string
    '''A custom node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomNodeType'
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
        return "Press f2"
        # return self.my_bool

    def init(self, context):
        
        self.inputs.new('CustomSocketType', "")
        # self.inputs.new('CustomSocketType_2', "")
        # self.inputs[0].display_shape = 'DIAMOND'
        
        # self.inputs.new('NodeSocketFloat', "World")
        # self.inputs.new('NodeSocketVector', "!")
        # self.inputs.new('NodeSocketColor', "")

        # self.outputs.new('NodeSocketColor', "")
        self.outputs.new('CustomSocketType', "")
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

        

        

        # # self.inputs.new('CustomSocketType', "")

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
        pass

    def update(self):

        count = 0
        for i in self.inputs:
            if i.is_linked == True:
                count += 1

        if len(self.inputs) - count == 0:
            self.inputs.new('CustomSocketType', "")
            # self.inputs.new('CustomSocketType_2', "")

        elif len(self.inputs) - count > 1:

            for i in self.inputs:
                if i.is_linked == False:
                    # if i.bl_idname == 'CustomSocketType_2':
                    self.inputs.remove(i)
                    break

    def insert_link(self, link):
        count = 0
        for i in self.inputs:
            if i.is_linked == True:
                count += 1

        if len(self.inputs) - count == 0:
            self.inputs.new('CustomSocketType', "")
        elif len(self.inputs) - count == 1:
            pass
        elif len(self.inputs) - count > 1:

            for i in self.inputs:
                if i.is_linked == False:
                    self.inputs.remove(i)
                    break




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
        return context.space_data.tree_type == 'CustomTreeType'

class NODE_PT_active_node_generic(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Noter"
    bl_label = "Noter"
    
    def draw(self, context):
        layout = self.layout
        # layout.prop(self, "text", text = '')
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


# all categories in a list
node_categories = [
    # identifier, label, items list
    # MyNodeCategory('SOMENODES', "Some Nodes", NodeItem("CustomNodeType") ),

    # NodeItem("CustomNodeType"),

    MyNodeCategory('SOMENODES', "Note", items=[
        # our basic node
    NodeItem("CustomNodeType", label = 'Note Node'),
    ]),

    # MyNodeCategory("CustomNodeType"),

    MyNodeCategory('OTHERNODES', "Other Notes", items=[
        # the node item can have additional settings,
        # which are applied to new nodes
        # NB: settings values are stored as string expressions,
        # for this reason they should be converted to strings using repr()
        NodeItem("CustomNodeType", label="Without extra buttons", settings={
            "draw_extra": repr("+"),
        }),
        NodeItem("CustomNodeType", label="Without extra buttons +", settings={
            "draw_extra": repr(""),
        }),
    ]),
]

Nodes_blender_classes = (
    MyCustomTree,
    MyCustomSocket,
    MyCustomNode,
    NodeOperator,
    NODE_PT_active_node_generic,
    NODE_PT_active_node_color_2,
    MyCustomSocket_2,
    Node_Bool_Operator,
    
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
