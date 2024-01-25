
import omni.ui as ui
import omni.graph.core as og
import omni.kit.widget.stage
import omni.graph.window.action
import omni.graph.window.particle.system
import omni.kit.window.material_graph
import omni.graph.window.generic
import omni.anim.graph.ui.scripts.extension
from omni.kit.viewport.utility import frame_viewport_selection, get_active_viewport
import functools
from .utils import get_Window

#-------------------------------------------------------------------------------
def _show_particle_graph(*args):
	omni.graph.window.particle.system.ParticleGraphExtension.show_graph([args[0]])
#-------------------------------------------------------------------------------
def _show_animation_graph(*args):
	""""""
	omni.anim.graph.ui.scripts.extension.ext._graph_window.open_graph(args[0])
#-------------------------------------------------------------------------------
def _show_action_graph(*args):
	omni.graph.window.action.action_graph_extension.ActionGraphExtension.show_graph([args[0]])
#-------------------------------------------------------------------------------
def _show_generic_graph(*args):
	omni.graph.window.generic.generic_graph_extension._extension_instance.show_graph([args[0]])

#-------------------------------------------------------------------------------
def _show_material_graph(*args):
	window = get_Window('Material Graph')
	omni.kit.window.material_graph.graph_extension.GraphExtension.show_materials([args[0]])
	try:
		window.focus()
		window._main_widget._graph_view.layout_all()
		window = None
	except:
		pass
#-------------------------------------------------------------------------------
def _set_acive_camera(*args):
	""""""
	viewport = get_active_viewport()
	if viewport:
		viewport.camera_path = args[0]
#-------------------------------------------------------------------------------
def _frame_acive_object(*args):
	""""""
	frame_viewport_selection(viewport_api=None)
################################################################################
class NameColumnDelegate(omni.kit.widget.stage.stage_extension.NameColumnDelegate):
	#-------------------------------------------------------------------------------
	def _is_particle_graph(self, graph):
		""""""
		for node in graph.get_nodes():
			if node.get_type_name().startswith("omni.particle.system.core"):
				return True
		return False
	#-------------------------------------------------------------------------------
	def _is_action_graph(self, graph):
		""""""
		return og.get_graph_settings(graph).evaluator_type == "execution"
	#-------------------------------------------------------------------------------
	def __draw_all_icons(self, item, item_is_native, is_highlighted):
		""""""
		icon_filenames = self.__get_all_icons_to_draw(item, item_is_native)
		# Gray out the icon if the filter string is not in the text
		iconname = "object_icon" if is_highlighted else "object_icon_grey"
		
		parent_layout = ui.ZStack(width=20, height=20)
		with parent_layout:
			
			for icon_filename in icon_filenames:
				image = ui.Image(icon_filename, name=iconname, style_type_name_override="TreeView.Image")

				if item.type_name in ["Camera"]:
					image.set_mouse_double_clicked_fn(functools.partial(_set_acive_camera, item.path.pathString))
				
				elif item.type_name in ["Mesh", "Xform", 'Cylinder', 'Sphere', 'Cube', 'Capsule']:
					image.set_mouse_double_clicked_fn(functools.partial(_frame_acive_object))
				
				elif item.type_name == 'Material':
					image.set_mouse_double_clicked_fn(functools.partial(_show_material_graph, item.prim ))
				
				elif item.type_name == 'AnimationGraph':
					image.set_mouse_double_clicked_fn(functools.partial(_show_animation_graph, item.prim ))
					
				elif item.type_name == 'OmniGraph':
					graph = og.get_graph_by_path(item.path.pathString)
					
					if self._is_particle_graph(graph):
						image.set_mouse_double_clicked_fn(functools.partial(_show_particle_graph, item.prim ))
						
					elif self._is_action_graph(graph):
						image.set_mouse_double_clicked_fn(functools.partial(_show_action_graph, item.prim ))
						
					else:
						image.set_mouse_double_clicked_fn(functools.partial(_show_generic_graph, item.prim ))

		if item.instance_proxy:
			parent_layout.set_tooltip("Instance Proxy")