import kivy
kivy.require('1.10.0') # replace with your current kivy version !

from kivy.app import App

from pylib.mainbox import MainBox

class TestApp(App):

	def build(self):
		mainbox = MainBox()
		return mainbox

if __name__ == '__main__':
    TestApp().run()