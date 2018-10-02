from pylib.previewer import Previewer
from pylib.filebrowser import FileBrowser
from pylib.kerneleditor import KernelEditor
from pylib.dblink import DBlink

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

	selectedFilterList = ObjectProperty([])

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
		#matrica = self.previewer.src
		#self.previewer.convImg.blit_buffer(picToTextureBuffer(matrica), colorfmt='bgr')
		self.selectedFilterList=[3]
		print(self)
		print(self.selectedFilterList)
		print(self.previewer.filterselector.lockChild.selectedFilterList)

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




	def __init__(self, **kwargs):
		super(MainBox, self).__init__(**kwargs)
		self.database = DBlink("PicThor.db")

		# Functions for quick debugging

		# self.browseButtonFunction = partial(self.browserReturnFunction, ("/home/alion/Desktop/cat.jpg",0), 0)
		# self.applyButtonFunction = partial(self.browserReturnFunction, ("/home/alion/Desktop/black_cat.jpg",0), 0)


		# Main Widgets
		self.previewer=Previewer(main=self)
		self.browser=FileBrowser(main=self)
		self.kernelEditor=KernelEditor(main=self)


		# Binding filter lists
		# self.previewer.filterselector.lockChild.bind(selectedFilterList=self.setter('selectedFilterList'))
		self.bind(selectedFilterList=self.previewer.filterselector.lockChild.setter('selectedFilterList'))

		self.add_widget(self.previewer)


	# This is required for android to correctly display widgets on screen rotate

	def on_size(self, val1, val2):
		Clock.schedule_once(lambda dt: self.canvas.ask_update(), 0.2)

	def on_selectedFilterList(self, val1, val2):
		print('test')