from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.accordion import Accordion
from kivy.uix.accordion import AccordionItem

from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty

from kivy.animation import Animation

from functools import partial

def inRect(rect, point):
	x,y = point
	xbound = (x > rect.x) and (x < (rect.x + rect.width))
	ybound = (y > rect.y) and (y < (rect.y + rect.height))
	return (xbound and ybound)


class ClickMenuButton(ToggleButton):

	def __init__(self, main, contentLength=0.5, **kwargs):
		self.contentLength = contentLength
		self.lockChild = MoveableContent(main, self)
		super(ClickMenuButton, self).__init__(**kwargs)

	def on_state(self, val1, state):
		if state=="normal":
			Animation(x = self.lockChild.lowVal, duration=0.4, t='out_cubic').start(self.lockChild)
		else:
			Animation(x = self.lockChild.highVal, duration=0.4, t='out_cubic').start(self.lockChild)

class MoveableContent(RelativeLayout):
	lowVal = NumericProperty(0)
	highVal = NumericProperty(0)

	# This list object should be bound to mainview's
	selectedFilterList = ObjectProperty([])

	def __init__(self, main, lockParent, **kwargs):
		self.lockParent = lockParent
		super(MoveableContent, self).__init__(**kwargs)

		self.x = -1000
		
		# Add functions
		self.ids.kerbutton.on_press=main.kernelButtonFunction
		self.on_touch_down = partial(self.on_touch_down1, self.on_touch_down)


		# Add children
		self.filterSelectMaster = FilterSelectMaster(main)
		self.ids.container.add_widget(self.filterSelectMaster)

	def on_lowVal(self, val1, val2):
		if self.lockParent.state=="normal":
			self.x = self.lowVal
		else:
			self.x = self.highVal

	def on_touch_down1(self, oldFun, val):
		oldFun(val)
		if self.lockParent.state=="down":
			if not (inRect(self, val.pos) or inRect(self.lockParent, val.pos)):
				self.lockParent.state="normal"

	# When filters get updated, propagate to children
	def updateFilterList(self):
		self.filterSelectMaster.updateFlterList(self)


class FilterSelectMaster(Accordion):
	"""docstring for FilterSelectMaster"""
	def __init__(self, main, **kwargs):
		super(FilterSelectMaster, self).__init__(**kwargs)
		self.orientation="vertical"

		for group in main.database.groupList():
			section = AccordionItem(title=group)
			container = FilterGroupContainter(db=main.database, group=group)

			section.add_widget(container)
			self.add_widget(section)
			

class FilterGroupContainter(GridLayout):
	def __init__(self, db, group, **kwargs):
		super(FilterGroupContainter, self).__init__(**kwargs)
		self.cols = 5
		self.db = db
		self.group = group
		self.updateFilters()

	def updateFilters(self):
		for row in self.db.getAllFromGroup(self.group):
			self.add_widget(ToggleButton(text=row[1]))
