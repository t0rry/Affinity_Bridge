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
        file_name = ''
        
        for area in bpy.context.screen.areas:
            if area.type =='IMAGE_EDITOR':
                n = n + 1
                file_name = area.spaces.active.image.name
                file_path = bpy.data.images[file_name].filepath_from_user(image_user=None)
                print(file_path)
                if file_path == '':
                    self.report({'INFO'},'未実装:Render Result、ViewerNode未対応です')
                    
                    #make dir
                    
                    #save
                    
                    #load
                    
                    #rename
                    
                    
                    
                else:
                    
                
                    if n ==1:
                        #make start-up AffinityPhoto2 path
                        users_path = os.path.expanduser('~')
                        ap2_path = '\AppData\Local\Microsoft\WindowsApps\AffinityPhoto2.exe'
                        affinity_photo2_path = users_path + ap2_path

                        #make image path
                        
                        #start-up AffinityPhoto2
                        subprocess.Popen([ affinity_photo2_path, file_path ],shell = True)
                        
                    else:
                        self.report({'INFO'},'ERROR:画面上にIMAGE_EDITORが複数存在しています')

        
        return {'FINISHED'}
    
    
    
    #memo
# for area in bpy.context.screen.areas:
#     if area.type =='IMAGE_EDITOR':
#         print(area.spaces.active.image.name)

# for area in bpy.context.screen.areas:
#     if area.type =='IMAGE_EDITOR':
#         file_name =area.spaces.active.image.name
#         file_path = bpy.data.images[file_name].filepath