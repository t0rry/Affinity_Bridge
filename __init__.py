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
    "author" : "Hattori_Kaoru( t0rry_ )",
    "description" : "BlenderからAffinityPhoto2を起動します",
    "blender" : (4, 0, 0),
    "version" : (0, 6, 0),
    "location" : "Image Editor >> Property Panel",
    "warning" : "This vertions experiment",
    "support" : "COMMUNITY",
    "category" : "User",
    "doc_url" : "https://github.com/t0rry/Affinity_Bridge"
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

    is_used_affinityphoto:BoolProperty(
        name = 'AffinityPhotoを利用する',
        description = 'AffinityBridgeするときにAffinityPhotoV2が起動されます',
        default = True
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
    
class AFFINITYBRIDGE_MT_CompositPanel(bpy.types.Menu):
    
    bl_idname = "AFFINITYBRIDGE_MT_SetOpenExrSelected"
    bl_label = "AffnityBridge"
    bl_description = "コンポジット上で機能するパネル"
    
    def draw(self,context):
        layout = self.layout
        ui_type = context.area.ui_type
        if ui_type == "CompositorNodeTree":
            layout.operator(ot.AFFINTYBRIDGE_OT_SetOpenEXR_Selected.bl_idname,icon='NODETREE')  
            layout.operator(ot.AFFINITYBRIDGE_OT_SetOpenEXR_RenderLayer.bl_idname,icon='NODETREE')               

class AFFINITYBRIDGE_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

        
    option_image_editing_exe:StringProperty(
        name = "画像編集ソフトを指定",
        subtype = "FILE_PATH",
        default = ""
    )
    
    is_display_filepath:BoolProperty(
        name = "UI上にexeファイルのファイルパス指定を表示する",
        default = False
    )
    
    def draw(self,context):
        layout = self.layout
        
        box = layout.box()
        box.prop(self, 'option_image_editing_exe')
        box.prop(self,'is_display_filepath',text = "画像エディタ上でexeファイルを編集できるようにする")
        box.label(icon = 'ERROR',text = 'イメージエディタ上にファイルパスが表示されるため無効にすることを推奨します。')
def menu_register_func(cls, context):
    
    ui_type = context.area.ui_type
    if ui_type == "CompositorNodeTree":
        cls.layout.separator()
        cls.layout.menu(AFFINITYBRIDGE_MT_CompositPanel.bl_idname, icon = 'NODETREE')
        
classes = [
    AffinityBridgeProp,
    AFFINITYBRIDGE_Preferences,
    AFFINITYBRIDGE_MT_CompositPanel,
    ot.AFFINITYBRIDGE_OT_SetOpenEXR_RenderLayer,
    ot.AFFINTYBRIDGE_OT_SetOpenEXR_Selected,
    ot.AFFINITYBRIDGE_OT_Photo,
    ot.AFFINITYBRIDGE_OT_Reload,
    ui.AFFINITYBRIDGE_PT_Panel,
    ui.AFFINITYBRIDGE_PT_RenderSettingPanel,
    ui.AFFINITYBRIDGE_PT_InformationPanel
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.affinitybridge = bpy.props.PointerProperty(type = AffinityBridgeProp)
    bpy.types.NODE_MT_context_menu.append(menu_register_func)
    
def unregister():
    bpy.types.NODE_MT_context_menu.remove(menu_register_func)
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.affinitybridge

