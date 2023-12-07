import sqlite3

class Database_Stock:
	
	def __init__(self, name='fevox.db'):
		self.name, self.conexao = name, None


	def Connect(self):
		self.conexao = sqlite3.connect(self.name)


	def Disconnect(self):
		try:
			self.conexao.close()
		except AttributeError:
			pass


	def Create_Stock_Table(self):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""CREATE TABLE IF NOT EXISTS stock(
				  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				  user_name TEXT NOT NULL,
				  brand_name_stock INTEGER NOT NULL,
				  model_name_stock INTEGER NOT NULL,
				  product_name_stock INTEGER NOT NULL,
				  color_product_stock INTEGER NOT NULL,
				  product_stock_amount INTEGER NOT NULL,
				  value_sale INTEGER,
				  tax INTEGER,
				  profit INTEGER,
				  foreign key(brand_name_stock) references brands(id),
				  foreign key(model_name_stock) references models(id),
				  foreign key(product_name_stock) references product(id),
				  foreign key(color_product_stock) references color(id)
				  );"""
				  )
		except AttributeError:
			pass
		self.Disconnect()


	def Insert_Stock(
			self,
			user_name,
			brand_name_stock,
			model_name_stock,
			product_name_stock,
			color_product_stock,
			product_stock_amount,
			):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			try:
				cursor.execute("""
				INSERT INTO stock (user_name, brand_name_stock, model_name_stock, product_name_stock, color_product_stock, product_stock_amount) VALUES (?,?,?,?,?,?);
				""", (user_name, brand_name_stock, model_name_stock, product_name_stock, color_product_stock, product_stock_amount))
				self.conexao.commit()
			except sqlite3.IntegrityError:
				pass
		except AttributeError:
			pass
		self.Disconnect()


	def Fetch_Stock(self, ):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute("""SELECT * FROM stock""")
		Products = cursor.fetchall()
		self.Disconnect()
		return Products
	

	def Update_Stock_Sales(self,
					product_stock_amount,
					id,
					):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""UPDATE stock SET product_stock_amount=? WHERE id=?;""",
			(product_stock_amount, id)
			)
		self.conexao.commit()
		self.Disconnect()


	def Update_Stock(self,
					product_stock_amount,
					id,
					):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""UPDATE stock SET product_stock_amount=? WHERE id=?;""",
			(product_stock_amount, id)
			)
		self.conexao.commit()
		self.Disconnect()


	def Update_Stock_Pricing(self,
					id,
					value_sale,
					tax,
					profit
					):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""UPDATE stock SET value_sale=? WHERE id=?;""",
			(value_sale, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE stock SET tax=? WHERE id=?;""",
			(tax, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE stock SET profit=? WHERE id=?;""",
			(profit, id)
			)
		self.conexao.commit()
		self.Disconnect()

	def Update_Stock_Colum(self):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""ALTER TABLE stock ADD value_sale INTEGER"""
			)
		self.conexao.commit()
		self.Disconnect()

	def Update_Stock_Colum1(self):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""ALTER TABLE stock ADD tax INTEGER"""
			)
		self.conexao.commit()
		self.Disconnect()

	def Update_Stock_Colum2(self):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""ALTER TABLE stock ADD profit INTEGER"""
			)
		self.conexao.commit()
		self.Disconnect()


	# def Delete_Stock_Product(self, color_product_stock,):
	# 	self.Connect()
	# 	cursor = self.conexao.cursor()	
	# 	cursor.execute(
	# 		"""DELETE FROM stock WHERE color_product_stock=?;""",
	# 		(color_product_stock,) 
	# 		)
	# 	self.conexao.commit()
	# 	self.Disconnect()

