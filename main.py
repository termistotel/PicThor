import kivy
kivy.require('1.10.0') # replace with your current kivy version !

from kivy.app import App

from pylib.mainbox import MainBox
from pylib.irregularNameTest import testIfRegular
from pylib.dblink import DBlink

class TestApp(App):
	dbFilename = "PicThor.db"

	def connectToDb(self):
		return DBlink(self.dbFilename)

	def build(self):
		db = self.connectToDb()
		mainbox = MainBox(db=db)
		return mainbox

if __name__ == '__main__':
    TestApp().run()

