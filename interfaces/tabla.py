# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:15:29 2023

@author: yolexis
"""
from tkinter import ttk
from datetime import datetime


def tabla_selecc_clientes(ventana_venta,datos,ecab_1,ecab_2,ecab_3,ecab_4):            
    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 12))
    ventana_venta.datos_listados = datos
    ventana_venta.datos_listados.reverse()
    
    ventana_venta.tabla = ttk.Treeview(ventana_venta, columns = (('nombre'),('Apellidos', 150),('Edad',150)), height=10)
    ventana_venta.tabla.column("# 0", width=50)
    ventana_venta.tabla.column("# 1", width=230)
    ventana_venta.tabla.column("# 2", width=140)
    ventana_venta.tabla.column("# 3", width=140)
    ventana_venta.tabla.grid(row=7, column=8, padx=4, pady=3, rowspan=4, columnspan=4, sticky='nse')
          
    ventana_venta.tabla.heading('#0', text=ecab_1)
    ventana_venta.tabla.heading('#1', text=ecab_2)
    ventana_venta.tabla.heading('#2', text=ecab_3)
    ventana_venta.tabla.heading('#3', text=ecab_4)
   

    for p in ventana_venta.datos_listados:
        ventana_venta.tabla.insert('',4, text=p[0], values = (p[1],p[2],p[3]))  

#Seleccionar productos tabla ordenada por encabezado de columna
def tabla_selecc_prod(ventana_venta, datos, ecab_1, ecab_2, ecab_3, ecab_4):
    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 12))
    ventana_venta.datos_listados = datos[::-1]  # copia invertida

    columnas = ('nombre', 'apellidos', 'edad')
    ventana_venta.tabla = ttk.Treeview(
        ventana_venta,
        columns=columnas,
        height=20
    )

    ventana_venta.tabla.column("#0", width=50)
    ventana_venta.tabla.column("nombre", width=230)
    ventana_venta.tabla.column("apellidos", width=140)
    ventana_venta.tabla.column("edad", width=140)
    ventana_venta.tabla.grid(row=7, column=8, padx=4, pady=3, rowspan=4, columnspan=4, sticky='nse')

    # Encabezados con orden automático
    ventana_venta.tabla.heading('#0', text=ecab_1,
                                command=lambda: ordenar_tabla(ventana_venta.tabla, '#0'))
    ventana_venta.tabla.heading('nombre', text=ecab_2,
                                command=lambda: ordenar_tabla(ventana_venta.tabla, 'nombre'))
    ventana_venta.tabla.heading('apellidos', text=ecab_3,
                                command=lambda: ordenar_tabla(ventana_venta.tabla, 'apellidos'))
    ventana_venta.tabla.heading('edad', text=ecab_4,
                                command=lambda: ordenar_tabla(ventana_venta.tabla, 'edad'))

    # Insertar datos
    for p in ventana_venta.datos_listados:
        ventana_venta.tabla.insert('', 'end', text=p[0], values=(p[1], p[2], p[3]))


#Tabla ventana principal
def tabla_0(ventana, datos, ecab_1, ecab_2, ecab_3, ecab_4, ecab_5, ecab_6, ecab_7, buscar, nomb_tabla):
    datos_2 = []
    largo_fila = 0

    an = ventana.winfo_screenwidth()
    al = ventana.winfo_screenheight()         

    if buscar != '':
        for i in range(len(datos)):
            for j in range(len(datos[i])):
                if buscar in datos[i][j]:
                    datos_2.append(datos[i])
        if nomb_tabla == 'inventarios':
            total_inv = 0
            total_cantidad = 0
            total_peso = 0
            for i in range(len(datos_2)):
                total_inv += float(datos_2[i][5])
                total_cantidad += float(datos_2[i][3])
                total_peso += float(datos_2[i][4])
            total = ['-', 'Totales','', total_cantidad, total_peso, total_inv,'']
            datos_2.append(total)
    else:
        datos_2 = datos

    if len(datos_2) != 0:
        largo_fila = len(datos_2[0])
    else:
        largo_fila = 7

    if largo_fila < 7:
        control = 7 - largo_fila
        for i in range(len(datos_2)):
            for p in range(control):
                datos_2[i].append('-')

    style = ttk.Style()
    style.configure("Treeview", font=('Arial', int(an*0.007)))
    ventana.datos_listados = datos_2
    ventana.datos_listados.reverse()

    columnas = ('c1', 'c2', 'c3', 'c4', 'c5', 'c6')
    ventana.tabla = ttk.Treeview(
        ventana,
        columns=columnas,
        height=int(al*0.0415)
    )

    ventana.tabla.column("#0", width=int(an*0.03))
    ventana.tabla.column("c1", width=int(an*0.295))
    ventana.tabla.column("c2", width=int(an*0.1))
    ventana.tabla.column("c3", width=int(an*0.1))
    ventana.tabla.column("c4", width=int(an*0.1))
    ventana.tabla.column("c5", width=int(an*0.1))
    ventana.tabla.column("c6", width=int(an*0.1))
    ventana.tabla.grid(row=7, column=8, rowspan=4, columnspan=4, sticky='nse')

    # Encabezados con callback de orden automático
    ventana.tabla.heading('#0', text=ecab_1, command=lambda: ordenar_tabla(ventana.tabla, '#0'))
    ventana.tabla.heading('c1', text=ecab_2, command=lambda: ordenar_tabla(ventana.tabla, 'c1'))
    ventana.tabla.heading('c2', text=ecab_3, command=lambda: ordenar_tabla(ventana.tabla, 'c2'))
    ventana.tabla.heading('c3', text=ecab_4, command=lambda: ordenar_tabla(ventana.tabla, 'c3'))
    ventana.tabla.heading('c4', text=ecab_5, command=lambda: ordenar_tabla(ventana.tabla, 'c4'))
    ventana.tabla.heading('c5', text=ecab_6, command=lambda: ordenar_tabla(ventana.tabla, 'c5'))
    ventana.tabla.heading('c6', text=ecab_7, command=lambda: ordenar_tabla(ventana.tabla, 'c6'))

    # Scrollbar
    scrull = ttk.Scrollbar(orient='vertical', command=ventana.tabla.yview, cursor="hand2")
    scrull.place(x=int(an*0.156), y=int(al*0.067), height=int(al*0.84))
    scrull.set(0.0, 0.01)
    ventana.tabla.configure(yscrollcommand=scrull.set)

    # Insertar datos
    for p in ventana.datos_listados:
        ventana.tabla.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]))


# ==========================
# FUNCIONES DE ORDENACIÓN
# ==========================
def detectar_tipo(valor):
    """Detecta el tipo de dato automáticamente"""
    # Enteros
    try:
        return int(valor)
    except:
        pass
    # Flotantes
    try:
        return float(valor)
    except:
        pass
    # Fechas (YYYY-MM-DD)
    try:
        return datetime.strptime(valor, "%Y-%m-%d")
    except:
        pass
    # Texto por defecto
    return str(valor)


def ordenar_tabla(tree, col_id):
    """Ordena el Treeview automáticamente según el tipo de dato"""
    datos = [
        (tree.set(k, col_id) if col_id != '#0' else tree.item(k, 'text'), k)
        for k in tree.get_children('')
    ]

    datos_convertidos = [(detectar_tipo(val), k) for val, k in datos]

    datos_convertidos.sort(key=lambda t: t[0])

    # Alternar entre ascendente/descendente
    if getattr(tree, "_orden_inverso", False):
        datos_convertidos.reverse()
    tree._orden_inverso = not getattr(tree, "_orden_inverso", False)

    for index, (val, k) in enumerate(datos_convertidos):
        tree.move(k, '', index)