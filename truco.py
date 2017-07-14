# -*- coding: cp1252 -*-
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

class Conexao(object):
        def bancoDados(self):
                cliente = MySQLdb.connect(host='localhost', user='usr', passwd='admin', db='truco')
                return cliente.cursor()

class TelaTransicao(ScreenManager):
	pass

class TelaLogin(Screen):
	resp = StringProperty()

	def login(self, nome, senha):

		var = "SELECT * FROM t_usuarios WHERE nome = '%s' and senha = '%s';"%(nome.text, md5.md5(senha.text.encode('utf-8')).hexdigest())

		if Conexao().bancoDados().execute(var):
			self.manager.get_screen('loby').label_text = nome.text
			self.manager.current = 'loby'
			Conexao().bancoDados().close()
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
			self.inf = 'Capo User Obrigatório!'
		elif se.text == '':
			self.inf = 'Capo Senha Obrigatório!'
		elif email.text == '':
			self.inf = 'Capo Email Obrigatório'

		if self.insert(no.text, md5.md5(se.text.encode('utf-8')).hexdigest(), email.text):
			self.manager.current = 'login'

		self.inf = 'Usuario ja cadastrado!'


	def insert(self, name, passw, email):

		cadastro = "INSERT INTO t_usuarios(nome, senha, email) VALUES('%s', '%s', '%s')"%(name, passw, email)
		try:
			Conexao().bancoDados().execute(cadastro)
			Conexao().bancoDados().close()
			return True
		except Exception as e:
			print(e)
			Conexao().bancoDados().rollback()

class MesaTruco(Screen):
	pass


documentoKV = Builder.load_file("truco.kv")

class truco(App):
	def build(self):
		return documentoKV

if __name__ == "__main__":
	truco().run()
