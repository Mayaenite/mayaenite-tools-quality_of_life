

################################################################################
class OmniGraphWidget_Overides():
	
	#-------------------------------------------------------------------------------
	def __init__(self, graph):
		""""""
		self.graph   = None
		self._org_fn = None
		
	#-------------------------------------------------------------------------------
	def update_assignments(self, graph):
		""""""
		
		self.graph = graph
		self._org_fn =  graph.__on_mouse_released
		graph.__on_mouse_released = self.__on_mouse_released
		
	def __on_mouse_released(self, x, y, button, m):
		if m == 2:
			print("YAAAA")
		else:
			self._org_fn(x, y, button, m)