import bpy
import subprocess
import os


class AFFINITYBRIDGE_OT_SetOpenEXR(bpy.types.Operator):
    """
    OpenExr(MultiLayer)で出力する設定を自動化
    """
    
    bl_idname = "affinity_bridge.setopenexr"
    bl_label = "set open exr"
    
    def add_output_node(self):
        #重複確認
        try:
            scene = bpy.context.scene
            scene.node_tree.nodes['export_openexr_AB']
        except KeyError:
            pass
        else:
            #ノード削除
            node = scene.node_tree.nodes['export_openexr_AB']
            scene.node_tree.nodes.remove(node)
        finally:
            bpy.ops.node.add_node(use_transform=True, type="CompositorNodeOutputFile")
            output_node = bpy.context.scene.node_tree.nodes.active
            #アウトプットノードの設定(ID、ビジュアル)
            output_node.name = "export_openexr_AB"
            output_node.label = "Export_OpenEXR(MultiLayer)"
            output_node.use_custom_color = True
            output_node.color = (0.6,0.3,0.5)
            #アウトプットノードの設定（ファイル設定）
            output_node.format.file_format = "OPEN_EXR_MULTILAYER"        
    
    def get_render_pass_dict(self):
        view_layer = bpy.context.view_layer
        scene = bpy.context.scene 
        #辞書データの初期化
        pathes_dict = {}
        #辞書データ構造設計
        #dict
        #     --key1:
        #     ------[value1(ソケット数),[value2(有効判定)]]
        #
        
        #全体共通パス
        common_pathes = {"z":[1],"mist":[1],"position":[1],"normal":[1]}
        pathes_dict.update(common_pathes)
        
        #cycles
        cycles_pathes = {"vector":[1],"uv":[1],
                        "diffuse_direct":[1],"diffuse_indirect":[1],"diffuse_color":[1],
                        "glossy_direct":[1],"glossy_indirect":[1],"glossy_color":[1],
                        "transmission_direct":[1],"transmission_indirect":[1],"transmission_color":[1]}
        #eevee
        eevee_pathes = {"diffuse_direct":[1],"diffuse_color":[1],
                        "glossy_direct":[1],"glossy_color":[1],
                        "emit":[1],"environment":[1],"shadow":[1],"ambient_occlusion":[1]}
        #リスト、辞書データの初期化
        bool_dict = {}
        if scene.render.engine == "CYCLES":
            #cycles要素を全体共通パスに合成
            pathes_dict.update(cycles_pathes)
            
            #bool判定取得
            for pathname,value_list in pathes_dict.items():
                bool_get = eval(f"bpy.context.view_layer.use_pass_{pathname}")
                #辞書データにboolを格納
                value_list.append(bool_get)       
        else:
            pass
                #EEVEE
        if scene.render.engine == "BLENDER_EEVEE":
            #EEVEE要素を全体共通パスに合成
            pathes_dict.update(eevee_pathes)
            
            #bool判定取得
            for pathname,value_list in pathes_dict.items():
                bool_get = eval(f"bpy.context.view_layer.use_pass_{pathname}")
                #辞書データにboolを格納
                value_list.append(bool_get)                         
            #ボリュームライトだけ例外処理すること（後回し）
        else:
            pass
        
        return pathes_dict
    
    def setting_export_node(self,pathdata_dict):
        #bool判定,Trueの数だけソケットを追加する
        #cyclesはアルファ分があるので1を追加
        if bpy.context.scene.render.engine == "CYCLES":
            active_paths = 2
        elif bpy.context.scene.render.engine == "BLENDER_EEVEE":
            active_paths = 1
            
        for key,value_list in pathdata_dict.items():
            if value_list[1] == True:
                active_paths = active_paths + value_list[0]
        
        #ソケットの数を追加
        #ソケットの名称は読み取り専用のため断念
        #もし変更できるならばitemsで取得したkeyを活用
        for i in range(active_paths):
            bpy.ops.node.output_file_add_socket()
            
        return active_paths
    
    def conecting_nodes(self,pathdata_dict):
        pass 
    
    def execute(self,context):
        #アウトプットノードを追加・設定        
        self.add_output_node()
        
        #ビューレイヤーから出力パス情報を取得
        pathdata_dict  = self.get_render_pass_dict()
        print(pathdata_dict)
        
        #パス情報をノードに適用
        self.setting_export_node(pathdata_dict)
        
        #ノードを接続する
        self.conecting_nodes(pathdata_dict)
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