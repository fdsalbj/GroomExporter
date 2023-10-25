import bpy
import addon_utils
from . import ExporterOperators

class VIEW_3D_PT_GroomQOL(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' 
    bl_category = "Groom" 
    bl_label = "Groom Exporter Fast Setup"

    def draw(self, context):
        layout = self.layout
        space = "       "
        scene = context.scene
        GProp = scene.groom_qol
        ##box Strand
        layout.label(text="Fast_setter")
        layout.label(text="Fast_setter_search")
        box = layout.box()
        col = box.column(align = True)
        row = col.row(align = True)
        row.label(text="Strand", icon='FORCE_CURVE')
        row = col.row(align = True)
        row.label(text=space+"Groom_root_uv")
        row.prop(GProp, "att_groom_root_uv", text="")
        row = col.row(align = True)
        row.label(text=space+"Groom_knots")
        row.prop(GProp, "att_groom_knots", text="")
        row = col.row(align = True)
        row.label(text=space+"Groom_orders")
        row.prop(GProp, "att_groom_orders", text="")
        row = col.row(align = True)
        row.label(text=space+"Groom_guide")
        row.prop(GProp, "att_groom_guide", text="")
        row = col.row(align = True)
        row.label(text=space+"Groom_id")
        row.prop(GProp, "att_groom_id", text="")
        row = col.row(align = True)
        row.label(text=space+"Groom_closest_guides")
        row.prop(GProp, "att_groom_closest_guides", text="")
        row = col.row(align = True)
        row.label(text=space+"Groom_guide_weights")
        row.prop(GProp, "att_groom_guide_weights", text="")
        ##box Vertex
        box = layout.box()
        col = box.column(align = True)
        row = col.row(align = True)
        row.label(text="Vertex", icon='SNAP_MIDPOINT')
        row = col.row(align = True)
        row.label(text=space+"Groom_color")
        row.prop(GProp, "att_groom_color", text="")
        row = col.row(align = True)
        row.label(text=space+"Groom_roughness")
        row.prop(GProp, "att_groom_roughness", text="")
        row = col.row(align = True)
        row.label(text=space+"Groom_width")
        row.prop(GProp, "att_groom_width", text="")
        row = layout.row()
        if bpy.types.WindowManager.dependencies_installed:
            row.operator("GROOM.buttonfastsetter")

class VIEW_3D_PT_Groom(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' 
    bl_category = "Groom" 
    bl_label = "Groom Exporter"

    def draw(self, context):
        op = ExporterOperators
        layout = self.layout
        scene = context.scene
        space = "       "

        ##box Settings
        box = layout.box()
        col = box.column(align = True)
        row = col.row(align = True)
        row.label(text="header_info", icon='INFO')
        props = row.operator("GROOM.headertooltip", text = "", icon = 'QUESTION')
        
        version = "-1"
        for addon in addon_utils.modules():
            if addon.bl_info['name'] == "Groom Exporter":
                version = addon.bl_info.get('version', (-1, -1, -1))

        row = col.row(align = True)
        row.label(text=space+"Groom_tool")            
        row.label(text="blender "+ bpy.app.version_string +" Groom Exporter " + str(version))
        row = col.row(align = True)
        row.label(text=space+"Groom_version_major")
        row.label(text="1")
        row = col.row(align = True)
        row.label(text=space+"Groom_version_minor")
        row.label(text="5")
        row = col.row(align = True)
        row.label(text=space+"Groom_properties")
        row.prop(scene, 'groom_properties', text="")

        curvesObjects = op.GetCurvesObjects(context)
        for obj in curvesObjects:

            atts = obj.data.attributes
            GProp = obj.GroomProperty
            num_curves = len(obj.data.curves)
            num_curves_points = len( obj.data.points )
            
            op.LayoutSection(obj, layout, "groom_curves_expanded", obj.name)
            if obj.groom_curves_expanded:

                ##box Groom
                box = layout.box()
                col = box.column(align = True)
                row = col.row(align = True)
                row.label(text="Groom", icon='STRANDS')
                props = row.operator("GROOM.groomtooltip", text = "", icon = 'QUESTION')
                row = col.row(align = True)
                row.label(text=space+"Num Strands: " + str(num_curves))
                row.label(text="Num Vertex: " + str(num_curves_points))
                row = col.row(align = True)
                row.label(text=space+"Total Attributes: " + str(len(atts)))

                ##box Strand
                box = layout.box()
                col = box.column(align = True)
                row = col.row(align = True)
                row.label(text="Strand", icon='FORCE_CURVE')
                props = row.operator("GROOM.strandtooltip", text = "", icon = 'QUESTION')
                row = col.row(align = True)
                row.label(text=space+"Groom_root_uv")
                row.prop_search(GProp, "att_groom_root_uv", obj.data, "attributes", text="")
                
                row = col.row(align = True)
                box = row.box()
                col = box.column(align = True)
                col.row(align = True).label(text=space+"Strand_specialcases")
                col.row(align = True).label(text=space+"Strand_nottested")
                row = col.row(align = True)
                row.label(text=space+"Groom_knots")
                row.prop_search(GProp, "att_groom_knots", obj.data, "attributes", text="")
                row = col.row(align = True)
                row.label(text=space+"Groom_orders")
                row.prop_search(GProp, "att_groom_orders", obj.data, "attributes", text="")
                col.row(align = True).label(text=space+"Strand_interpolation")
                row = col.row(align = True)
                row.label(text=space+"Groom_guide")
                row.prop_search(GProp, "att_groom_guide", obj.data, "attributes", text="")
                row = col.row(align = True)
                row.label(text=space+"Groom_id")
                row.prop_search(GProp, "att_groom_id", obj.data, "attributes", text="")
                row = col.row(align = True)
                row.label(text=space+"Groom_closest_guides")
                row.prop_search(GProp, "att_groom_closest_guides", obj.data, "attributes", text="")
                row = col.row(align = True)
                row.label(text=space+"Groom_guide_weights")
                row.prop_search(GProp, "att_groom_guide_weights", obj.data, "attributes", text="")

                ##box Vertex
                box = layout.box()
                col = box.column(align = True)
                row = col.row(align = True)
                row.label(text="Vertex", icon='SNAP_MIDPOINT')
                props = row.operator("GROOM.vertextooltip", text = "", icon = 'QUESTION')
                
                row = col.row(align = True)
                row.label(text=space+"Groom_color")
                row.prop_search(GProp, "att_groom_color", obj.data, "attributes", text="")
                row = col.row(align = True)
                row.label(text=space+"Groom_roughness")
                row.prop_search(GProp, "att_groom_roughness", obj.data, "attributes", text="")
                row = col.row(align = True)
                row.label(text=space+"Groom_width")
                row.prop_search(GProp, "att_groom_width", obj.data, "attributes", text="")
                        
        row = layout.row()

        if bpy.types.WindowManager.dependencies_installed:
            row.operator("GROOM.buttonexport")

class VIEW_3D_PT_warning_panel(bpy.types.Panel):
    bl_label = "Message Warning"
    bl_category = "Groom" 
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        lines = [f"Install_line1",
                 f"Install_line2",
                 f"Install_line3",
                 f"Install_line4",
                 f"Install_line5",
                 f"Install_line6",
                 f"Install_line7",
                 f"Install_line8",
                 f"Install_line9",
                 f"Install_line10",
                 f"Install_line11",
                 f"https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyalembic",]
        
        if not bpy.types.WindowManager.dependencies_installed:
            for line in lines:
                layout.label(text=line)

class GROOM_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        layout.operator("groom.install_dependencies", icon="CONSOLE")
        #layout.operator("groom.uninstall_dependencies", icon="CONSOLE")

class GROOM_MT_HeaderTooltip(bpy.types.Menu):
    bl_label = "Header Information"
    bl_idname = "GROOM_MT_HeaderTooltip"

    def draw(self, context):
        layout = self.layout
        layout.label(text="header_info_tt")

        #multiple iteration on do this, row and columns brokes on a stair case
        row = layout.row(align = False)
        col1 = row.column(align = False)
        col2 = row.column(align = False)

        col1.label(text="groom_tool")
        col1.label(text="groom_version_major")
        col1.label(text="groom_version_minor")
        col1.label(text="groom_properties")
        col2.label(text="groom_tool_tt")
        col2.label(text="groom_version_major_tt")
        col2.label(text="groom_version_minor_tt")
        col2.label(text="groom_properties_tooltip")

class GROOM_MT_GroomTooltip(bpy.types.Menu):
    bl_label = "Groom Information"
    bl_idname = "GROOM_MT_GroomTooltip"

    def draw(self, context):
        layout = self.layout
        layout.label(text="groom_tt")

class GROOM_MT_StrandTooltip(bpy.types.Menu):
    bl_label = "Strand Information"
    bl_idname = "GROOM_MT_StrandTooltip"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Strand_tt_t1")
        layout.label(text="Strand_tt_t2")
        layout.label(text="Strand_tt_t3")
        
        row = layout.row(align = False)
        col1 = row.column(align = False)
        col2 = row.column(align = False)
        col3 = row.column(align = False)
        
        col1.label(text="groom_root_uv")
        col1.label(text="groom_knots")
        col1.label(text="groom_orders")
        col1.label(text="groom_guide")
        col1.label(text="groom_id")
        col1.label(text="groom_closest_guides")
        col1.label(text="groom_guide_weights")
        col2.label(text="FLOAT2")
        col2.label(text="FLOAT")
        col2.label(text="INT8")
        col2.label(text="INT | INT8")
        col2.label(text="INT | INT8")
        col2.label(text="BYTE_COLOR")
        col2.label(text="FLOAT_VECTOR")
        col3.label(text="Groom_root_uv_tt")
        col3.label(text="Undocumented")
        col3.label(text="Undocumented")
        col3.label(text="Groom_guide_tt")
        col3.label(text="Groom_id_tt")
        col3.label(text="Groom_closest_guides_tt")
        col3.label(text="Groom_guide_weights_tt")
        
class GROOM_MT_VertexTooltip(bpy.types.Menu):
    bl_label = "Vertex Information"
    bl_idname = "GROOM_MT_VertexTooltip"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Vertex_tt_t1")

        row = layout.row(align = False)
        col1 = row.column(align = False)
        col2 = row.column(align = False)
        col3 = row.column(align = False)

        col1.label(text="groom_color")
        col1.label(text="groom_roughness")
        col1.label(text="groom_width")
        col2.label(text="FLOAT_COLOR | FLOAT_VECTOR")
        col2.label(text="FLOAT")
        col2.label(text="FLOAT")
        col3.label(text="Vertex_param_tt")
        col3.label(text="Vertex_param_tt")
        col3.label(text="Vertex_width_tt")
        