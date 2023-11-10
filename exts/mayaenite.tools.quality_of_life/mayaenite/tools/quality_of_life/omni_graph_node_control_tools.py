
from typing import List
import omni.ui as ui
import omni.kit.widget.graph
import omni.kit.widget.graph.isolation_graph_model
import omni.kit.hotkeys.core
import omni.graph.core as og
import omni.kit.commands
from pxr import Sdf, Gf
from . import utils
################################################################################
class HORIZONTAL_ANCHOR_POINT:
	LEFT   = "L"
	RIGHT  = "R"
	MIDDLE = "M"
	
################################################################################
class VERTICAL_ANCHOR_POINT:
	TOP    = "T"
	BOTTOM = "B"
	MIDDLE = "M"
	
################################################################################
class ALIGNMENTS:
	VERTICAL   = "V"
	HORIZONTAL = "H"
	
################################################################################
class EXPANSION_STATE:
	CLOSED    = "closed"
	MINIMIZED = "minimized"
	OPEN      = "open"
	TOGGLE    = "toggle"

#-------------------------------------------------------------------------------	
def get_Graph_View_With_Current_Focus() -> omni.kit.widget.graph.GraphView:
	""""""
	for name in ['Generic Graph', 'Action Graph', 'Material Graph', 'Particles Editor']:
		window = utils.get_Window(name)
		if window:
			if window.visible:
				if window.focused:
					try:
						return window._main_widget._graph_view
					except:
						pass

#-------------------------------------------------------------------------------
def get_Selected_Nodes_For_Focused_Graph_View() -> List[omni.kit.widget.graph.isolation_graph_model.IsolationGraphModel._IsolationItemProxy]:
	""""""
	gv = get_Graph_View_With_Current_Focus()
	if gv:
		return [gv._model[node] for node in  gv.selection]
	else:
		return []
		
		


################################################################################
class _Graph_Node_Set_Command:
	""""""
	#-------------------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		self._command_name = 'UsdUINodeGraphNodeSetCommand'
		self.attribute    =  None
		self.value        =  None
		self.prim_path     =  None
		self.prev          =  None
	#-------------------------------------------------------------------------------
	def execute(self):	
		omni.kit.commands.execute(self._command_name,
								  attribute=self.attribute,
								  prim_path=self.prim_path,
								  value=self.value,
								  prev=self.prev
								  )

################################################################################
class Set_Node_ExpansionState_Command(_Graph_Node_Set_Command):
	""""""
	#-------------------------------------------------------------------------------
	def __init__(self, prim, value):
		"""Constructor"""
		super(Set_Node_ExpansionState_Command, self).__init__()
		self.attribute  =  'ui:nodegraph:node:expansionState'
		self.value      =  value
		self.prim_path  =  prim.GetPath()
		self.prev       =  prim.GetAttribute(self.attribute).Get()
		
	

################################################################################
class Set_Node_Position_Command(_Graph_Node_Set_Command):
	""""""
	#-------------------------------------------------------------------------------
	def __init__(self, node_prim,  node_proxy : omni.kit.widget.graph.isolation_graph_model.IsolationGraphModel._IsolationItemProxy, newpos):
		"""Constructor"""
		super(Set_Node_Position_Command, self).__init__()
		self.attribute     =  'ui:nodegraph:node:pos'
		self.prim_path     =  node_prim.GetPath()
		self.value         =  (newpos[0], newpos[1])
		self.prev          =  Gf.Vec2f(node_proxy.position[0], node_proxy.position[1])
	

################################################################################
class _Node_Graph_View_Data:
	""""""
	#-------------------------------------------------------------------------------
	def __init__(self):
		""""""
		self._nodes = get_Selected_Nodes_For_Focused_Graph_View()
		self._graph_view =  get_Graph_View_With_Current_Focus()
		
################################################################################
class _Node_Locations(_Node_Graph_View_Data):
	""""""		
	#-------------------------------------------------------------------------------
	def get_node_and_pos_lists(self):
		""""""
		return [[n, n.position] for n in self._nodes]
	#-------------------------------------------------------------------------------
	def get_right_most_node(self):
		""""""
		nodes = self._nodes[::]
		winner =  nodes.pop(0)
		for node in nodes:
			if node.position[0] > winner.position[0]:
				winner = node
		return winner
	#-------------------------------------------------------------------------------
	def get_left_most_node(self):
		nodes = self._nodes[::]
		winner =  nodes.pop(0)
		for node in nodes:
			if node.position[0] < winner.position[0]:
				winner = node
		return winner
	#-------------------------------------------------------------------------------
	def get_bottom_most_node(self):
		nodes = self._nodes[::]
		winner =  nodes.pop(0)
		for node in nodes:
			if node.position[1] > winner.position[1]:
				winner = node
		return winner
	#-------------------------------------------------------------------------------
	def get_top_most_node(self):
		nodes = self._nodes[::]
		winner =  nodes.pop(0)
		for node in nodes:
			if node.position[1] < winner.position[1]:
				winner = node
		return winner
	#-------------------------------------------------------------------------------
	def get_top_left_point(self):
		y = self.get_top_most_node().position[1]
		x = self.get_left_most_node().position[0]
		return (x,y)
	#-------------------------------------------------------------------------------
	def get_top_right_point(self):
		y = self.get_top_most_node().preview
		x = right_most_node(listOfNodes).xpos()
		return (x,y)
	#-------------------------------------------------------------------------------
	def get_bottom_left_point(self):
		y = self.get_bottom_most_node().position[1]
		x = self.get_left_most_node().position[0]
		return (x,y)
	#-------------------------------------------------------------------------------
	def bottom_right_point(self):
		y = self.get_bottom_most_node().position[1]
		x = self.get_right_most_node().position[0]
		return (x,y)
	#-------------------------------------------------------------------------------
	def get_center_point(self):
		nNodes = len(self._nodes)
		x=0 
		y=0
		for node in self._nodes:
			x += node.position[0]
		for node in self._nodes:
			y += node.position[1]
		try:
			return [x/nNodes,y/nNodes]
		except ZeroDivisionError:
			return [0,0]
	#-------------------------------------------------------------------------------
	def reorder_From_left_to_right(self):
		reorderList = []
		while len(self._nodes):
			node =  self.get_left_most_node()
			reorderList.append(node)
			self._nodes.remove(node)
		self._nodes = reorderList
	#-------------------------------------------------------------------------------
	def reorder_from_top_to_bottom(self):
		reorderList = []
		while len(self._nodes):
			node =  self.get_top_most_node()
			reorderList.append(node)
			self._nodes.remove(node)
		self._nodes = reorderList


################################################################################
class Node_Alignment_Tool(_Node_Locations):
	""""""

	def __init__(self,h_anchor_type=HORIZONTAL_ANCHOR_POINT.LEFT, v_anchor_type=VERTICAL_ANCHOR_POINT.TOP, alignment=ALIGNMENTS.VERTICAL):
		"""Constructor"""
		
		super(Node_Alignment_Tool, self).__init__()
		
		self.h_anchor_type =  h_anchor_type
		self.v_anchor_type =  v_anchor_type
		self.h_anchor_pos =  0
		self.v_anchor_pos =  0
		self.anchor_position =  []
		self.alignment    =  alignment
		
	#-------------------------------------------------------------------------------
	def apply_Tool(self):
		""""""
		#-------------------------------------------------------------------------------
		def apply_anchors():
			if self.h_anchor_type ==  HORIZONTAL_ANCHOR_POINT.LEFT:
				self.h_anchor_pos =  self.get_left_most_node().position[0]
			elif self.h_anchor_type ==  HORIZONTAL_ANCHOR_POINT.RIGHT:
				self.h_anchor_pos =  self.get_right_most_node().position[0]
			elif self.h_anchor_type ==  HORIZONTAL_ANCHOR_POINT.MIDDLE:
				self.h_anchor_pos =  self.get_center_point()[0]
			else:
				raise ValueError(f"Invalid Input {self.h_anchor_type} for HORIZONTAL ANCHOR POINT ")
			
			if self.v_anchor_type ==  VERTICAL_ANCHOR_POINT.TOP:
				self.v_anchor_pos =  self.get_top_most_node().position[1]
			elif self.v_anchor_type ==  VERTICAL_ANCHOR_POINT.BOTTOM:
				self.v_anchor_pos =  self.get_bottom_most_node().position[1]
			elif self.v_anchor_type ==  VERTICAL_ANCHOR_POINT.MIDDLE:
				self.v_anchor_pos =  self.get_center_point()[1]		
			else:
				raise ValueError(f"Invalid Input {self.v_anchor_type} for VERTICAL ANCHOR POINT ")

		#-------------------------------------------------------------------------------
		def build_new_pos(item):
			if self.alignment ==  ALIGNMENTS.VERTICAL:
				return self.h_anchor_pos, item.position[1]
			elif self.alignment ==  ALIGNMENTS.HORIZONTAL:
				return item.position[0], self.v_anchor_pos
			else:
				raise ValueError(f"Invalid Input {self.alignment} for ALIGNMENT")
		
		apply_anchors()
		
		commands =  []
		
		for prim, proxy in  zip(self._graph_view.model.selection, self._nodes):
			newpos =  build_new_pos(proxy)	
			commands.append(Set_Node_Position_Command(prim, proxy, newpos))
		
		with omni.kit.undo.group():	
			[cmd.execute() for cmd in commands]

################################################################################
class Node_Expansion_State_Tool(_Node_Graph_View_Data):
	""""""

	def __init__(self,value=EXPANSION_STATE.MINIMIZED):
		"""Constructor"""
		
		super(Node_Expansion_State_Tool, self).__init__()
		self.new_value = value
		
	#-------------------------------------------------------------------------------
	def apply_Tool(self):
		""""""
		commands =  []
		
		for prim in self._graph_view.model.selection:
			cmd =  Set_Node_ExpansionState_Command(prim, self.new_value)
			if self.new_value ==  EXPANSION_STATE.TOGGLE:
				if prim.GetAttribute(cmd.attribute).Get() in [EXPANSION_STATE.MINIMIZED, EXPANSION_STATE.OPEN]:
					cmd.value =  EXPANSION_STATE.CLOSED
				else:
					cmd.value =  EXPANSION_STATE.OPEN
			commands.append(cmd)
		
		with omni.kit.undo.group():
			[cmd.execute() for cmd in commands]
			
#-------------------------------------------------------------------------------
def _node_Alignment_Tool_Options(h_anchor_type=HORIZONTAL_ANCHOR_POINT.LEFT, v_anchor_type=VERTICAL_ANCHOR_POINT.TOP, alignment=ALIGNMENTS.VERTICAL):
	""""""
	tool_cls = Node_Alignment_Tool(h_anchor_type, v_anchor_type, alignment)
	tool_cls.apply_Tool()

#-------------------------------------------------------------------------------
def _node_Expansion_State_Tool_Options(value=EXPANSION_STATE.MINIMIZED):
	""""""
	tool_cls = Node_Expansion_State_Tool(value)
	tool_cls.apply_Tool()


qol_tool_align_selected_graph_nodes_vertical_left   =  lambda : _node_Alignment_Tool_Options(h_anchor_type=HORIZONTAL_ANCHOR_POINT.LEFT,v_anchor_type=VERTICAL_ANCHOR_POINT.TOP,alignment=ALIGNMENTS.VERTICAL)

qol_tool_align_selected_graph_nodes_vertical_mid    =  lambda : _node_Alignment_Tool_Options(h_anchor_type=HORIZONTAL_ANCHOR_POINT.MIDDLE,v_anchor_type=VERTICAL_ANCHOR_POINT.MIDDLE,alignment=ALIGNMENTS.VERTICAL)

qol_tool_align_selected_graph_nodes_vertical_right  =  lambda : _node_Alignment_Tool_Options(h_anchor_type=HORIZONTAL_ANCHOR_POINT.RIGHT,v_anchor_type=VERTICAL_ANCHOR_POINT.TOP,alignment=ALIGNMENTS.VERTICAL)

qol_tool_align_selected_graph_nodes_horizontal_top  =  lambda : _node_Alignment_Tool_Options(h_anchor_type=HORIZONTAL_ANCHOR_POINT.LEFT,v_anchor_type=VERTICAL_ANCHOR_POINT.TOP,alignment=ALIGNMENTS.HORIZONTAL)

qol_tool_align_selected_graph_nodes_horizontal_bot  =  lambda : _node_Alignment_Tool_Options(h_anchor_type=HORIZONTAL_ANCHOR_POINT.LEFT,v_anchor_type=VERTICAL_ANCHOR_POINT.BOTTOM,alignment=ALIGNMENTS.HORIZONTAL)

qol_tool_align_selected_graph_nodes_horizontal_mid  =  lambda : _node_Alignment_Tool_Options(h_anchor_type=HORIZONTAL_ANCHOR_POINT.MIDDLE,v_anchor_type=VERTICAL_ANCHOR_POINT.MIDDLE,alignment=ALIGNMENTS.HORIZONTAL)



qol_tool_set_selected_graph_nodes_expansion_state_close   =  lambda : _node_Expansion_State_Tool_Options(EXPANSION_STATE.CLOSED)

qol_tool_set_selected_graph_nodes_expansion_state_min     =  lambda : _node_Expansion_State_Tool_Options(EXPANSION_STATE.MINIMIZED)

qol_tool_set_selected_graph_nodes_expansion_state_open    =  lambda : _node_Expansion_State_Tool_Options(EXPANSION_STATE.OPEN)

qol_tool_set_selected_graph_nodes_expansion_state_toggle  =  lambda : _node_Expansion_State_Tool_Options(EXPANSION_STATE.TOGGLE)



#-------------------------------------------------------------------------------
def de_somthing():
	""""""
	alignment = Node_Alignment_Tool(h_anchor_type=HORIZONTAL_ANCHOR_POINT.RIGHT)
	alignment.apply_Tool()