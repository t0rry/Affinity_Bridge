# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Affinity_Bridge",
    "author" : "Hattori_Kaoru(t0rry_)",
    "description" : "",
    "blender" : (3, 00, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Interface"
}

if "bpy" in locals():
    import imp
    imp.reload(ot)
    imp.reload(ui)
else:
    from . import ot
    from . import ui
    
import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    PointerProperty,
    StringProperty
)

class AffinityBridgeProp(bpy.types.PropertyGroup):
    file_format:EnumProperty(
        name = 'file_fromat',
        description = 'file_format',
        items = [('PNG','PNG','select PNG(file format)'),
                ('JPEG','JPEG','select JPEG(file format)'),
                ('OPEN_EXR','Open_EXR','select OpenEXR(file format)'),
                ('OPEN_EXR_MULTILAYER','Open EXR Multilayer','select OpenEXR_Multilayer(file format)')]
    )
    
    color_mode:EnumProperty(
        name = 'color_mode',
        description ='color mode',
        items = [('BW', "BW",'select BW(color mode)'),
                ('RGB','RGB','select RGB(color mode)'),
                ('RGBA','RGBA','select RGBA(color mode)')]
    )
    
    file_name:StringProperty(
        name = 'file_name',
        description = 'use to saved image',
        default = 'AffinityBridge'
    )
    
    path_str:StringProperty(
        name = 'path_string',
        description = 'display of saved image path',
        default = ''
    )    
    
    is_change_name:BoolProperty(
        name = 'change_name',
        description = 'use to input orignal name',
        default = False
    )
    
    #maybe dont use old_ff,old_cm
    
    old_ff:StringProperty(
        name = 'old file_format',
        description = 'to changing parameter when saved image'
    )
    
    old_cm:StringProperty(
        name = 'old color_mode',
        description = 'to changing parameter when saved image'        
    )
    

classes = [
    AffinityBridgeProp,
    ot.AFFINITYBRIDGE_OT_Photo,
    ot.AFFINITYBRIDGE_OT_Reload,
    ui.AFFINITYBRIDGE_PT_Panel,
    ui.AFFINITYBRIDGE_PT_InformationPanel
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.affinitybridge = bpy.props.PointerProperty(type = AffinityBridgeProp)
    
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.affinitybridge

