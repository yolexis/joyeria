from models.conexion_sql import conectar
import tkinter as tk
from interfaces.tabla import tabla_selecc_clientes, tabla_selecc_prod
from utilidades.decisiones import aceptar_error,confirmar
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
from utilidades.validar import *
from models.consultas import ventas_devoluciones, productos_inv, productos_activos, act_prod_dev, comprobar_inv
from itertools import chain
from utilidades.recursos import resource_path


def seleccionar_cliente_pagar(nombre_tabla):
    try:
        conexion = conectar()
        sql = "select id, nombre, carnet, empresa from clientes"
        conexion.execute(sql)
        datos = conexion.fetchall()
        conexion.close()
    except Exception as ex:
        titulo = "Seleccionar cliente"
        mensaje = f"No se ha podido conectar: \n{ex}"
        aceptar_error(titulo,mensaje,ventana)    
    
    def selecc_cliente():
        try:
            id_seleccion = ventana.tabla.item(ventana.tabla.selection())['text']
            id_seleccion=int(id_seleccion)
            ventana.destroy()
            seleccionar_productos(id_seleccion,nombre_tabla)
        except Exception as ex:
            titulo = "Diamante negro"
            mensaje = (f"Ha ocurrido un error\n verifique q ha seleccionado un cliente:\n{ex}")
            aceptar_error(titulo,mensaje,ventana)


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
            aceptar_error(titulo,mensaje,ventana)

    def ejecutar_continuar(productos):
        control = 0
        if fecha==[]:
            control = 1
            titulo='Validando'
            mensaje='Seleccione la fecha del pago' 
            aceptar_error(titulo, mensaje,ventana)
        if productos  == []:
            control = 1
            titulo='Validando'
            mensaje='No ha seleccionado ningún producto.\n Seleccione hasta 8 productos para efectuar pago.' 
            aceptar_error(titulo,mensaje,ventana)

        prod = list(set(productos))
        if len(prod) > 8:
            control = 1
            productos = []            
            titulo = "Venta de productos"
            mensaje = "Ha elegido más de 8 productos.\n Vuelva a seleccionar hasta 8 productos por proceso de pago"
            aceptar_error(titulo,mensaje,ventana)
            ventana.destroy()
        if control == 0:
            ventana.destroy()
            listar_productos(id_cliente,prod,nombre_tabla)   
        
    ventana = tk.Tk()
    ventana.title("Pago de productos")
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
        cal = Calendar(top, selectmode='day', year=hoy.year, month=hoy.month, day=hoy.day)
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
        mensaje = "Realmente quiere abandonar el pago de productos. \n Los cambios no se guardarán"
        control = confirmar(titulo,mensaje,ventana)
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
            mensaje=f'Ha ocurrido un error al recuperar los productos\n{ex}'
            titulo='Guardar pago'
            aceptar_error(titulo, mensaje,ventana) 
        
        #preparando datos para la consulta
        id_prod = []
        id_cl = []
        fecha_arr = []
        for i in range(len(list_claves)):
            id_prod.append(list_claves[i][0][0])
            id_cl.append(id_cliente)
            fecha_arr.append(fecha)

        valores_sql = list(zip(id_cl,id_prod,cantidad,precio,peso,fecha_arr))
        try:
            conexion = conectar()
            sql = f"""INSERT INTO {nombre_tabla} 
            (id_cliente,id_producto, cantidad, precio, peso, fecha) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """                       
            titulo = "Pago de productos"
            mensaje = "Está seguro de efectuar el pago.\nVerifique los datos antes de guardar.\n Haga click en Cancelar para modificar los datos\n Haga click en aceptar para proceder con la devolución."
            control = confirmar(titulo,mensaje,ventana)
            if control == True:
                conexion.executemany(sql, valores_sql)                
            conexion.close()    
        except Exception as ex:
            titulo='Guardar cambios'
            mensaje=ex
            aceptar_error(titulo,mensaje,ventana)
        ventana.destroy()
        
    alto_ventana = (len(prod))*105+70
    control_filas = 0       

    ventana = tk.Tk()                             
    ventana.title('Pago de venta')
    ventana.geometry(f'610x{alto_ventana}')
    ventana.config(bg="#649be2")
    ventana.resizable(width=0, height=0)    
    ventana.attributes('-topmost', True)

    icono = resource_path("imagenes/data_base.ico")
    ventana.iconbitmap(icono) 

    #Prepara datos de consulta tabla pagar joyas
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
        titulo="Pagos"
        mensaje="Eligió productos que el cliente seleccionado no tiene pagos pendientes"
        aceptar_error(titulo,mensaje,ventana)
        ventana.destroy()
    
    prod_inv = productos_inv()
    #creando campos para insertar
    prod_validar = []            
    for i in range(len(prod)):
       if i < len(prod):
            j=tk.Label(ventana,font=("arial", 14), text=f"Clave:{prod[i]} (Consulte pestaña prod.)")
            j.config(bg="#649be2", justify="left")
            j.grid(column=0, row=control_filas,pady=5, columnspan=6)
            ing=tk.Label(ventana,font=("arial", 14), text="Ingreso($)")
            ing.config(bg="#649be2", justify="left")
            ing.grid(column=8, row=control_filas,pady=5, columnspan=2)
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
            dinero = tk.StringVar(value='0')

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

                aaaa=tk.Entry(ventana,font=("arial", 12), textvariable=dinero)
                aaaa.config(width=11, justify="left")
                aaaa.grid(column=8, row=control_filas,padx=2,pady=10)    

                control_filas=control_filas+1
                
                divisor = tk.Label(ventana, text='-----'*22)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=9)
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
                
                bbbb=tk.Entry(ventana,font=("arial", 12), textvariable=dinero)
                bbbb.config(width=11, justify="left")
                bbbb.grid(column=8, row=control_filas,padx=2,pady=10)    
                
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*22)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=9)
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
                
                cccc=tk.Entry(ventana,font=("arial", 12), textvariable=dinero)
                cccc.config(width=11, justify="left")
                cccc.grid(column=8, row=control_filas,padx=2,pady=10)    
                
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*22)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=9)
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
                
                dddd=tk.Entry(ventana,font=("arial", 12), textvariable=dinero)
                dddd.config(width=11, justify="left")
                dddd.grid(column=8, row=control_filas,padx=2,pady=10)    
                
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*22)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=9)
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
                
                eeee=tk.Entry(ventana,font=("arial", 12), textvariable=dinero)
                eeee.config(width=11, justify="left")
                eeee.grid(column=8, row=control_filas,padx=2,pady=10)    
                
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*22)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=9)
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
                
                ffff=tk.Entry(ventana,font=("arial", 12), textvariable=dinero)
                ffff.config(width=11, justify="left")
                ffff.grid(column=8, row=control_filas,padx=2,pady=10)    
                
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*22)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=9)
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
                
                gggg=tk.Entry(ventana,font=("arial", 12), textvariable=dinero)
                gggg.config(width=11, justify="left")
                gggg.grid(column=8, row=control_filas,padx=2,pady=10)    
                
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*22)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=9)
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
                
                hhhh=tk.Entry(ventana,font=("arial", 12), textvariable=dinero)
                hhhh.config(width=11, justify="left")
                hhhh.grid(column=8, row=control_filas,padx=2,pady=10)    
                
                control_filas=control_filas+1

                divisor = tk.Label(ventana, text='-----'*22)
                divisor.config(bg="#649be2")
                divisor.grid(column=0, row=control_filas, columnspan=9)
                control_filas=control_filas+1

                h.insert(0, prod_dev[i][1])
                hh.insert(0, round(prod_dev[i][2]/prod_dev[i][3], 2))
                hh.config(state="disable")
                hhh.insert(0, prod_dev[i][3])


    def calcular():
        precio = []
        dinero = []
        cantidad = []
        peso = []
                
        for i in range(len(prod)):            
            if i==0:
               cantidad.append(a.get())
               peso.append(aaa.get())
               precio.append(aa.get())
               dinero.append(aaaa.get())
            if i==1:
               cantidad.append(b.get())
               peso.append(bbb.get())
               precio.append(bb.get())
               dinero.append(bbbb.get())
            if i==2:
               cantidad.append(c.get())
               peso.append(ccc.get())
               precio.append(cc.get())
               dinero.append(cccc.get())
            if i==3:
               cantidad.append(d.get())
               peso.append(ddd.get())
               precio.append(dd.get())
               dinero.append(dddd.get())            
            if i==4:
               cantidad.append(e.get())
               peso.append(eee.get())
               precio.append(ee.get())
               dinero.append(eeee.get())
            if i==5:
               cantidad.append(f.get())
               peso.append(fff.get())
               precio.append(ff.get())
               dinero.append(ffff.get())
            if i==6:
               cantidad.append(g.get())
               peso.append(ggg.get())
               precio.append(gg.get())
               dinero.append(gggg.get())
            if i==7:
               cantidad.append(h.get())
               peso.append(hhh.get())
               precio.append(hh.get())
               dinero.append(hhhh.get())
        control = 0
        for i in range(len(dinero)):            
            try:
                dinero[i] = float(dinero[i])
            except Exception as ex:
                control = 1
                titulo='Validando'
                mensaje=f'Verifique las cantidades de dinero insertadas, \npara el producto con código: {prod[0]} \ndebe ser un número positivo.\n Considere usar (.) en vez de (,) para los numeros decimales.'
                aceptar_error(titulo,mensaje,ventana)
            
            if dinero[i] <=0:
                control = 1
                titulo='Validando'
                mensaje='Verifique las cantidades de dinero insertadas,\n existen valores negativos o en cero.'
                aceptar_error(titulo,mensaje,ventana)
        if control == 1:
            return
        else:
            for i in range(len(prod)):
                p = round(dinero[i]/float(precio[i]), 6)                
                q=round(p*float(cantidad[i])/float(peso[i]), 6)
                if i==0:
                    a.config(state="normal")
                    aaa.config(state="normal")
                    a.delete(first=0,last=8)
                    a.insert(0, q)
                    a.config(state="disable")
                    aaa.delete(first=0,last=8)
                    aaa.insert(0, p)
                    aaa.config(state="disable")
                    #aaaa.config(state="disable")
                if i==1:
                    b.config(state="normal")
                    bbb.config(state="normal")
                    b.delete(first=0,last=8)
                    b.insert(0, q)
                    b.config(state="disable")
                    bbb.delete(first=0,last=8)
                    bbb.insert(0, p)
                    bbb.config(state="disable")
                    bbbb.config(state="disable")
                if i==2:
                    c.config(state="normal")
                    ccc.config(state="normal")
                    c.delete(first=0,last=8)
                    c.insert(0, q)
                    c.config(state="disable")
                    ccc.delete(first=0,last=8)
                    ccc.insert(0, p)
                    ccc.config(state="disable")
                    cccc.config(state="disable")
                if i==3:
                    d.config(state="normal")
                    ddd.config(state="normal")
                    d.delete(first=0,last=8)
                    d.insert(0, q)
                    d.config(state="disable")
                    ddd.delete(first=0,last=8)
                    ddd.insert(0, p)
                    ddd.config(state="disable")
                    dddd.config(state="disable")
                if i==4:
                    e.config(state="normal")
                    eee.config(state="normal")
                    e.delete(first=0,last=8)
                    e.insert(0, q)
                    e.config(state="disable")
                    eee.delete(first=0,last=8)
                    eee.insert(0, p)
                    eee.config(state="disable")
                    eeee.config(state="disable")
                if i==5:
                    f.config(state="normal")
                    fff.config(state="normal")
                    f.delete(first=0,last=8)
                    f.insert(0, q)
                    f.config(state="disable")
                    fff.delete(first=0,last=8)
                    fff.insert(0, p)
                    fff.config(state="disable")
                    ffff.config(state="disable")
                if i==6:
                    g.config(state="normal")
                    ggg.config(state="normal")
                    g.delete(first=0,last=8)
                    g.insert(0, q)
                    g.config(state="disable")
                    ggg.delete(first=0,last=8)
                    ggg.insert(0, p)
                    ggg.config(state="disable")
                    gggg.config(state="disable")
                if i==7:
                    h.config(state="normal")
                    hhh.config(state="normal")
                    h.delete(first=0,last=8)
                    h.insert(0, q)
                    h.config(state="disable")
                    hhh.delete(first=0,last=8)
                    hhh.insert(0, p)
                    hhh.config(state="disable")
                    hhhh.config(state="disable")                


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
                titulo='Validando'
                mensaje='Verifique las cantidades, deben ser un número positivo.\n Considere usar (.) en vez de (,) para los numeros decimales.'
                aceptar_error(titulo,mensaje,ventana)
            
            if cantidad[i] <=0:
                control = 1
                titulo='Validando'
                mensaje='Verifique las cantidades, existen valores negativos o en cero.'
                aceptar_error(titulo,mensaje,ventana)
        
        for i in range(len(precio)):
            try:
                precio[i] = float(precio[i])
            except Exception as ex:
                control = 1
                titulo='Validando'
                mensaje='Verifique los precios, deben ser un número positivo.\n Considere usar (.) en vez de (,) para los numeros decimales.'
                aceptar_error(titulo,mensaje,ventana)

            if precio[i] <=0:
                control = 1
                titulo='Validando'
                mensaje='Verifique los precios, existen valores negativos o en cero.'
                aceptar_error(titulo,mensaje,ventana)  
        
        for i in range(len(peso)):
            try:
                peso[i] = float(peso[i])
            except Exception as ex:
                control = 1
                titulo='Validando'
                mensaje='Verifique los pesos, deben ser un número positivo.\n Considere usar (.) en vez de (,) para los numeros decimales.'
                aceptar_error(titulo,mensaje,ventana)

            if peso[i] <=0:
                control = 1
                titulo='Validando'
                mensaje='Verifique los pesos, existen valores negativos o en cero.'
                aceptar_error(titulo,mensaje,ventana)  

        #precio = []
        for i in range(len(cantidad)):
            if cantidad[i]> prod_dev[i][1]:
                control = 1                   
                titulo="Validando"
                mensaje=f"Solo puede hacer pagos para la cantidad de hasta: {prod_dev[i][1]} \npara el producto con código: {prod_dev[i][0]}"
                aceptar_error(titulo,mensaje,ventana)
            
            elif peso[i]> prod_dev[i][3]:
                control = 1                 
                titulo="Validando"
                mensaje=f"Solo puede hacer pagos correspondientes al peso hasta: {prod_dev[i][3]} \npara el producto con código: {prod_dev[i][0]}"  
                aceptar_error(titulo,mensaje,ventana)
                        
            elif  cantidad[i]-prod_dev[i][1]==0:
                if  peso[i]-prod_dev[i][3]!=0:
                    control = 1
                    titulo='Validando'
                    mensaje=f'Revise cantidad y peso, si el peso cuando paga queda en cero\nlas cantidades tambien deben ser ceros y viceversa\nDisponibilidad\nCantidad: {cantidad}\nPeso: {peso}'
                    aceptar_error(titulo,mensaje,ventana) 
           
            elif  peso[i]-prod_dev[i][3]==0:
                if  cantidad[i]-prod_dev[i][1]!=0:
                    control = 1
                    titulo='Validando'
                    mensaje='Revise cantidad y peso, si el peso cuando paga queda en cero\nlas cantidades tambien deben ser ceros y viceversa\nDisponibilidad\nCantidad: {cantidad}\nPeso: {peso}'
                    aceptar_error(titulo,mensaje,ventana) 
            #precio.append(prod_dev[i][2]/prod_dev[i][3])         
        
        if control==0:
            guardar_venta(ventana,id_cliente,prod,cantidad,precio,peso,nombre_tabla)
            

    boton_0 = tk.Button(ventana, command=lambda:recuperar_datos())
    boton_0.config(bg="LimeGreen", activebackground="SpringGreen", fg="White", relief="groove", font=("arial", 12, 'bold')
                   , width=15,justify='center', border=5, text='Guardar')
    boton_0.grid(row=control_filas, column=0, padx=15, pady=10, columnspan=3)
         
    boton_0 = tk.Button(ventana, text='Cancelar', width=15,justify='center', border=5, command= lambda: cancelar_2())
    boton_0.config(bg="Crimson", activebackground="Red", fg="White", relief="groove", font=("arial", 12, 'bold'))
    boton_0.grid(row=control_filas, column=4, columnspan=3)

    boton_0 = tk.Button(ventana, text='Calcular', width=9,justify='center', border=5, command= lambda: calcular())
    boton_0.config(bg="Blue", activebackground="SpringGreen", fg="White", relief="groove", font=("arial", 12, 'bold'))
    boton_0.grid(row=control_filas, column=8, columnspan=2)

    ventana.mainloop() 