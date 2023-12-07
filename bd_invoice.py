import sqlite3

class Database_Invoice:
	
	def __init__(self, name='fevox.db'):
		self.name, self.conexao = name, None


	def Connect(self):
		self.conexao = sqlite3.connect(self.name)


	def Disconnect(self):
		try:
			self.conexao.close()
		except AttributeError:
			pass


	def Create_Invoice_Table(self):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""CREATE TABLE IF NOT EXISTS invoice(
				  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				  user_name TEXT NOT NULL,
				  date_invoice TIMESTAMP NOT NULL,
				  invoice_number TEXT NOT NULL,
				  supplier TEXT NOT NULL,
				  id_product_invoice INTEGER NOT NULL,
				  product_amount_invoice INTEGER NOT NULL,
				  unitary_value INTEGER NOT NULL,
				  foreign key(id_product_invoice) references stock(id)
				  );"""
				  )
		except AttributeError:
			pass
		self.Disconnect()


	def Insert_Invoice(
			self,
			user_name,
			date_invoice,
			invoice_number,
			supplier,
			id_product_invoice,
			product_amount_invoice,
			unitary_value,
			):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			try:
				cursor.execute("""
				INSERT INTO invoice (user_name, date_invoice, invoice_number, supplier, id_product_invoice, product_amount_invoice, unitary_value) VALUES (?,?,?,?,?,?,?);
				""", (user_name, date_invoice, invoice_number, supplier, id_product_invoice, product_amount_invoice, unitary_value))
				self.conexao.commit()
			except sqlite3.IntegrityError:
				pass
		except AttributeError:
			pass
		self.Disconnect()


	def Fetch_Invoice(self, ):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute("""SELECT * FROM invoice""")
		Products = cursor.fetchall()
		self.Disconnect()
		return Products
	

	# def Update_Invoice(self,
	# 				product_stock_amount,
	# 				id,
	# 				):
	# 	self.Connect()
	# 	cursor = self.conexao.cursor()	
	# 	cursor.execute(
	# 		"""UPDATE invoice SET product_stock_amount=? WHERE id=?;""",
	# 		(product_stock_amount, id)
	# 		)
	# 	self.conexao.commit()
	# 	self.Disconnect()


	# def Delete_Stock_Product(self, color_product_stock,):
	# 	self.Connect()
	# 	cursor = self.conexao.cursor()	
	# 	cursor.execute(
	# 		"""DELETE FROM stock WHERE color_product_stock=?;""",
	# 		(color_product_stock,) 
	# 		)
	# 	self.conexao.commit()
	# 	self.Disconnect()



	def Delete_Table_total(self,):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""DROP table invoice;""" 
			)
		self.conexao.commit()
		self.Disconnect()

