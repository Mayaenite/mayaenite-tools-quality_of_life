
import omni.kit.actions.core
from omni.kit.actions.core import  Action
from omni.kit.hotkeys.core import  Hotkey
import omni.kit.hotkeys.core
from . import omni_graph_node_control_tools
import carb
from inspect import getsource
get_lambda_name = lambda l: getsource(l).split('=')[0].strip()
################################################################################
class QOL_Actions:
	""""""
	def __init__(self, ext_id):
		"""Constructor"""
		self._ext_id = ext_id
		self._tag    =  "Quality Of Life"
		self._all_actions =  []
		self._all_hotkeys =  []		
		self._hotkey_filter = omni.kit.hotkeys.core.filter.HotkeyFilter(windows=['Action Graph','Generic Graph', 'Material Graph', 'Particles Editor'])
		self._register_Actions()
		
	#-------------------------------------------------------------------------------
	def add_action(self, fn, hk):
		""""""
		name   = get_lambda_name(fn)
		
		action = Action(self._ext_id, name, fn, name.replace("_", " "))
		
		self._all_actions.append(action)
		omni.kit.actions.core.get_action_registry().register_action(action)
		
		key    = Hotkey(self._ext_id, hk, action.extension_id, action.id, filter=self._hotkey_filter)
		omni.kit.hotkeys.core.get_hotkey_registry().register_hotkey(key)
		self._all_hotkeys.append(key)
		
	def _register_Actions(self):
		""""""
		
		self.add_action(omni_graph_node_control_tools.qol_tool_align_selected_graph_nodes_vertical_left,"NUMPAD_4")
		self.add_action(omni_graph_node_control_tools.qol_tool_align_selected_graph_nodes_vertical_mid,"NUMPAD_5")
		self.add_action(omni_graph_node_control_tools.qol_tool_align_selected_graph_nodes_vertical_right,"NUMPAD_6")
		
		self.add_action(omni_graph_node_control_tools.qol_tool_align_selected_graph_nodes_horizontal_top,"NUMPAD_8")
		self.add_action(omni_graph_node_control_tools.qol_tool_align_selected_graph_nodes_horizontal_mid,"CTRL + NUMPAD_5")
		self.add_action(omni_graph_node_control_tools.qol_tool_align_selected_graph_nodes_horizontal_bot,"NUMPAD_2")
		
		self.add_action(omni_graph_node_control_tools.qol_tool_set_selected_graph_nodes_expansion_state_close,"NUMPAD_0")
		self.add_action(omni_graph_node_control_tools.qol_tool_set_selected_graph_nodes_expansion_state_min,"NUMPAD_1")
		self.add_action(omni_graph_node_control_tools.qol_tool_set_selected_graph_nodes_expansion_state_open,"NUMPAD_3")
		self.add_action(omni_graph_node_control_tools.qol_tool_set_selected_graph_nodes_expansion_state_toggle,"NUMPAD_DEL")
		
	def _deregister_Actions(self):
		""""""
		hotkey_registry = omni.kit.hotkeys.core.get_hotkey_registry()
		action_registry = omni.kit.actions.core.get_action_registry()
		
		for hk in  self._all_hotkeys:
			hotkey_registry.deregister_hotkey(hk)
		for act in self._all_actions:
			action_registry.deregister_action(act)