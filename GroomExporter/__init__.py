import bpy
from . import GroomPanel
from . import GroomAttributes
from . import GroomOperators
from . import GroomText

import site
site.addsitedir(GroomOperators.absolute_path("PyAlembic"))
from . import AlembicGroomExporter
            
bl_info = {
    "name" : "Groom Exporter",
    "author" : "Turbocheke",
    "description" : "",
    "blender" : (3, 3, 0),#the minimal version I checked
    "version" : (0, 1, 4),
    "location" : "View3D > UI > Groom",
    "warning" : "",
    'tracker_url': 'https://turbocheke.gumroad.com/l/Groomexporter',
    'support': 'COMMUNITY',
    'category': 'Import-Export'
}

classes = ( 
    GroomAttributes.AbcGroomProperties,
    GroomPanel.VIEW_3D_PT_GroomQOL,
    GroomPanel.VIEW_3D_PT_Groom,
    GroomPanel.VIEW_3D_PT_warning_panel,
    GroomPanel.GROOM_preferences,
    GroomPanel.GROOM_MT_HeaderTooltip,
    GroomPanel.GROOM_MT_GroomTooltip,
    GroomPanel.GROOM_MT_StrandTooltip,
    GroomPanel.GROOM_MT_VertexTooltip,
    #operators
    GroomOperators.GROOM_OT_install_dependencies,
    GroomOperators.GROOM_OT_uninstall_dependencies,
    GroomOperators.GROOM_OT_ButtonFastSetter,
    GroomOperators.GROOM_OT_HeaderTooltip,
    GroomOperators.GROOM_OT_GroomTooltip,
    GroomOperators.GROOM_OT_StrandTooltip,
    GroomOperators.GROOM_OT_VertexTooltip,
    #export
    AlembicGroomExporter.GROOM_OT_ButtonExport,
)

def Register_var_utils():
    bpy.types.WindowManager.dependencies_installed  = bpy.props.BoolProperty(False)
    bpy.types.Object.groom_curves_expanded          = bpy.props.BoolProperty(False)
    bpy.types.Object.GroomProperty                  = bpy.props.PointerProperty(type=GroomAttributes.AbcGroomProperties)
    bpy.types.Scene.groom_properties                = bpy.props.StringProperty(default="Properties")
    bpy.types.Scene.groom_qol                       = bpy.props.PointerProperty(type=GroomAttributes.AbcGroomProperties)

def Unregister_var_utils():
    del bpy.types.WindowManager.dependencies_installed
    del bpy.types.Object.groom_curves_expanded
    del bpy.types.Object.GroomProperty
    del bpy.types.Scene.groom_properties
    del bpy.types.Scene.groom_qol

def register():
    site.addsitedir(GroomOperators.absolute_path("PyAlembic"))

    for clas in classes:
        bpy.utils.register_class(clas)

    Register_var_utils()
    try:
        import alembic
        bpy.types.WindowManager.dependencies_installed = True
    except ModuleNotFoundError:
        bpy.types.WindowManager.dependencies_installed = False

    bpy.app.translations.register(__name__, GroomText.langs)
        

def unregister():
    for clas in classes:
        bpy.utils.unregister_class(clas)
    
    bpy.app.translations.unregister(__name__)
    Unregister_var_utils()
        
if __name__ == "__main__":
    register()