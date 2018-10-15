from pylib.previewer import Previewer
from pylib.filebrowser import FileBrowser
from pylib.kerneleditor import KernelEditor
from pylib.dblink import DBlink
from pylib.irregularNameTest import testIfRegular

from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock

from kivy.properties import ObjectProperty

from functools import partial

import numpy as np
import cv2



# Function for converting cv2 image type, to kivy texture type
def picToTextureBuffer(matrix):
	return cv2.flip(matrix[:,:,[2,1,0]],0).tostring()



class MainBox(BoxLayout):

	def changeView(self,ime):
		self.clear_widgets()
		if ime=="browser":
			self.add_widget(self.browser)
		elif ime=="kernelEditor":
			self.add_widget(self.kernelEditor)
		else:
			self.add_widget(self.previewer)



	#Button action Functions:

	#browse button action function
	def	browseButtonFunction(self):
		self.changeView("browser")

	#kernel edit button action function
	def kernelButtonFunction(self):
		self.changeView("kernelEditor")

	#Filter apply button action function
	def applyButtonFunction(self):
		matrica = self.previewer.src
		if not (matrica is None):
			if self.filter:
				filtered = cv2.filter2D(matrica, -1, self.filter.filterarray)
				self.previewer.convImg.blit_buffer(picToTextureBuffer(filtered), colorfmt='bgr')

	#Done/Return functions:

	#Function to use when browser is done
	def browserReturnFunction(self, selection, touch):
		self.changeView("previewer")

		srcLocation = selection[0]

		matrica = np.array(cv2.imread(srcLocation,cv2.IMREAD_COLOR))


		self.previewer.src = matrica
		self.previewer.ratio = float(matrica.shape[0])/matrica.shape[1]


		#Create textures and blit source image

		zablit = picToTextureBuffer(matrica)

		self.previewer.srcImg = Texture.create(size=(matrica.shape[1], matrica.shape[0]), colorfmt='rgb', bufferfmt='ubyte')
		self.previewer.convImg = Texture.create(size=(matrica.shape[1], matrica.shape[0]), colorfmt='rgb', bufferfmt='ubyte')
		self.previewer.srcImg.blit_buffer(zablit, colorfmt='rgb')
		self.previewer.convImg.blit_buffer(picToTextureBuffer(matrica), colorfmt='rgb')


		#Set the right layout for current sizes

		self.previewer.adjustImageLayout()


	# Function to use when done editing kernel
	def kernelEditorReturnFunction(self):
		self.changeView("previewer")
		#nextStep

	def kernelEditorSave(self, group, name, npArray):
		if testIfRegular(group, name):
			self.database.saveFilter(group, name, npArray)

	def selectCallback(self, object, state):
		if state=="down":
			self.filter = object

	def __init__(self, db, **kwargs):
		super(MainBox, self).__init__(**kwargs)
		self.filter = None
		self.database = db

		# Functions for quick debugging

		# self.browseButtonFunction = partial(self.browserReturnFunction, ("/home/alion/Desktop/cat.jpg",0), 0)
		# self.applyButtonFunction = partial(self.browserReturnFunction, ("/home/alion/Desktop/black_cat.jpg",0), 0)


		# Main Widgets
		self.previewer=Previewer(main=self)
		self.browser=FileBrowser(main=self)
		self.kernelEditor=KernelEditor(main=self)


		self.add_widget(self.previewer)

	# This is required for android to correctly display widgets on screen rotate

	def on_size(self, val1, val2):
		Clock.schedule_once(lambda dt: self.canvas.ask_update(), 0.2)
