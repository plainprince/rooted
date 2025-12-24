# Rooted - Procedural Tree Generator
# Based on Easy Tree by Jacob Johnston
# Licensed under GPL-3.0-or-later

bl_info = {
    "name":        "Rooted",
    "author":      "Based on Easy Tree by Jacob Johnston",
    "version":     (1, 0, 0),
    "blender":     (4, 5, 0),
    "location":    "View3D > Sidebar > Rooted",
    "description": "Generate procedural trees with Geometry Nodes",
    "category":    "Add Mesh"
}

import bpy
from . import panel, operators
from .operators import tree_operators, bush_operators

classes = []
classes += panel.classes
classes += operators.classes
classes += tree_operators.classes
classes += bush_operators.classes

def register():
    # Global type selection
    bpy.types.Scene.rooted_type = bpy.props.EnumProperty(
        name="Type",
        description="Choose what type of vegetation to generate",
        items=[
            ('TREE', "Tree", "Generate a tree"),
            ('BUSH', "Bush", "Generate a bush"),
        ],
        default='TREE'
    )
    
    bpy.types.Scene.tree_preset = bpy.props.EnumProperty(
        name="preset",
        description="Choose a tree preset",
        items=[
            ('SMALL', "Small", "A default tree"),
            ('TALL', "Tall", "Tall Tree Preset"),
            ('THIN', "Thin", "Thin Tree Preset"),
            ('LARGE', "Large", "Large Tree Preset"),
            ('DEAD', "Dead", "Dead Tree Preset (No Leaves)"),
            ('CUSTOM', "Custom", "Custom tree parameters"),
        ],
        default='SMALL'
    )
    
    bpy.types.Scene.season = bpy.props.EnumProperty(
        name="Mode",
        description="Choose a mode",
        items=[
            ('SPRING', "Spring", "Light Green Leaves"),
            ('SUMMER', "Summer", "Green Leaves"),
            ('FALL', "Fall", "Red & Orange Leaves"),
            ('CUSTOM', "Custom", "Custom season value"),
        ],
        default='SPRING'
    )
    
    # Custom preset properties
    bpy.types.Scene.custom_trunk = bpy.props.IntProperty(
        name="Trunk Height",
        description="Height of the trunk before branching",
        default=2,
        min=0,
        max=10
    )
    bpy.types.Scene.custom_treetop = bpy.props.IntProperty(
        name="Treetop",
        description="Size of the treetop area",
        default=3,
        min=0,
        max=10
    )
    bpy.types.Scene.custom_num_levels = bpy.props.IntProperty(
        name="Branch Levels",
        description="Number of branching levels",
        default=4,
        min=1,
        max=8
    )
    bpy.types.Scene.custom_branch_length = bpy.props.IntProperty(
        name="Branch Length",
        description="Length of branches",
        default=6,
        min=1,
        max=15
    )
    bpy.types.Scene.custom_branch_angle = bpy.props.FloatProperty(
        name="Branch Angle",
        description="Angle of branches (radians)",
        default=0.523,
        min=0.0,
        max=1.57
    )
    bpy.types.Scene.custom_jitter = bpy.props.FloatProperty(
        name="Jitter",
        description="Random rotation jitter",
        default=0.1,
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.custom_gravity = bpy.props.FloatProperty(
        name="Gravity",
        description="Gravity effect on branches",
        default=0.5,
        min=0.0,
        max=3.0
    )
    bpy.types.Scene.custom_thickness = bpy.props.FloatProperty(
        name="Thickness",
        description="Thickness of branches",
        default=2.0,
        min=0.5,
        max=5.0
    )
    bpy.types.Scene.custom_min_height = bpy.props.IntProperty(
        name="Min Height",
        description="Minimum height for branching",
        default=0,
        min=0,
        max=10
    )
    bpy.types.Scene.custom_add_leaves = bpy.props.BoolProperty(
        name="Add Leaves",
        description="Whether to add leaves to the tree",
        default=True
    )
    bpy.types.Scene.custom_n_branches = bpy.props.IntProperty(
        name="N Branches",
        description="Number of branches per level",
        default=2,
        min=1,
        max=3
    )
    bpy.types.Scene.custom_scale = bpy.props.FloatProperty(
        name="Scale",
        description="Overall scale of the tree",
        default=1.0,
        min=0.1,
        max=3.0
    )
    
    # Custom season property
    bpy.types.Scene.custom_season_value = bpy.props.FloatProperty(
        name="Season Value",
        description="Season blend (0=Spring, 0.5=Summer, 1=Fall)",
        default=0.0,
        min=0.0,
        max=1.0
    )
    
    # Seed property
    bpy.types.Scene.tree_seed = bpy.props.IntProperty(
        name="Seed",
        description="Random seed for tree generation (auto-increments after each tree)",
        default=0,
        min=0
    )
    
    # ===== BUSH PROPERTIES =====
    bpy.types.Scene.bush_preset = bpy.props.EnumProperty(
        name="Bush Preset",
        description="Choose a bush preset",
        items=[
            ('SMALL', "Small", "A small compact bush"),
            ('MEDIUM', "Medium", "A medium-sized bush"),
            ('LARGE', "Large", "A large sprawling bush"),
            ('HEDGE', "Hedge", "Tall and narrow hedge-style bush"),
            ('CUSTOM', "Custom", "Custom bush parameters"),
        ],
        default='MEDIUM'
    )
    
    bpy.types.Scene.bush_season = bpy.props.EnumProperty(
        name="Bush Season",
        description="Choose a season for the bush",
        items=[
            ('SPRING', "Spring", "Light Green Leaves"),
            ('SUMMER', "Summer", "Green Leaves"),
            ('FALL', "Fall", "Red & Orange Leaves"),
            ('CUSTOM', "Custom", "Custom season value"),
        ],
        default='SUMMER'
    )
    
    # Bush custom properties
    bpy.types.Scene.bush_custom_spread = bpy.props.IntProperty(
        name="Spread",
        description="How wide the bush spreads",
        default=2,
        min=1,
        max=5
    )
    bpy.types.Scene.bush_custom_levels = bpy.props.IntProperty(
        name="Branch Levels",
        description="Number of branching levels",
        default=4,
        min=2,
        max=6
    )
    bpy.types.Scene.bush_custom_branch_length = bpy.props.IntProperty(
        name="Branch Length",
        description="Length of branches",
        default=4,
        min=1,
        max=8
    )
    bpy.types.Scene.bush_custom_branch_angle = bpy.props.FloatProperty(
        name="Branch Angle",
        description="Angle of branches (lower = more upward)",
        default=0.3,
        min=0.1,
        max=1.0
    )
    bpy.types.Scene.bush_custom_jitter = bpy.props.FloatProperty(
        name="Jitter",
        description="Random rotation jitter",
        default=0.15,
        min=0.0,
        max=0.5
    )
    bpy.types.Scene.bush_custom_gravity = bpy.props.FloatProperty(
        name="Gravity",
        description="Gravity effect on branches",
        default=2.4,
        min=0.0,
        max=5.0
    )
    bpy.types.Scene.bush_custom_thickness = bpy.props.FloatProperty(
        name="Thickness",
        description="Thickness of branches",
        default=1.3,
        min=0.5,
        max=3.0
    )
    bpy.types.Scene.bush_custom_n_branches = bpy.props.IntProperty(
        name="N Branches",
        description="Number of branches per level",
        default=2,
        min=1,
        max=3
    )
    bpy.types.Scene.bush_custom_add_leaves = bpy.props.BoolProperty(
        name="Add Leaves",
        description="Whether to add leaves to the bush",
        default=True
    )
    bpy.types.Scene.bush_custom_leaf_density = bpy.props.FloatProperty(
        name="Leaf Density",
        description="Density of leaves on branches",
        default=0.66,
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.bush_custom_leaf_min_scale = bpy.props.FloatProperty(
        name="Leaf Min Scale",
        description="Minimum scale of leaves",
        default=0.3,
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.bush_custom_leaf_max_scale = bpy.props.FloatProperty(
        name="Leaf Max Scale",
        description="Maximum scale of leaves",
        default=1.0,
        min=0.0,
        max=2.0
    )
    bpy.types.Scene.bush_custom_scale = bpy.props.FloatProperty(
        name="Scale",
        description="Overall scale of the bush",
        default=1.0,
        min=0.1,
        max=2.0
    )
    
    bpy.types.Scene.bush_custom_season_value = bpy.props.FloatProperty(
        name="Season Value",
        description="Season blend (0=Spring, 0.5=Summer, 1=Fall)",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    bpy.types.Scene.bush_seed = bpy.props.IntProperty(
        name="Bush Seed",
        description="Random seed for bush generation (auto-increments after each bush)",
        default=0,
        min=0
    )
    
    
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Remove custom properties
    # Bush properties
    del bpy.types.Scene.bush_seed
    del bpy.types.Scene.bush_custom_season_value
    del bpy.types.Scene.bush_custom_leaf_max_scale
    del bpy.types.Scene.bush_custom_leaf_min_scale
    del bpy.types.Scene.bush_custom_leaf_density
    del bpy.types.Scene.bush_custom_add_leaves
    del bpy.types.Scene.bush_custom_scale
    del bpy.types.Scene.bush_custom_n_branches
    del bpy.types.Scene.bush_custom_thickness
    del bpy.types.Scene.bush_custom_gravity
    del bpy.types.Scene.bush_custom_jitter
    del bpy.types.Scene.bush_custom_branch_angle
    del bpy.types.Scene.bush_custom_branch_length
    del bpy.types.Scene.bush_custom_levels
    del bpy.types.Scene.bush_custom_spread
    del bpy.types.Scene.bush_season
    del bpy.types.Scene.bush_preset
    
    # Tree properties
    del bpy.types.Scene.tree_seed
    del bpy.types.Scene.custom_season_value
    del bpy.types.Scene.custom_scale
    del bpy.types.Scene.custom_n_branches
    del bpy.types.Scene.custom_add_leaves
    del bpy.types.Scene.custom_min_height
    del bpy.types.Scene.custom_thickness
    del bpy.types.Scene.custom_gravity
    del bpy.types.Scene.custom_jitter
    del bpy.types.Scene.custom_branch_angle
    del bpy.types.Scene.custom_branch_length
    del bpy.types.Scene.custom_num_levels
    del bpy.types.Scene.custom_treetop
    del bpy.types.Scene.custom_trunk
    del bpy.types.Scene.season
    del bpy.types.Scene.tree_preset
    del bpy.types.Scene.rooted_type

if __name__ == "__main__":
    register()
