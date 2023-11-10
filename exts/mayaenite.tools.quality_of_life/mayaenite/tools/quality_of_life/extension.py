import omni.ext
import omni.kit.actions.core
from .stage_name_delegate_overide import NameColumnDelegate
from .actions import QOL_Actions

#action_registry = omni.kit.actions.core.get_action_registry()

#show_hide_stage_widget_action = action_registry.get_action("omni.kit.ui.editor_menu_bridge","action_editor_menu_bridge_window_visual_scripting_action_graph")
#show_hide_stage_widget_action.execute()
#show_hide_stage_widget_action.execute()

#show_hide_stage_widget_action = action_registry.get_action("omni.kit.ui.editor_menu_bridge","action_editor_menu_bridge_window_mdl_material_graph")
#show_hide_stage_widget_action.execute()
#show_hide_stage_widget_action.execute()

#show_hide_stage_widget_action = action_registry.get_action("omni.kit.ui.editor_menu_bridge","action_editor_menu_bridge_window_visual_scripting_generic_graph")
#show_hide_stage_widget_action.execute()
#show_hide_stage_widget_action.execute()


#show_hide_stage_widget_action = action_registry.get_action("omni.kit.ui.editor_menu_bridge","action_editor_menu_bridge_window_particles_editor")
#show_hide_stage_widget_action.execute()
#show_hide_stage_widget_action.execute()



class MayaeniteToolsQuality_of_lifeExtension(omni.ext.IExt):
	# ext_id is current extension id. It can be used with extension manager to query additional information, like where
	# this extension is located on filesystem.
	def on_startup(self, ext_id):
		print("[mayaenite.tools.quality_of_life] mayaenite tools quality_of_life startup")
		#show_hide_stage_widget_action.execute()
		self._ext_id = ext_id
		self._orig_NameColumnDelegate =  omni.kit.widget.stage.StageColumnDelegateRegistry().get_column_delegate("Name")
		omni.kit.widget.stage.StageColumnDelegateRegistry()._delegates["Name"] = NameColumnDelegate
		self._ext_actions =  QOL_Actions(self._ext_id)
		
	def on_shutdown(self):
		print("[mayaenite.tools.quality_of_life] mayaenite tools quality_of_life shutdown")
		omni.kit.widget.stage.StageColumnDelegateRegistry()._delegates["Name"] = self._orig_NameColumnDelegate
		#show_hide_stage_widget_action.execute()
		self._ext_actions._deregister_Actions()
		self._ext_id = None
		self._orig_NameColumnDelegate = None
		
