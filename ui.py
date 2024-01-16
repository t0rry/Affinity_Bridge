import bpy
import os

class AFFINITYBRIDGE_PT_Panel(bpy.types.Panel):
    bl_idname = "AFFINITY_BRIDGE_PT_Panel"
    bl_label = "Bridge AffinityPhoto"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "AffinityBridge"

    def render_setting(self):
        layout = self.layout
        context = bpy.context
        scene = context.scene
        
        box = layout.box()
        box.label(text= 'Render Setting',icon = 'RENDER_STILL')
        
        col = layout.column(align=True)
        col.prop(scene.affinitybridge, "file_format", text="Format") 
        col.prop(scene.affinitybridge, "color_mode", text="Color Mode")   
        
        layout.separator()                
    
    def affinity_bridge(self,af_bool):
        layout = self.layout
        context = bpy.context
        scene = context.scene
        prefs = context.preferences.addons['Affinity_Bridge'].preferences
        is_display_filepath  = prefs.is_display_filepath
        
        box = layout.box()
        box.label(text= 'AffinityBridge',icon = 'SEQUENCE_COLOR_04')
        
        if af_bool == True:
            button_name = 'Bridge AffinityPhoto2'
        else:
            button_name = 'Bridge Custom Software'
        
        col = layout.column(align=True)
        col.prop(scene.affinitybridge, 'is_used_affinityphoto',text = 'Used AffinityBridge')
        col = layout.column(align=True)                

        layout.separator()
        col = layout.column(align=True)
        col.scale_x = 3
        col.scale_y = 3
        col.operator('affinity_bridge.open_affinity_photo',text= button_name ,icon = 'EXPORT')
        col.separator(factor = 1)
        col.operator('affinity_bridge.reload_affinity_photo',text='Reload Image',icon = 'IMPORT') 
        if af_bool == False:
            col = layout.column(align=True)
            col.prop(prefs,'is_display_filepath',text = "ファイルパス表示")   
            if is_display_filepath == True:
                col.prop(prefs,'option_image_editing_exe',text="出力ソフトウェア") 

    def used_original_name(self):
        layout = self.layout
        context = bpy.context
        scene = context.scene
        
        col = layout.column(align=True)
        col.prop(scene.affinitybridge, 'is_change_name',text = 'used orignal name')
        if scene.affinitybridge.is_change_name == True:
            col.prop(scene.affinitybridge, 'file_name', text='File Name')  
        
    def draw(self, context):
        layout = self.layout

        try:
            #ファイルパスが存在しない場合を判定
            if context.space_data.image.filepath_from_user(image_user=None) == '':
                #ファイルパスが存在しない場合
                self.render_setting()
                self.used_original_name()
                #Affinity PhotoV2と連携するか外部ソフトと連携するか選択する
                #affinity bridgeのボタン
                is_affinity = context.scene.affinitybridge.is_used_affinityphoto
                self.affinity_bridge(is_affinity)
            else:
                #ファイルパスが存在する場合                
                is_affinity = context.scene.affinitybridge.is_used_affinityphoto
                self.affinity_bridge(is_affinity)         
                                            
        except:
            col = layout.column(align=True)
            col.label(text= '有効な画像を開いてください',icon = 'ERROR')
                        
class AFFINITYBRIDGE_PT_RenderSettingPanel(bpy.types.Panel):
    bl_idname = "AFFINITY_BRIDGE_PT_RenderSettingPanel"
    bl_label = "Bridge AffinityPhoto RenderSettings"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "AffinityBridge"

    def make_ui_alltype(self):
            context = bpy.context
            layout = self.layout
            box = layout.box()
            box.label(text= 'All Type RenderPass',icon = 'KEYTYPE_KEYFRAME_VEC')
                
            col = layout.column(align=True)            
            view_layer = context.view_layer
            col.prop(view_layer,"use_pass_combined")
            col.prop(view_layer, "use_pass_z")
            col.prop(view_layer, "use_pass_mist")
            col.prop(view_layer, "use_pass_position")
            col.prop(view_layer, "use_pass_normal")   
    
    def draw(self, context):
            layout = self.layout
            #swith render engine
            rd = context.scene.render
            layout.prop(rd,'engine',text = 'Render Engine')

            box = layout.box()                
            
            if context.scene.render.engine == 'CYCLES':
                #cycles
                view_layer = context.view_layer                
                cycles_view_layer = view_layer.cycles
                
                self.make_ui_alltype()
                
                box = layout.box()
                box.label(text= 'Cycles',icon = 'KEYTYPE_EXTREME_VEC')
                col = layout.column(align=True) 
                sub = col.column()
                sub.active = not rd.use_motion_blur
                sub.prop(view_layer, "use_pass_vector")
                col.prop(view_layer, "use_pass_uv")
                
                col = layout.column(heading="Diffuse", align=True)
                col.prop(view_layer, "use_pass_diffuse_direct", text="Direct")
                col.prop(view_layer, "use_pass_diffuse_indirect", text="Indirect")
                col.prop(view_layer, "use_pass_diffuse_color", text="Color")
                
                col = layout.column(heading="Glossy", align=True)
                col.prop(view_layer, "use_pass_glossy_direct", text="Direct")
                col.prop(view_layer, "use_pass_glossy_indirect", text="Indirect")
                col.prop(view_layer, "use_pass_glossy_color", text="Color")

                col = layout.column(heading="Transmission", align=True)
                col.prop(view_layer, "use_pass_transmission_direct", text="Direct")
                col.prop(view_layer, "use_pass_transmission_indirect", text="Indirect")
                col.prop(view_layer, "use_pass_transmission_color", text="Color")

                col = layout.column(heading="Other", align=True)
                col.prop(view_layer, "use_pass_emit", text="Emission")
                col.prop(view_layer, "use_pass_environment")
                col.prop(view_layer, "use_pass_shadow")
                col.prop(view_layer, "use_pass_ambient_occlusion", text="Ambient Occlusion")
                col.prop(cycles_view_layer, "use_pass_shadow_catcher")
                
                box = layout.box()
                box.label(text= 'Cryptomatte',icon = 'KEYTYPE_EXTREME_VEC')      
    
                col = layout.column()
                col.prop(view_layer, "use_pass_cryptomatte_object", text="Object")
                col.prop(view_layer, "use_pass_cryptomatte_material", text="Material")
                col.prop(view_layer, "use_pass_cryptomatte_asset", text="Asset")
                col = layout.column()
                col.active = any((view_layer.use_pass_cryptomatte_object,
                                        view_layer.use_pass_cryptomatte_material,
                                        view_layer.use_pass_cryptomatte_asset))
                col.prop(view_layer, "pass_cryptomatte_depth", text="Levels")

                if context.engine == 'BLENDER_EEVEE':
                    col.prop(view_layer, "use_pass_cryptomatte_accurate",
                            text="Accurate Mode")
                
            elif context.scene.render.engine == 'BLENDER_EEVEE':
                
                self.make_ui_alltype()
                
                box = layout.box()
                box.label(text= 'EEVEE',icon = 'KEYTYPE_EXTREME_VEC')
                col = layout.column(align=True) 
                
                #eevee
                view_layer = context.view_layer    
                view_layer_eevee = view_layer.eevee
                
                col = layout.column(heading="Diffuse", align=True)
                col.prop(view_layer, "use_pass_diffuse_direct", text="Light")
                col.prop(view_layer, "use_pass_diffuse_color", text="Color")

                col = layout.column(heading="Specular", align=True)
                col.prop(view_layer, "use_pass_glossy_direct", text="Light")
                col.prop(view_layer, "use_pass_glossy_color", text="Color")

                col = layout.column(heading="Volume", align=True)
                col.prop(view_layer_eevee, "use_pass_volume_direct", text="Light")

                col = layout.column(heading="Other", align=True)
                col.prop(view_layer, "use_pass_emit", text="Emission")
                col.prop(view_layer, "use_pass_environment")
                col.prop(view_layer, "use_pass_shadow")
                col.prop(view_layer, "use_pass_ambient_occlusion",
                        text="Ambient Occlusion")
                
                box = layout.box()
                box.label(text= 'Cryptomatte',icon = 'KEYTYPE_EXTREME_VEC')      
    
                col = layout.column()
                col.prop(view_layer, "use_pass_cryptomatte_object", text="Object")
                col.prop(view_layer, "use_pass_cryptomatte_material", text="Material")
                col.prop(view_layer, "use_pass_cryptomatte_asset", text="Asset")
                col = layout.column()
                col.active = any((view_layer.use_pass_cryptomatte_object,
                                        view_layer.use_pass_cryptomatte_material,
                                        view_layer.use_pass_cryptomatte_asset))
                col.prop(view_layer, "pass_cryptomatte_depth", text="Levels")

                if context.engine == 'BLENDER_EEVEE':
                    col.prop(view_layer, "use_pass_cryptomatte_accurate",
                            text="Accurate Mode")
                
            else:
                box = layout.box()
                box.label(text= 'ERROR:Not applicable',icon = 'ERROR')                
            
class AFFINITYBRIDGE_PT_InformationPanel(bpy.types.Panel):
    bl_idname = "AFFINITY_BRIDGE_PT_InformationPanel"
    bl_label = "Bridge AffinityPhoto Information"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "AffinityBridge"
    
    def draw(self, context):
            layout = self.layout
            box = layout.box()
            box.label(text= 'saved images path')
            box.label(text = context.scene.affinitybridge.path_str)
            
