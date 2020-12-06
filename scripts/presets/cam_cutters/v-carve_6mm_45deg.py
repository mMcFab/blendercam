import bpy
d = bpy.context.scene.cam_cutting_tools[bpy.context.scene.cam_active_cutting_tool]

d.cutter_type = 'VCARVE'
d.cutter_diameter = 0.006
d.cutter_length = 25.0
d.cutter_tip_angle = 45.0
