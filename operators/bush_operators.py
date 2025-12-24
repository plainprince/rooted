import bpy
import os
import math
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


class ROOTED_OT_BushHideLeaves(bpy.types.Operator):
    bl_idname = "rooted.bush_hide_leaves"
    bl_label = "Hide Leaves"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Hides all bush leaves in the viewport"

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.name.startswith("Bush"):
                for mod in obj.modifiers:
                    if mod.type == 'NODES' and mod.node_group == bpy.data.node_groups.get("Simple Tree Generator"):
                        mod[SOCKET["showLeaves"]] = False
                        obj.update_tag()
        bpy.context.view_layer.update()

        self.report({'INFO'}, "Hid Bush Leaves")
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class ROOTED_OT_BushShowLeaves(bpy.types.Operator):
    bl_idname = "rooted.bush_show_leaves"
    bl_label = "Show Leaves"
    bl_description = "Shows all bush leaves in the viewport"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.name.startswith("Bush"):
                for mod in obj.modifiers:
                    if mod.type == 'NODES' and mod.node_group == bpy.data.node_groups.get("Simple Tree Generator"):
                        mod[SOCKET["showLeaves"]] = True
                        obj.update_tag()
        bpy.context.view_layer.update()

        self.report({'INFO'}, "Showed Bush Leaves")
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class ROOTED_OT_AddBush(bpy.types.Operator):
    bl_idname = "rooted.add_bush"
    bl_label = "Add Bush"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a new procedural bush"

    def execute(self, context):
        filepath = os.path.join(get_addon_filepath(), "assets", "assets.blend")
        name = "Simple Tree Generator"

        if not filepath or not os.path.exists(filepath):
            self.report({'ERROR'}, f"Asset .blend file not found: {filepath}. Please ensure it exists in the 'assets' subfolder of the add-on.")
            return {'CANCELLED'}

        bpy.ops.mesh.primitive_cube_add(location=bpy.context.scene.cursor.location)
        obj = bpy.context.active_object
        obj.name = "Bush"

        mod = obj.modifiers.new(name="Bush Generator", type='NODES')

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

        # Bush base settings: no trunk, branches point upward, dense foliage
        # These get overridden by presets below, but set sensible defaults
        mod[SOCKET["trunk"]] = 0  # No stem
        mod[SOCKET["minHeight"]] = 0  # Branches from ground level

        # Apply preset (all based on user-tested MEDIUM values)
        if context.scene.bush_preset == 'SMALL':
            # Compact, less complex version
            mod[SOCKET["nBranches"]] = 0  # Two Branches
            mod[SOCKET["treetop"]] = 1
            mod[SOCKET["numLevels"]] = 4
            mod[SOCKET["bLength"]] = 3
            mod[SOCKET["rAngle"]] = math.radians(24.0)
            mod[SOCKET["rJitter"]] = 0.2
            mod[SOCKET["gravity"]] = 2.2
            mod[SOCKET["thickness"]] = 1.0
            mod[SOCKET["leafDensity"]] = 0.66
            mod[SOCKET["leafMinScale"]] = 0.25
            mod[SOCKET["leafMaxScale"]] = 0.8
            mod[SOCKET["scale"]] = 0.5

        elif context.scene.bush_preset == 'MEDIUM':
            # User-tested values
            mod[SOCKET["nBranches"]] = 0  # Two Branches
            mod[SOCKET["treetop"]] = 1
            mod[SOCKET["numLevels"]] = 5
            mod[SOCKET["bLength"]] = 4
            mod[SOCKET["rAngle"]] = math.radians(25.2)
            mod[SOCKET["rJitter"]] = 0.2
            mod[SOCKET["gravity"]] = 2.4
            mod[SOCKET["thickness"]] = 1.3
            mod[SOCKET["leafDensity"]] = 0.66
            mod[SOCKET["leafMinScale"]] = 0.3
            mod[SOCKET["leafMaxScale"]] = 1.0
            mod[SOCKET["scale"]] = 0.6

        elif context.scene.bush_preset == 'LARGE':
            # Bigger, more sprawling
            mod[SOCKET["nBranches"]] = 0  # Two Branches
            mod[SOCKET["treetop"]] = 2
            mod[SOCKET["numLevels"]] = 6
            mod[SOCKET["bLength"]] = 5
            mod[SOCKET["rAngle"]] = math.radians(26.0)
            mod[SOCKET["rJitter"]] = 0.2
            mod[SOCKET["gravity"]] = 2.6
            mod[SOCKET["thickness"]] = 1.5
            mod[SOCKET["leafDensity"]] = 0.66
            mod[SOCKET["leafMinScale"]] = 0.35
            mod[SOCKET["leafMaxScale"]] = 1.0
            mod[SOCKET["scale"]] = 0.8

        elif context.scene.bush_preset == 'HEDGE':
            # More vertical, compact for hedges
            mod[SOCKET["nBranches"]] = 0  # Two Branches
            mod[SOCKET["treetop"]] = 1
            mod[SOCKET["numLevels"]] = 5
            mod[SOCKET["bLength"]] = 3
            mod[SOCKET["rAngle"]] = math.radians(18.0)  # More upward
            mod[SOCKET["rJitter"]] = 0.15
            mod[SOCKET["gravity"]] = 1.5  # Less droop for vertical shape
            mod[SOCKET["thickness"]] = 1.0
            mod[SOCKET["leafDensity"]] = 0.75
            mod[SOCKET["leafMinScale"]] = 0.2
            mod[SOCKET["leafMaxScale"]] = 0.7
            mod[SOCKET["scale"]] = 0.7

        elif context.scene.bush_preset == 'CUSTOM':
            mod[SOCKET["nBranches"]] = 0 if context.scene.bush_custom_n_branches == 2 else 1  # 0=Two, 1=Three
            mod[SOCKET["treetop"]] = context.scene.bush_custom_spread
            mod[SOCKET["numLevels"]] = context.scene.bush_custom_levels
            mod[SOCKET["bLength"]] = context.scene.bush_custom_branch_length
            mod[SOCKET["rAngle"]] = context.scene.bush_custom_branch_angle
            mod[SOCKET["rJitter"]] = context.scene.bush_custom_jitter
            mod[SOCKET["gravity"]] = context.scene.bush_custom_gravity
            mod[SOCKET["thickness"]] = context.scene.bush_custom_thickness
            mod[SOCKET["addLeaves"]] = context.scene.bush_custom_add_leaves
            mod[SOCKET["leafDensity"]] = context.scene.bush_custom_leaf_density
            mod[SOCKET["leafMinScale"]] = context.scene.bush_custom_leaf_min_scale
            mod[SOCKET["leafMaxScale"]] = context.scene.bush_custom_leaf_max_scale
            mod[SOCKET["scale"]] = context.scene.bush_custom_scale

        # Apply season
        if context.scene.bush_season == 'SPRING':
            mod[SOCKET["season"]] = 0.0
        elif context.scene.bush_season == 'SUMMER':
            mod[SOCKET["season"]] = 0.5
        elif context.scene.bush_season == 'CUSTOM':
            mod[SOCKET["season"]] = context.scene.bush_custom_season_value
        else:
            mod[SOCKET["season"]] = 1.0

        mod[SOCKET["seed"]] = context.scene.bush_seed

        # Force update to apply all modifier values
        obj.update_tag()
        context.view_layer.update()

        # Auto-increment seed for next bush
        context.scene.bush_seed += 1

        self.report({'INFO'}, f"Added {obj.name}!")
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


classes = [ROOTED_OT_AddBush, ROOTED_OT_BushHideLeaves, ROOTED_OT_BushShowLeaves]

