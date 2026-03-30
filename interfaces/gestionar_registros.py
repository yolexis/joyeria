from models.conexion_sql import conectar
import tkinter as tk
import os
import sys
from utilidades.decisiones import confirmar, aceptar_error, aceptar_informacion
from interfaces.venta_productos import seleccionar_cliente
from interfaces.venta_productos_ferret import seleccionar_cliente_2
from interfaces.dev_productos import seleccionar_cliente_dev
from interfaces.pagar_productos import seleccionar_cliente_pagar
from interfaces.agregar_productos import insertar_productos
from interfaces.vale_entrada import vale_in
from datetime import datetime
from utilidades.recursos import resource_path
from models.consultas import productos_inv_2, ventas_devoluciones_editar
from tkinter import messagebox


def editar_elementos(id,table_name):
    
    try:
        conexion = conectar()
        sql = (f"select * from {table_name} where id={id}")
        conexion.execute(sql)
        datos = conexion.fetchone()
        column_names = [desc[0] for desc in conexion.description]
       
        conexion.close()

    except Exception as ex:
        titulo = "Diamante negro"
        mensaje = f"No se ha podido recuperar los datos:\n {ex}"
        aceptar_error(titulo,mensaje, ventana)

    
    
    def cancelar():
        ventana.destroy()

    #Guarda los cambios 
    def guardar():
        datos_nuevos=[id]           
        for i in range(1, len(datos)):            
            if i==1:
               datos_nuevos.append(a.get())
            if i==2:
               datos_nuevos.append(b.get())
            if i==3:
               datos_nuevos.append(c.get())
            if i==4:
               datos_nuevos.append(d.get())            
            if i==5:
               datos_nuevos.append(e.get())
            if i==6:
               datos_nuevos.append(f.get())
            if i==7:
               datos_nuevos.append(g.get())
            if i==8:
               datos_nuevos.append(h.get())
        
                 
        columns_names=tuple(column_names)
        control =validar_datos(datos_nuevos,columns_names)        
        datos_nuevos=tuple(datos_nuevos)
        condition = f"id = {id}"
        
        if control == True:                    
            try:
                conexion=conectar()                
                consulta, parametros = prepara_update_consulta(table_name, columns_names, datos_nuevos, condition)
                titulo = "Editar registro"
                mensaje = "Esta seguro que desea cambiar los valores del elemento seleccionado.\n Verifique los datos antes de dar click en aceptar"
                control = confirmar(titulo,mensaje, ventana)
                if control==True:
                    conexion.execute(consulta, parametros)
                    if table_name =="clientes_productos":                           
                        sql_2 = f"select cantidad, peso from productos where id = {datos[2]}"
                        conexion.execute(sql_2)
                        productos = conexion.fetchall()
                        cantidad = float(productos[0][0])+float(datos[3])-float(datos_nuevos[3])
                        peso = float(productos[0][1])+float(datos[5])-float(datos_nuevos[5])
                        sql_3 = f"update productos set cantidad = {cantidad}, peso = {peso} where id = {datos_nuevos[2]};"
                        conexion.execute(sql_3)

                    if table_name =="clientes_productos_ferret":
                        sql_2 = f"select cantidad from productos where id = {datos[2]}"
                        conexion.execute(sql_2)
                        productos = conexion.fetchall()
                        cantidad = float(productos[0][0])+float(datos[3])-float(datos_nuevos[3])
                        sql_3 = f"update productos set cantidad = {cantidad} where id = {datos_nuevos[2]};"
                        conexion.execute(sql_3)

                    if table_name =="devolucion_productos":
                        sql_2 = f"select cantidad, peso from productos where id = {datos[2]}"
                        conexion.execute(sql_2)
                        productos = conexion.fetchall()
                        cantidad = float(productos[0][0])-float(datos[3])+float(datos_nuevos[3])
                        peso = float(productos[0][1])-float(datos[5])+float(datos_nuevos[5])
                        sql_3 = f"update productos set cantidad = {cantidad}, peso = {peso} where id = {datos_nuevos[2]};"
                        conexion.execute(sql_3)

                    if table_name =="vale_entrada":
                        sql_2 = f"select cantidad, peso from productos where id = {datos[4]}"
                        conexion.execute(sql_2)
                        productos = conexion.fetchall()                        
                        cantidad = float(productos[0][0])-float(datos[3])+float(datos_nuevos[3])
                        peso = float(productos[0][1])-float(datos[2])+float(datos_nuevos[2])
                        sql_3 = f"update productos set cantidad = {cantidad}, peso = {peso} where id = {datos[4]};"
                        conexion.execute(sql_3)                    
                    titulo = "Editar registro"
                    mensaje = "Se han guardado los cambios realizados al registro"
                    aceptar_informacion(titulo,mensaje,ventana)
                    ventana.destroy()                                                       
            except Exception as ex:
                titulo = "Editar registro"
                mensaje = f"Ha ocurrido un error al editar el registroooo:\n{ex}"
                aceptar_error(titulo,mensaje,ventana)   

    #validacion de datos
    def validar_datos(arreglo,columnas):
        control = 0
        if table_name == "productos":
            for i in range(len(arreglo)):
                if arreglo[i] == '' :
                    titulo = "Editar productos"
                    mensaje = "No pueden haber campos vacios"
                    aceptar_error(titulo,mensaje,ventana)
                    control = 1

        if 'estado'  in columnas:
            posicion = columnas.index('estado')
            if arreglo[posicion] != '8k' and arreglo[posicion] != '10k' and arreglo[posicion] != 'Ag' and arreglo[posicion] != '':
                titulo = "Editar productos"
                mensaje = "El campo Tipo de productos solo puede tomar los valores:\n (8k), (10k), (Ag) o estar vacío"
                aceptar_error(titulo,mensaje,ventana)
                control = 1    
        
        if 'carnet'  in columnas:
            posicion = columnas.index('carnet')
            try:
                valor = int(arreglo[posicion])
            except Exception as ex:
                control = 1
                titulo = "Editar registros"
                mensaje = "El campo carnet debe ser un entero"
                aceptar_error(titulo, mensaje,ventana)

            if len(arreglo[posicion]) != 11:
                titulo = "Editar productos"
                mensaje = "El campo carnet debe tener 11 dígitos"
                aceptar_error(titulo,mensaje,ventana)
                control = 1 
        
        if table_name == 'clientes_productos' or table_name=='devolucion_productos':
            #controlar edicion 
            cant_dispon = ventas_devoluciones_editar(arreglo[2],arreglo[1])
            if table_name == 'clientes_productos':         
                if float(datos[3])-float(arreglo[3])>float(cant_dispon[0][1]):
                    messagebox.showerror('Error edición',f'No se puede editar este registro, la cantidad disponible del cliente no lo permite: \n{cant_dispon[0][1]}',parent=ventana)
                    control = 1
                if float(datos[3])-float(arreglo[3])==float(cant_dispon[0][1]):
                    if float(datos[5])-float(arreglo[5])!=float(cant_dispon[0][3]):
                        messagebox.showerror('Error edición',f'Si al editar el registro utiliza la cantidad disponible para el cliente: {cant_dispon[0][1]},\ntambien debe utilizar el peso disponible: {cant_dispon[0][3]}',parent=ventana)
                        control = 1

                if float(datos[5])-float(arreglo[5])>float(cant_dispon[0][3]):
                    messagebox.showerror('Error edición',f'No se puede editar este registro, el peso disponible del cliente no lo permite {cant_dispon[0][3]}',parent=ventana)
                    control = 1
                if float(datos[5])-float(arreglo[5])==float(cant_dispon[0][3]):
                    if float(datos[3])-float(arreglo[3])!=float(cant_dispon[0][1]):
                        messagebox.showerror('Error edición',f'Si al editar el registro utiliza el peso disponible para el cliente: {cant_dispon[0][3]},\ntambien debe utilizar la cantidad disponible: {cant_dispon[0][1]}',parent=ventana)
                        control = 1

            if table_name=='devolucion_productos':
                if float(arreglo[3])-float(datos[3])>float(cant_dispon[0][1]):
                    messagebox.showerror('Error edición','No se puede editar este registro, la cantidad disponible del cliente no lo permite',parent=ventana)
                    control = 1
                if float(arreglo[3])-float(datos[3])==float(cant_dispon[0][1]):
                    if float(arreglo[5])-float(datos[5])!=float(cant_dispon[0][3]):
                        messagebox.showerror('Error edición',f'Si al editar el registro utiliza la cantidad disponible para el cliente: {cant_dispon[0][1]},\ntambien debe utilizar el peso disponible: {cant_dispon[0][3]}',parent=ventana)
                        control = 1

                if float(arreglo[5])-float(datos[5])>float(cant_dispon[0][3]):
                    messagebox.showerror('Error edición','No se puede editar este registro, el peso disponible del cliente no lo permite',parent=ventana)
                    control = 1 
                if float(arreglo[5])-float(datos[5])==float(cant_dispon[0][3]):
                    if float(arreglo[3])-float(datos[3])!=float(cant_dispon[0][1]):
                        messagebox.showerror('Error edición',f'Si al editar el registro utiliza el peso disponible para el cliente: {cant_dispon[0][3]},\ntambien debe utilizar la cantidad disponible: {cant_dispon[0][1]}',parent=ventana)
                        control = 1

            #comprobar valores acorde a la entrada esperada
            try:
                datetime.strptime(arreglo[7], '%Y-%m-%d').date()               
            except Exception as ex:
                control=1
                messagebox.showerror('Validando', f'Escriba una fecha válida Ej: 2025-01-31\n{ex}',parent=ventana)
            
            try:
                float(arreglo[3])
                float(arreglo[4])
                float(arreglo[5])
            except Exception as ex:
                control=1
                messagebox.showerror('Validando',f'Los valores precio, peso y cantidad deben ser del tipo número\n{ex}',parent=ventana)
                   
            #comprobar q sean valores numericos positivos             
            if float(arreglo[3])<0 or float(arreglo[4])<=0 or float(arreglo[5])<0:
                control=1
                messagebox.showerror('Validando','Los valores precio, peso y cantidad deben se mayores que cero',parent=ventana)        
            
            for i in range(len(arreglo)):
                if arreglo[i] == '' and i!=6 and i!=8:
                    titulo = "Editar productos"
                    mensaje = "No pueden haber campos vacios"
                    messagebox.showerror(titulo,mensaje,parent=ventana)
                    control = 1
                if arreglo[i] == '' and i==6:
                    arreglo[i]=None

                if arreglo[i] == '' and i==8:
                    arreglo[i]=None


        if table_name == 'vale_entrada':
            inventario = productos_inv_2(arreglo[4])
            #comprobar valores acorde a la entrada esperada
            try:
                datetime.strptime(arreglo[1], '%Y-%m-%d').date()               
            except Exception as ex:
                control=1
                messagebox.showerror('Validando',f'Escriba una fecha válida Ej: 2025-01-31\n{ex}',parent=ventana)
            
            try:
                float(arreglo[2])
                float(arreglo[3])
            except Exception as ex:
                control=1
                messagebox.showerror('Validando',f'Los valores peso y cantidad deben ser del tipo número\n{ex} ',parent=ventana)
                   
            #comprobar q sean valores numericos positivos             
            if float(arreglo[3])<0 or float(arreglo[2])<0:
                control=1
                messagebox.showerror('Validando','Los valores peso y cantidad deben ser igual o  mayores que cero',parent=ventana)        

            for i in range(len(arreglo)):
                if arreglo[i] == '' and i!=6 and i!=5:
                    titulo = "Editar productos"
                    mensaje = "No pueden haber campos vacios"
                    messagebox.showerror(titulo,mensaje,parent=ventana)
                    control = 1    
                if arreglo[i] == '' and i==5:
                    arreglo[i]=None

                if arreglo[i] == '' and i==6:
                    arreglo[i]=None
            
            #Comprobar cantidad disponible para editar
            limite_peso = float(datos[2])-float(inventario[0][2])
            limite_cant = float(datos[3])-float(inventario[0][1]) 
            
            if float(datos[2])-float(arreglo[2])>float(inventario[0][2]):
                messagebox.showerror('Error de edición',f'No puede realizar esta operación con los valores proporcionados.\nEl peso límite inferior es: {limite_peso}',parent=ventana)
                control = 1
            if float(datos[2])-float(arreglo[2])==float(inventario[0][2]):                
                if float(datos[3])-float(arreglo[3])!=float(inventario[0][1]):                    
                    messagebox.showerror('Error de edición',f'No puede realizar esta operación con los valores proporcionados.\nSi utiliza el peso límite inferior: {limite_peso}.\nDebe utilizar la cantidad límite inferior: {limite_cant}',parent=ventana)
                    control = 1
            
            if float(datos[3])-float(arreglo[3])>float(inventario[0][1]):
                messagebox.showerror('Error de edición',f'No puede realizar esta operación con los valores proporcionados.\nLa cantidad límite inferior es: {limite_cant}',parent=ventana)
                control = 1
            if float(datos[3])-float(arreglo[3])==float(inventario[0][1]):
                if float(datos[2])-float(arreglo[2])!=float(inventario[0][2]):
                    messagebox.showerror('Error de edición',f'No puede realizar esta operación con los valores proporcionados.\nSi utiliza la cantidad límite inferior: {limite_cant}.\nDebe utilizar el peso límite inferior: {limite_peso}',parent=ventana)
                    control = 1           
            

        if table_name == 'clientes_productos':
            prod = productos_inv_2(arreglo[2])
            cantidad=prod[0][1]+datos[3]
            if cantidad-float(arreglo[3])<0:
                control=1
                messagebox.showerror('Validando',f'La cantidad disponible para la venta\nde este producto es: {cantidad}',parent=ventana)  
            
            peso=prod[0][2]+datos[5]
            if peso-float(arreglo[5])<0:
                control=1
                messagebox.showerror('Validando',f'El peso disponible para la venta\nde este producto es: {peso}',parent=ventana)  

            if cantidad-float(arreglo[3])==0.0:
               if peso-float(arreglo[5])!=0.0:
                   control = 1
                   messagebox.showerror('Validando',f'Revise cantidad y peso, si el peso cuando vende queda en cero\nlas cantidades tambien deben ser ceros y viceversa\nDisponibilidad\nCantidad: {cantidad}\nPeso: {peso}',parent=ventana)                
            
            if peso-float(arreglo[5])==0.0:
                if cantidad-float(arreglo[3])!=0.0:
                   control = 1
                   messagebox.showerror('Validando',f'Revise cantidad y peso, si el peso cuando vende queda en cero\nlas cantidades tambien deben ser ceros y viceversa\nDisponibilidad\nCantidad: {cantidad}\nPeso: {peso}',parent=ventana)                
        
        if table_name=='devolucion_productos':
            cantidad=datos[3]
            if cantidad-float(arreglo[3])<0:
                control=1
                messagebox.showerror('Validando',f'Este cliente puede hacer devoluciones\npara este producto de hasta: {cantidad} unidades',parent=ventana)  
            
            peso=datos[5]
            if peso-float(arreglo[5])<0:
                control=1
                messagebox.showerror('Validando',f'El peso disponible para devoluciones\nde este producto es: {peso}',parent=ventana)  
            
            if cantidad-float(arreglo[3])==0:
                if peso-float(arreglo[5])!=0:
                   control = 1
                   messagebox.showerror('Validando',f'Revise cantidad y peso, si el peso cuando devuelve queda en cero\nlas cantidades tambien deben ser ceros y viceversa\nDisponibilidad\nCantidad: {cantidad}\nPeso: {peso}',parent=ventana)                
            
            if peso-float(arreglo[5])==0:
                if cantidad-float(arreglo[3])!=0:
                   control = 1
                   messagebox.showerror('Validando',f'Revise cantidad y peso, si el peso cuando vende queda en cero\nlas cantidades tambien deben ser ceros y viceversa\nDisponibilidad\nCantidad: {cantidad}\nPeso: {peso}',parent=ventana)                
        
        if table_name=='productos':
            if arreglo[7]!='Joyeria' and arreglo[7]!='Alimento' and arreglo[7]!='Ferreteria':
                messagebox.showerror('Validando','Verifique el campo categoría, este puede tomar los valores:\n1-Alimentos\n2-Joyeria\n3-Ferreteria',parent=ventana)
                control = 1
            if arreglo[6]!='8k' and arreglo[6]!='10k' and arreglo[6]!='Ag':
                messagebox.showerror('Validando','Verifique el campo estado, este puede tomar los valores:\n1-8k\n2-10k\n3-Ag',parent=ventana)
                control = 1
                
        if control == 0:
            return True
          

    alto_ventana = (len(datos)-1)*73+70
    control_filas = 0

    ventana = tk.Tk()                             
    ventana.title('Editar registros')
    ventana.geometry(f'430x{alto_ventana}')
    ventana.config(bg="#649be2")
    ventana.resizable(width=0, height=0)    
    #utl.centrar_ventana(ventana,430,alto_ventana)
    ventana.attributes('-topmost', True)
    icono = resource_path("imagenes/data_base.ico")
    ventana.iconbitmap(icono)    
    
    #creando campos para editar    
    for i in range(1, len(datos)):
       if i < len(datos):
            j=tk.Label(ventana,font=("arial", 16), text=f"{column_names[i]}:")
            j.config(bg="#649be2", relief="sunken",justify="left")
            j.grid(column=0, row=control_filas,pady=5)
            control_filas=control_filas+1
            if i==1:
                valor_v = tk.StringVar(ventana, datos[i])
                a=tk.Entry(ventana,font=("arial", 12), textvariable=valor_v)
                a.config(width=45)
                if table_name == 'clientes_productos' or table_name=='devolucion_productos' or table_name == 'clientes_productos_ferret':
                    a.config(state='disabled')
                a.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                                
                control_filas=control_filas+1

            if i==2:
                valor_v = tk.StringVar(ventana, datos[i])
                b=tk.Entry(ventana,font=("arial", 12), textvariable=valor_v)
                b.config(width=45)
                if table_name == 'clientes_productos' or table_name=='devolucion_productos' or table_name == 'clientes_productos_ferret':
                    b.config(state='disabled')
                b.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                control_filas=control_filas+1

            if i==3:
                valor_v = tk.StringVar(ventana, datos[i])
                c=tk.Entry(ventana,font=("arial", 12), textvariable=valor_v)
                c.config(width=45)
                c.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                control_filas=control_filas+1
            
            if i==4:
                valor_v = tk.StringVar(ventana, datos[i])
                d=tk.Entry(ventana,font=("arial", 12), textvariable=valor_v)
                d.config(width=45)
                if table_name=='devolucion_productos' or table_name=='productos' or table_name=='vale_entrada':
                    d.config(state='disabled')
                d.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                control_filas=control_filas+1

            if i==5:
                valor_v = tk.StringVar(ventana, datos[i])
                e=tk.Entry(ventana,font=("arial", 12), textvariable=valor_v)
                e.config(width=45)
                if table_name=='productos' or table_name == 'clientes_productos_ferret' or table_name=='vale_entrada':
                    e.config(state='disabled')
                e.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                control_filas=control_filas+1

            if i==6:
                valor_v = tk.StringVar(ventana, datos[i])
                f=tk.Entry(ventana,font=("arial", 12), textvariable=valor_v)
                f.config(width=45)
                if table_name=='devolucion_productos' or table_name=='clientes_productos' or table_name=='vale_entrada':
                    f.config(state='disabled')
                f.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                control_filas=control_filas+1

            if i==7:
                valor_v = tk.StringVar(ventana, datos[i])
                g=tk.Entry(ventana,font=("arial", 12), textvariable=valor_v)
                g.config(width=45)
                if table_name=='devolucion_productos' or table_name=='clientes_productos':
                    g.config(state='disabled')                
                g.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                control_filas=control_filas+1

            if i==8:
                valor_v = tk.StringVar(ventana, datos[i])
                h=tk.Entry(ventana,font=("arial", 12), textvariable=valor_v)
                h.config(width=45)
                if table_name=='devolucion_productos' or table_name=='clientes_productos':
                    h.config(state='disabled')
                h.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                control_filas=control_filas+1
       
    boton_0 = tk.Button(ventana, command=lambda:guardar())
    boton_0.config(bg="LimeGreen", activebackground="SpringGreen", fg="White", relief="groove", font=("arial", 12, 'bold')
                   , width=15,justify='center', border=5, text='Guardar')
    boton_0.grid(row=control_filas, column=0, padx=15, pady=10)
           
    
    titulo = "Cancelar"
    mensaje = "Desea cancelar la insercion de datos"
    boton_0 = tk.Button(ventana, text='Cancelar', width=15,justify='center', border=5, command=cancelar)
    boton_0.config(bg="Crimson", activebackground="Red", fg="White", relief="groove", font=("arial", 12, 'bold'))
    boton_0.grid(row=control_filas, column=1)

    ventana.mainloop()


def prepara_update_consulta(table_name, columns_tuple, values_tuple, condition):    
    
    if len(columns_tuple) != len(values_tuple):
        raise ValueError("Las tuplas de columnas y valores deben tener la misma longitud")
    
    # Generar la parte SET de la consulta
    set_clause = ", ".join([f"{col} = %s" for col in columns_tuple])
    
    # Construir la consulta completa
    query = f"UPDATE {table_name} SET {set_clause} WHERE {condition} RETURNING *"
    
    # Los parámetros son los valores de la tupla
    params = values_tuple
    
    return query, params

def insertar_registros(table_name):
    if table_name == 'clientes_productos':
        seleccionar_cliente(table_name)

    elif table_name == 'clientes_productos_ferret':
        seleccionar_cliente_2(table_name)

    elif table_name == 'devolucion_productos':
        seleccionar_cliente_dev(table_name)

    elif table_name == 'pagar_venta_joyeria':
        seleccionar_cliente_pagar(table_name)

    elif table_name== 'productos':
        insertar_productos()

    elif table_name== 'vale_entrada':
        vale_in()
    
    else:    
        try:
            conexion = conectar()
            sql = (f"select * from {table_name}")
            conexion.execute(sql)
            datos = conexion.fetchone()
            column_names = [desc[0] for desc in conexion.description]
           
            conexion.close()
    
        except Exception as ex:
            titulo = "Diamante negro"
            mensaje = f"No se ha podido recuperar los datos:\n {ex}"
            aceptar_error(titulo,mensaje,ventana)
        
        def cancelar():
            ventana.destroy()
    
    
        #Guarda los cambios 
        def guardar():
            datos_nuevos=[0]           
            for i in range(1, len(datos)):            
                if i==1:
                   datos_nuevos.append(a.get())
                if i==2:
                   datos_nuevos.append(b.get())
                if i==3:
                   datos_nuevos.append(c.get())
                if i==4:
                   datos_nuevos.append(d.get())            
                if i==5:
                   datos_nuevos.append(e.get())
                if i==6:
                   datos_nuevos.append(f.get())
                if i==7:
                   datos_nuevos.append(g.get())
                if i==8:
                   datos_nuevos.append(h.get())
    
            columns_names=tuple(column_names)
            datos_nuevos=tuple(datos_nuevos)
            prep_sql = column_names[1:]
            set_clause = ", ".join([f"{col}" for col in prep_sql])
            control =validar_productos(datos_nuevos,columns_names) 
            if control == True:                    
                try:
                    conexion=conectar()
                    sql_1= f"INSERT INTO {table_name} ({set_clause}) VALUES {datos_nuevos[1:]};" 
                    titulo = "Añadir registro"
                    mensaje = "Esta seguro que desea añadir la nueva información.\n Verifique los datos antes de dar click en aceptar"
                    control = confirmar(titulo,mensaje, ventana)
                    if control==True:
                        conexion.execute(sql_1)
                        titulo = "Añadir registro"
                        mensaje = "Se han guardado los cambios realizados al registro"
                        aceptar_informacion(titulo,mensaje,ventana)
                        ventana.destroy()                                                       
                except Exception as ex:
                    titulo = "Añadir registro"
                    mensaje = f"Ha ocurrido un error al añadir el registro:\n{ex}"
                    aceptar_error(titulo,mensaje,ventana)   
    
        #validacion de datos
        def validar_productos(arreglo,columnas):
            control = 0
            for i in range(len(arreglo)):
                if arreglo[i] == '' :
                    titulo = "Editar productos"
                    mensaje = "No pueden haber campos vacios"
                    aceptar_error(titulo,mensaje,ventana)
                    control = 1
    
            if 'estado'  in columnas:
                posicion = columnas.index('estado')
                if arreglo[posicion] != '8k' and arreglo[posicion] != '10k' and arreglo[posicion] != 'Ag' and arreglo[posicion] != '':
                    titulo = "Editar productos"
                    mensaje = "El campo Tipo de productos solo puede tomar los valores:\n (8k), (10k), (Ag) o estar vacío"
                    aceptar_error(titulo,mensaje,ventana)
                    control = 1    
            
            if 'carnet'  in columnas:
                posicion = columnas.index('carnet')
                try:
                    valor = int(arreglo[posicion])
                except Exception as ex:
                    control = 1
                    titulo = "Editar registros"
                    mensaje = "El campo carnet debe ser un entero"
                    aceptar_error(titulo, mensaje,ventana)
    
                if len(arreglo[posicion]) != 11:
                    titulo = "Editar productos"
                    mensaje = "El campo carnet debe tener 11 dígitos"
                    aceptar_error(titulo,mensaje,ventana)
                    control = 1               
    
            if control == 0:
                return True
              
    
        alto_ventana = (len(datos)-1)*73+70
        control_filas = 0
    
        ventana = tk.Tk()                             
        ventana.title('Añadir registros')
        ventana.geometry(f'430x{alto_ventana}')
        ventana.config(bg="#649be2")
        ventana.resizable(width=0, height=0)    
        #utl.centrar_ventana(ventana,430,alto_ventana)
        ventana.attributes('-topmost', True)
    
        #direccion absoluta de recursos        
        def resourse_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
        icono = resourse_path("imagenes/data_base.ico")
        ventana.iconbitmap(icono)    
        
        #creando campos para editar    
        for i in range(1, len(datos)):        
           if i < len(datos):
                j=tk.Label(ventana,font=("arial", 16), text=f"{column_names[i]}:")
                j.config(bg="#649be2", relief="sunken",justify="left")
                j.grid(column=0, row=control_filas,pady=5)
                control_filas=control_filas+1
                if i==1:
                    a=tk.Entry(ventana,font=("arial", 12))
                    a.config(width=45)
                    a.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                    control_filas=control_filas+1
    
                if i==2:
                    b=tk.Entry(ventana,font=("arial", 12))
                    b.config(width=45)
                    b.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                    control_filas=control_filas+1
    
                if i==3:
                    c=tk.Entry(ventana,font=("arial", 12))
                    c.config(width=45)
                    c.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                    control_filas=control_filas+1
                
                if i==4:
                    d=tk.Entry(ventana,font=("arial", 12))
                    d.config(width=45)
                    d.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                    control_filas=control_filas+1
    
                if i==5:
                    e=tk.Entry(ventana,font=("arial", 12))
                    e.config(width=45)
                    e.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                    control_filas=control_filas+1
    
                if i==6:
                    f=tk.Entry(ventana,font=("arial", 12))
                    f.config(width=45)
                    f.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                    control_filas=control_filas+1
    
                if i==7:
                    g=tk.Entry(ventana,font=("arial", 12))
                    g.config(width=45)
                    g.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                    control_filas=control_filas+1
    
                if i==8:
                    h=tk.Entry(ventana,font=("arial", 12))
                    h.config(width=45)
                    h.grid(column=0, row=control_filas,padx=12,pady=5, columnspan=2)
                    control_filas=control_filas+1
           
        boton_0 = tk.Button(ventana, command=lambda:guardar())
        boton_0.config(bg="LimeGreen", activebackground="SpringGreen", fg="White", relief="groove", font=("arial", 12, 'bold')
                       , width=15,justify='center', border=5, text='Guardar')
        boton_0.grid(row=control_filas, column=0, padx=15, pady=10)
               
        
        titulo = "Cancelar"
        mensaje = "Desea cancelar la insercion de datos"
        boton_0 = tk.Button(ventana, text='Cancelar', width=15,justify='center', border=5, command=cancelar)
        boton_0.config(bg="Crimson", activebackground="Red", fg="White", relief="groove", font=("arial", 12, 'bold'))
        boton_0.grid(row=control_filas, column=1)
    
        ventana.mainloop()

def borrar_registros(id,tabla):
    control = 0
    titulo = 'Eliminar registro'
    mensaje = ''
    if tabla == 'clientes_productos' or tabla == 'devolucion_productos':
        conexion = conectar()
        sql = f'select * from {tabla} where id = {id}'
        conexion.execute(sql)
        datos = conexion.fetchall()
        if float(datos[0][3])!=0.0 or float(datos[0][5])!=0.0:
            control = 1
            mensaje = 'No se puede eliminar una venta activa. Para eliminar:\n1-Edítela haciendo que los valores cantidad y peso sean igual a 0\n2-Seleccione la venta y haga clic en eliminar'
        if datos[0][6]!=None:
            control = 1
            mensaje = 'Este vale de venta sirve de testigo de Inventario inicial\npara el mes, y no puede ser borrado'
    if tabla == 'clientes_productos_ferret':
        conexion = conectar()
        sql = f'select * from {tabla} where id = {id}'
        conexion.execute(sql)
        datos = conexion.fetchall()
        if float(datos[0][3])!=0.0:
            control = 1
            mensaje = 'No se puede eliminar una venta activa. Para eliminar:\n1-Edítela haciendo que cantidad sea igual a 0\n2-Seleccione la venta y haga clic en eliminar'
    
    if tabla =='productos' or tabla =='clientes':
        try:
            conexion = conectar()
            sql = f'select * from {tabla}'
            conexion.execute(sql)
            datos = conexion.fetchall()
        except Exception as ex:
            messagebox.showerror('Borrar', 'No se han podido verificar los datos para eliminar: {ex}')
        if len(datos)<2:
            control = 1    

    if tabla == 'vale_entrada':
        try:
            conexion = conectar()
            sql = f'select * from {tabla} where id = {id}'
            conexion.execute(sql)
            datos = conexion.fetchall()            
        except Exception as ex:
            messagebox.showerror('!!!Error!!!!', f'No se han recuperado los datos:\n{ex}')
        if float(datos[0][3])!=0.0 or float(datos[0][2])!=0.0:
            control = 1
            mensaje = 'No se puede eliminar un vale activo. Para eliminar:\n1-Edítela haciendo que los valores cantidad y peso sean igual a 0\n2-Seleccione el vale y haga clic en eliminar'
        
    if control==0:
        titulo = "Eliminar registro"
        mensaje = "Esta seguro de querer eliminar el registro"
        control = messagebox.askokcancel(titulo,mensaje)
        if control == True:        
            try:
                conexion = conectar()
                sql = (f"delete from {tabla} where id = {id}")
                conexion.execute(sql)
                titulo = "Eliminar registro"
                mensaje = "Se ha eliminado el registro correctamente"
                conexion.close 
                messagebox.showinfo(titulo,mensaje)        
            except Exception as ex:
                titulo = "Eliminar registro"
                mensaje = f"No se ha eliminado el registro:\n {ex}"        
                messagebox.showerror(titulo,mensaje)
    else:
        messagebox.showerror(titulo,mensaje)