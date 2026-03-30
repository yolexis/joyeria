# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 10:27:07 2023

@author: yolexis
"""

import tkinter as tk
from interfaces.ventana_database import salva_database
from interfaces.datos_globales import crear_datos
from tkinter import messagebox
from interfaces.acerca_de import informacion



def menus_0(ventana):
    barra_menu = tk.Menu(ventana)
    ventana.config(menu = barra_menu, width=300, height=300)
    
    menu_inicio=tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='Inicio', menu=menu_inicio)    
    menu_inicio.add_command(label='Configuracion inicial', command=crear_datos)
   # menu_inicio.add_command(label='Eliminar Tabla de la base de datos', command=borrar_tabla)
    menu_inicio.add_command(label='Salir', command=ventana.destroy)
    
    menu_edicion=tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='Edicion', menu=menu_edicion)
    #menu_edicion.add_command(label='Crear base de datos', command=lambda:editar_usuario(ventana))
    menu_edicion.add_command(label='Realizar salva de datos', command=lambda:salva_database())
    
    menu_ayuda=tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='Ayuda', menu=menu_ayuda)
    menu_ayuda.add_command(label='Acerca de', command=lambda:informacion(ventana))    

