import bpy

langs = {
    'en_US': {
        #Header
        ('*', 'header_info'): 'Header',
        #Tooltip Header
        ('*', 'header_info_tt'): 'This section outlines properties that apply to the groom as a whole.',
        ('*', 'groom_tool_tt'): 'The name and version of the tool that generated this file. Useful for debugging and tracking down issues.',
        ('*', 'groom_version_major_tt'): 'Used to identify which major version of the groom schema this file conforms to.',
        ('*', 'groom_version_minor_tt'): 'Used to Identify which minor version of the schema this file conforms to.',
        ('*', 'groom_properties_tooltip'): 'String describing the parameters used to generate this groom. These are tool-specific options, used for debugging.',
        #Groom
        ('*', 'groom_info'): 'Groom',
        #Groom tooltip
        ('*', 'groom_tt'): 'Basic information of the Curves object.',
        #Strand
        ('*', 'Strand_info'): 'Strand',
        ('*', 'Strand_specialcases'): 'Specialized use cases.',
        ('*', 'Strand_nottested'): 'Curve control, not tested.',
        ('*', 'Strand_interpolation'): 'Interpolation data computed outside of UE.',
        #Groom tooltip
        ('*', 'Strand_tt_t1'): 'These parameters have a value per-curves. Indicates the expected Attribute data type.',
        ('*', 'Strand_tt_t2'): 'Knots and Orders work together. The use case are untested.',
        ('*', 'Strand_tt_t3'): '(groom_guide, groom_id, groom_closest_guides, groom_guide_weights) works together and are the interpolation data.  The use case are untested.',
        ('*', 'Groom_root_uv_tt'): 'Root of the strand aligned to a UV map.',
        ('*', 'Undocumented'): 'Undocumented.',
        ('*', 'Groom_guide_tt'): 'Guides are generated from the imported strands and decimation settings. 0 = Not a guide / 1 = Guide.',
        ('*', 'Groom_id_tt'): 'Strands Guide IDs. This is intended for use in debugging and with groom_closest_guides attribute.',
        ('*', 'Groom_closest_guides_tt'): 'List of the 3 nearest Strand Guide IDs.',
        ('*', 'Groom_guide_weights_tt'): 'Value of interpolation of the 3 nearest Strand Guide IDs.',
        #Vertex
        ('*', 'Vertex_info'): 'Vertex',
        #Vertex tooltip
        ('*', 'Vertex_tt_t1'): 'These parameters have a value per-point on the curves. Indicates the expected Attribute data type.',
        ('*', 'Vertex_param_tt'): 'Can be accesed on the Hair Attributes Expression on the Material.',
        ('*', 'Vertex_width_tt'): 'Width of the strand, uses a scale of centimeters.',
        #Operators
        ('*', 'Install_dependencies'): 'Install Alembic python library dependencies.',
        ('*', 'Uninstall_dependencies'): 'Uninstall python library dependencies.',
        ('*', 'Button Export'): 'Process the export.',
        #Fast setter
        ('*', 'Fast_setter'): 'Fast attribute setter.',
        ('*', 'Fast_setter_search'): 'Search on every object and set the attribute if its found.',
        #Test
        ('*', 'Simple Custom Menu'): 'Simple Custom Menu',
        ('*', 'Tooltip_test'): 'Tooltip test.',
        #Installation
        ('*', 'Install_line1'): 'Please install the missing dependencies for the Groom Exporter add-on.',
        ('*', 'Install_line2'): '1. Open the preferences (Edit > Preferences > Add-ons).',
        ('*', 'Install_line3'): '2. Search for the Groom Exporter add-on.',
        ('*', 'Install_line4'): '3. Open the details section of the add-on.',
        ('*', 'Install_line5'): '4. Click on the Install dependencies button.',
        ('*', 'Install_line6'): 'Select the PyAlembic library to install as a dependency.',
        ('*', 'Install_line7'): 'It will be installed on the Addon folder.',
        ('*', 'Install_line8'): 'After install PyAlembic its needed to restart blender to load correctly the library.',
        ('*', 'Install_line9'): 'PyAlembic isnt availaible on the pip installer.',
        ('*', 'Install_line10'): 'If you need another version of the library, because uses another python version or OS.',
        ('*', 'Install_line11'): 'Site for precompiled library versions, install it instead of the attachment file.',
    },
    'es': {
        ('*', 'header_info'): 'Encabezado',
        #Tooltip Header
        ('*', 'header_info_tt'): 'Esta sección indica propiedades que se aplican por completo en el Groom.',
        ('*', 'title'): 'sfds',
        ('*', 'groom_tool_tt'): 'El nombre y la version de la herramienta que generó el archivo. Útil para depurar y encontrar ocurrencias.',
        ('*', 'groom_version_major_tt'): 'Usado para identificar la version principal del archivo Groom.',
        ('*', 'groom_version_minor_tt'): 'Usado para identificar la version menor del archivo Groom.',
        ('*', 'groom_properties_tooltip'): 'Parámetros descritos usados para generar este Groom. Son opciones enfocadas en la herramienta, usado para depuración.',
        #Groom
        ('*', 'groom_info'): 'Groom',
        #Groom tooltip
        ('*', 'groom_tt'): 'Información básica del las curvas.',
        #Strand
        ('*', 'Strand_info'): 'Strand',
        ('*', 'Strand_specialcases'): 'Casos de uso expecializados.',
        ('*', 'Strand_nottested'): 'Control de Curva, sin probar.',
        ('*', 'Strand_interpolation'): 'Datos de interpolación calculados exteriormente a UE.',
        #Groom tooltip
        ('*', 'Strand_tt_t1'): 'Estos parámetros se aplican por curva. Indican el tipo de dato de atributo necesario.',
        ('*', 'Strand_tt_t2'): '(groom_knots, groom_orders) trabajan en conjunto. Funcionalidad sin probar.',
        ('*', 'Strand_tt_t3'): '(groom_guide, groom_id, groom_closest_guides, groom_guide_weights) trabajan en conjunto y son los datos de interpolación. Funcionalidad sin probar.',
        ('*', 'Groom_root_uv_tt'): 'La base de la curva alineada a un mapa UV.',
        ('*', 'Undocumented'): 'Sin documentar.',
        ('*', 'Groom_guide_tt'): 'Las guías gestionan las curvas adyacentes y la simplificación. 0 = No es guia / 1 = Guia.',
        ('*', 'Groom_id_tt'): 'Strands Guide IDs. Usado para depurar y en conjunto con el atributo groom_closest_guides.',
        ('*', 'Groom_closest_guides_tt'): 'Lista de los 3 mas cercanos Strand Guide IDs.',
        ('*', 'Groom_guide_weights_tt'): 'Valor de la interpolación de los 3 más cercanos Strand Guide IDs.',
        #Vertex
        ('*', 'Vertex_info'): 'Vertex',
        #Vertex tooltip
        ('*', 'Vertex_tt_t1'): 'Estos parámetros se aplican por vértice. Indican el tipo de dato de atributo necesario.',
        ('*', 'Vertex_param_tt'): 'Puede accederse mediante los atributos del pelo en el Material.',
        ('*', 'Vertex_width_tt'): 'Grosor del pelo, usa una escala de centímetros.',
        #Operators
        ('*', 'Install_dependencies'): 'Instalar libreria PyAlembic.',
        ('*', 'Button Export'): 'Exportar.',
        #Fast setter
        ('*', 'Fast_setter'): 'Rápida inserción de Atributos.',
        ('*', 'Fast_setter_search'): 'Busca por cada objeto y inserta el Atributo si es válido.',
        #Test
        ('*', 'Simple Custom Menu'): 'Simple Custom Menu',
        ('*', 'Tooltip_test'): 'Tooltip test.',
        #Installation
        ('*', 'Install_line1'): 'Es necesario instalar una librería para usar el complemento Groom Exporter.',
        ('*', 'Install_line2'): '1. Abre preferencias (Editar > Preferencias > Complementos).',
        ('*', 'Install_line3'): '2. Busca el complemento Groom Exporter.',
        ('*', 'Install_line4'): '3. Abre la sección de detalles del complemento.',
        ('*', 'Install_line5'): '4. Realiza click en el botón Install Dependencies.',
        ('*', 'Install_line6'): 'Selecciona la librería PyAlembic para instalarla.',
        ('*', 'Install_line7'): 'Será instalada en la carpeta del complemento.',
        ('*', 'Install_line8'): 'Después de instalar PyAlembic es necesario reiniciar blender para cargar correctamente la librería.',
        ('*', 'Install_line9'): 'PyAlembic solo puede instalarse manualmente.',
        ('*', 'Install_line10'): 'Si se requiere otra version de la librería, por diferente version de python o sistema operativo.',
        ('*', 'Install_line11'): 'Página web con versiones alternativas precompiladas de la librería PyAlembic.',
    }
}