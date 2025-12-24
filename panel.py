import bpy


class ROOTED_PT_MainPanel(bpy.types.Panel):
    bl_label = "Rooted"
    bl_idname = "ROOTED_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rooted"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Type selection (always visible)
        layout.prop(scene, "rooted_type", text="Type")

        layout.separator()

        # Type-specific UI
        if scene.rooted_type == 'TREE':
            self.draw_tree_ui(layout, scene)
        elif scene.rooted_type == 'BUSH':
            self.draw_bush_ui(layout, scene)

    def draw_tree_ui(self, layout, scene):
        """Draw tree-specific UI elements."""
        layout.prop(scene, "tree_preset", text="Preset")

        # Show custom preset sliders when Custom is selected
        if scene.tree_preset == 'CUSTOM':
            box = layout.box()
            box.label(text="Custom Tree Parameters")
            box.prop(scene, "custom_trunk")
            box.prop(scene, "custom_treetop")
            box.prop(scene, "custom_num_levels")
            box.prop(scene, "custom_branch_length")
            box.prop(scene, "custom_branch_angle")
            box.prop(scene, "custom_jitter")
            box.prop(scene, "custom_gravity")
            box.prop(scene, "custom_thickness")
            box.prop(scene, "custom_min_height")
            box.prop(scene, "custom_n_branches")
            box.prop(scene, "custom_scale")
            box.prop(scene, "custom_add_leaves")

        layout.prop(scene, "season", text="Season")

        # Show custom season slider when Custom is selected
        if scene.season == 'CUSTOM':
            box = layout.box()
            box.label(text="Custom Season")
            box.prop(scene, "custom_season_value")

        layout.prop(scene, "tree_seed", text="Seed")

        layout.operator("rooted.add_tree", text="Add Tree")

        row = layout.row()
        row.operator("rooted.tree_hide_leaves", text="Hide Leaves")
        row.operator("rooted.tree_show_leaves", text="Show Leaves")

    def draw_bush_ui(self, layout, scene):
        """Draw bush-specific UI elements."""
        layout.prop(scene, "bush_preset", text="Preset")

        # Show custom preset sliders when Custom is selected
        if scene.bush_preset == 'CUSTOM':
            box = layout.box()
            box.label(text="Custom Bush Parameters")
            box.prop(scene, "bush_custom_n_branches")
            box.prop(scene, "bush_custom_spread")
            box.prop(scene, "bush_custom_levels")
            box.prop(scene, "bush_custom_branch_length")
            box.prop(scene, "bush_custom_branch_angle")
            box.prop(scene, "bush_custom_jitter")
            box.prop(scene, "bush_custom_gravity")
            box.prop(scene, "bush_custom_thickness")
            box.prop(scene, "bush_custom_add_leaves")
            box.separator()
            box.label(text="Leaf Settings")
            box.prop(scene, "bush_custom_leaf_density")
            box.prop(scene, "bush_custom_leaf_min_scale")
            box.prop(scene, "bush_custom_leaf_max_scale")
            box.separator()
            box.prop(scene, "bush_custom_scale")

        layout.prop(scene, "bush_season", text="Season")

        # Show custom season slider when Custom is selected
        if scene.bush_season == 'CUSTOM':
            box = layout.box()
            box.label(text="Custom Season")
            box.prop(scene, "bush_custom_season_value")

        layout.prop(scene, "bush_seed", text="Seed")

        layout.operator("rooted.add_bush", text="Add Bush")

        row = layout.row()
        row.operator("rooted.bush_hide_leaves", text="Hide Leaves")
        row.operator("rooted.bush_show_leaves", text="Show Leaves")


classes = [ROOTED_PT_MainPanel]
