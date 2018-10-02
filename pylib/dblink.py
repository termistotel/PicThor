import sqlite3
import numpy as np
import io


"""Thanks SoulNibbler for functions adapt_array & convert_array and initialization for converters 
	http://stackoverflow.com/a/31312102/190597 (SoulNibbler)"""

def adapt_array(arr):
	out = io.BytesIO()
	np.save(out, arr)
	out.seek(0)
	return sqlite3.Binary(out.read())

def convert_array(text):
	out = io.BytesIO(text)
	out.seek(0)
	return np.load(out)


# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)

class DBlink(object):
	"""Object for linking with app database, allows saving of numpy matrices"""
	def __init__(self, loc):
		super(DBlink, self).__init__()
		self.loc = loc
		self.openFilterTable()

	def openFilterTable(self):
		self.con = sqlite3.connect(self.loc, detect_types=sqlite3.PARSE_DECLTYPES)
		self.cur = self.con.cursor()
		try:
			self.cur.execute("select * from filterkernels limit 1")
		except:
			print("Filter kernel table not found, creating new ...")
			self.cur.execute("create table filterkernels (filtergroup text, filtername text, matrix array)")

	def saveFilter(self, group, name, matrix):
		self.cur.execute("insert into filterkernels (filtergroup, filtername, matrix) values (?, ?, ?)", (group, name, matrix))
		self.save()

	def groupList(self):
		return [x[0] for x in self.cur.execute("SELECT filtergroup FROM filterkernels GROUP BY filtergroup")]

	def getAllFromGroup(self, group):
		return self.cur.execute("SELECT * FROM filterkernels WHERE filtergroup=?",(group, ))

	def save(self):
		self.con.commit()

	def close(self):
		self.con.close()

	def reset(self):
		try:
			self.cur.execute("drop table filterkernels")
		except:
			pass
		self.cur.execute("create table filterkernels (filtergroup text, filtername text, grayscale integer, matrix array)")
