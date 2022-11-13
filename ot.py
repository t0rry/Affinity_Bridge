import bpy
import subprocess
import os

class AFFINITYBRIDGE_OT_Photo(bpy.types.Operator):
    """
    image loaded start-up AffinityPhoto2 
    """    
    bl_idname = "affinity_bridge.open_affinity_photo"
    bl_label = "atart-up to affinity photo"

    def execute(self,context):
        #Can only be used when there is only one IMAGE_EDITOR on the screen
        n = 0
        for area in bpy.context.screen.areas:
            if area.type =='IMAGE_EDITOR':
                n = n + 1
                
        if n ==1:
            #make start-up AffinityPhoto2 path
            users_path = os.path.expanduser('~')
            ap2_path = '\AppData\Local\Microsoft\WindowsApps\AffinityPhoto2.exe'
            affinity_photo2_path = users_path + ap2_path

            #make image path
            
            #start-up AffinityPhoto2
            subprocess.Popen([ affinity_photo2_path, "ここに画像のパスが入ります" ],shell = True)
            
        else:
            self.report({'INFO'},'ERROR:画面上にIMAGE_EDITORが複数存在しています')

        
        return {'FINISHED'}