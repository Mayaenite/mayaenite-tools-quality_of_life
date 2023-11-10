import os
os.sys.path.append(r"D:\Program Files\Wing Pro 9")
import wingdbstub
wingdbstub.Ensure()

import omni.ui_query
import omni.ui as ui
for win in sorted([win.title for win in ui.Workspace.get_windows()]):
	print(win)

import carb
import omni.usd
import omni.graph.core as og
import pxr.Usd as Usd
import  omni.kit.widget.graph.isolation_graph_model

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
	windows = ui.Workspace.get_windows()
	for window in windows:
		if window.title == window_name:
			return window
		
#-------------------------------------------------------------------------------
def get_Graph_View():
	""""""
	windows = ui.Workspace.get_windows()
	for window in windows:
		if window.title == window_name:
			return window
		
#Material_Graph_Win = get_Window('Material Graph')
#Action_Graph_Win = get_Window('Action Graph')
#Stage_Win = get_Window('Stage')
print(sorted([window.title for window in get_All_Windows()]))
#print([window.title for window in get_All_Windows()])
#ctx = omni.usd.get_context()
#stage : Usd.Stage = ctx.get_stage()
#prim_path = "/World/AG"
#graph = og.get_graph_by_path(prim_path)
#for node in graph.get_nodes():
	#prim_path = node.get_prim_path()
	#prim = stage.GetPrimAtPath(prim_path)
	#att = prim.GetAttribute("ui:nodegraph:node:pos")
	#print(att.Get()
