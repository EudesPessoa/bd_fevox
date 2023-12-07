import sqlite3

class Database_Sales:
	
	def __init__(self, name='fevox.db'):
		self.name, self.conexao = name, None


	def Connect(self):
		self.conexao = sqlite3.connect(self.name)


	def Disconnect(self):
		try:
			self.conexao.close()
		except AttributeError:
			pass


	def Create_Sales_Table(self):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""CREATE TABLE IF NOT EXISTS sales(
				  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				  cod_sales_day TEXT NOT NULL,
				  date_sales TIMESTAMP NOT NULL,
				  seller_name TEXT NOT NULL,
				  product_stock_id INTEGER NOT NULL,
				  product_name TEXT NOT NULL,
				  amount_sales INTEGER NOT NULL,
				  value_item_sales INTEGER NOT NULL,
				  sum_sales INTEGER NOT NULL,
				  form_payment TEXT NOT NULL,
				  number_payment TEXT NOT NULL,
				  foreign key(product_stock_id) references stock(id)
				  );"""
				  )
		except AttributeError:
			pass
		self.Disconnect()


	def Insert_Sales(
			self,
			cod_sales_day,
			date_sales,
			seller_name,
			product_stock_id,
			product_name,
			amount_sales,
			value_item_sales,
			sum_sales,
			form_payment,
			number_payment,
			):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			try:
				cursor.execute("""
				INSERT INTO sales (cod_sales_day, date_sales, seller_name, product_stock_id, product_name, amount_sales, value_item_sales, sum_sales, form_payment, number_payment) VALUES (?,?,?,?,?,?,?,?,?,?);
				""", (cod_sales_day, date_sales, seller_name, product_stock_id, product_name, amount_sales, value_item_sales, sum_sales, form_payment, number_payment))
				self.conexao.commit()
			except sqlite3.IntegrityError:
				pass
		except AttributeError:
			pass
		self.Disconnect()


	def Fetch_Cod_Sales_Day(self, ):
		self.Connect()
		cursor = self.conexao.cursor()	
		# cursor.execute("""SELECT cod_sales_day FROM sales""")
		# cursor.execute("""SELECT max(id) FROM sales""")
		cursor.execute("""SELECT * FROM sales ORDER BY id DESC LIMIT 1""")
		Products = cursor.fetchone()
		self.Disconnect()
		return Products
	

	def Fetch_Sales(self, ):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute("""SELECT * FROM sales""")
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

