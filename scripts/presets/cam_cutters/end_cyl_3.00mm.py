import bpy
d = bpy.context.scene.cam_cutting_tools[bpy.context.scene.cam_active_cutting_tool]

d.cutter_type = 'END'
d.cutter_diameter = 0.003
d.cutter_length = 25.0
d.cutter_tip_angle = 60.0
