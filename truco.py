import md5, random, MySQLdb
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.core.image import Image
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.uix.widget import Widget

#Window.size = (450, 250)

class TelaTransicao(ScreenManager):
	pass

class TelaLogin(Screen):
	resp = StringProperty()

	def login(self, nome, senha):
		cliente = MySQLdb.connect(host='localhost', user='root', passwd='toor', db='Truco')
		cursor = cliente.cursor()

		var = "SELECT * FROM T_Usuarios WHERE nome = '%s' and senha = '%s';"%(nome.text, md5.md5(senha.text).hexdigest())

		if cursor.execute(var):
			self.manager.get_screen('loby').label_text = nome.text
			self.manager.current = 'loby'
			cliente.close()
		else:
			self.resp = 'Usuario ou senha invalido!'

	def telas(self, tipo):
		if tipo == 'cadastro':
			self.manager.current = tipo

		elif tipo == 'sair':
			exit()

class TelaConfig(Screen):

	def volta(self):
		self.manager.get_screen('loby').bt1 = 'cfg.png'
		self.manager.current = 'loby'

class TelaLoby(Screen):
	label_text = StringProperty('')
	bt1 = StringProperty('cfg.png')
	bt2 = StringProperty('start.png')


	def buttonpress(self, tipe):
		if tipe == 'bt1':
			self.bt1 = 'config.png'
			self.manager.current = 'config'
		if tipe == 'bt2':
			self.manager.current = 'mesa'


class TelaCadastro(Screen):

	inf = StringProperty('')
	def criaUsuario(self, no, se, email):
		if no.text == '':
			self.inf = 'Capo User Obrigatorio!'
		elif se.text == '':
			self.inf = 'Capo Senha Obrigatorio!'
		elif email.text == '':
			self.inf = 'Capo Email Obrigatorio'

		if self.insert(no.text, md5.md5(se.text).hexdigest(), email.text):
			self.manager.current = 'login'

		self.inf = 'Usuario ja cadastrado!'


	def insert(self, name, passw, email):

		cliente = MySQLdb.connect(host='localhost', user='root', passwd='toor', db='Truco')

		r = "INSERT INTO T_Usuarios(nome, senha, email) VALUES('%s', '%s', '%s')"%(name, passw, email)
		try:
			cursor = cliente.cursor()
			cursor.execute(r)
			cliente.commit()
			cliente.close()
			return True
		except Exception as e:
			print(e)
			cliente.rollback()

class MesaTruco(Screen):
	pass


documentoKV = Builder.load_file("truco.kv")

class truco(App):
	def build(self):
		return documentoKV

if __name__ == "__main__":
	truco().run()



'''

	GridLayout:
		cols: 2

		Label:
            pos_hint:{'x':.4 'y':.1}
			text: 'usuario'
		TextInput:
			id: user
			text: 'admin'

		Label:
			text: 'Senha'
		TextInput:
			id: senha
			text: 'admin'
			password: True

        Button:
            text: 'Conectar'
            on_press: root.login(user, senha)

        Button:
            text: 'Sair'
'''
