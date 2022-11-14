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
        col = layout.column(align=True)
        
        col.scale_x = 1
        col.scale_y = 1

        col.prop(scene.affinitybridge, "file_format", text="Format") 
        col.prop(scene.affinitybridge, "color_mode", text="Color Mode") 
        
        layout.separator()
        col.prop(scene.affinitybridge, "file_name", text="File Name")         
        
        layout.separator()
        col = layout.column(align=True)
        col.scale_x = 3
        col.scale_y = 3
        col.operator('affinity_bridge.open_affinity_photo',text='Bridge AffinityPhoto2',icon = 'EXPORT')
        
