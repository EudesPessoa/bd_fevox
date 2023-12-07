import sqlite3

class Database_Provider:
	
	def __init__(self, name='fevox.db'):
		self.name, self.conexao = name, None


	def Connect(self):
		self.conexao = sqlite3.connect(self.name)


	def Disconnect(self):
		try:
			self.conexao.close()
		except AttributeError:
			pass


	def Create_Provider_Table(self):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""CREATE TABLE IF NOT EXISTS provider(
				  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				  supplier_fantasy TEXT NOT NULL,
				  provider_supplier TEXT NOT NULL
				  );"""
				  )
		except AttributeError:
			pass
		self.Disconnect()


	def Insert_Provider(
			self,
			supplier_fantasy,
			provider_supplier,
			):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			try:
				cursor.execute("""
				INSERT INTO provider (supplier_fantasy, provider_supplier) VALUES (?,?);
				""", (supplier_fantasy, provider_supplier))
				self.conexao.commit()
			except sqlite3.IntegrityError:
				pass
		except AttributeError:
			pass
		self.Disconnect()


	def Fetch_Provider(self, ):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute("""SELECT * FROM provider""")
		Products = cursor.fetchall()
		self.Disconnect()
		return Products
	

	def Search_Provider_Name(self, supplier_fantasy, provider_supplier):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""SELECT * FROM provider;""")
			for linha in cursor.fetchall():
				if linha[1] == supplier_fantasy:
					if linha[2] == provider_supplier:
						return 'sim'
				else:
					pass
		except AttributeError:
			pass
		except sqlite3.OperationalError:
			pass
		self.Disconnect()


	def Update_Provider(self,
					provider_supplier,
					id,
					):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""UPDATE provider SET provider_supplier=? WHERE id=?;""",
			(provider_supplier, id)
			)
		self.conexao.commit()
		self.Disconnect()


	def Delete_Provider(self, provider_supplier,id):
		self.Connect()
		cursor = self.conexao.cursor()	
		cursor.execute(
			"""DELETE FROM provider WHERE provider_supplier=? and id=?;""",
			(provider_supplier,id) 
			)
		self.conexao.commit()
		self.Disconnect()

