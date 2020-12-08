# blender CAM ui.py (c) 2012 Vilem Novak
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

import bpy
from bpy.types import UIList

from cam import simple
from cam.simple import *

# EXPERIMENTAL=True#False


####Panel definitions
class CAMButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.engine in cls.COMPAT_ENGINES

        


class CAM_MACHINE_Panel(CAMButtonsPanel, bpy.types.Panel):
    """CAM machine panel"""
    bl_label = "Machine Settings"
    bl_idname = "WORLD_PT_CAM_MACHINE"

    COMPAT_ENGINES = {'BLENDERCAM_RENDER'}

    bl_options = {'DEFAULT_CLOSED'}
    #def draw_header(self, context):
    #    self.layout.menu("CAM_MACHINE_MT_presets", text="CAM Machine")

    def draw(self, context):
        layout = self.layout.box()
        s = bpy.context.scene
        us = s.unit_settings

        ao = s.cam_machine

        if ao:
            use_experimental = bpy.context.preferences.addons['cam'].preferences.experimental

            # machine preset
            row = layout.row(align=True)
            row.menu("CAM_MACHINE_MT_presets", text=bpy.types.CAM_MACHINE_MT_presets.bl_label)
            row.operator("render.cam_preset_machine_add", text="", icon='ADD')
            row.operator("render.cam_preset_machine_add", text="", icon='REMOVE').remove_active = True
            # layout.prop(ao,'name')
            layout.prop(ao, 'post_processor')
            

            layout.prop(us, 'system')

            
            
            #grid = layout.grid_flow(columns=3, even_columns=True, align=True)
            box = layout.box()

            box.row().prop(ao, 'working_area')
            
            box.prop(ao, 'use_position_definitions')
            if ao.use_position_definitions:
                column = box.column()
                column.row().prop(ao, 'starting_position')
                column.row().prop(ao, 'mtc_position')
                column.row().prop(ao, 'ending_position')

            box = layout.box()
            column = box.column()
            row = column.row(align=True)
            row.prop(ao, 'feedrate_min')
            row.prop(ao, 'feedrate_max')
            #Spindle and feedrate defaults are not actually used currently, so just need removing anyway
            #column.prop(ao,
            #            'feedrate_default')  # TODO: spindle default and feedrate default should become part of the cutter definition...
            
            #box.separator(factor=0.5)
            column = box.column()
            row = column.row(align=True)
            row.prop(ao, 'spindle_min')
            row.prop(ao, 'spindle_max')
            #column.prop(ao, 'spindle_default')
            column.prop(ao, 'spindle_start_time')

            box = layout.box()
            box.prop(ao, 'eval_splitting')
            if ao.eval_splitting:
                box.prop(ao, 'split_limit')

            if use_experimental:
                box = layout.box().column()
                box.prop(ao, 'axis4')
                box.prop(ao, 'axis5')
                box.prop(ao, 'collet_size')

                box.prop(ao, 'output_block_numbers')
                if ao.output_block_numbers:
                    box.prop(ao, 'start_block_number')
                    box.prop(ao, 'block_number_increment')
                box.prop(ao, 'output_tool_definitions')
                box.prop(ao, 'output_tool_change')
                if ao.output_tool_change:
                    box.prop(ao, 'output_g43_on_tool_change')


class CAM_UL_cutting_tools(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # assert(isinstance(item, bpy.types.VertexGroup)
        #operation = item
        if self.layout_type in {'DEFAULT', 'COMPACT'}:

            layout.label(text=item.cutter_name, translate=False, icon_value=icon)
            
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class CAM_UL_operations(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # assert(isinstance(item, bpy.types.VertexGroup)
        operation = item
        if self.layout_type in {'DEFAULT', 'COMPACT'}:

            layout.label(text=item.name, translate=False, icon_value=icon)
            icon = 'LOCKED' if operation.computing else 'UNLOCKED'
            if operation.computing:
                layout.label(text=operation.outtext)  # "computing" )
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


class CAM_UL_orientations(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # assert(isinstance(item, bpy.types.VertexGroup)
        #operation = item
        if self.layout_type in {'DEFAULT', 'COMPACT'}:

            layout.label(text=item.name, translate=False, icon_value=icon)
        # icon = 'LOCKED' if operation.computing else 'UNLOCKED'
        # if operation.computing:
        #	layout.label(text=operation.outtext)#"computing" )
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


class CAM_UL_chains(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # assert(isinstance(item, bpy.types.VertexGroup)
        chain = item
        if self.layout_type in {'DEFAULT', 'COMPACT'}:

            layout.label(text=item.name, translate=False, icon_value=icon)
            icon = 'LOCKED' if chain.computing else 'UNLOCKED'
            if chain.computing:
                layout.label(text="computing")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


class CAM_CHAINS_Panel(CAMButtonsPanel, bpy.types.Panel):
    """CAM chains panel"""
    bl_label = "Operation Sequences"
    bl_idname = "WORLD_PT_CAM_CHAINS"

    COMPAT_ENGINES = {'BLENDERCAM_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout = layout.box()

        column = layout.column()
        column.label(text="Operation Sequences")
        row = column.row()
        scene = bpy.context.scene

        row.template_list("CAM_UL_chains", '', scene, "cam_chains", scene, 'cam_active_chain')
        col = row.column(align=True)
        col.operator("scene.cam_chain_add", icon='ADD', text="")
        if len(scene.cam_chains) > 0:
        # col.operator("scene.cam_operation_copy", icon='COPYDOWN', text="")
            col.operator("scene.cam_chain_remove", icon='REMOVE', text="")
        # if collection:
        # col.separator()
        # col.operator("scene.cam_operation_move", icon='TRIA_UP', text="").direction = 'UP'
        # col.operator("scene.cam_operation_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
        # row = layout.row()

        if len(scene.cam_chains) > 0:
            chain = scene.cam_chains[scene.cam_active_chain]
            

            if chain:
                #layout.separator()
                layout = layout.box()
                layout.prop(chain, 'name')

                #layout.label(text="Operations in '" + chain.name + "'")
                if len(scene.cam_operations) > 0:
                    column = layout.column()
                    column.label(text="Operations in Sequence")
                    row = column.row(align=True)

                    row.template_list("CAM_UL_operations", '', chain, "operations", chain, 'active_operation')
                    col = row.column(align=True)
                    col.operator("scene.cam_chain_operation_add", icon='ADD', text="")
                    col.operator("scene.cam_chain_operation_remove", icon='REMOVE', text="")
                    if len(chain.operations) > 0:
                        col.operator("scene.cam_chain_operation_up", icon='TRIA_UP', text="")
                        col.operator("scene.cam_chain_operation_down", icon='TRIA_DOWN', text="")

                        if not chain.computing:
                            if chain.valid:
                                
                                layout.operator("object.calculate_cam_paths_chain", text="Calculate Sequence Paths")
                                row = layout.row(align=True)
                                row.operator("object.cam_simulate_chain", text="Simulate Sequence")
                                row.operator("object.cam_export_paths_chain", text="Export gcode")
                                # layout.operator("object.calculate_cam_paths_background", text="Calculate path in background")
                            
                            else:
                                layout.label(text="Sequence invalid, can't compute")
                        else:
                            layout.label(text='Sequence is currently computing')
                    else:
                        layout.label(text="Add some operations to this Sequence!")
                else:
                    layout.label(text="Create an Operation to continue")
                
                # layout.prop(chain, 'filename')


class CAM_OPERATIONS_Panel(CAMButtonsPanel, bpy.types.Panel):
    """CAM operations panel"""
    bl_label = "Cutting Operations"
    bl_idname = "WORLD_PT_CAM_OPERATIONS"

    COMPAT_ENGINES = {'BLENDERCAM_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout.box()

        row = layout.row()
        scene = bpy.context.scene
        row.template_list("CAM_UL_operations", '', scene, "cam_operations", scene, 'cam_active_operation')
        col = row.column(align=True)
        col.operator("scene.cam_operation_add", icon='ADD', text="")
        if(len(scene.cam_operations) > 0):
            col.operator("scene.cam_operation_copy", icon='COPYDOWN', text="")
            col.operator("scene.cam_operation_remove", icon='REMOVE', text="")
            # if collection:
            col.separator()
            col.operator("scene.cam_operation_move", icon='TRIA_UP', text="").direction = 'UP'
            col.operator("scene.cam_operation_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
        # row = layout.row()

        if len(scene.cam_operations) > 0:
            use_experimental = bpy.context.preferences.addons['cam'].preferences.experimental
            ao = scene.cam_operations[scene.cam_active_operation]
            
            col = layout.column()

            col.label(text="'" + ao.name + "' Properties")

            layout = col.box()

            row = layout.row(align=True)
            row.menu("CAM_OPERATION_MT_presets", text=bpy.types.CAM_OPERATION_MT_presets.bl_label)
            row.operator("render.cam_preset_operation_add", text="", icon='ADD')
            row.operator("render.cam_preset_operation_add", text="", icon='REMOVE').remove_active = True

            if ao:
                layout.prop(ao, 'name')
                #if len(scene.cam_cutting_tools) > 0:
                

                if not ao.computing:
                    if ao.valid:
                        row = layout.row(align=True)
                        row.operator("object.calculate_cam_path", text="Calculate")

                        #hidden as it doesn't currently work
                        #row.operator("object.calculate_cam_paths_background", text="Calculate in BG")

                        
                        if ao.name is not None:
                            name = "cam_path_{}".format(ao.name)
                            if scene.objects.get(name) is not None:
                                row = layout.row(align=True)
                                row.operator("object.cam_simulate", text="Simulate")
                                row.operator("object.cam_export", text="Export gcode")
                        
                        
                        
                        #ao = scene.cam_operations[scene.cam_active_operation]

                    else:
                        layout.label(text="operation invalid, can't compute")
                else:
                    row = layout.row(align=True)
                    row.label(text='computing')
                    row.operator('object.kill_calculate_cam_paths_background', text="", icon='CANCEL')
                # layout.prop(ao,'computing')
                if ao.warnings != '':
                    box = layout.box()
                    box.label(text=" WARNING!")
                    col = box.column()
                    lines = ao.warnings.split('\n')
                    for l in lines:
                        if(l != '' and l != ' '):
                            col.label(text=l, icon='COLOR_RED')

                if ao.duration > 0:
                    if ao.name is not None:
                        name = "cam_path_{}".format(ao.name)
                        if scene.objects.get(name) is not None:
                            box = layout.box()
                            box.label(text=" Operation Info:")
                            col = box.column()
                            col.label(text='Estimated Time: ~' + str(int(ao.duration / 60)) + \
                                                        ' hour, ' + str(int(ao.duration) % 60) + ' min, ' + \
                                                        str(int(ao.duration * 60) % 60) + ' sec.')
                            col.label(text='Chipload: ~' + strInUnits(ao.chipload, 4) + ' / tooth')
                #sub = layout.column()
                #sub.active = not ao.computing
                if len(scene.cam_chains) > 0 and scene.cam_active_chain > -1:
                    layout.operator("scene.cam_chain_operation_add", icon='ADD', text="Add to '" + scene.cam_chains[scene.cam_active_chain].name + "'")
                #export_box = sub.box()

                
                #export_box.prop(ao, 'filename')

                #export_box.prop(ao, 'auto_export')

                

            else:
                layout.label(text='Add operation first')

            


class CAM_CUTTING_TOOLS_Panel(CAMButtonsPanel, bpy.types.Panel):
    """Cutting Tools panel"""
    bl_label = "Cutting Tools"
    bl_idname = "WORLD_PT_CAM_CUTTING_TOOLS"

    COMPAT_ENGINES = {'BLENDERCAM_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}
    #def draw_header(self, context):
    #    self.layout.menu("CAM_CUTTER_MT_presets", text="Cutting Tools")

    def draw(self, context):
        layout = self.layout.box()
        
        
        row = layout.row()
        scene = bpy.context.scene
        row.template_list("CAM_UL_cutting_tools", '', scene, "cam_cutting_tools", scene, 'cam_active_cutting_tool')
        #row.template_list("CAM_UL_chains", '', scene, "cam_chains", scene, 'cam_active_chain')
        
        col = row.column(align=True)
        col.operator("scene.cam_cutting_tool_add", icon='ADD', text="")
        if(len(scene.cam_cutting_tools) > 0):
            col.operator("scene.cam_cutting_tool_copy", icon='COPYDOWN', text="")
            col.operator("scene.cam_cutting_tool_remove", icon='REMOVE', text="")
            # if collection:
            col.separator()
            col.operator("scene.cam_cutting_tool_move", icon='TRIA_UP', text="").direction = 'UP'
            col.operator("scene.cam_cutting_tool_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
        # row = layout.row()

        if len(scene.cam_cutting_tools) > 0:
            #use_experimental = bpy.context.preferences.addons['cam'].preferences.experimental
            ao = scene.cam_cutting_tools[scene.cam_active_cutting_tool]
            
            col = layout.column()

            col.label(text="'" + ao.cutter_name + "' Properties")
            
            layout = col.box()
            row = layout.row(align=True)
            #row.menu("CAM_OPERATION_MT_presets", text=bpy.types.CAM_OPERATION_MT_presets.bl_label)
            #row.operator("render.cam_preset_operation_add", text="", icon='ADD')
            #row.operator("render.cam_preset_operation_add", text="", icon='REMOVE').remove_active = True
            row.menu("CAM_CUTTER_MT_presets", text=bpy.types.CAM_CUTTER_MT_presets.bl_label)
            row.operator("render.cam_preset_cutter_add", text="", icon='ADD')
            row.operator("render.cam_preset_cutter_add", text="", icon='REMOVE').remove_active = True
                

            if ao:
                #sub = layout.column()
                #layout.prop(ao, 'cutter_static_id')#Hidden! only here for debug
                layout.prop(ao, 'cutter_name')
                #sub.prop(ao, 'cutter_description')
                # cutter preset
                #row = layout.row(align=True)
                layout.prop(ao, 'cutter_id')
                row = layout.row(align=True)

                row.prop(ao, 'cutter_type')
                row.prop(ao, 'cutter_flutes')

                if ao.cutter_type == 'VCARVE':
                    layout.prop(ao, 'cutter_tip_angle')
                if ao.cutter_type == 'CUSTOM':
                    layout.prop_search(ao, "cutter_object_name", bpy.data, "objects")

                #layout.separator()
                column = layout.column()
                column.prop(ao, 'cutter_diameter')
                column.prop(ao,'cutter_total_length')
                column.prop(ao,'cutter_collet_tip_distance')

                #layout.prop(ao,'cutter_length')
                
                #layout.prop(ao, 'cutter_name')
                #layout.prop(ao, 'cutter_description')

                

class CAM_MATERIAL_Panel(CAMButtonsPanel, bpy.types.Panel):
    """CAM material panel"""
    bl_label = "Material Dimensions and Cutting Area"
    bl_idname = "WORLD_PT_CAM_MATERIAL"

    COMPAT_ENGINES = {'BLENDERCAM_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "WORLD_PT_CAM_OPERATIONS"

    def draw(self, context):
        layout = self.layout.box()
        scene = bpy.context.scene

        if len(scene.cam_operations) == 0:
            layout.label(text='Add operation first')
        if len(scene.cam_operations) > 0:
            ao = scene.cam_operations[scene.cam_active_operation]
            if ao:
                box = layout.box()
                # label(text='dir(layout))
                box.label(text="Position and Size")
                box.template_running_jobs()
                if ao.geometry_source in ['OBJECT', 'COLLECTION']:
                    #row = layout.row(align=True)
                    col = box.column()
                    row = col.row()
                    row.prop(ao, 'material_from_model')

                    if ao.material_from_model:
                        row.prop(ao, 'material_radius_around_model')
                    else:
                        col = box.column()
                        col.row().prop(ao, 'material_origin')
                        col.row().prop(ao, 'material_size')

                    box.operator("object.cam_position", text="Position object")
                else:
                    box.label(text='Estimated from image')


                box = layout.box()
                box.label(text="Cutting Region Bounds")

                col = box.column()
                #starting Z position
                #doMinZ = False
                  # experimental
                if ao.geometry_source in ['OBJECT', 'COLLECTION']:
                    col.prop(ao, 'minz_from_ob')
                    row = col.row()
                    row.prop(ao, 'maxz')
                    if not ao.minz_from_ob:
                        #ending z position
                        doMinZ = True
                        row.prop(ao, 'minz')
                else:
                    col.prop(ao, 'maxz')

                    col.prop(ao, 'source_image_scale_z')
                    col.prop(ao, 'source_image_size_x')
                    if ao.source_image_name != '':
                        i = bpy.data.images[ao.source_image_name]
                        if i is not None:
                            sy = int((ao.source_image_size_x / i.size[0]) * i.size[1] * 1000000) / 1000
                            col.label(text='image size on y axis: ' + strInUnits(sy, 8))
                            # label(text='dir(layout))
                            col.separator()
                    col.prop(ao, 'source_image_offset')
                    col = box.column(align=True)
                    # col.label(text='image crop:')
                    # col=layout.column()
                    col.prop(ao, 'source_image_crop', text='Crop source image')
                    if ao.source_image_crop:
                        col.prop(ao, 'source_image_crop_start_x', text='start x')
                        col.prop(ao, 'source_image_crop_start_y', text='start y')
                        col.prop(ao, 'source_image_crop_end_x', text='end x')
                        col.prop(ao, 'source_image_crop_end_y', text='end y')
                


                col = box.column()
                col.prop(ao, 'ambient_behaviour')
                if ao.ambient_behaviour == 'AROUND':
                    col.prop(ao, 'ambient_radius')
                col.prop(ao, "ambient_cutter_restrict")

                col.prop(ao, 'use_limit_curve')
                if ao.use_limit_curve:
                    col.prop_search(ao, "limit_curve", bpy.data, "objects")

                box = layout.box()
                box.label(text="Material to Leave")

                
                box.prop(ao, 'skin')

                if ao.strategy not in ['POCKET', 'DRILL', 'CURVE', 'MEDIAL_AXIS']:
                    box = box.box()
                    box.prop(ao, 'use_bridges')
                    
                    if ao.use_bridges:
                        # layout.prop(ao,'bridges_placement')
                        col = box.column()
                        row = col.row()
                        row.prop(ao, 'bridges_width')
                        row.prop(ao, 'bridges_height')

                        col.prop_search(ao, "bridges_collection_name", bpy.data, "collections")
                        col.prop(ao, 'use_bridge_modifiers')
                    # if ao.bridges_placement == 'AUTO':
                    #	layout.prop(ao,'bridges_per_curve')
                    #	layout.prop(ao,'bridges_max_distance')
                        box.operator("scene.cam_bridges_add", text="Autogenerate Tabs")



class CAM_OPERATION_PROPERTIES_Panel(CAMButtonsPanel, bpy.types.Panel):
    """CAM operation properties panel"""
    bl_label = "Operation Setup"
    bl_idname = "WORLD_PT_CAM_OPERATION"
    bl_parent_id = "WORLD_PT_CAM_OPERATIONS"

    COMPAT_ENGINES = {'BLENDERCAM_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout.box()
        scene = bpy.context.scene
        use_experimental = bpy.context.preferences.addons['cam'].preferences.experimental

        #row = layout.row()
        if len(scene.cam_operations) == 0:
            layout.label(text='Add operation first')
        else: #if len(scene.cam_operations) > 0:
            ao = scene.cam_operations[scene.cam_active_operation]

            layout.prop(ao, 'cutting_tool')
            
            grid = layout.box().column()
            if use_experimental:
                grid.prop(ao, 'machine_axes')
            
            if ao.machine_axes == '3':
                grid.prop(ao, 'strategy')
            elif ao.machine_axes == '4':
                grid.prop(ao, 'strategy4axis')
                if ao.strategy4axis == 'INDEXED':
                    grid.prop(ao, 'strategy')
                grid.prop(ao, 'rotary_axis_1')

            elif ao.machine_axes == '5':
                grid.prop(ao, 'strategy5axis')
                if ao.strategy5axis == 'INDEXED':
                    grid.prop(ao, 'strategy')
                grid.prop(ao, 'rotary_axis_1')
                grid.prop(ao, 'rotary_axis_2')

            if ao.strategy in ['BLOCK', 'SPIRAL', 'CIRCLES', 'OUTLINEFILL']:
                grid.prop(ao, 'movement_insideout')

            if ao.strategy == 'CUTOUT':
                grid.prop(ao, 'cut_type')
                grid.prop(ao, 'dont_merge')


            column = layout.box().column()
            column.prop(ao, 'geometry_source')
            if not ao.strategy == 'CURVE':
                if ao.geometry_source == 'OBJECT':
                    column.prop_search(ao, "object_name", bpy.data, "objects")
                elif ao.geometry_source == 'COLLECTION':
                    column.prop_search(ao, "collection_name", bpy.data, "collections")
                else:
                    column.prop_search(ao, "source_image_name", bpy.data, "images")
            else:
                if ao.geometry_source == 'OBJECT':
                    column.prop_search(ao, "object_name", bpy.data, "objects")
                elif ao.geometry_source == 'COLLECTION':
                    column.prop_search(ao, "collection_name", bpy.data, "collections")

            if ao.strategy in ['CARVE', 'PROJECTED_CURVE']:
                column.prop_search(ao, "curve_object", bpy.data, "objects")
                if ao.strategy == 'PROJECTED_CURVE':
                    layout.prop_search(ao, "curve_object1", bpy.data, "objects")

            if use_experimental and ao.geometry_source in ['OBJECT', 'COLLECTION']:
                column.prop(ao, 'use_modifiers')
            column.prop(ao, 'hide_all_others')
            column.prop(ao, 'parent_path_to_object')
            if(ao.strategy not in ['CUTOUT', 'CARVE', 'PENCIL', 'MEDIAL_AXIS', 'CRAZY', 'DRILL', 'POCKET']):
                column.prop(ao, 'inverse')

            
            # if gname in bpy.data.collections:
            #	layout.label(text='orientations')
            #	collection=bpy.data.collections[ao.name+'_orientations']
            #	layout.template_list("CAM_UL_orientations", '', collection, "objects", ao, 'active_orientation')
            #	layout.prop(collection.objects[ao.active_orientation],'location')
            #	layout.prop(collection.objects[ao.active_orientation],'rotation_euler')
            if ao.machine_axes == '3':
                box = layout.box()
                box.prop(ao, 'array')
                if ao.array:
                    col = box.column()
                    row = col.row(align=True)
                    row.prop(ao, 'array_x_count')
                    row.prop(ao, 'array_x_distance')
                    row = col.row(align=True)
                    row.prop(ao, 'array_y_count')
                    row.prop(ao, 'array_y_distance')


class CAM_MOVEMENT_Panel(CAMButtonsPanel, bpy.types.Panel):
    """CAM movement panel"""
    bl_label = "Movements and Feedrate"
    bl_idname = "WORLD_PT_CAM_MOVEMENT"

    COMPAT_ENGINES = {'BLENDERCAM_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "WORLD_PT_CAM_OPERATIONS"

    def draw(self, context):
        layout = self.layout.box()
        scene = bpy.context.scene
        use_experimental = bpy.context.preferences.addons['cam'].preferences.experimental

        #row = layout.row()
        if len(scene.cam_operations) == 0:
            layout.label(text='Add operation first')
        if len(scene.cam_operations) > 0:
            ao = scene.cam_operations[scene.cam_active_operation]
            if ao.valid:
                
                    # if ao.geometry_source=='OBJECT' or ao.geometry_source=='COLLECTION':

                    # o=bpy.data.objects[ao.object_name]
                    #
                    # if o.type=='MESH' and (ao.strategy=='DRILL'):
                    #     layout.label(text='Not supported for meshes')
                    #     return

                # elif o.type=='CURVE' and (ao.strategy!='CARVE' and ao.strategy!='POCKET' and ao.strategy!='DRILL' and ao.strategy!='CUTOUT'):
                #   layout.label(text='Not supported for curves')
                #   return
                #Speed-related stuff
                box = layout.box()
                box.label(text="Feedrate and RPM")
                row = box.row()
                row.prop(ao, 'spindle_rotation_direction')
                row.prop(ao, 'spindle_rpm')
                #feedrate
                col = box.column()
                col.prop(ao, 'feedrate')
                col.prop(ao, 'do_simulation_feedrate')
                row = box.row()
                row.prop(ao, 'plunge_feedrate')
                row.prop(ao, 'plunge_angle')
                
                box = layout.box()
                box.label(text="Tool Motion")

                col = box.column()
                if ao.strategy == 'CUTOUT':
                    #grid.prop(ao, 'cut_type')
                    # layout.prop(ao,'tool_stepover')
                    if use_experimental:
                        col.prop(ao, 'outlines_count')
                        if ao.outlines_count > 1:
                            col.prop(ao, 'tool_stepover')
                            col.prop(ao, 'movement_insideout')
                    
                elif ao.strategy == 'WATERLINE':
                    col.prop(ao, 'slice_detail')
                    col.prop(ao, 'waterline_fill')
                    if ao.waterline_fill:
                        col.prop(ao, 'tool_stepover')
                        col.prop(ao, 'waterline_project')
                    #col.prop(ao, 'inverse')
                elif ao.strategy == 'CARVE':
                    col.prop(ao, 'carve_depth')
                    col.prop(ao, 'dist_along_paths')
                elif ao.strategy == 'PENCIL':
                    col.prop(ao, 'dist_along_paths')
                    col.prop(ao, 'pencil_threshold')
                elif ao.strategy == 'MEDIAL_AXIS':
                    col.prop(ao, 'medial_axis_threshold')
                    col.prop(ao, 'medial_axis_subdivision')
                elif ao.strategy == 'CRAZY':
                    col.prop(ao, 'crazy_threshold1')
                    col.prop(ao, 'crazy_threshold5')
                    col.prop(ao, 'crazy_threshold2')
                    col.prop(ao, 'crazy_threshold3')
                    col.prop(ao, 'crazy_threshold4')
                    col.prop(ao, 'tool_stepover')
                    col.prop(ao, 'dist_along_paths')
                elif ao.strategy == 'DRILL':
                    col.prop(ao, 'drill_type')
                elif ao.strategy == 'POCKET':
                    col.prop(ao, 'pocket_option')
                    col.prop(ao, 'tool_stepover')
                else:
                    col.prop(ao, 'tool_stepover')
                    col.prop(ao, 'dist_along_paths')
                    if ao.strategy == 'PARALLEL' or ao.strategy == 'CROSS':
                        col.prop(ao, 'parallel_angle')

               
                #material cutting related properties (e.g, excess left, extra, whatever)
                row = col.row()
                row.prop(ao, 'use_layers')
                if ao.use_layers:
                    row.prop(ao, 'stepdown')
                
                col = box.column()
                
                col.prop(ao, 'movement_type')

                if ao.movement_type in ['BLOCK', 'SPIRAL', 'CIRCLES']:
                    col.prop(ao, 'movement_insideout')

                
                
                if ao.strategy == 'CUTOUT' or (
                        use_experimental and (ao.strategy == 'POCKET' or ao.strategy == 'MEDIAL_AXIS')):
                    col.prop(ao, 'first_down')
                # if ao.first_down:

                if ao.strategy == 'POCKET':
                    col.prop(ao, 'helix_enter')
                    if ao.helix_enter:
                        col.prop(ao, 'ramp_in_angle')
                        col.prop(ao, 'helix_diameter')
                    col.prop(ao, 'retract_tangential')
                    if ao.retract_tangential:
                        col.prop(ao, 'retract_radius')
                        col.prop(ao, 'retract_height')
                col = box.column()
                row = col.row()
                row.prop(ao, 'ramp')
                if ao.ramp:
                    row.prop(ao, 'ramp_in_angle')
                    row = col.row()
                    row.prop(ao, 'ramp_out')
                    if ao.ramp_out:
                        row.prop(ao, 'ramp_out_angle')

                #area
                # o=bpy.data.objects[ao.object_name]
                if ao.strategy == 'PARALLEL' or ao.strategy == 'CROSS':
                    if not ao.ramp:
                        box.prop(ao, 'parallel_step_back')
                
                
                row = box.row()
                row.prop(ao, 'stay_low')
                if ao.stay_low:
                    row.prop(ao, 'merge_dist')
                
                
                
                box = layout.box()
                box.label(text="Motion Safety")
                col = box.column()
                col.prop(ao, 'free_movement_height')
                row = col.row()
                row.prop(ao, 'protect_vertical')
                if ao.protect_vertical:
                    row.prop(ao, 'protect_vertical_limit')

                
                

               
                

                


class CAM_OPTIMISATION_Panel(CAMButtonsPanel, bpy.types.Panel):
    """CAM optimisation panel"""
    bl_label = "CAM Optimisation"
    bl_idname = "WORLD_PT_CAM_OPTIMISATION"
    bl_parent_id = "WORLD_PT_CAM_OPERATIONS"

    COMPAT_ENGINES = {'BLENDERCAM_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout.box()
        scene = bpy.context.scene

        #row = layout.row()
        if len(scene.cam_operations) == 0:
            layout.label(text='Add operation first')
        if len(scene.cam_operations) > 0:
            ao = scene.cam_operations[scene.cam_active_operation]
            if ao.valid:
                col = layout.column()
                col.prop(ao, 'optimize')
                if ao.optimize:
                    col.prop(ao, 'optimize_threshold')
                if ao.geometry_source == 'OBJECT' or ao.geometry_source == 'COLLECTION':
                    #if(o.strategy == 'WATERLINE' or o.strategy == 'POCKET' or o.inverse):
                    exclude_exact = (ao.strategy in [ 'POCKET', 'CUTOUT', 'DRILL', 'PENCIL', 'WATERLINE']) or ao.inverse
                    if not exclude_exact:
                        row = layout.row()
                        row.prop(ao, 'use_exact')
                        if ao.use_exact:
                            row.prop(ao, 'exact_subdivide_edges')
                    if exclude_exact or not ao.use_exact:
                        col = layout.column()
                        col.prop(ao, 'pixsize')
                        col.prop(ao, 'imgres_limit')

                        sx = ao.max.x - ao.min.x
                        sy = ao.max.y - ao.min.y
                        resx = int(sx / ao.pixsize)
                        resy = int(sy / ao.pixsize)
                        l = 'resolution: ' + str(resx) + ' x ' + str(resy)
                        col.label(text=l)

                layout.prop(ao, 'simulation_detail')
                layout.prop(ao, 'circle_detail')
                layout.prop(ao, 'use_opencamlib')


class CAM_GCODE_Panel(CAMButtonsPanel, bpy.types.Panel):
    """CAM operation g-code options panel"""
    bl_label = "Extra G-code Options "
    bl_idname = "WORLD_PT_CAM_GCODE"

    COMPAT_ENGINES = {'BLENDERCAM_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "WORLD_PT_CAM_OPERATIONS"

    def draw(self, context):
        layout = self.layout.box()
        scene = bpy.context.scene
        
        if len(scene.cam_operations) == 0:
            layout.label(text='Add operation first')
        if len(scene.cam_operations) > 0:
            use_experimental = bpy.context.preferences.addons['cam'].preferences.experimental
            if use_experimental:
                ao = scene.cam_operations[scene.cam_active_operation]
                if ao.valid:
                    box = layout.box()
                    box.prop(ao, 'output_header')
                    if ao.output_header:
                        box.prop(ao, 'gcode_header')
                    box = layout.box()
                    box.prop(ao, 'output_trailer')
                    if ao.output_trailer:
                        box.prop(ao, 'gcode_trailer')
            else:
                col = layout.column()
                col.label(text='Enable Show experimental features')
                col.label(text='in Blender CAM Addon preferences')


class CAM_EXTRAS_Panel(CAMButtonsPanel, bpy.types.Panel):
    """CAM Bonus panel"""
    bl_label = "Extra Features"
    bl_idname = "WORLD_PT_CAM_EXTRAS"

    COMPAT_ENGINES = {'BLENDERCAM_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        pass


class CAM_PACK_Panel(CAMButtonsPanel, bpy.types.Panel):
    """CAM material panel"""
    bl_label = "Pack curves on sheet"
    bl_idname = "WORLD_PT_CAM_PACK"

    COMPAT_ENGINES = {'BLENDERCAM_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "WORLD_PT_CAM_EXTRAS"

    def draw(self, context):
        layout = self.layout.box()
        scene = bpy.context.scene
        settings = scene.cam_pack
        layout.label(text='warning - algorithm is slow.')
        layout.label(text='only for curves now.')

        layout.operator("object.cam_pack_objects")
        layout.prop(settings, 'sheet_fill_direction')
        layout.prop(settings, 'sheet_x')
        layout.prop(settings, 'sheet_y')
        layout.prop(settings, 'distance')
        layout.prop(settings, 'rotate')


class CAM_SLICE_Panel(CAMButtonsPanel, bpy.types.Panel):
    """CAM slicer panel"""
    bl_label = "Slice model to plywood sheets"
    #bl_label = "Extra Features"
    bl_idname = "WORLD_PT_CAM_SLICE"
    bl_parent_id = "WORLD_PT_CAM_EXTRAS"

    COMPAT_ENGINES = {'BLENDERCAM_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout #.box()
        scene = bpy.context.scene
        settings = scene.cam_slice
        box = layout.box()
        box.operator("object.cam_slice_objects")
        box.prop(settings, 'slice_distance')
        box.prop(settings, 'indexes')


# panel containing all tools
class VIEW3D_PT_tools_curvetools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_label = "Curve CAM Tools"

    # bl_category = "Blender CAM"
    # bl_options = {'DEFAULT_CLOSED'}
    

    def draw(self, context):
        layout = self.layout
        # col = layout.column(align=True)
        # lt = context.window_manager.looptools
        layout.operator("object.curve_boolean")
        layout.operator("object.curve_intarsion")
        layout.operator("object.curve_overcuts")
        layout.operator("object.curve_overcuts_b")
        layout.operator("object.silhouete")
        layout.operator("object.silhouete_offset")
        layout.operator("object.curve_remove_doubles")
        layout.operator("object.mesh_get_pockets")
