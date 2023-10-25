import bpy

import os
import site
site.addsitedir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "PyAlembic"))

from mathutils import Vector
try:
    import alembic
    from imath import *
    from alembic.Abc import *
except ModuleNotFoundError:
    print("imath module not installed")

def LayoutSection(obj, layout, PropName, PropLabel):
        expanded = eval("obj."+PropName)
        tria_icon = "TRIA_DOWN" if expanded else "TRIA_RIGHT"
        layout.row().prop(obj, PropName, icon=tria_icon, icon_only=True, text=PropLabel, emboss=False)
        return expanded

def GetCurvesObjects(context):
    curves_objects = []
    for obj in context.selected_objects:
        if obj.type == "CURVES" :
            curves_objects.append(obj.evaluated_get(context.evaluated_depsgraph_get()))
    return curves_objects

def GetCurveParentLocation(Curve):
    if Curve.data.surface:
        return Curve.data.surface.location
    elif Curve.parent:
        return Curve.parent.location
    else:
        return Vector((0,0,0))

def getAttribute(attributes_dict, att_name, default_att, att_types):
    att_temp = default_att
    att_valid = False
    if att_name != "":
        if att_name in attributes_dict:
            att_temp = attributes_dict[att_name]
            for att_type in att_types:
                if att_temp.data_type == att_type:
                    att_valid = True
    return att_temp, att_valid

def getAttributeValue(att_valid, att_prop, number, value, uv_flip=False):
    if not att_valid:
        match value:
            case "INT" | "INT8":
                return 0
            case "FLOAT":
                return 1.0 #width minimun
            case "FLOAT2":
                 return V2f( 0.0, 0.0 )
            case "FLOAT_VECTOR":
                return V3f( 0.0, 0.0, 0.0)
            case "BYTE_COLOR":
                return V3i( 0, 0, 0)
    #strange behaviour
    #point = number #min(number, len(att_prop.data)-1)
    out_value = ( 0.0, 0.0, 0.0, 0.0 )
    match att_prop.data_type:
        case "INT" | "INT8" | "FLOAT":
            out_value = att_prop.data[ number ].value
        case "FLOAT2" | "FLOAT_VECTOR":
            out_value = att_prop.data[ number ].vector
        case "FLOAT_COLOR" | "BYTE_COLOR":
            out_value = att_prop.data[ number ].color
    match value:
        case "INT" | "INT8" | "FLOAT":
            return out_value
        case "FLOAT2":#fast uv rotator, to give an unreal engine coordinate
            return V2f(out_value[1], 1 - out_value[0]) if uv_flip else V2f(out_value[0], out_value[1])
        case "FLOAT_VECTOR":
            return V3f(out_value[0], out_value[1], out_value[2])
        case "BYTE_COLOR":
            return V3i(out_value[0], out_value[1], out_value[2])        
    
def vectorLocTransform(vector, loc_diff, scale):
    loc_new = vector + loc_diff
    loc_new *= scale
    return V3f(loc_new[0], -loc_new[1], loc_new[2])
