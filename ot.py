import bpy
import subprocess
import os


class AFFINITYBRIDGE_OT_SetOpenEXR(bpy.types.Operator):
    """
    set open exr
    """
    
    bl_idname = "affinity_bridge.setopenexr"
    bl_label = "set open exr"
    
    def render_pass_count(self):
        view_layer = bpy.context.view_layer
        scene = bpy.context.scene 
        #RAWを接続するため初期値は１
        pathes_list = []
        count = 1
        
        #全体共通パス
        common_pathes = ["z","mist","position","normal"]
        pathes_list.extend(common_pathes)
        
        if view_layer.use_pass_z == True:
            count += 1
        elif view_layer.use_pass_mist == True:
            count += 1
        elif view_layer.use_pass_position == True:
            count += 1
        elif view_layer.use_pass_normal == True:
            count += 1
        
        #cycles
        cycles_pathes = ["vector","uv",
                        "diffuse_direct","diffuse_indirect","diffuse_color",
                        "glossy_direct","glossy_indirect","glossy_color",
                        "transmission_direct","transmission_indirect","transmission_color"]
        #eevee
        eevee_pathes = ["diffuse_direct","diffuse_color",
                        "glossy_direct","glossy_color",
                        "emit","enviroment","shadow","ambient_occlussion"]
        #辞書データの初期化
        pathes_dict = {}
        if scene.render.engine == "CYCLES":
            pathes_list.extend(cycles_pathes)
            for pathname in pathes_list:
                print(pathname)
                #bool 判定
                #辞書データ　item:bool
                pass
        
        else:
            pass
                #EEVEE
        if scene.render.engine == "BLENDER_EEVEE":
            pathes_list.extend(eevee_pathes)
            #bool判定
            #._{itemname}
            #辞書データ　item:bool
            #ボリュームライトだけ例外処理すること
            pass
        else:
            pass
        return pathes_list
    #レンダラーによって処理をわける
    
    def execute(self,context):
        #アウトプットノードを追加
        bpy.ops.node.add_node(use_transform=True, type="CompositorNodeOutputFile")
        output_node = bpy.context.scene.node_tree.nodes.active
        #アウトプットノードの設定(ID、ビジュアル)
        output_node.name = "export_openexr_AB"
        output_node.label = "Export_OpenEXR(MultiLayer)"
        output_node.use_custom_color = True
        output_node.color = (0.6,0.3,0.5)
        #アウトプットノードの設定（ファイル設定）
        output_node.format.file_format = "OPEN_EXR_MULTILAYER"
        
        #AffinityBridgeから出力パス情報を取得
        render_pass_count  = self.render_pass_count()
        print(render_pass_count)
        return{'FINISHED'}


def convert_fileformat(fileformat):
    
    file_format = 'EXR' if fileformat == 'OPEN_EXR' else fileformat
    file_format = 'EXR' if fileformat == 'OPEN_EXR_MULTILAYER' else fileformat
    
    return file_format

def save_render_setting():
    img_stg =bpy.context.scene.render.image_settings
    old_ff = img_stg.file_format
    old_cc = img_stg.color_mode
    
    old_setting = [old_ff,old_cc]
    
    return old_setting

def undo_render_setting(old_setting):
    img_stg =bpy.context.scene.render.image_settings    
    img_stg.file_format = old_setting[0]
    img_stg.color_mode = old_setting[1]
    
def open_affinity_photo(file_path):
    #AffinityPhotoのパス
    users_path = os.path.expanduser('~')
    ap2_path = '\AppData\Local\Microsoft\WindowsApps\AffinityPhoto2.exe'
    affinity_photo2_path = users_path + ap2_path    
    
    subprocess.Popen([ affinity_photo2_path, file_path ],shell = True)
    
    return affinity_photo2_path
    
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

        is_exist_filepath = True
        #ファイルパスが存在するときはTrue、存在しないときはFalse
    
        try:
            #ファイルパス取得
            file_path = context.space_data.image.filepath_from_user(image_user=None)
            file_name = context.space_data.image.name
            
        except:
            #例外処理
            self.report({'ERROR'},'有効な画像が選択されていません') 
            
        else:
            #ファイルパスが存在しないとき
            if file_path == '':
                is_exist_filepath = False
                bl_path = os.path.dirname(bpy.data.filepath)
                save_dir = bl_path + "\AffinityBridge"
            
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                    self.report({'INFO'},'フォルダを作成しました'+ save_dir) 
                
            else:
                is_exist_filepath = True
                print('開発用:パスが存在しています')
                save_dir = file_path
                    
            #レンダリング設定を一時保存する
            old_rebder_setting = save_render_setting()
            print('開発用：現在使用しているレンダリング設定をバックアップしました')
            
            #ファイルパスが存在しないデータのみ使用
            if is_exist_filepath == False:
                #レンダリング設定を上書する
                #file_mode,color_mode
                afy_brg = context.scene.affinitybridge
                context.scene.render.image_settings.file_format = afy_brg.file_format
                context.scene.render.image_settings.color_mode = afy_brg.color_mode
                print('開発用：ファイルパスが存在しないためレンダリング設定を上書しています')
                
            else:
                print('開発用：ファイルパスが存在するためレンダリング設定を上書していません')
            
            #convert exr
            file_format = convert_fileformat(context.scene.render.image_settings.file_format)

            print('レンダリング設定を任意の内容に変更しました')
            
            #save
            if is_exist_filepath == False:
                        
                if context.scene.affinitybridge.is_change_name == True:
                    file_name_change = afy_brg.file_name
                    saved_path = save_dir + "\\" + file_name_change + '.' + file_format.lower()                            
                    
                else:
                    file_name_change = file_name
                    saved_path = save_dir + "\\" + file_name_change +'.' + file_format.lower()
                    
                    bpy.data.images[file_name].save_render(saved_path,scene = bpy.context.scene)
                    print('開発用：画像を保存しましたファイルパスは以下の通りです')
                    #load
                    bpy.ops.image.open(filepath = saved_path)
                    print('開発用:画像を再ロードしました')
                    
            else:
                saved_path = file_path
                
            open_affinity_photo(saved_path)
        
            #UIにファイルパスを表示する
            context.scene.affinitybridge.path_str = saved_path
            
            #レンダリング設定を元に戻す
            undo_render_setting(old_rebder_setting)
            
            self.report({'INFO'},'Success!:'+ saved_path) 
    
        return {'FINISHED'}