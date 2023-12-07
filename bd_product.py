import sqlite3

class Database_Product:
	
	def __init__(self, name='fevox.db'):
		self.name, self.conexao = name, None


	def Connect(self):
		self.conexao = sqlite3.connect(self.name)


	def Disconnect(self):
		try:
			self.conexao.close()
		except AttributeError:
			pass


	def Create_Product_Table(self):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""CREATE TABLE IF NOT EXISTS product(
				  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				  user_name TEXT NOT NULL,
				  brand_name_product INTEGER NOT NULL,
				  model_name_product INTEGER NOT NULL,
				  product_name TEXT NOT NULL,
				  foreign key(brand_name_product) references brands(id),
				  foreign key(model_name_product) references models(id)
				  );"""
				  )
		except AttributeError:
			pass
		self.Disconnect()


	def Insert_Product(
			self,
			user_name,
			brand_name_product,
			model_name_product,
			product_name,
			):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			try:
				cursor.execute("""
				INSERT INTO product (user_name, brand_name_product, model_name_product, product_name) VALUES (?,?,?,?);
				""", (user_name, brand_name_product, model_name_product, product_name))
				self.conexao.commit()
			except sqlite3.IntegrityError:
				pass
		except AttributeError:
			pass
		self.Disconnect()


	def Search_Product_Name(
			self,
			product_name,
			model_name_product,
			brand_name_product
			):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""SELECT * FROM product;""")
			for linha in cursor.fetchall():
				if linha[4] == product_name:
					if linha[3] == model_name_product:
						if linha[2] == brand_name_product:
							return 'sim'
				else:
					pass
		except AttributeError:
			pass
		except sqlite3.OperationalError:
			pass
		self.Disconnect()


	def Fetch_Product(self, ):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute("""SELECT * FROM product""")
		Products = cursor.fetchall()
		self.Disconnect()
		return Products
	

	def Update_Product(self,
					product_name,
					id,
					):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""UPDATE product SET product_name=? WHERE id=?;""",
			(product_name, id)
			)
		self.conexao.commit()
		self.Disconnect()

	def Delete_Product(self, product_name, id):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""DELETE FROM product WHERE product_name=? and id=?;""",
			(product_name, id) 
			)
		self.conexao.commit()
		self.Disconnect()

