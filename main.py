# -*- coding: utf-8 -*-

import kivy
import controller
kivy.require('1.7.2') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.event import EventDispatcher


class row(BoxLayout):
	name = ObjectProperty(None)
	code = ObjectProperty(None)
	quantity = ObjectProperty(None)
	close = ObjectProperty(None)
	add = ObjectProperty(None)
	priceU = ObjectProperty(None)
	priceT = ObjectProperty(None)
	counter = 1
	price = ""

class CBoton (Button):
	name = ""
	code = ""
	price = ""


class Interfaz(BoxLayout):
	listA = []
	cost = 0

	def __init__(self,**kwargs):
		#Inicializacion de la interfaz
		super(Interfaz, self).__init__(**kwargs)
		#Definicion de Variables
		listB = []
		aux = 1
		box = ObjectProperty(None)
		txt = ObjectProperty(None)
		grid = ObjectProperty(None)
		discount = ObjectProperty(None)
		total = ObjectProperty(None)
		save = ObjectProperty(None)
		printAct = ObjectProperty(None)
		send = ObjectProperty(None)
		money = ObjectProperty(None)
		self.discount.bind(is_open = self.addDiscount)
		products = controller.get_products()
		users = controller.get_users()
		self.save.background_color = 0,147,0,.5
		self.send.background_color = 162,0,170,.5
		self.printAct.background_color = 162,0,170,.5
		#Ingreso de usuarios al Spinner
		for i in users:
			listB.append(i[0])
		self.txt.text = listB[0]
		self.txt.values = listB
		#Ingreso de productos a la listA deslizante
		for fila in products:
			Q = CBoton()
			Q.background_color = 1,1,1,(aux%2+0.5)
			aux = aux+1
			Q.name = fila[0]
			Q.text = fila[0][:20]
			Q.code = fila[1]
			Q.precio = fila[2]
			Q.bind(on_press = self.addRow)
			self.grid.add_widget(Q)
			self.grid.bind(minimum_width=self.grid.setter('width'))



	def addRow(interfaz,self):#Agrega productos a la grid
		test = True
		temp = row()
		temp.name.text = (self.text)
		temp.code.text = (self.code)
		temp.priceU.text = ("$ "+str(self.precio))
		temp.precio = self.precio
		temp.priceT.text = format_price(self.precio*temp.counter)
		temp.close.bind(on_press= interfaz.removeStuff)
		temp.add.bind(on_press = interfaz.moarStuff)
		for tmp in interfaz.listA:
			if tmp.name.text == self.text:
				tmp.counter = tmp.counter + 1
				tmp.quantity.text = str(tmp.counter)
				tmp.priceT.text = format_price(self.precio*tmp.counter)
				test = False
				setPrice(interfaz)
		if test == True:
			interfaz.listA.append(temp)
			interfaz.box.add_widget(temp)
			interfaz.box.bind(minimum_height=interfaz.box.setter('height'))
			setPrice(interfaz)
		test = True

	def moarStuff(interfaz, self):#Agrega mas productos a elementos de la grid, mediante el boton
		self.parent.counter = self.parent.counter +1
		self.parent.quantity.text = str(self.parent.counter)
		self.parent.priceT.text = format_price(self.parent.precio*self.parent.counter)
		setPrice(interfaz)

	def removeStuff(interfaz,self):#Reduce y elimina productos de la grid
		self.parent.counter = self.parent.counter - 1
		self.parent.quantity.text = str(self.parent.counter)
		self.parent.priceT.text = format_price(self.parent.precio*self.parent.counter)
		if self.parent.counter == 0:
			interfaz.box.remove_widget(self.parent)
			interfaz.listA.remove(self.parent)
		setPrice(interfaz)

	def addDiscount(interfaz,self, value):
		temp = interfaz.cost
		if temp == 0:
			pass
		if value == False:
			if float(self.text) > 0:
				temp = interfaz.cost - ((interfaz.cost)*int(self.text))/100
				interfaz.total.text = format_price(temp)
			if float(self.text) == 0:
				interfaz.total.text = format_price(interfaz.cost)

	def calcDiscount(self):
		self.addDiscount(self.discount,False)


def setPrice(interfaz):#Sets prices
	temp = 0
	#print(interfaz.money.text)
	for i in interfaz.listA:
		temp = temp + i.precio*i.counter
	interfaz.money.text = format_price(temp)
	interfaz.cost = temp
	interfaz.calcDiscount()

def format_float(n, decimals=1):
    """float -> string"""
    t = {",": ".", ".": ","}
    return "".join(t.get(c, c) for c in format(n, ",.{}f".format(decimals)))


def format_price(p, sym="$", decimals=0):
    """int -> string"""
    if sym == "CL":
        sym = "$"
    return u"{0} {1}".format(sym, format_float(p, decimals=decimals))



def Check(self):
	if self.listA.__contains__(self.text)==True:
		pass

class BetaUiApp(App):
	def build(self):
		return Interfaz()


if __name__ =='__main__':
	BetaUiApp().run()