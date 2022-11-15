import bpy
import subprocess
import os

def convert_fileformat(fileformat):
    
    file_format = 'EXR' if fileformat == 'OPEN_EXR' else fileformat
    file_format = 'EXR' if fileformat == 'OPEN_EXR_MULTILAYER' else fileformat
    
    return file_format

class AFFINITYBRIDGE_OT_Reload(bpy.types.Operator):
    """
    image reloaded image
    """    
    bl_idname = "affinity_bridge.reload_affinity_photo"
    bl_label = "atart-up to affinity photo"
    
    def execute(self,countext):
        bpy.ops.image.reload()
        self.report({'INFO'},'Success!:Reload image!') 
        return {'FINISHED'}
    
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
                            
                            print('保存先フォルダが存在しないためフォルダを作成しました')
                            print(save_dir)
                            
                        #backup saved parameter    
                        img_stg =bpy.context.scene.render.image_settings
                        old_ff = img_stg.file_format
                        old_cc = img_stg.color_mode
                        print('現在使用しているレンダリング設定をバックアップしました')
                        
                        #change savedparameter
                        afy_brg = context.scene.affinitybridge
                        img_stg.file_format = afy_brg.file_format
                        
                        #convert exr
                        file_format = convert_fileformat(img_stg.file_format)
                        
                        img_stg.color_mode = afy_brg.color_mode
                        print('レンダリング設定を任意の内容に変更しました')
                        
                        #save
                        if context.scene.affinitybridge.is_change_name == True:
                            file_name_change = afy_brg.file_name
                            saved_path = save_dir + "\\" + file_name_change + '.' + file_format.lower()                            
                            
                        else:
                            file_name_change = file_name
                            saved_path = save_dir + "\\" + file_name_change + '.' + file_format.lower()

                        bpy.data.images[file_name].save_render(saved_path,scene = bpy.context.scene)
                        print('画像を保存しましたファイルパスは以下の通りです')
                        
                        #情報の上書き
                        file_path = save_dir + "\\" + file_name_change + "." + file_format.lower()
                        print(file_path)
                        
                        context.scene.affinitybridge.path_str = file_path
                        
                        #load
                        bpy.ops.image.open(filepath = file_path)
                        print('画像を再ロードしました')
                        
                        #Undo image saved parameter
                        img_stg.file_format = old_ff
                        img_stg.color_mode = old_cc
                        
                        self.report({'INFO'},'Success!:'+ file_path) 
                        
                    else:
                        self.report({'INFO'},'Success!:Start AffinityPhoto2 Enjoy<3') 
                                        
                    if n == 1:
                        #make start-up AffinityPhoto2 path
                        users_path = os.path.expanduser('~')
                        ap2_path = '\AppData\Local\Microsoft\WindowsApps\AffinityPhoto2.exe'
                        affinity_photo2_path = users_path + ap2_path
                        
                        context.scene.affinitybridge.path_str = file_path
                        
                        #start-up AffinityPhoto2
                        subprocess.Popen([ affinity_photo2_path, file_path ],shell = True)
                        
                    else:
                        self.report({'ERROR'},'ERROR:画面上にIMAGE_EDITORが複数存在しています')
    
                except AttributeError:
                    self.report({'ERROR'},'未実装:何も画像が選択されていません') 
                
        return {'FINISHED'}