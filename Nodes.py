import bpy
from bpy.types import NodeTree, Node, NodeSocket


class NodeOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "node.noter_operator"
    bl_label = "Simple Node Operator"

    action: bpy.props.StringProperty()

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
        file_name = bpy.context.window_manager.noter.file_name

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


        print(node_active.text, 1111111111111)

        if action == 'node':
            node_active.text = main_text

        elif action == 'node_get':
            bpy.data.texts[file_name].clear()
            bpy.data.texts[file_name].write(text_node)

        elif action == 'node_delete':
            node_active.text = ""

        # now we have the context, perform a simple operation
        # if node_active in node_selected:
        #     node_selected.remove(node_active)
        # if len(node_selected) != 1:
        #     operator.report({'ERROR'}, "2 nodes must be selected")
        #     return

        # node_other, = node_selected

        # now we have 2 nodes to operate on
        # if not node_active.inputs:
            # operator.report({'ERROR'}, "Active node has no inputs")
            # return

        # if not node_other.outputs:
        #     operator.report({'ERROR'}, "Selected node has no outputs")
        #     return

        # socket_in = node_active.inputs[0]
        # socket_out = node_other.outputs[0]

        # add a link between the two nodes
        # node_link = node_tree.links.new(socket_in, socket_out)
        return {'FINISHED'}




# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class MyCustomTree(NodeTree):
    # Description string
    '''A custom node tree type that will show up in the editor type list'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomTreeType'
    # Label for nice name display
    bl_label = "Notes Tree"
    # Icon identifier
    bl_icon = 'FILE'


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
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "my_enum_prop", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)


# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class MyCustomTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'CustomTreeType'

def draw_text_node(self, text):
    text_parts_list = text.split('\n')
    # layout = self.layout
    box = layout.box()
    # column.separator(factor=.5)
    col = box.column(align = 1)
    for i in text_parts_list:
        row = col.row(align = 1)
        row.label(text = i)
        row.scale_y = 0

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

    # === Custom Properties ===
    # These work just like custom properties in ID data blocks
    # Extensive information can be found under
    # http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Properties
    my_string_prop: bpy.props.StringProperty()
    text: bpy.props.StringProperty()
    my_float_prop: bpy.props.FloatProperty(default=3.1415926)

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    # This is the most common place to create the sockets for a node, as shown below.
    # NOTE: this is not the same as the standard __init__ function in Python, which is
    #       a purely internal Python method and unknown to the node system!
    def init(self, context):
        # self.inputs.new('CustomSocketType', "")
        # self.inputs.new('NodeSocketFloat', "World")
        # self.inputs.new('NodeSocketVector', "!")
        self.inputs.new('NodeSocketColor', "")

        self.outputs.new('NodeSocketColor', "")
        # self.outputs.new('NodeSocketColor', "are")
        # self.outputs.new('NodeSocketFloat', "you")

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.label(text="Node settings")
        text = self.text

        if text.count("\n") == 0:
            layout.prop(self, "text", text = '')
        else:
            # draw_text_node(self, self.text)
            text_parts_list = text.split('\n')
            # layout = self.layout
            box = layout.box()
            # column.separator(factor=.5)
            col = box.column(align = 1)
            for i in text_parts_list:
                row = col.row(align = 1)
                row.label(text = i)
                row.scale_y = 0
        # col = layout.column(align = 1)
        # col.operator("node.noter_operator", text = '', icon = "IMPORT").action = 'node'
        # col.operator("node.noter_operator", text = '', icon = "EXPORT").action = 'node_get'
        # col.operator("node.noter_operator", text = '', icon = "TRASH").action = 'node_delete'

        # col.operator("window_manager.export_note_text", text = 'Node', icon = 'IMPORT').action = "node"
        # col.operator("window_manager.export_note_text", text = '', icon = 'EXPORT').action = "node_get"
        # col.operator("window_manager.export_note_text", text = '', icon = 'TRASH').action = "node_delete"



    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    # def draw_buttons_ext(self, context, layout):
    #     layout.prop(self, "my_float_prop")
    #     # my_string_prop button will only be visible in the sidebar
    #     layout.prop(self, "my_string_prop")

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        return "I am a custom node"


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
        col = layout.column(align = 1)
        col.operator("node.noter_operator", text = '', icon = "IMPORT").action = 'node'
        col.operator("node.noter_operator", text = '', icon = "EXPORT").action = 'node_get'
        col.operator("node.noter_operator", text = '', icon = "TRASH").action = 'node_delete'


# all categories in a list
node_categories = [
    # identifier, label, items list
    MyNodeCategory('SOMENODES', "Some Nodes", items=[
        # our basic node
        NodeItem("CustomNodeType"),
    ]),
    MyNodeCategory('OTHERNODES', "Other Nodes", items=[
        # the node item can have additional settings,
        # which are applied to new nodes
        # NB: settings values are stored as string expressions,
        # for this reason they should be converted to strings using repr()
        NodeItem("CustomNodeType", label="Node A", settings={
            "my_string_prop": repr("Lorem ipsum dolor sit amet"),
            "my_float_prop": repr(1.0),
        }),
        NodeItem("CustomNodeType", label="Node B", settings={
            "my_string_prop": repr("consectetur adipisicing elit"),
            "my_float_prop": repr(2.0),
        }),
    ]),
]

Nodes_blender_classes = (
    MyCustomTree,
    MyCustomSocket,
    MyCustomNode,
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
