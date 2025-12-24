import bpy
import os
from . import get_addon_filepath


SOCKET = {
    # Branch structure
    "nBranches": "Socket_25",
    "trunk": "Socket_40",
    "treetop": "Socket_26",
    "numLevels": "Socket_27",
    "bLength": "Socket_28",
    "rAngle": "Socket_29",
    "rJitter": "Socket_30",
    "gravity": "Socket_31",
    "thickness": "Socket_32",
    "barkMaterial": "Socket_8",
    "seed": "Socket_16",
    "scale": "Socket_42",
    # Leaves
    "addLeaves": "Socket_19",
    "leafType": "Socket_11",
    "season": "Socket_17",
    "minHeight": "Socket_12",
    "leafDensity": "Socket_13",
    "leafMinScale": "Socket_14",
    "leafMaxScale": "Socket_15",
    "showLeaves": "Socket_39",
    "customTwigLeaf": "Socket_23",
    "customLeaf": "Socket_24",
    # Wind
    "wind": "Socket_34",
    "windAngle": "Socket_35",
    "windSpeed": "Socket_36",
    "windStrength": "Socket_37",
    "windShape": "Socket_38",
}


class ROOTED_OT_TreeHideLeaves(bpy.types.Operator):
    bl_idname = "rooted.tree_hide_leaves"
    bl_label = "Hide Leaves"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Hides all tree leaves in the viewport"

    def execute(self, context):
        for obj in bpy.data.objects:
            for mod in obj.modifiers:
                if mod.type == 'NODES' and mod.node_group == bpy.data.node_groups.get("Simple Tree Generator"):
                    mod[SOCKET["showLeaves"]] = False
                    obj.update_tag()
        bpy.context.view_layer.update()

        self.report({'INFO'}, "Hid Tree Leaves")
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class ROOTED_OT_TreeShowLeaves(bpy.types.Operator):
    bl_idname = "rooted.tree_show_leaves"
    bl_label = "Show Leaves"
    bl_description = "Shows all tree leaves in the viewport"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.data.objects:
            for mod in obj.modifiers:
                if mod.type == 'NODES' and mod.node_group == bpy.data.node_groups.get("Simple Tree Generator"):
                    mod[SOCKET["showLeaves"]] = True
                    obj.update_tag()
        bpy.context.view_layer.update()

        self.report({'INFO'}, "Showed Tree Leaves")
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class ROOTED_OT_AddTree(bpy.types.Operator):
    bl_idname = "rooted.add_tree"
    bl_label = "Add Tree"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a new procedural tree"

    def execute(self, context):
        filepath = os.path.join(get_addon_filepath(), "assets", "assets.blend")
        name = "Simple Tree Generator"

        if not filepath or not os.path.exists(filepath):
            self.report({'ERROR'}, f"Asset .blend file not found: {filepath}. Please ensure it exists in the 'assets' subfolder of the add-on.")
            return {'CANCELLED'}

        bpy.ops.mesh.primitive_cube_add(location=bpy.context.scene.cursor.location)
        obj = bpy.context.active_object
        obj.name = "Tree"

        mod = obj.modifiers.new(name="Tree Generator", type='NODES')

        if name in bpy.data.node_groups:
            mod.node_group = bpy.data.node_groups[name]
        else:
            try:
                with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
                    if name in data_from.node_groups:
                        data_to.node_groups.append(name)
                    else:
                        self.report({'ERROR'}, f"Node Group '{name}' not found in '{filepath}'.")
                        return {'CANCELLED'}
                if name in bpy.data.node_groups:
                    mod.node_group = bpy.data.node_groups[name]
                    self.report({'INFO'}, f"Successfully appended Node Group '{name}' from '{filepath}'.")
                else:
                    self.report({'ERROR'}, f"Failed to append Node Group '{name}'.")
                    return {'CANCELLED'}
            except Exception as e:
                self.report({'ERROR'}, f"Error appending node group: {e}")
                return {'CANCELLED'}

        # Apply preset (scale=1.0 for all tree presets)
        if context.scene.tree_preset == 'SMALL':
            mod[SOCKET["scale"]] = 1.0

        elif context.scene.tree_preset == 'TALL':
            mod[SOCKET["trunk"]] = 5
            mod[SOCKET["numLevels"]] = 5
            mod[SOCKET["bLength"]] = 8
            mod[SOCKET["rAngle"]] = 0.698
            mod[SOCKET["thickness"]] = 3.0
            mod[SOCKET["scale"]] = 1.0

        elif context.scene.tree_preset == 'THIN':
            mod[SOCKET["trunk"]] = 2
            mod[SOCKET["treetop"]] = 5
            mod[SOCKET["numLevels"]] = 4
            mod[SOCKET["bLength"]] = 6
            mod[SOCKET["rAngle"]] = 0.523
            mod[SOCKET["thickness"]] = 1.8
            mod[SOCKET["minHeight"]] = 5
            mod[SOCKET["scale"]] = 1.0

        elif context.scene.tree_preset == 'DEAD':
            mod[SOCKET["nBranches"]] = 0  # 0=Two Branches
            mod[SOCKET["trunk"]] = 1
            mod[SOCKET["numLevels"]] = 4
            mod[SOCKET["bLength"]] = 10
            mod[SOCKET["rAngle"]] = 0.41
            mod[SOCKET["rJitter"]] = 0.25
            mod[SOCKET["gravity"]] = 1.7
            mod[SOCKET["thickness"]] = 1.8
            mod[SOCKET["addLeaves"]] = False
            mod[SOCKET["scale"]] = 1.0

        elif context.scene.tree_preset == 'LARGE':
            mod[SOCKET["trunk"]] = 2
            mod[SOCKET["treetop"]] = 2
            mod[SOCKET["numLevels"]] = 6
            mod[SOCKET["bLength"]] = 8
            mod[SOCKET["rAngle"]] = 0.488
            mod[SOCKET["thickness"]] = 2.9
            mod[SOCKET["scale"]] = 1.0

        elif context.scene.tree_preset == 'CUSTOM':
            mod[SOCKET["trunk"]] = context.scene.custom_trunk
            mod[SOCKET["treetop"]] = context.scene.custom_treetop
            mod[SOCKET["numLevels"]] = context.scene.custom_num_levels
            mod[SOCKET["bLength"]] = context.scene.custom_branch_length
            mod[SOCKET["rAngle"]] = context.scene.custom_branch_angle
            mod[SOCKET["rJitter"]] = context.scene.custom_jitter
            mod[SOCKET["gravity"]] = context.scene.custom_gravity
            mod[SOCKET["thickness"]] = context.scene.custom_thickness
            mod[SOCKET["minHeight"]] = context.scene.custom_min_height
            mod[SOCKET["nBranches"]] = 0 if context.scene.custom_n_branches == 2 else 1  # 0=Two, 1=Three
            mod[SOCKET["addLeaves"]] = context.scene.custom_add_leaves
            mod[SOCKET["scale"]] = context.scene.custom_scale

        # Apply season
        if context.scene.season == 'SPRING':
            mod[SOCKET["season"]] = 0.0
        elif context.scene.season == 'SUMMER':
            mod[SOCKET["season"]] = 0.5
        elif context.scene.season == 'CUSTOM':
            mod[SOCKET["season"]] = context.scene.custom_season_value
        else:
            mod[SOCKET["season"]] = 1.0

        mod[SOCKET["seed"]] = context.scene.tree_seed

        # Auto-increment seed for next tree
        context.scene.tree_seed += 1

        self.report({'INFO'}, f"Added {obj.name}!")
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


classes = [ROOTED_OT_AddTree, ROOTED_OT_TreeHideLeaves, ROOTED_OT_TreeShowLeaves]

