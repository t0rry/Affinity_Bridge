import bpy
import os

class AFFINITYBRIDGE_PT_Panel(bpy.types.Panel):
    bl_idname = "AFFINITY_BRIDGE.PT_Panel"
    bl_label = "Start-up AffinityPhoto"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "AffinityBridge"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene.affinitybridge, "file_name", text="file name") 
        layout.prop(scene.affinitybridge, "file_format", text="file name") 
        layout.prop(scene.affinitybridge, "color_mode", text="file name") 
                
        layout.operator('affinity_bridge.open_affinity_photo',text='Bridge AffinityPhoto2')
        
