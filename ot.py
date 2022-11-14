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
                
                #画像パスの生成
                #画面上の画像エディタ状で画像を開いているか
                try:
                    file_name = area.spaces.active.image.name
                    file_path = bpy.data.images[file_name].filepath_from_user(image_user=None)            
                    
                        #保存されていない画像の処理
                    if file_path == '':                    
                        #make dir
                        bl_path = os.path.dirname(bpy.data.filepath)
                        
                        save_dir = bl_path + "\AffinityBridge"
                        if not os.path.exists(save_dir):
                            os.makedirs(save_dir)
                        #save
                        bpy.data.images[file_name].save_render(save_dir + "\\" + file_name) 
                        
                        #情報の上書き
                        file_path = save_dir + "\\" + file_name
                        
                        #load
                        
                        #rename
                        
                        print(file_path)     
                    
                    else:
                        pass
                                        
                    if n ==1:
                        #make start-up AffinityPhoto2 path
                        users_path = os.path.expanduser('~')
                        ap2_path = '\AppData\Local\Microsoft\WindowsApps\AffinityPhoto2.exe'
                        affinity_photo2_path = users_path + ap2_path
                        
                        #start-up AffinityPhoto2
                        subprocess.Popen([ affinity_photo2_path, file_path ],shell = True)
                        
                    else:
                        self.report({'INFO'},'ERROR:画面上にIMAGE_EDITORが複数存在しています')
    
                except AttributeError:
                    self.report({'INFO'},'未実装:何も画像が選択されていません') 
                
                
        
        return {'FINISHED'}
    
    
    
    #memo
# for area in bpy.context.screen.areas:
#     if area.type =='IMAGE_EDITOR':
#         print(area.spaces.active.image.name)

for area in bpy.context.screen.areas:
    if area.type =='IMAGE_EDITOR':
        file_name =area.spaces.active.image.name
        print(file_name)
        test = area.spaces.active.image.is_dirty
        print(test)
        file_path = bpy.data.images[file_name].filepath
        print(file_path)
        
        
for area in bpy.context.screen.areas:
    if area.type =='IMAGE_EDITOR':
        file_name =area.spaces.active.image.name
        test = area.spaces.active.image.is_dirty
        file_path = bpy.data.images[file_name].filepath
        print(file_path)
        if file_path == '':
            print('None')
        else:
            print('else')