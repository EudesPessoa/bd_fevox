import sqlite3

class Database_Supplier:
	
	def __init__(self, name='fevox.db'):
		self.name, self.conexao = name, None


	def Connect(self):
		self.conexao = sqlite3.connect(self.name)


	def Disconnect(self):
		try:
			self.conexao.close()
		except AttributeError:
			pass


	def Create_Supplier_Table(self):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""CREATE TABLE IF NOT EXISTS supplier(
				  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				  name_supplier TEXT NOT NULL,
				  supplier_fantasy TEXT NOT NULL,
				  cnpj TEXT NOT NULL,
				  state_registration TEXT NOT NULL,
				  county_registration TEXT NOT NULL,
				  address TEXT NOT NULL,
				  address_state TEXT NOT NULL,
				  supplier_email TEXT NOT NULL,
				  phone TEXT NOT NULL
				  );"""
				  )
		except AttributeError:
			pass
		self.Disconnect()


	def Insert_Supplier(
			self,
			name_supplier,
			supplier_fantasy,
			cnpj,
			state_registration,
			county_registration,
			address,
			address_state,
			supplier_email,
			phone,
			):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			try:
				cursor.execute("""
				INSERT INTO supplier (name_supplier, supplier_fantasy, cnpj, state_registration, county_registration, address, address_state, supplier_email, phone) VALUES (?,?,?,?,?,?,?,?,?);
				""", (name_supplier, supplier_fantasy, cnpj, state_registration, county_registration, address, address_state, supplier_email, phone))
				self.conexao.commit()
			except sqlite3.IntegrityError:
				pass
		except AttributeError:
			pass
		self.Disconnect()


	def Fetch_Supplier(self, ):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute("""SELECT * FROM supplier""")
		Products = cursor.fetchall()
		self.Disconnect()
		return Products
	

	def Update_Supplier(self,
					id,
					name_supplier,
					supplier_fantasy,
					cnpj,
					state_registration,
					county_registration,
					address,
					address_state,
					supplier_email,
					phone
					):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""UPDATE supplier SET name_supplier=? WHERE id=?;""",
			(name_supplier, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE supplier SET supplier_fantasy=? WHERE id=?;""",
			(supplier_fantasy, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE supplier SET cnpj=? WHERE id=?;""",
			(cnpj, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE supplier SET state_registration=? WHERE id=?;""",
			(state_registration, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE supplier SET county_registration=? WHERE id=?;""",
			(county_registration, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE supplier SET address=? WHERE id=?;""",
			(address, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE supplier SET address_state=? WHERE id=?;""",
			(address_state, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE supplier SET supplier_email=? WHERE id=?;""",
			(supplier_email, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE supplier SET phone=? WHERE id=?;""",
			(phone, id)
			)
		self.conexao.commit()
		self.Disconnect()


	def Delete_Supplier(self, id,):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""DELETE FROM supplier WHERE id=?;""",
			(id,) 
			)
		self.conexao.commit()
		self.Disconnect()



	# def Delete_Table_total(self,):
	# 	self.Connect()
	# 	cursor = self.conexao.cursor()	
	# 	cursor.execute(
	# 		"""DROP table invoice;""" 
	# 		)
	# 	self.conexao.commit()
	# 	self.Disconnect()

