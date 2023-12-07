import sqlite3

class Database_Model:
	
	def __init__(self, name='fevox.db'):
		self.name, self.conexao = name, None


	def Connect(self):
		self.conexao = sqlite3.connect(self.name)


	def Disconnect(self):
		try:
			self.conexao.close()
		except AttributeError:
			pass


	def Create_Model_Table(self):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""CREATE TABLE IF NOT EXISTS models(
				  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				  user_name TEXT NOT NULL,
				  brand_name_model INTEGER NOT NULL,
				  model_name TEXT NOT NULL,
				  foreign key(brand_name_model) references brands(id)
				  );"""
				  )
		except AttributeError:
			pass
		self.Disconnect()


	def Insert_Model(self, user_name, brand_name_model, model_name):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			try:
				cursor.execute("""
				INSERT INTO models (user_name, brand_name_model, model_name) VALUES (?,?,?);
				""", (user_name, brand_name_model, model_name))
				self.conexao.commit()
			except sqlite3.IntegrityError:
				pass
		except AttributeError:
			pass
		self.Disconnect()


	def Search_Model_Name(self, model_name, brand_name_model):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""SELECT * FROM models;""")
			for linha in cursor.fetchall():
				if linha[3] == model_name:
					if linha[2] == brand_name_model:
						return 'sim'
				else:
					pass
		except AttributeError:
			pass
		except sqlite3.OperationalError:
			pass
		self.Disconnect()


	def Fetch_Model(self, ):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute("""SELECT * FROM models""")
		Products = cursor.fetchall()
		self.Disconnect()
		return Products
	

	def Update_Model(self, new_name_model, id, name_user, brand_name_model):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""UPDATE models SET model_name=? WHERE id=?;""",
			(new_name_model, id)
			)
		cursor.execute(
			"""UPDATE models SET user_name=? WHERE id=?;""",
			(name_user, id)
			)
		cursor.execute(
			"""UPDATE models SET brand_name_model=? WHERE id=?;""",
			(brand_name_model, id)
			)
		self.conexao.commit()
		self.Disconnect()


	def Delete_Model(self, name_model, id):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""DELETE FROM models WHERE model_name=? and id=?;""",
			(name_model, id) 
			)
		self.conexao.commit()
		self.Disconnect()

