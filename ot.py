from typing import Set
import bpy
import subprocess
import os
from bpy.types import Context

class AFFINTYBRIDGE_OT_SetOpenEXR_Selected(bpy.types.Operator):
    """
    OpenExr(MultiLayer)で出力する設定を自動化
    """
    
    bl_idname = "affinity_bridge.setopenexr_selectednode"
    bl_label = "選択したノードのすべてのソケットに自動接続するOpenEXR出力のエクスポートノードを追加 "    
    
    def add_output_node(self,overlap):
        #アウトプットノードを追加するメソッド
        #重複確認
        if overlap == True:
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

                add_node = scene.node_tree.nodes['export_openexr_AB']   
        else:
                bpy.ops.node.add_node(use_transform=True, type="CompositorNodeOutputFile")
                output_node = bpy.context.scene.node_tree.nodes.active
                #アウトプットノードの設定(ID、ビジュアル)
                output_node.name = "export_openexr_selected_AB"
                output_node.label = "Export_OpenEXR(MultiLayer)"
                output_node.use_custom_color = True
                output_node.color = (0.6,0.3,0.5)
                #アウトプットノードの設定（ファイル設定）
                output_node.format.file_format = "OPEN_EXR_MULTILAYER"               

                add_node = bpy.context.scene.node_tree.nodes.active
                
        return  add_node
    
    def setting_export_node(self,input_node):
        #インプットノードの性質に合わせてアウトプットノードを設定するメソッド
        input_node_1 = input_node
        socket_counts = len(input_node_1.outputs)
        
        for num in range(socket_counts - 1):
            bpy.ops.node.output_file_add_socket()
            
        return socket_counts

    def conecting_nodes(self,count,outputnode,inputnode):
        #インプットノードとアウトプットを接続するメソッド
        scene = bpy.context.scene
        node_tree = scene.node_tree
        socket_count = count
        exportnode = outputnode
        selected_node = inputnode
        
        print(socket_count)
        for i in range(socket_count):
            node_tree.links.new(exportnode.inputs[i],
                                selected_node.outputs[i])
        #ソケットの名称は変更できない(ReadOnlyのため)

    def node_location(self,outputnode,inputnode):
        #ノードの位置調整
            exportnode = outputnode
            selectnode = inputnode
            
            x= selectnode.location.x
            exportnode.location.x = x + 300
            
            y= selectnode.location.y
            exportnode.location.y = y - 20        
        
    def execute(self,context):
        #インプットノードの取得
        input_node = bpy.context.scene.node_tree.nodes.active
        #対象ノードがレンダーレイヤーの場合、処理を行わない
        if not input_node.type == "R_LAYERS":
            #アウトプットノードの設定        
            output_node = self.add_output_node(overlap = False)
            socket_count = self.setting_export_node(input_node)
            
            #ノードの接続
            self.conecting_nodes(socket_count,output_node,input_node)

            #ノードの位置調整
            self.node_location(output_node,input_node)
        else:
            self.report({'ERROR'},'レンダーレイヤーには使用できません') 
        return {'FINISHED'}

class AFFINITYBRIDGE_OT_SetOpenEXR_RenderLayer(bpy.types.Operator):
    """
    OpenExr(MultiLayer)で出力する設定を自動化
    """
    
    bl_idname = "affinity_bridge.setopenexr"
    bl_label = "RenderLayerに自動接続するOpenEXR出力のエクスポートノードを追加"
    
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
            
            return scene.node_tree.nodes['export_openexr_AB']

    def add_input_node(self):
        #重複確認
        try:
            scene = bpy.context.scene
            scene.node_tree.nodes['input_openexr_AB']
        except KeyError:
            pass
        else:
            #ノード削除
            node = scene.node_tree.nodes['input_openexr_AB']
            scene.node_tree.nodes.remove(node)
        finally:
            bpy.ops.node.add_node(use_transform=True, type="CompositorNodeRLayers")
            input_node = bpy.context.scene.node_tree.nodes.active
            #アウトプットノードの設定(ID、ビジュアル)
            input_node.name = "input_openexr_AB"
            input_node.label = "Input_OpenEXR(MultiLayer)"
            input_node.use_custom_color = True
            input_node.color = (0.6,0.3,0.5)
            #アウトプットノードの設定（ファイル設定）   
            
            return scene.node_tree.nodes['input_openexr_AB']
    
    def get_render_pass_dict(self,outputnode,inputnode):
        scene = bpy.context.scene
        node_tree = scene.node_tree
        
        exportnode = outputnode
        renderlayer = inputnode
        
        output_sockets = len(renderlayer.outputs)
        output_sockets_name = []
        output_sockets_enable = []
        output_sockets_dict = {}
        
        #ノードのソケットを全部取得（非表示含め）
        for i in range(output_sockets):
            names = renderlayer.outputs[i].name
            output_sockets_name.append(names)
            
            enables = renderlayer.outputs[i].enabled
            output_sockets_enable.append(enables)
        output_sockets_dict = dict(zip(output_sockets_name,output_sockets_enable))
        
        #ノードの全ソケットから表示されているものだけ抽出
        for name,enable in list(output_sockets_dict.items()):
            if enable == False:
                output_sockets_dict.pop(name)
        
        #dictについて
        #{ソケットの名前：True or False}
        #RenderLayerについてはoutputsを参照すると非表示になっているソケットについても参照してしまう
        #そのためoutputsをすべて参照したのちに有効なノードのみを出力する辞書データを作成する
        return output_sockets_dict
                    
    def setting_export_node(self,pathdata_dict):

        for i in range(len(pathdata_dict)-1):
            bpy.ops.node.output_file_add_socket()
            
    def conecting_nodes(self,pathdata_dict,outputnode,inputnode):
        scene = bpy.context.scene
        node_tree = scene.node_tree
        
        exportnode = outputnode
        renderlayer = inputnode
        
        for i in range(len(pathdata_dict)):
            node_tree.links.new(exportnode.inputs[i],
                                renderlayer.outputs[i])
        #ソケットの名称は変更できない(ReadOnlyのため)
        
    def node_location(self,outputnode,inputnode):
        exportnode = outputnode
        renderlayer = inputnode
        
        x= exportnode.location.x
        renderlayer.location.x = x-300
        
    def execute(self,context):
        #アウトプットノードを追加・設定  
        inputnode = self.add_input_node()      
        outputnode = self.add_output_node()
        
        #ビューレイヤーから出力パス情報を取得
        pathdata_dict  = self.get_render_pass_dict(outputnode,inputnode)
        
        
        #パス情報をノードに適用
        self.setting_export_node(pathdata_dict)
        
        #ノードを接続する
        self.conecting_nodes(pathdata_dict,outputnode,inputnode)
        
        #ノードの位置情報変更
        self.node_location(outputnode,inputnode)
        return{'FINISHED'}
    
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

    def convert_fileformat(self,fileformat):
        
        file_format = 'EXR' if fileformat == 'OPEN_EXR' else fileformat
        file_format = 'EXR' if fileformat == 'OPEN_EXR_MULTILAYER' else fileformat
        
        return file_format

    def save_render_setting(self,):
        img_stg =bpy.context.scene.render.image_settings
        old_ff = img_stg.file_format
        old_cc = img_stg.color_mode
        
        old_setting = [old_ff,old_cc]
        
        return old_setting

    def undo_render_setting(self,old_setting):
        img_stg =bpy.context.scene.render.image_settings    
        img_stg.file_format = old_setting[0]
        img_stg.color_mode = old_setting[1]
        
    def open_affinity_photo(self,file_path,is_ap,other_path):
        #AffinityPhotoのパス
        if is_ap == True:
            users_path = os.path.expanduser('~')
            ap2_path = '\AppData\Local\Microsoft\WindowsApps\AffinityPhoto2.exe'
            affinity_photo2_path = users_path + ap2_path    
            
            subprocess.Popen([ affinity_photo2_path, file_path ],shell = True)
            
        else:
            subprocess.Popen([ other_path, file_path ],shell = True)
            
        
        return 

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
                #ファイルパスが存在するときの処理
                is_exist_filepath = True
                save_dir = file_path
                    
            #レンダリング設定を一時保存する
            old_rebder_setting = self.save_render_setting()
            
            #ファイルパスが存在しないデータのみ使用
            if is_exist_filepath == False:
                #レンダリング設定を上書する
                #file_mode,color_mode
                afy_brg = context.scene.affinitybridge
                context.scene.render.image_settings.file_format = afy_brg.file_format
                context.scene.render.image_settings.color_mode = afy_brg.color_mode
                
            else:
                pass
            
            #convert exr
            file_format = self.convert_fileformat(context.scene.render.image_settings.file_format)
            
            #save
            if is_exist_filepath == False:
                        
                if context.scene.affinitybridge.is_change_name == True:
                    file_name_change = afy_brg.file_name
                    saved_path = save_dir + "\\" + file_name_change + '.' + file_format.lower()                            
                    
                else:
                    file_name_change = file_name
                    saved_path = save_dir + "\\" + file_name_change +'.' + file_format.lower()
                    
                    #画像を保存
                    bpy.data.images[file_name].save_render(saved_path,scene = bpy.context.scene)

                    #保存した画像のリロード
                    bpy.ops.image.open(filepath = saved_path)
                    
            else:
                saved_path = file_path
                
            #画像編集ソフトにブリッジ
            is_ap = context.scene.affinitybridge.is_used_affinityphoto
            
            prefs = context.preferences.addons['Affinity_Bridge'].preferences
            other_file_path = prefs.option_image_editing_exe
            self.open_affinity_photo(saved_path,is_ap,other_file_path)
        
            #UIにファイルパスを表示する
            context.scene.affinitybridge.path_str = saved_path
            
            #レンダリング設定を元に戻す
            self.undo_render_setting(old_rebder_setting)
            
            self.report({'INFO'},'Success!:'+ saved_path) 
    
        return {'FINISHED'}