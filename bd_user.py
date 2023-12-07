import sqlite3

class Database_User:
	
	def __init__(self, name='fevox.db'):
		self.name, self.conexao = name, None


	def Connect(self):
		self.conexao = sqlite3.connect(self.name)


	def Disconnect(self):
		try:
			self.conexao.close()
		except AttributeError:
			pass


	def Create_user_table(self):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""
			CREATE TABLE IF NOT EXISTS user_login (
					id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				  	name TEXT NOT NULL,
					email TEXT NOT NULL,
                    pass_user TEXT NOT NULL
			);
			""")
		except AttributeError:
			pass
		self.Disconnect()


	def Insert_user(self, name, email, pass_user):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			try:
				cursor.execute("""
				INSERT INTO user_login (name, email, pass_user) VALUES (?,?,?);
				""", (name, email, pass_user))
				self.conexao.commit()
			except sqlite3.IntegrityError:
				pass
		except AttributeError:
			pass
		self.Disconnect()


	def Search_user(self, email, pass_user):
		self.Connect()
		try:
			cursor = self.conexao.cursor()
			cursor.execute("""SELECT * FROM user_login;""")
			if pass_user == None:
				for linha in cursor.fetchall():
					if linha[2] == email:
						return 'existe'
					else:
						pass
			else:			
				for linha in cursor.fetchall():
					if linha[2] == email:
						if linha[3] == pass_user:
							return ('sim', linha[1])
						else:
							return ('não', 'não')
					else:
						pass
				return ('não', 'não')

		except AttributeError:
			pass
		except sqlite3.OperationalError:
			pass
		self.Disconnect()

