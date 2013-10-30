# -*- coding: utf-8 -*-

import sqlite3

def connect():
	"""
	Conecta la base de datos con el programa
	"""
	#Connect with the database
	con = sqlite3.connect("pos2.db")
	con.row_factory = sqlite3.Row
	return con

def get_products():
	"""
	Obtiene productos
	"""
	con = connect()
	c = con.cursor()
	query = """SELECT name, supplier_code, gross_price FROM product WHERE id < 51"""
	result = c.execute(query)
	products = result.fetchall()
	con.close()
	return products

def get_users():
	"""
	Obtiene Usuarios
	"""
	con = connect()
	c = con.cursor()
	query = """SELECT username FROM auth_user"""
	result = c.execute(query)
	users = result.fetchall()
	con.close()
	return users