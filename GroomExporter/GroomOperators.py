import bpy
import subprocess
import os
import sys
import shutil

import site

import addon_utils
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
from . import ExporterOperators

def absolute_path(component):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), component)

def install_pip():
    try:
        # Check if pip is already installed
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
    except subprocess.CalledProcessError:
        import ensurepip
        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)

def install_and_import_requirements(filepath):
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"
    subprocess.run([sys.executable, "-m", "pip", "install", filepath,  "--target", absolute_path('PyAlembic')], check=True, env=environ_copy)
 
class GROOM_OT_install_dependencies(Operator, ImportHelper):
    bl_idname = "groom.install_dependencies"
    bl_label = bpy.app.translations.pgettext("Install_dependencies")
    bl_description = ("Select and installs the required python packages for this add-on. ")
    bl_options = {"REGISTER", "INTERNAL"}

    # ImportHelper mixin class uses this
    filename_ext = ".whl"

    filter_glob: StringProperty(
        default="*.whl",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return not bpy.types.WindowManager.dependencies_installed

    def execute(self, context):
        try:
            install_pip()
            install_and_import_requirements(self.filepath)
        except (subprocess.CalledProcessError, ImportError) as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}
        bpy.types.WindowManager.dependencies_installed = True
        return {"FINISHED"}

class GROOM_OT_uninstall_dependencies(Operator):
    bl_idname = "groom.uninstall_dependencies"
    bl_label = bpy.app.translations.pgettext("Uninstall_dependencies")
    bl_description = ("Uninstall the required python packages for this add-on. ")
    bl_options = {"REGISTER", "INTERNAL"}
    
    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return bpy.types.WindowManager.dependencies_installed
    
    def execute(self, context):
        site.addsitedir(absolute_path("PyAlembic"))
        # Get directory name
        mydir= absolute_path('PyAlembic')
        """print(mydir)
        try:
            shutil.rmtree(mydir)
            return {"FINISHED"}
        except:
            print("unable to uninstall pyalembic")
            return {"CANCELLED"}"""
        try:
            environ_copy = dict(os.environ)
            environ_copy["PYTHONNOUSERSITE"] = "1"
            subprocess.run([sys.executable, "-m", "pip", "uninstall", 'PyAlembic' ], check=True, env=environ_copy)
            return {"FINISHED"}
        except:
            print("unable to uninstall pyalembic")
            return {"CANCELLED"}

class GROOM_OT_ButtonFastSetter(Operator):
    bl_idname = "groom.buttonfastsetter"
    bl_label = "Button_SetAttributes"
    
    def execute(self, context):
        op = ExporterOperators
        scene = context.scene
        groomProperty = scene.groom_qol
        #filter the selected objects to Curves
        curvesObjects = op.GetCurvesObjects(context)
        for obj in curvesObjects:
            attributes_dict = {}
            type(attributes_dict)
            data_curves_attributes = obj.evaluated_get(context.evaluated_depsgraph_get()).data.attributes
            #loop attributes and set on a dict
            for attribute in data_curves_attributes :
                attributes_dict[attribute.name] = attribute
            att_width_prop,      att_width_valid        = op.getAttribute(attributes_dict, groomProperty.att_groom_width,     data_curves_attributes[0], ["FLOAT"])
            att_color_prop,      att_color_valid        = op.getAttribute(attributes_dict, groomProperty.att_groom_color,     data_curves_attributes[0], ["FLOAT_COLOR", "FLOAT_VECTOR"])
            att_roughness_prop,  att_roughness_valid    = op.getAttribute(attributes_dict, groomProperty.att_groom_roughness, data_curves_attributes[0], ["FLOAT"])
            att_surface_uv_prop, att_surface_uv_valid   = op.getAttribute(attributes_dict, groomProperty.att_groom_root_uv,   data_curves_attributes[0], ["FLOAT2"])
            #specialized case
            att_knots_prop,      att_knots_valid        = op.getAttribute(attributes_dict, groomProperty.att_groom_knots,     data_curves_attributes[0], ["FLOAT"])
            att_orders_prop,     att_orders_valid       = op.getAttribute(attributes_dict, groomProperty.att_groom_orders,    data_curves_attributes[0], ["INT8"])
            att_guide_prop,         att_guide_valid             = op.getAttribute(attributes_dict, groomProperty.att_groom_guide,          data_curves_attributes[0], ["INT", "INT8"])
            att_id_prop,            att_id_valid                = op.getAttribute(attributes_dict, groomProperty.att_groom_id,             data_curves_attributes[0], ["INT", "INT8"])
            att_closest_guide_prop, att_closest_guide_valid     = op.getAttribute(attributes_dict, groomProperty.att_groom_closest_guides, data_curves_attributes[0], ["BYTE_COLOR"])
            att_guide_weights_prop, att_guide_weights_valid     = op.getAttribute(attributes_dict, groomProperty.att_groom_guide_weights,  data_curves_attributes[0], ["FLOAT_VECTOR"])
            #set the attribute name if its valid
            if att_width_valid:         obj.GroomProperty.att_groom_width           = groomProperty.att_groom_width
            if att_color_valid:         obj.GroomProperty.att_groom_color           = groomProperty.att_groom_color
            if att_roughness_valid:     obj.GroomProperty.att_groom_roughness       = groomProperty.att_groom_roughness
            if att_surface_uv_valid:    obj.GroomProperty.att_groom_root_uv         = groomProperty.att_groom_root_uv
            if att_knots_valid:         obj.GroomProperty.att_groom_knots           = groomProperty.att_groom_knots
            if att_orders_valid:        obj.GroomProperty.att_groom_orders          = groomProperty.att_groom_orders
            if att_guide_valid:         obj.GroomProperty.att_groom_guide           = groomProperty.att_groom_guide
            if att_id_valid:            obj.GroomProperty.att_groom_id              = groomProperty.att_groom_id
            if att_closest_guide_valid: obj.GroomProperty.att_groom_closest_guides  = groomProperty.att_groom_closest_guides
            if att_guide_weights_valid: obj.GroomProperty.att_groom_guide_weights   = groomProperty.att_groom_guide_weights
            
        return {"FINISHED"}

class GROOM_OT_HeaderTooltip(Operator):
    bl_idname = "groom.headertooltip"
    bl_label = "Tooltip_test"
    
    def execute(self, context):
        bpy.ops.wm.call_menu(name="GROOM_MT_HeaderTooltip")
        return {"FINISHED"}
        
class GROOM_OT_GroomTooltip(Operator):
    bl_idname = "groom.groomtooltip"
    bl_label = "Tooltip_test"
    
    def execute(self, context):
        bpy.ops.wm.call_menu(name="GROOM_MT_GroomTooltip")
        return {"FINISHED"}
        
class GROOM_OT_StrandTooltip(Operator):
    bl_idname = "groom.strandtooltip"
    bl_label = "Tooltip_test"
    
    def execute(self, context):
        bpy.ops.wm.call_menu(name="GROOM_MT_StrandTooltip")
        return {"FINISHED"}  
      
class GROOM_OT_VertexTooltip(Operator):
    bl_idname = "groom.vertextooltip"
    bl_label = "Tooltip_test"
    
    def execute(self, context):
        bpy.ops.wm.call_menu(name="GROOM_MT_VertexTooltip")
        return {"FINISHED"}
        