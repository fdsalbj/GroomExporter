import bpy
import addon_utils
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
from bpy.types import Operator
from . import ExporterOperators
from . import GroomAttributes

import os
import site
site.addsitedir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "PyAlembic"))

try:
    import alembic
    from imath import *
    from alembic.Abc import *
    from alembic.AbcGeom import *
    from alembic.AbcCoreAbstract import *
    from alembic.AbcCollection import *
except ModuleNotFoundError:
    print("alembic module not installed")

class GROOM_OT_ButtonExport(Operator, ExportHelper):
    bl_idname = "groom.buttonexport"
    bl_label = "Button Export"
    bl_description ="Process the export."

    # ExportHelper mixin class uses this
    filename_ext = ".abc"

    filter_glob: StringProperty(
        default="*.abc",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    groom_scale : FloatProperty(
        name="Groom scale multiplier",
        description="The scale between blender and Unreal Engine, blender its normally 0,01 of UE",
        default=100.0,
        soft_min=1.0,
        soft_max=1000.0,
        min=1.0,
        max=1000.0,
    )

    def cancel(self, context):
        print("Cancel modal")

    def execute(self, context):
        return create_file(context, self.filepath, self.groom_scale)

def create_file(context, filepath, groom_scale):
    blender_version = "blender "+ bpy.app.version_string
    userStr = "Groom Exporter for UE"
    #create new base alembic archive
    oarch = CreateArchiveWithInfo( filepath, blender_version, userStr )
    WriteAbcContent(context, oarch, groom_scale)
    return {'FINISHED'}

def WriteAbcContent(context, oarch, groom_scale):
    op = ExporterOperators
    debug = False
    scene = context.scene
    #filter the selected objects to Curves
    curvesObjects = op.GetCurvesObjects(context)
    #evaluate geometry nodes on the curve objects
    for obj in curvesObjects:
        obj.evaluated_get(context.evaluated_depsgraph_get()).data

    loc_origin = op.GetCurveParentLocation(curvesObjects[0])
    #variables alembic
    kVertexScope  = GeometryScope.kVertexScope
    kUniformScope = GeometryScope.kUniformScope
    kCubic        = CurveType.kCubic
    kNonPeriodic  = CurvePeriodicity.kNonPeriodic
    curve_basis   = BasisType.kBezierBasis
    #variables declaration
    version = "-1"
    for addon in addon_utils.modules():
        if addon.bl_info['name'] == "Groom Exporter":
            version = addon.bl_info.get('version', (-1, -1, -1))

    blender_version = "blender "+ bpy.app.version_string +" Groom Exporter " + str(version)

    #custom property extremelly rare
    prop_uv_flip = "uv_flip" in scene.groom_properties
    print(prop_uv_flip)
    
    for num_curve in range(len(curvesObjects)):
        #variables context
        obj = curvesObjects[num_curve]
        loc_curve = obj.location
        loc_curve_diff = loc_curve - loc_origin

        groomProperty = obj.GroomProperty
        #generate curve object on iteration
        myCurves = OCurves( oarch.getTop(), obj.name )
        curves = myCurves.getSchema()
        #variable iterator
        data_curves = obj.data.curves #curve iterator
        #generate lengths arrays
        num_curves_points = len( obj.data.points ) #point data iterator
        num_data_curves = len( data_curves ) #num curveslices

        #clear vars on iteration    
        numVerts    = Int32TPTraits.arrayType(  num_data_curves) 
        out_uvs     = V2fTPTraits.arrayType(    num_data_curves)
        out_verts   = V3fTPTraits.arrayType(    num_curves_points)
        out_widths  = Float32TPTraits.arrayType(num_curves_points)
        out_color   = V3fTPTraits.arrayType(    num_curves_points)
        out_rough   = Float32TPTraits.arrayType(num_curves_points)
        out_knots   = Float32TPTraits.arrayType(num_curves_points)
        out_orders  = Uint8TPTraits.arrayType(  num_curves_points)
        #specialized case
        out_guide           = Int32TPTraits.arrayType(  num_data_curves)
        out_closest_guide   = V3iTPTraits.arrayType(    num_data_curves)
        out_guide_weights   = V3fTPTraits.arrayType(    num_data_curves)
        out_id              = Int32TPTraits.arrayType(  num_data_curves)
        #curve object specific
        out_group_id    = Int32TPTraits.arrayType( num_curves_points) 
        out_group_name  = StringTPTraits.arrayType(num_curves_points) 

        attributes_dict = {}
        type(attributes_dict)

        data_curves_attributes = obj.evaluated_get(context.evaluated_depsgraph_get()).data.attributes
        #loop attributes and set on a dict
        for attribute in data_curves_attributes :
            attributes_dict[attribute.name] = attribute

        #attribute booleans
        #width colot and roughness are setted by vertex, this solves
        att_width_prop,      att_width_valid        = op.getAttribute(attributes_dict, groomProperty.att_groom_width,     data_curves_attributes[0], ["FLOAT"])
        att_color_prop,      att_color_valid        = op.getAttribute(attributes_dict, groomProperty.att_groom_color,     data_curves_attributes[0], ["FLOAT_COLOR", "FLOAT_VECTOR"])
        att_roughness_prop,  att_roughness_valid    = op.getAttribute(attributes_dict, groomProperty.att_groom_roughness, data_curves_attributes[0], ["FLOAT"])
        att_surface_uv_prop, att_surface_uv_valid   = op.getAttribute(attributes_dict, groomProperty.att_groom_root_uv,   data_curves_attributes[0], ["FLOAT2", "FLOAT_VECTOR"])
        att_knots_prop,      att_knots_valid        = op.getAttribute(attributes_dict, groomProperty.att_groom_knots,     data_curves_attributes[0], ["FLOAT"])
        att_orders_prop,     att_orders_valid       = op.getAttribute(attributes_dict, groomProperty.att_groom_orders,    data_curves_attributes[0], ["INT8"])
        #specialized case
        att_guide_prop,         att_guide_valid             = op.getAttribute(attributes_dict, groomProperty.att_groom_guide,          data_curves_attributes[0], ["INT", "INT8"])
        att_id_prop,            att_id_valid                = op.getAttribute(attributes_dict, groomProperty.att_groom_id,             data_curves_attributes[0], ["INT", "INT8"])
        att_closest_guide_prop, att_closest_guide_valid     = op.getAttribute(attributes_dict, groomProperty.att_groom_closest_guides, data_curves_attributes[0], ["BYTE_COLOR"])
        att_guide_weights_prop, att_guide_weights_valid     = op.getAttribute(attributes_dict, groomProperty.att_groom_guide_weights,  data_curves_attributes[0], ["FLOAT_VECTOR"])

        num_point = 0
        for num_curveslice in range(num_data_curves):
            data_curve_points = data_curves[num_curveslice].points # curveslices points
            
            numVerts[           num_curveslice] = len( data_curve_points ) 
            out_uvs[            num_curveslice] = op.getAttributeValue(att_surface_uv_valid,  att_surface_uv_prop,    num_curveslice, "FLOAT2", uv_flip=prop_uv_flip)
            #specialized case
            out_guide[          num_curveslice] = op.getAttributeValue(att_guide_valid,             att_guide_prop,         num_curveslice, "INT")
            out_id[             num_curveslice] = op.getAttributeValue(att_id_valid,                att_id_prop,            num_curveslice, "INT")
            out_closest_guide[  num_curveslice] = op.getAttributeValue(att_closest_guide_valid,     att_closest_guide_prop, num_curveslice, "BYTE_COLOR")
            out_guide_weights[  num_curveslice] = op.getAttributeValue(att_guide_weights_valid,     att_guide_weights_prop, num_curveslice, "FLOAT_VECTOR")
            for curveslice_point in data_curve_points:
                #vert position its scaled and corrected to a valid Unreal Engine space transform
                out_verts[num_point]    = op.vectorLocTransform(curveslice_point.position, loc_curve_diff, groom_scale )
                #value setter via attribute or default value
                out_widths[     num_point] = op.getAttributeValue(att_width_valid,     att_width_prop,      num_point, "FLOAT")
                out_color[      num_point] = op.getAttributeValue(att_color_valid,     att_color_prop,      num_point, "FLOAT_VECTOR")
                out_rough[      num_point] = op.getAttributeValue(att_roughness_valid, att_roughness_prop,  num_point, "FLOAT")
                out_knots[      num_point] = op.getAttributeValue(att_knots_valid,     att_knots_prop,      num_point, "FLOAT")
                out_orders[     num_point] = op.getAttributeValue(att_orders_valid,    att_orders_prop,     num_point, "INT8")
                out_group_name[ num_point] = obj.name
                out_group_id[   num_point] = num_curve
                num_point += 1

        samp_width      = OFloatGeomParamSample( out_widths, kVertexScope )
        samp_uvs        = OV2fGeomParamSample(   out_uvs,    kUniformScope )
        samp_knots      = OFloatGeomParamSample( out_knots,  kVertexScope )
        samp_orders     = OUcharGeomParamSample( out_orders, kVertexScope )
        samp_normals    = ON3fGeomParamSample()

        curvesSamp = OCurvesSchemaSample( out_verts, numVerts, kCubic, kNonPeriodic, samp_width, samp_uvs, samp_normals, curve_basis)
        curves.set( curvesSamp )
        if att_knots_valid:  curves.setKnots( samp_knots)
        if att_orders_valid: curves.setOrders(samp_orders)
        
        #Metadata manages the scope
        metaCS = MetaData()
        metaCS.set("geoScope", "con")#kConstantScope
        metaVS = MetaData()
        metaVS.set("geoScope", "vtx")#kVertexScope
        metaUS = MetaData()
        metaUS.set("geoScope", "uni")#kUniformScope

        #properties used on global or specific grooms
        gContainer = curves.getUserProperties()
        if num_curve == 0:#only set on the first curve
            OStringProperty(gContainer, "groom_tool",          metaCS).setValue(blender_version)
            OInt16Property( gContainer, "groom_version_major", metaCS).setValue(1)
            OInt16Property( gContainer, "groom_version_minor", metaCS).setValue(5)
            OStringProperty(gContainer, "groom_properties",    metaCS).setValue(scene.groom_properties)

        #properties used on global or specific grooms
        gContainer = curves.getArbGeomParams()
        OInt32ArrayProperty( gContainer, "groom_group_id",   metaCS).setValue(out_group_id)
        OStringArrayProperty(gContainer, "groom_group_name", metaCS).setValue(out_group_name)
        if att_surface_uv_valid:
            OV2fArrayProperty(  gContainer, "groom_root_uv",   metaUS).setValue(out_uvs)
        if att_color_valid:
            OV3fArrayProperty(  gContainer, "groom_color",     metaVS).setValue(out_color)
        if att_roughness_valid:
            OFloatArrayProperty(gContainer, "groom_roughness", metaVS).setValue(out_rough)
        #specialized case
        if att_guide_valid:
            OInt32ArrayProperty(gContainer, "groom_guide",         metaUS).setValue(out_guide)
        if att_id_valid:
            OInt32ArrayProperty(gContainer, "groom_id",            metaUS).setValue(out_id)
        if att_closest_guide_valid:
            OV3iArrayProperty(  gContainer, "groom_closest_guide", metaUS).setValue(out_closest_guide)
        if att_guide_weights_valid:
            OV3fArrayProperty(  gContainer, "groom_guide_weights", metaUS).setValue(out_guide_weights)