#!/bin/python
import mysql.connector
import string
import random


def main():
	global user
	user = User()
	o = user.setOption()
	if o in ("1", "2"):
		u = user.setUsername()
		p = user.setPassword()
		print p
	else:
		p = ""
		u = user.setUsername()
	mail = Mail()
	mail.sqlExec(o, u, p)

class User(object):
	def setOption(self):
		option = raw_input("""Choose option:\n1) Create user\n2) Update password\n3) Create alias\n4) Deactivate user\n: """)
		if option in ("1", "2", "3", "4"):
			return option
		else:
			self.setOption()
	def passGenerator(self,size=8, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))
	def setUsername(self):
		mailuser = raw_input("Enter Username : ")
		return mailuser
		if not mailuser:
			self.setUsername()
	def setPassword(self):
		password = raw_input("Enter Password or Enter for generate a new one : ")
		if not password:
			password = self.passGenerator()
			return password

class Mail():
	def sqlExec(self, option, mailuser, password):
		connection = mysql.connector.connect(host='10.0.0.13',database='mail',user='mail_admin',password='kadam2015',buffered=True)
		cursor = connection.cursor()
		self.mailuser = mailuser
		self.password = password
		if option == "1":
			homedir = "/"+self.mailuser
			cursor.execute("""INSERT INTO mailbox (username, password, maildir, domain, active) VALUES (%s, %s, %s, %s, %s)""", (self.mailuser, self.password, homedir, 'kadam.ru', 1,))
		elif option == "2":
			cursor.execute("""UPDATE mailbox SET password = %s where username = %s""", (self.password, self.mailuser,))
		elif option == "3": 
			alias = raw_input("Enter alias : ")
			addr = self.mailuser+"@kadam.ru"
			cursor.execute("""INSERT INTO alias (address, goto, active) VALUES (%s, %s, %s)""", (addr, alias, 1,))
		else:
			cursor.execute("""UPDATE mailbox SET active = 0 WHERE username = %s""", (self.mailuser,))
		cursor.close()
		connection.commit()
		connection.close()	

if __name__ == '__main__':
    main()
