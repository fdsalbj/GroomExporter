import bpy

from bpy.props import StringProperty, PointerProperty

class AbcGroomProperties(bpy.types.PropertyGroup):
    att_groom_group_id          : StringProperty(default="")
    att_groom_guide             : StringProperty(default="")
    att_groom_id                : StringProperty(default="")
    att_groom_root_uv           : StringProperty(default="")
    att_groom_closest_guides    : StringProperty(default="")
    att_groom_guide_weights     : StringProperty(default="")
    att_groom_basis_type        : StringProperty(default="")
    att_groom_curve_type        : StringProperty(default="")
    att_groom_knots             : StringProperty(default="")
    att_groom_orders            : StringProperty(default="")
    att_groom_group_name        : StringProperty(default="")
    att_groom_color             : StringProperty(default="")
    att_groom_roughness         : StringProperty(default="")
    att_groom_width             : StringProperty(default="")
