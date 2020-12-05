from . import nc
from . import iso
import math
import datetime
import time
import traceback

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
		self.first_tool = True
		self.free_movement_height = 200

	def PROGRAM_END(self):	return('M5')
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
	def DWELL(self, dwell): return('G4' + self.SPACE() + self.TIME() + (self.FORMAT_TIME().string(dwell)))
	
	
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
			
			# self.comment('Tool change to \'' + self.tool_defn_params[id]['name'] + '\' (' + self.tool_defn_params[id]['description'] + ')  - D = %s type %s flutes %s' % (strInUnits(o.cutter_diameter, 4), o.cutter_type, o.cutter_flutes));
		
		if self.first_tool: 
			self.first_tool = False
			if self.output_comment_before_tool_change:
				self.comment('Not changing tool since this is the first one')
		else: 
			if self.output_comment_before_tool_change:
				self.comment('Automagic tool change thing made for Marlin - DOES NOT CURRENTLY COMPENSATE FOR TOOL HEIGHT DIFFERENCES!')
			#self.write(self.SPACE() + self.FEED() + self.SPACE_STR() + self.Z() + ('%.2f' % (self.free_movement_height)) + '; \'feed\' to safe Z (keeps things slower and safer than a quick move) z is currently 10cm until I work out the safe position');
			#Should add max new tool height to allow removal?
			add_to_shift_z = 0
			arbitrary_shank_length = 30
			resting_z = self.free_movement_height + arbitrary_shank_length
			
			#print(self.tool_defn_params[self.t]);
			if(id != None and id in self.tool_defn_params):
				if(self.t != None and self.t in self.tool_defn_params):
					#print(self.tool_defn_params[id]);
					# This will actually only make a difference if we can specify tool lengths. 
					#print(self.shift_z);
					self.shift_z += 1000 * (self.tool_defn_params[id]['cutting edge height'] - self.tool_defn_params[self.t]['cutting edge height'])
					#print(self.shift_z);
					resting_z += 1000 * max(self.tool_defn_params[id]['cutting edge height'], self.tool_defn_params[self.t]['cutting edge height'])
				else: 
					resting_z += 1000 * self.tool_defn_params[id]['cutting edge height']
					
			
			
			self.feed(x=None, y=None, z=self.free_movement_height)
			self.write(self.SPACE() + 'M5 ;stop the spindle\n');
			self.write(self.SPACE() + 'G4 S2 ;dwell for 2 second to give some spin-down time\n');
			self.rapid(x=0, y=0, z=resting_z)
			self.write(self.SPACE() + 'M1 Change Tool + Click... ;Await user confirmation\n');
			self.write(self.SPACE() + 'G4 S1 ;dwell for 1 second to give some user escape time\n');
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
			self.write_blocknum()
			self.write( (self.WORKPLANE() % (id + self.WORKPLANE_BASE())) + '\t; (Select Relative Coordinate System)\n')
		if ((id >= 7) and (id <= 9)):
			self.write_blocknum()
			self.write( ((self.WORKPLANE() % (6 + self.WORKPLANE_BASE())) + ('.%i' % (id - 6))) + '\t; (Select Relative Coordinate System)\n')


nc.creator = Creator()
