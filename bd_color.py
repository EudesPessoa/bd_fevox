import sqlite3

class Database_Color:
	
	def __init__(self, name='fevox.db'):
		self.name, self.conexao = name, None


	def Connect(self):
		self.conexao = sqlite3.connect(self.name)

	def Connect1(self):
		self.conexao = sqlite3.connect(self.name)
		return self.conexao


	def Disconnect(self):
		try:
			self.conexao.close()
		except AttributeError:
			pass


	def Create_Color_Table(self):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""CREATE TABLE IF NOT EXISTS color(
				  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				  user_name TEXT NOT NULL,
				  brand_name_color INTEGER NOT NULL,
				  model_name_color INTEGER NOT NULL,
				  product_name_color INTEGER NOT NULL,
				  color_name TEXT NOT NULL,
				  foreign key(brand_name_color) references brands(id),
				  foreign key(model_name_color) references models(id),
				  foreign key(product_name_color) references product(id)
				  );"""
				  )
		except AttributeError:
			pass
		self.Disconnect()


	def Insert_Color(
			self,
			user_name,
			brand_name_color,
			model_name_color,
			product_name_color,
			color_name,
			):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			try:
				cursor.execute("""
				INSERT INTO color (user_name, brand_name_color, model_name_color, product_name_color, color_name) VALUES (?,?,?,?,?);
				""", (user_name, brand_name_color, model_name_color, product_name_color, color_name))
				self.conexao.commit()
			except sqlite3.IntegrityError:
				pass
		except AttributeError:
			pass
		self.Disconnect()


	def Search_Color(
			self,
			color_name,
			product_name_color,
			model_name_color,
			brand_name_color
			):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""SELECT * FROM color;""")
			for linha in cursor.fetchall():
				if linha[5] == color_name:
					if linha[4] == product_name_color:
						if linha[3] == model_name_color:
							if linha[2] == brand_name_color:
								return 'sim'
				else:
					pass
		except AttributeError:
			pass
		except sqlite3.OperationalError:
			pass
		self.Disconnect()


	def Fetch_Color(self, ):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute("""SELECT * FROM color""")
		Products = cursor.fetchall()
		self.Disconnect()
		return Products
	

	def Update_Color(self,
					color_name,
					id,
					):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""UPDATE color SET color_name=? WHERE id=?;""",
			(color_name, id)
			)
		self.conexao.commit()
		self.Disconnect()

	def Delete_Color(self, color_name, id):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""DELETE FROM color WHERE color_name=? and id=?;""",
			(color_name, id) 
			)
		self.conexao.commit()
		self.Disconnect()

