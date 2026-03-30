from models.conexion_sql import conectar
import tkinter as tk
from interfaces.tabla import tabla_selecc_clientes, tabla_selecc_prod
from utilidades.decisiones import aceptar_error,confirmar
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
from utilidades.validar import *
from models.consultas import ventas_devoluciones, productos_inv, productos_activos, act_prod_dev, comprobar_inv
from itertools import chain
from utilidades.recursos import resource_path
import customtkinter as ctk


def seleccionar_cliente_dev(nombre_tabla):
    try:
        conexion = conectar()
        sql = "select id, nombre, carnet, empresa from clientes"
        conexion.execute(sql)
        datos = conexion.fetchall()
        conexion.close()
    except Exception as ex:
        titulo = "Seleccionar comprador"
        mensaje = f"No se ha podido conectar: \n{ex}"
        aceptar_error(titulo,mensaje, ventana)    
    
    def selecc_cliente():
        try:
            id_seleccion = ventana.tabla.item(ventana.tabla.selection())['text']
            id_seleccion=int(id_seleccion)
            ventana.destroy()
            seleccionar_productos(id_seleccion,nombre_tabla)
        except Exception as ex:
            titulo = "Diamante negro"
            mensaje = (f"Ha ocurrido un error\n verifique q ha seleccionado un cliente:\n{ex}")
            aceptar_error(titulo,mensaje, ventana)


    ecab_1 = "ID"    
    ecab_2 = "NOMBRE"
    ecab_3 = "CARNET"
    ecab_4 = "EMPRESA"
    

    buscar = ''
    ventana = tk.Tk()
    ventana.title("Seleccionar cliente")
    ventana.geometry("570x270")
    ventana.config(bg="#bfd1e9")
    ventana.resizable(width=0, height=0)    
    ventana.attributes('-topmost', True)

    icono = resource_path("imagenes/data_base.ico")
    ventana.iconbitmap(icono) 

    #area para buscar informacion    
    busqueda_lbl=tk.Label(ventana, font=("arial", 16), text="Seleccione un cliente y haga click en continuar ", background="#bfd1e9", fg="Red")
    busqueda_lbl.place(x=5, y=235)     

    
    btn_continuar = tk.Button(ventana, text="Continuar", command=selecc_cliente)
    btn_continuar.config(activebackground="SpringGreen", compound="left", padx=5, font=("arial", 12)
                   ,justify='center', border=5, cursor="hand2")
    btn_continuar.place(x=470, y=230)
    for i in range(len(datos)):
        datos[i]=list(datos[i])
    tabla_selecc_clientes(ventana,datos,ecab_1,ecab_2,ecab_3,ecab_4)

    ventana.mainloop()       

        
# Trabajo con productos
fecha = []
def seleccionar_productos(id_cliente,nombre_tabla):
    #Consulta DB
    datos = productos_activos()

    ecab_1 = "ID"
    ecab_2 = "DESCRIPCION"
    ecab_3 = "CODIGO"
    ecab_4 = "CANTIDAD"

    buscar = ''
    productos = []       
    def selecc_producto():
        try:
            id_seleccion = ventana.tabla.item(ventana.tabla.selection())['values']
            productos.append(id_seleccion[1])
            
        except Exception as ex:
            titulo = "Diamante negro"
            mensaje = (f"Ha ocurrido un error\n verifique q ha seleccionado algun producto:\n{ex}")
            aceptar_error(titulo,mensaje, ventana)

    def ejecutar_continuar(productos):
        control = 0
        if fecha==[]:
            control = 1 
            messagebox.showerror('Validando', 'Seleccione la fecha de la devolución', parent=ventana)
        if productos  == []:
            control = 1 
            messagebox.showerror('Validando', 'No ha seleccionado ningún producto.\n Seleccione hasta 8 productos para devolver.', parent=ventana)

        prod = list(set(productos))
        if len(prod) > 8:
            control = 1
            productos = []            
            titulo = "Venta de productos"
            mensaje = "Ha elegido más de 8 productos.\n Vuelva a seleccionar hasta 8 productos por proceso de venta"
            aceptar_error(titulo,mensaje, ventana)
            ventana.destroy()
        if control == 0:
            ventana.destroy()
            listar_productos(id_cliente,prod,nombre_tabla)   
        
    ventana = tk.Tk()
    ventana.title("Venta de productos")
    ventana.geometry("570x470")
    ventana.config(bg="#bfd1e9")
    ventana.resizable(width=0, height=0)    
    ventana.attributes('-topmost', True)

    icono = resource_path("imagenes/data_base.ico")
    ventana.iconbitmap(icono)

    #obtener fecha factura
    
    def seleccionar_fecha():
        def devolver_fecha():
            global fecha
            fecha = (cal.get_date())
            objDate = datetime.strptime(fecha, '%m/%d/%y')
            fecha = datetime.strftime(objDate, '%d/%m/%y')
            top.destroy()              
        hoy = datetime.today()
        top = tk.Toplevel(ventana)
        top.attributes('-topmost', True)
        cal = Calendar(top, selectmode='day',
                        year=hoy.year, month=hoy.month, day=hoy.day,
                        background="#649be2", foreground="white",
                        headersbackground="#4a7dc1", headersforeground="white",
                        selectbackground="#ffb703", selectforeground="black")

        cal.pack(pady=20)
        btn_aceptar = ttk.Button(top, text="Aceptar", command= devolver_fecha)
        btn_aceptar.pack(pady=10)

    #area para buscar informacion    
    busqueda_lbl=tk.Label(ventana, font=("arial", 16), text="Selec hasta 8 productos", background="#bfd1e9", fg="Red")
    busqueda_lbl.place(x=5, y=435)
    
    
    fecha_seleccionar = tk.Button(ventana, text="Fecha", command= lambda :seleccionar_fecha())
    fecha_seleccionar.config(activebackground="SpringGreen", bg="#e22564", compound="left", padx=5, font=("arial", 12)
                   ,justify='center', border=5, cursor="hand2")
    fecha_seleccionar.place(x=238, y=430)
    
    
    btn_seleccionar = tk.Button(ventana, text="Añadir producto", command=selecc_producto)
    btn_seleccionar.config(activebackground="SpringGreen", bg="red", compound="left", padx=5, font=("arial", 12)
                   ,justify='center', border=5, cursor="hand2")
    btn_seleccionar.place(x=320, y=430)

    btn_continuar_2 = tk.Button(ventana, text="Continuar", command=lambda: ejecutar_continuar(productos))
    btn_continuar_2.config(activebackground="SpringGreen", compound="left", padx=5, font=("arial", 12)
                   ,justify='center', border=5, cursor="hand2")
    btn_continuar_2.place(x=470, y=430)
    
    tabla_selecc_prod(ventana,datos,ecab_1,ecab_2,ecab_3,ecab_4)   

    ventana.mainloop()
   

def listar_productos(id_cliente, prod, nombre_tabla):
    def cancelar_2():
        titulo = "Venta de productos"
        mensaje = "Realmente quiere abandonar la devolución de productos. \n Los cambios no se guardarán"
        control = messagebox.askokcancel(titulo,mensaje, parent=ventana)
        if control == True:
            ventana.destroy()
       

    def guardar_venta(ventana,id_cliente,prod,cantidad,precio,peso,nombre_tabla):
        list_claves = []
        try:
            conexion = conectar()
            for p in prod:
                sql = (f"select id, cantidad, peso from productos where clave = '{p}';")
                conexion.execute(sql)
                clave = conexion.fetchall()
                list_claves.append(clave)                
            conexion.close() 
        except Exception as ex:
            messagebox.showerror('Guardar devolución',f'Ha ocurrido un error al recuperar los productos\n{ex}', parent=ventana) 
        
        #preparando datos para la consulta
        id_prod = []
        id_cl = []
        fecha_arr = []
        inventario = []
        inv_peso = [] 
        for i in range(len(list_claves)):
            compr_inv = comprobar_inv(fecha,list_claves[i][0][0])
            id_prod.append(list_claves[i][0][0])
            if compr_inv ==0:
                inventario.append(list_claves[i][0][1])
                inv_peso.append(list_claves[i][0][2])            
            else:
                inventario.append(None)
                inv_peso.append(None)
            id_cl.append(id_cliente)
            fecha_arr.append(fecha)

        valores_sql = list(zip(id_cl,id_prod,cantidad,precio,peso,inventario,fecha_arr,inv_peso))
        #valores_tupla = ", ".join([f"{col}" for col in valores_sql])
        #Crea registros devolucion y llama funcion en consultas para actualizar productos
        try:
            conexion = conectar()
            sql = f"""INSERT INTO {nombre_tabla} 
            (id_cliente,id_producto, cantidad, precio, peso, inventario, fecha, inv_peso) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            titulo = "Devolucion de productos"
            mensaje = "Está seguro de efectuar la devolución.\nVerifique los datos antes de guardar.\n Haga click en Cancelar para modificar los datos\n Haga click en aceptar para proceder con la devolución."
            control = confirmar(titulo,mensaje, ventana)
            if control == True:
                conexion.executemany(sql, valores_sql)
                act_prod_dev(valores_sql)
            conexion.close()
    
        except Exception as ex:
            messagebox.showerror('Guardar cambios',ex, parent=ventana)
        ventana.destroy()

        
    alto_ventana = (len(prod))*105+70
    control_filas = 0       

    ventana = tk.Tk()                             
    ventana.title('Devolución de productos')
    ventana.geometry(f'500x{alto_ventana}')
    ventana.config(bg="#649be2")
    ventana.resizable(width=0, height=0)    
    ventana.attributes('-topmost', True)

    icono = resource_path("imagenes/data_base.ico")
    ventana.iconbitmap(icono) 

    #Prepara datos de consulta tabla devoluciones
    utilidades = ventas_devoluciones(prod,id_cliente)
    if utilidades==None:
        prod_dev=[]
    else:
        prod_dev = list(chain.from_iterable(utilidades))
    if prod_dev !=[]:
        prod = []
        for i in range(len(prod_dev)):
            prod.append(prod_dev[i][0])
    else:
        messagebox.showerror("Devoluciones", "Eligió productos que el cliente seleccionado no puede devolver", parent=ventana)
        ventana.destroy()
    
    #prod_inv = productos_inv()
    #creando campos para insertar
    prod_validar = []            
    for i in range(len(prod)):
       if i < len(prod):
            j=tk.Label(ventana,font=("arial", 14), text=f"Clave:{prod[i]} (Consulte pestaña prod.)")
            j.config(bg="#649be2", justify="left")
            j.grid(column=0, row=control_filas,pady=5, columnspan=8)
            control_filas=control_filas+1
            
            p=tk.Label(ventana,font=("arial", 12), text=f"Cantidad:")
            p.config(bg="#d9e2d2", justify="left")
            p.grid(column=0, row=control_filas,pady=5)

            k=tk.Label(ventana,font=("arial", 12), text=f"precio:")
            k.config(bg="#95dd8c", justify="left")
            k.grid(column=3, row=control_filas,pady=5)

            q=tk.Label(ventana,font=("arial", 12), text=f"Peso:")
            q.config(bg="#95dd8c", justify="left")
            q.grid(column=6, row=control_filas,pady=5)
                        
            cantidad = tk.StringVar(value='0')
            precio = tk.StringVar(value='0')
            peso = tk.StringVar(value='0')

            if i==0:        
                a=tk.Entry(ventana,font=("arial", 12), textvariable=cantidad)
                a.config(width=7, justify="left")
                a.grid(column=1, row=control_filas,padx=2,pady=10)                   
                                    
                aa=tk.Entry(ventana,font=("arial", 12), textvariable=precio)
                aa.config(width=7, justify="left")
                aa.grid(column=4, row=control_filas,padx=2,pady=10)   
                
                aaa=tk.Entry(ventana,font=("arial", 12), textvariable=peso)
                aaa.config(width=7, justify="left")
                aaa.grid(column=7, row=control_filas,padx=2,pady=10)   
                control_filas=control_filas+1
                
                divisor = tk.Label(ventana, text='-----'*19)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=8)
                control_filas=control_filas+1
                a.insert(0, prod_dev[i][1])
                aa.insert(0, round(prod_dev[i][2]/prod_dev[i][3], 2))
                aa.config(state="disable")
                aaa.insert(0, prod_dev[i][3])
                prod_validar.append(prod_dev[i])
            if i==1:               

                b=tk.Entry(ventana,font=("arial", 12), textvariable=cantidad)
                b.config(width=7, justify="left")
                b.grid(column=1, row=control_filas,padx=2,pady=10)                   
                                    
                bb=tk.Entry(ventana,font=("arial", 12), textvariable=precio)
                bb.config(width=7, justify="left")
                bb.grid(column=4, row=control_filas,padx=2,pady=10)   
                
                bbb=tk.Entry(ventana,font=("arial", 12), textvariable=peso)
                bbb.config(width=7, justify="left")
                bbb.grid(column=7, row=control_filas,padx=2,pady=10)   
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*19)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=8)
                control_filas=control_filas+1

                b.insert(0, prod_dev[i][1])
                bb.insert(0, round(prod_dev[i][2]/prod_dev[i][3], 2))
                bb.config(state="disable")
                bbb.insert(0, prod_dev[i][3])
                prod_validar.append(prod_dev[i])

            if i==2:
                c=tk.Entry(ventana,font=("arial", 12), textvariable=cantidad)
                c.config(width=7, justify="left")
                c.grid(column=1, row=control_filas,padx=2,pady=10)                   
                                    
                cc=tk.Entry(ventana,font=("arial", 12), textvariable=precio)
                cc.config(width=7, justify="left")
                cc.grid(column=4, row=control_filas,padx=2,pady=10)   
                
                ccc=tk.Entry(ventana,font=("arial", 12), textvariable=peso)
                ccc.config(width=7, justify="left")
                ccc.grid(column=7, row=control_filas,padx=2,pady=10)   
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*19)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=8)
                control_filas=control_filas+1

                c.insert(0, prod_dev[i][1])
                cc.insert(0, round(prod_dev[i][2]/prod_dev[i][3], 2))
                cc.config(state="disable")
                ccc.insert(0, prod_dev[i][3])
            
            if i==3:
                d=tk.Entry(ventana,font=("arial", 12), textvariable=cantidad)
                d.config(width=7, justify="left")
                d.grid(column=1, row=control_filas,padx=2,pady=10)                   
                                    
                dd=tk.Entry(ventana,font=("arial", 12), textvariable=precio)
                dd.config(width=7, justify="left")
                dd.grid(column=4, row=control_filas,padx=2,pady=10)   
                
                ddd=tk.Entry(ventana,font=("arial", 12), textvariable=peso)
                ddd.config(width=7, justify="left")
                ddd.grid(column=7, row=control_filas,padx=2,pady=10)   
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*19)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=8)
                control_filas=control_filas+1

                d.insert(0, prod_dev[i][1])
                dd.insert(0, round(prod_dev[i][2]/prod_dev[i][3], 2))
                dd.config(state="disable")
                ddd.insert(0, prod_dev[i][3])

            if i==4:
                e=tk.Entry(ventana,font=("arial", 12), textvariable=cantidad)
                e.config(width=7, justify="left")
                e.grid(column=1, row=control_filas,padx=2,pady=10)                   
                                    
                ee=tk.Entry(ventana,font=("arial", 12), textvariable=precio)
                ee.config(width=7, justify="left")
                ee.grid(column=4, row=control_filas,padx=2,pady=10)   
                
                eee=tk.Entry(ventana,font=("arial", 12), textvariable=peso)
                eee.config(width=7, justify="left")
                eee.grid(column=7, row=control_filas,padx=2,pady=10)   
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*19)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=8)
                control_filas=control_filas+1

                e.insert(0, prod_dev[i][1])
                ee.insert(0, round(prod_dev[i][2]/prod_dev[i][3], 2))
                ee.config(state="disable")
                eee.insert(0, prod_dev[i][3])                            

            if i==5:
                f=tk.Entry(ventana,font=("arial", 12), textvariable=cantidad)
                f.config(width=7, justify="left")
                f.grid(column=1, row=control_filas,padx=2,pady=10)                   
                                    
                ff=tk.Entry(ventana,font=("arial", 12), textvariable=precio)
                ff.config(width=7, justify="left")
                ff.grid(column=4, row=control_filas,padx=2,pady=10)   
                
                fff=tk.Entry(ventana,font=("arial", 12), textvariable=peso)
                fff.config(width=7, justify="left")
                fff.grid(column=7, row=control_filas,padx=2,pady=10)   
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*19)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=8)
                control_filas=control_filas+1

                f.insert(0, prod_dev[i][1])
                ff.insert(0, round(prod_dev[i][2]/prod_dev[i][3], 2))
                ff.config(state="disable")
                fff.insert(0, prod_dev[i][3])

            if i==6:
                g=tk.Entry(ventana,font=("arial", 12), textvariable=cantidad)
                g.config(width=7, justify="left")
                g.grid(column=1, row=control_filas,padx=2,pady=10)                   
                                    
                gg=tk.Entry(ventana,font=("arial", 12), textvariable=precio)
                gg.config(width=7, justify="left")
                gg.grid(column=4, row=control_filas,padx=2,pady=10)   
                
                ggg=tk.Entry(ventana,font=("arial", 12), textvariable=peso)
                ggg.config(width=7, justify="left")
                ggg.grid(column=7, row=control_filas,padx=2,pady=10)   
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*19)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=8)
                control_filas=control_filas+1

                g.insert(0, prod_dev[i][1])
                gg.insert(0, round(prod_dev[i][2]/prod_dev[i][3], 2))
                gg.config(state="disable")
                ggg.insert(0, prod_dev[i][3])

            if i==7:
                h=tk.Entry(ventana,font=("arial", 12), textvariable=cantidad)
                h.config(width=7, justify="left")
                h.grid(column=1, row=control_filas,padx=2,pady=10)                   
                                    
                hh=tk.Entry(ventana,font=("arial", 12), textvariable=precio)
                hh.config(width=7, justify="left")
                hh.grid(column=4, row=control_filas,padx=2,pady=10)   
                
                hhh=tk.Entry(ventana,font=("arial", 12), textvariable=peso)
                hhh.config(width=7, justify="left")
                hhh.grid(column=7, row=control_filas,padx=2,pady=10)   
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*19)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=8)
                control_filas=control_filas+1

                h.insert(0, prod_dev[i][1])
                hh.insert(0, round(prod_dev[i][2]/prod_dev[i][3], 2))
                hh.config(state="disable")
                hhh.insert(0, prod_dev[i][3])

    def recuperar_datos():
        cantidad = []
        precio = []
        peso = []           
        for i in range(len(prod)):            
            if i==0:
               cantidad.append(a.get())
               precio.append(aa.get())
               peso.append(aaa.get())
            if i==1:
               cantidad.append(b.get())
               precio.append(bb.get())
               peso.append(bbb.get())
            if i==2:
               cantidad.append(c.get())
               precio.append(cc.get())
               peso.append(ccc.get())
            if i==3:
               cantidad.append(d.get())
               precio.append(dd.get())
               peso.append(ddd.get())            
            if i==4:
               cantidad.append(e.get())
               precio.append(ee.get())
               peso.append(eee.get())
            if i==5:
               cantidad.append(f.get())
               precio.append(ff.get())
               peso.append(fff.get())
            if i==6:
               cantidad.append(g.get())
               precio.append(gg.get())
               peso.append(ggg.get())
            if i==7:
               cantidad.append(h.get())
               precio.append(hh.get())
               peso.append(hhh.get())
        control = 0
        #Validando cantidades, precio y peso
        for i in range(len(cantidad)):            
            try:
                cantidad[i] = float(cantidad[i])
            except Exception as ex:
                control = 1
                messagebox.showerror('Validando','Verifique las cantidades, deben ser un número positivo.\n Considere usar (.) en vez de (,) para los numeros decimales.', parent=ventana)
            
            if cantidad[i] <=0:
                control = 1
                messagebox.showerror('Validando','Verifique las cantidades, existen valores negativos o en cero.', parent=ventana)
        
        for i in range(len(precio)):
            try:
                precio[i] = float(precio[i])
            except Exception as ex:
                control = 1
                messagebox.showerror('Validando','Verifique los precios, deben ser un número positivo.\n Considere usar (.) en vez de (,) para los numeros decimales.', parent=ventana)

            if precio[i] <=0:
                control = 1
                messagebox.showerror('Validando','Verifique los precios, existen valores negativos o en cero.', parent=ventana)  
        
        for i in range(len(peso)):
            try:
                peso[i] = float(peso[i])
            except Exception as ex:
                control = 1
                messagebox.showerror('Validando','Verifique los pesos, deben ser un número positivo.\n Considere usar (.) en vez de (,) para los numeros decimales.', parent=ventana)

            if peso[i] <=0:
                control = 1
                messagebox.showerror('Validando', 'Verifique los pesos, existen valores negativos o en cero.', parent=ventana)  

        #precio = []
        for i in range(len(cantidad)):
            if cantidad[i]> prod_dev[i][1]:
                control = 1                   
                messagebox.showerror("Validando",f"Solo puede hacer devoluciones de hasta: {prod_dev[i][1]} \npara el producto con código: {prod_dev[i][0]}", parent=ventana)
            
            elif peso[i]> prod_dev[i][3]:
                control = 1                   
                messagebox.showerror("Validando",f"Solo puede hacer devoluciones de peso de: {prod_dev[i][3]} \npara el producto con código: {prod_dev[i][0]}", parent=ventana)
                        
            elif  cantidad[i]-prod_dev[i][1]==0:
                if  peso[i]-prod_dev[i][3]!=0:
                    control = 1
                    messagebox.showerror('Validando',f'Revise cantidad y peso, si el peso cuando devuelve queda en cero\nlas cantidades tambien deben ser ceros y viceversa\nDisponibilidad\nCantidad: {cantidad}\nPeso: {peso}', parent=ventana) 
           
            elif  peso[i]-prod_dev[i][3]==0:
                if  cantidad[i]-prod_dev[i][1]!=0:
                    control = 1
                    messagebox.showerror('Validando','Revise cantidad y peso, si el peso cuando devuelve queda en cero\nlas cantidades tambien deben ser ceros y viceversa\nDisponibilidad\nCantidad: {cantidad}\nPeso: {peso}', parent=ventana) 
            #precio.append(prod_dev[i][2]/prod_dev[i][3])         
        
        if control==0:
            guardar_venta(ventana,id_cliente,prod,cantidad,precio,peso,nombre_tabla)
            

    boton_0 = tk.Button(ventana, command=lambda:recuperar_datos())
    boton_0.config(bg="LimeGreen", activebackground="SpringGreen", fg="White", relief="groove", font=("arial", 12, 'bold')
                   , width=15,justify='center', border=5, text='Guardar')
    boton_0.grid(row=control_filas, column=0, padx=15, pady=10, columnspan=4)
         
    boton_0 = tk.Button(ventana, text='Cancelar', width=15,justify='center', border=5, command= lambda: cancelar_2())
    boton_0.config(bg="Crimson", activebackground="Red", fg="White", relief="groove", font=("arial", 12, 'bold'))
    boton_0.grid(row=control_filas, column=5, columnspan=4)

    ventana.mainloop() 