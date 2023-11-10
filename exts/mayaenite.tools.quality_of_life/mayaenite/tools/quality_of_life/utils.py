import omni.kit.widget.graph
import omni.ui_query
import omni.ui as ui
import omni.usd

def get_current_selection():
	ctx = omni.usd.get_context()
	selection = ctx.get_selection().get_selected_prim_paths()
	return selection

#-------------------------------------------------------------------------------
def get_All_Windows():
	""""""
	return ui.Workspace.get_windows()

#-------------------------------------------------------------------------------
def get_Window(window_name):
	""""""
	windows = get_All_Windows()
	for window in windows:
		if window.title == window_name:
			return window