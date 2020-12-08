from . import nc
from . import iso
import math
import datetime
import time
import traceback

import bpy

now = datetime.datetime.now()

#Gcode post-processor for Marlin Compatibility

class Creator(iso.Creator):
	def __init__(self):
		iso.Creator.__init__(self)
		self.absolute_flag = True
		self.prev_g91 = ''
		self.useCrc = False
		self.start_of_line = True
		self.output_block_numbers = False
		self.output_tool_definitions = False
		self.g0123_modal = False
		self.m_codes_on_their_own_line = True
		self.output_tool_change = True
		self.output_comment_before_tool_change = True
		#Used to disable unnecessary output of a toolchange for the first tool
		self.first_tool = True
		self.free_movement_height = 200
		self.current_tool_definition = None
		#self.last_move_was_rapid = False

	def PROGRAM_END(self):	
		#G0 Z' + str(self.free_movement_height) + '\nM5\nG4 S2\nM211 S0\nG0 X0 Y0
		#self.feed(z=self.free_movement_height)
		
		return('M5')
	#optimize
	
	def SPACE_STR(self): return(' ')
	def COMMENT(self,comment): return( ('; %s' % comment ) )
	
	def SPINDLE_CW(self): 
		#traceback.print_stack()
		return('M3')
	def SPINDLE_CCW(self): return('M4')
	def COOLANT_OFF(self): return('M9')
	def COOLANT_MIST(self): return('M7')
	def COOLANT_FLOOD(self): return('M8')


	def RAPID(self): return('G0')
	def FEED(self): return('G1')
	def ARC_CW(self): return('G2')
	def ARC_CCW(self): return('G3')
	def DWELL(self, dwell): return('G4' + self.SPACE() + self.TIME() + (self.FORMAT_TIME().string(int(dwell * 1000))))
	
	
	def STOP_OPTIONAL(self): return('M1')
	def STOP(self): return('M0')
	
	def TOOL(self): return ' '
	
	#def TOOL(self): return('T%i' + self.SPACE() + 'M06')
	
	
	
	
	#self.z_for_g43 = None
	
############################################################################
## Begin Program


	def program_begin(self, id, comment):
		if (self.useCrc == False):
			self.write( ('; (Created with Marlin post processor ' + str(now.strftime("%Y/%m/%d %H:%M")) + ')' + '\n') )
		else:
			self.write( ('; (Created with Marlin Cutter Radius Compensation post processor ' + str(now.strftime("%Y/%m/%d %H:%M")) + ')' + '\n') )
		self.first_tool = True

		self.comment('Disabling soft endstops to allow -Z! Please be super careful!')
		#self.write("M211 S0\nM121\n")
		self.write("M211 S0\n")
		self.write("G92 X0 Y0 Z0 ; Set the current position to 0, or the work origin. Will be an option Soon!\n")
		


	def program_end(self):
		self.feed(z=self.free_movement_height)

		if self.z_for_g53 != None:
			self.write(self.SPACE() + self.MACHINE_COORDINATES() + self.SPACE() + 'Z' + self.fmt.string(self.z_for_g53) + '\n')
		self.write(self.SPACE() + self.PROGRAM_END() + '\n')

		self.write(self.SPACE() + self.DWELL(bpy.context.scene.cam_machine.spindle_start_time) + '\n')
		self.write(self.SPACE() + 'M211 S1' + '\n')
		self.rapid(x=0, y=0)
		self.write(self.SPACE() + 'M177 Job Complete' + '\n')

		if self.temp_file_to_append_on_close != None:
			f_in = open(self.temp_file_to_append_on_close, 'r')
			while (True):
				line = f_in.readline()
				if (len(line) == 0) : break
				self.write(line)
			f_in.close()

		self.file_close()

		if self.output_block_numbers:
			# number every line of the file afterwards
			self.number_file(self.filename)

			for f in self.subroutine_files:
				self.number_file(f)

		
	def rapid(self, x=None, y=None, z=None, a=None, b=None, c=None ):
		#self.last_move_was_rapid = True
		if self.same_xyz(x, y, z, a, b, c): return
		#if(x is None and y is None and z is None and a is None and b is None and c is None): return
		if(self.f.str and self.f.str != self.f.previous):
			#print("wuhuh")
			#print(self.f.str)
			self.write(self.SPACE() + self.RAPID())
			
			self.write_feedrate()
			self.write('\n')
		
		self.on_move()

		if self.g0123_modal:
			if self.prev_g0123 != self.RAPID():
				self.write(self.SPACE() + self.RAPID())
				self.prev_g0123 = self.RAPID()
		else:
			self.write(self.SPACE() + self.RAPID())
		self.write_preps()
		if (x != None):
			if (self.absolute_flag ):
				self.write(self.SPACE() + self.X() + (self.fmt.string(x + self.shift_x)))
			else:
				dx = x - self.x
				self.write(self.SPACE() + self.X() + (self.fmt.string(dx)))
			self.x = x
		if (y != None):
			if (self.absolute_flag ):
				self.write(self.SPACE() + self.Y() + (self.fmt.string(y + self.shift_y)))
			else:
				dy = y - self.y
				self.write(self.SPACE() + self.Y() + (self.fmt.string(dy)))

			self.y = y
		if (z != None):
			if (self.absolute_flag ):
				self.write(self.SPACE() + self.Z() + (self.fmt.string(z + self.shift_z)))
			else:
				dz = z - self.z
				self.write(self.SPACE() + self.Z() + (self.fmt.string(dz)))

			self.z = z

		if (a != None):
			if (self.absolute_flag ):
				self.write(self.SPACE() + self.A() + (self.fmt.string(a)))
			else:
				da = a - self.a
				self.write(self.SPACE() + self.A() + (self.fmt.string(da)))
			self.a = a

		if (b != None):
			if (self.absolute_flag ):
				self.write(self.SPACE() + self.B() + (self.fmt.string(b)))
			else:
				db = b - self.b
				self.write(self.SPACE() + self.B() + (self.fmt.string(db)))
			self.b = b

		if (c != None):
			if (self.absolute_flag ):
				self.write(self.SPACE() + self.C() + (self.fmt.string(c)))
			else:
				dc = c - self.c
				self.write(self.SPACE() + self.C() + (self.fmt.string(dc)))
			self.c = c
		
		
		self.write_spindle()
		self.write_misc()
		self.write('\n')
	# def rapid(self, x=None, y=None, z=None, a=None, b=None, c=None ):
	#  	self.write("penis\n")
	#  	iso.Creator.rapid(self, x=None, y=None, z=None, a=None, b=None, c=None)
	def feed(self, x=None, y=None, z=None, a=None, b=None, c=None):
		if self.same_xyz(x, y, z, a, b, c): return

		if(self.f.str and self.f.str != self.f.previous):
			#print("wuhuh")
			#print(self.f.str)
			self.write(self.SPACE() + self.FEED())
			
			self.write_feedrate()
			self.write('\n')

		self.on_move()
		if self.g0123_modal:
			if self.prev_g0123 != self.FEED():
				self.writem([self.SPACE() , self.FEED()])
				self.prev_g0123 = self.FEED()
		else:
			self.write(self.SPACE() + self.FEED())
		self.write_preps()
		dx = dy = dz = 0
		if (x != None):
			dx = x - self.x
			if (self.absolute_flag ):
				self.writem([self.SPACE() , self.X() , (self.fmt.string(x + self.shift_x))])
			else:
				self.writem([self.SPACE() , self.X() , (self.fmt.string(dx))])
			self.x = x
		if (y != None):
			dy = y - self.y
			if (self.absolute_flag ):
				self.writem([self.SPACE() , self.Y() , (self.fmt.string(y + self.shift_y))])
			else:
				self.writem([self.SPACE() , self.Y() , (self.fmt.string(dy))])

			self.y = y
		if (z != None):
			dz = z - self.z
			if (self.absolute_flag ):
				self.writem([self.SPACE() , self.Z() , (self.fmt.string(z + self.shift_z))])
			else:
				self.writem([self.SPACE() , self.Z() , (self.fmt.string(dz))])

			self.z = z

		if (a != None):
			da = a - self.a
			if (self.absolute_flag ):
				self.writem([self.SPACE() , self.A() , (self.fmt.string(a))])
			else:
				self.writem([self.SPACE() , self.A() , (self.fmt.string(da))])
			self.a = a

		if (b != None):
			db = b - self.b
			if (self.absolute_flag ):
				self.writem([self.SPACE() , self.B() , (self.fmt.string(b))])
			else:
				self.writem([self.SPACE() , self.B() , (self.fmt.string(db))])
			self.b = b

		if (c != None):
			dc = c - self.c
			if (self.absolute_flag ):
				self.writem([self.SPACE() , self.C() , (self.fmt.string(c))])
			else:
				self.writem([self.SPACE() , self.C() , (self.fmt.string(dc))])
			self.c = c

		if (self.fhv) : self.calc_feedrate_hv(math.sqrt(dx*dx+dy*dy), math.fabs(dz))
		self.write_feedrate()
		self.write_spindle()
		self.write_misc()
		self.write('\n')

############################################################################
##  Settings

	#def tool_defn(self, id, name='', params=None):
	#	pass

	#def tool_change(self, id):
	#	pass
	
	# since marlin does not support G43, we need a work around: 
	# Move the toolhead to a safe z position
	# stop the spindle
	# give it some slowdown time
	# pause the "print" - Show a message for which tool
	# ideally some kind of height adjust to keep the tool in the right place
	# After pause is "complete"
	# Start the spindle
	# Resume "printing"
	
	#I believe spindle spin and resume are handled by the gcode exporter anyway (well, Marlin resumes and spindle speed and direction is auto reset anyway
	
	def tool_change(self, id):
		#if id in self.tool_defn_params and self.output_comment_before_tool_change:
		
		
		if self.first_tool:
			self.first_tool = False
			
			if self.output_comment_before_tool_change:
				self.comment('Not changing tool since this is the first one')
			#self.feedrate()
			self.rapid(z=self.free_movement_height)
		else: 
			if self.output_comment_before_tool_change:
				self.comment('Automagic tool change thing made for Marlin!')
			#self.write(self.SPACE() + self.FEED() + self.SPACE_STR() + self.Z() + ('%.2f' % (self.free_movement_height)) + '; \'feed\' to safe Z (keeps things slower and safer than a quick move) z is currently 10cm until I work out the safe position');
			#Should add max new tool height to allow removal?
			add_to_shift_z = 0
			#arbitrary_shank_length = 30
			resting_z = self.free_movement_height# + arbitrary_shank_length
			
			#print(self.tool_defn_params[self.t]);
			if(id != None and id in self.tool_defn_params):
				if(self.t != None and self.t in self.tool_defn_params):
					#print(self.tool_defn_params[id]);
					# This will actually only make a difference if we can specify tool lengths. 
					#print(self.shift_z);
					add_to_shift_z += 1000 * (self.tool_defn_params[id]['collet_tip_distance'] - self.tool_defn_params[self.t]['collet_tip_distance'])
					#print(self.shift_z);
					resting_z += 1000 * max(self.tool_defn_params[id]['total_length'] - self.tool_defn_params[id]['collet_tip_distance'], self.tool_defn_params[self.t]['total_length'] - self.tool_defn_params[self.t]['collet_tip_distance'])
				else:
					resting_z += 1000 * (self.tool_defn_params[id]['total_length'] - self.tool_defn_params[id]['collet_tip_distance'])
					
			
			
			self.feed(x=None, y=None, z=self.free_movement_height)
			self.write(self.SPACE() + 'M5 ;stop the spindle\n')
			self.write(self.SPACE() + self.DWELL(bpy.context.scene.cam_machine.spindle_start_time) + ' ;dwell for 2 second to give some spin-down time\n')
			self.rapid(x=0, y=0, z=resting_z)
			self.write(self.SPACE() + 'M1 Change Tool + Click... ;Await user confirmation\n')
			self.write(self.SPACE() + self.DWELL(1) + ' ;dwell for 1 second to give some user escape time\n')
			self.rapid(x=None, y=None, z=self.free_movement_height)
			#Shorter tools make part go lower. Shift_z is additive. eg, new tool is shorter, shift_z must be negative small - big = negative
			#self.shift_z += ([new tool height] - [old tool height])
			
			
			self.shift_z += add_to_shift_z
				
			
			
		#Use shift_z to update offsets? 
		
		#print((self.tool_defn_params));
		
		#Output comment is made redundant by utils.py? It outputs the same thing anyway
		# if self.output_comment_before_tool_change:
			# if id in self.tool_defn_params:
				# self.comment('tool change to ' + self.tool_defn_params[id]['name']);

		# if self.output_cutviewer_comments:
			# import cutviewer
			# if id in self.tool_defn_params:
				# cutviewer.tool_defn(self, id, self.tool_defn_params[id])
		# if (self.t != None) and (self.z_for_g53 != None):
			# self.write('G53 Z' + str(self.z_for_g53) + '\n')
		# self.write(self.SPACE() + (self.TOOL() % id))
		# if self.output_g43_on_tool_change_line == True:
			# self.write(self.SPACE() + 'G43')
		# self.write('\n')
		# if self.output_h_and_d_at_tool_change == True:
			# if self.output_g43_on_tool_change_line == False:
				# self.write(self.SPACE() + 'G43')
			# self.write(self.SPACE() + 'D' + str(id) + self.SPACE() + 'H' + str(id) + '\n')
		
		self.t = id
		self.move_done_since_tool_change = False
	
	
	
	def tool_defn(self, id, name='',params=None):
		self.tool_defn_params[id] = params
		# if self.output_tool_definitions:
			# self.write(self.SPACE() + self.TOOL_DEFINITION())
			# self.write(self.SPACE() + ('P%i' % id) + ' ')

			# if (params['diameter'] != None):
				# self.write(self.SPACE() + ('R%.3f' % (float(params['diameter'])/2)))

			# if (params['cutting edge height'] != None):
				# self.write(self.SPACE() + 'Z%.3f' % float(params['cutting edge height']))

			# self.write('\n')
			
	# def spindle(self, s, clockwise):
		# if clockwise == True:
			# self.s.set(s, '', '')
		# else:
			# self.s.set(s, '', '')
	
	def write_spindle(self):
		if self.s.str2 != None:
		#if self.s.str:
		#	self.write('\n' if self.m_codes_on_their_own_line else '')
			self.write(self.s.str2 + self.SPACE_STR() + self.s.str + '\n')
			self.s.str2 = None

# This is the coordinate system we're using.  G54->G59, G59.1, G59.2, G59.3
# These are selected by values from 1 to 9 inclusive.
	def workplane(self, id):
		if ((id >= 1) and (id <= 6)):
			#I haven't seen blocknum defined anywhere in the Creator stuff? Also VS Code is upset it is not defined 
			#self.write_blocknum()
			self.write( (self.WORKPLANE() % (id + self.WORKPLANE_BASE())) + '\t; (Select Relative Coordinate System)\n')
		if ((id >= 7) and (id <= 9)):
			#self.write_blocknum()
			self.write( ((self.WORKPLANE() % (6 + self.WORKPLANE_BASE())) + ('.%i' % (id - 6))) + '\t; (Select Relative Coordinate System)\n')


nc.creator = Creator()
