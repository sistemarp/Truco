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

class BancoDados(object):
	def bancoDB(self, var):
		try:
			banco = MySQLdb.connect(host='localhost', user='root', passwd='toor', db='Truco')
			cursor = banco.cursor()
			cursor.execute(var)
			banco.commit()
			banco.close()
			return cursor
		except Exception as e:
			return str(e)



class TelaTransicao(ScreenManager):
	pass

class TelaLogin(Screen):
	resp = StringProperty()

	def login(self, nome, senha):
		conecta = "SELECT * FROM T_Usuarios WHERE nome = '%s' and senha = '%s';"%(nome, md5.md5(senha).hexdigest())
		grava = BancoDados().bancoDB(conecta)

		if grava.fetchall() != ():
			self.manager.get_screen('loby').label_text = nome
			self.manager.current = 'loby'

		else:
			self.resp = 'Usuario ou senha invalido!'

	def telas(self, tipo):
		if tipo == 'cadastro':
			self.manager.current = tipo

		elif tipo == 'sair':
			truco().on_stop()

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
	def criaUsuario(self, no, se, em):
		if no == '':
			self.inf = 'Capo User Obrigatorio!'
		elif se == '':
			self.inf = 'Capo Senha Obrigatorio!'
		elif em == '':
			self.inf = 'Capo Email Obrigatorio'
		elif '@' and '.' not in em:
			self.inf = 'Email invalido!'
		else:
			self.cadastra(no, se, em)

	def cadastra(self, name, password, email):

		self.nome = name
		self.senha =  md5.md5(password).hexdigest()
		self.ema = email

		conecta = "INSERT INTO T_Usuarios(nome, senha, email) VALUES('%s', '%s', '%s')"%(self.nome, self.senha, self.ema)
		grava = BancoDados().bancoDB(conecta)

		if grava:
			if 'Duplicate entry' in grava:
				usr = grava.split(' ')[3]
				self.inf = 'Usuario %s ja cadastrado!'%usr

			else:
				self.manager.current = 'login'

class MesaTruco(Screen):
	pass


documentoKV = Builder.load_file("truco.kv")

class truco(App):
	def build(self):
		return documentoKV

	#def on_stop(self):
	#	return True

if __name__ == "__main__":
	truco().run()
