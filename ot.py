import bpy
import os

class AFFINITY_BRIDGE_OT_OpenPhoto(bpy.types.Operator):
    """
    open to spotify development page(web)
    """    
    bl_idname = "bspotify.open_spotify_dev_page"
    bl_label = "open to affinity photo"

    def execute(self,context):
        webbrowser.open('https://developer.spotify.com/')
        return {'FINISHED'}