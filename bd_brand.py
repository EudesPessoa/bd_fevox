import sqlite3

class Database_Brand:
	
	def __init__(self, name='fevox.db'):
		self.name, self.conexao = name, None


	def Connect(self):
		self.conexao = sqlite3.connect(self.name)


	def Disconnect(self):
		try:
			self.conexao.close()
		except AttributeError:
			pass


	def Create_Brands_Table(self):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""CREATE TABLE IF NOT EXISTS brands(
				  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				  user_name TEXT NOT NULL,
				  brand_name TEXT NOT NULL
				  );"""
				  )
		except AttributeError:
			pass
		self.Disconnect()


	def Insert_Brands(self, user_name, brand_name):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			try:
				cursor.execute("""
				INSERT INTO brands (user_name, brand_name) VALUES (?,?);
				""", (user_name, brand_name,))
				self.conexao.commit()
			except sqlite3.IntegrityError:
				pass
		except AttributeError:
			pass
		self.Disconnect()


	def Search_Brand_Name(self, brand_name):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""SELECT * FROM brands;""")
			for linha in cursor.fetchall():
				if linha[2] == brand_name:
					return 'sim'
				else:
					pass
		except AttributeError:
			pass
		except sqlite3.OperationalError:
			pass
		self.Disconnect()


	def Fetch_Brand(self, ):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute("""SELECT * FROM brands""")
		Products = cursor.fetchall()
		self.Disconnect()
		return Products
	

	def Update_Brand(self, new_name_brand, id, name_user):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""UPDATE brands SET brand_name=? WHERE id=?;""",
			(new_name_brand, id)
			)
		cursor.execute(
			"""UPDATE brands SET user_name=? WHERE id=?;""",
			(name_user, id)
			)
		self.conexao.commit()
		self.Disconnect()
# and user_name=?
	def Delete_Brand(self, name_brand, id):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""DELETE FROM brands WHERE brand_name=? and id=?;""",
			(name_brand, id) 
			)

		self.conexao.commit()
		self.Disconnect()

