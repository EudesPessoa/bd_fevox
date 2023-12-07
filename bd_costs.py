import sqlite3

class Database_Costs:
	
	def __init__(self, name='fevox.db'):
		self.name, self.conexao = name, None


	def Connect(self):
		self.conexao = sqlite3.connect(self.name)


	def Disconnect(self):
		try:
			self.conexao.close()
		except AttributeError:
			pass


	def Create_Costs_Table(self):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""CREATE TABLE IF NOT EXISTS costs(
				  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				  user_name TEXT NOT NULL,
				  date_costs TIMESTAMP NOT NULL,
				  supplier_costs TEXT NOT NULL,
				  provider_costs TEXT NOT NULL,
				  types_of_costs TEXT NOT NULL,
				  days_the_costs INTEGER NOT NULL,
				  value_costs INTEGER NOT NULL,
				  number_of_costs INTEGER NOT NULL,
				  invoice_number_costs TEXT NOT NULL
				  );"""
				  )
		except AttributeError:
			pass
		self.Disconnect()


	def Insert_Costs(
			self,
			user_name,
			date_costs,
			supplier_costs,
			provider_costs,
			types_of_costs,
			days_the_costs,
			value_costs,
			number_of_costs,
			invoice_number_costs
			):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			try:
				cursor.execute("""
				INSERT INTO costs (user_name, date_costs, supplier_costs, provider_costs, types_of_costs, days_the_costs, value_costs, number_of_costs, invoice_number_costs) VALUES (?,?,?,?,?,?,?,?,?);
				""", (user_name, date_costs, supplier_costs, provider_costs, types_of_costs, days_the_costs, value_costs, number_of_costs, invoice_number_costs))
				self.conexao.commit()
			except sqlite3.IntegrityError:
				pass
		except AttributeError:
			pass
		self.Disconnect()


	def Fetch_Costs(self, ):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute("""SELECT * FROM costs""")
		Products = cursor.fetchall()
		self.Disconnect()
		return Products
	

	def Update_Costs(self,
					id,
					supplier_costs,
					provider_costs,
					types_of_costs,
					days_the_costs,
					value_costs,
					number_of_costs,
					invoice_number_costs
					):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""UPDATE costs SET supplier_costs=? WHERE id=?;""",
			(supplier_costs, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE costs SET provider_costs=? WHERE id=?;""",
			(provider_costs, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE costs SET types_of_costs=? WHERE id=?;""",
			(types_of_costs, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE costs SET days_the_costs=? WHERE id=?;""",
			(days_the_costs, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE costs SET value_costs=? WHERE id=?;""",
			(value_costs, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE costs SET number_of_costs=? WHERE id=?;""",
			(number_of_costs, id)
			)
		self.conexao.commit()
		cursor.execute(
			"""UPDATE costs SET invoice_number_costs=? WHERE id=?;""",
			(invoice_number_costs, id)
			)
		self.conexao.commit()
		self.Disconnect()


	def Delete_Costs(self, id,):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""DELETE FROM costs WHERE id=?;""",
			(id,) 
			)
		self.conexao.commit()
		self.Disconnect()



	def Delete_Table_total(self,):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""DROP table costs;""" 
			)
		self.conexao.commit()
		self.Disconnect()

