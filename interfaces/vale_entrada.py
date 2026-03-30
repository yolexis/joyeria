import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
from models.conexion_sql import conectar, cerrar_conectar
from utilidades.recursos import resource_path
from models.consultas import comprobar_inv


# ---------- Seleccionar fecha ----------
def seleccionar_fecha(ventana, callback):
    def devolver_fecha():
        fecha = cal.get_date()
        objDate = datetime.strptime(fecha, '%m/%d/%y')
        fecha = datetime.strftime(objDate, '%d/%m/%y')
        top.destroy()
        callback(fecha)

    hoy = datetime.today()
    top = tk.Toplevel(ventana)
    top.title("Seleccionar fecha")
    top.attributes('-topmost', True)
    cal = Calendar(top, selectmode='day', year=hoy.year, month=hoy.month, day=hoy.day)
    cal.pack(pady=20)
    btn_aceptar = ttk.Button(top, text="Aceptar", command=devolver_fecha)
    btn_aceptar.pack(pady=10)
    
    icono = resource_path("imagenes/data_base.ico")
    try:
        top.iconbitmap(icono)
    except Exception:
        pass

# ---------- Editar producto ----------
def vale_in():
    def mostrar_productos(filtro=""):
        for item in tree.get_children():
            tree.delete(item)

        conn = conectar()
        sql_2 = """SELECT id, clave, nombre, unidad_medida, peso, cantidad, estado, categoria 
                   FROM productos ORDER BY id DESC"""
        conn.execute(sql_2)
        for row in conn.fetchall():
            tree.insert("", "end", values=row)
        cerrar_conectar(conn)

    def limpiar_campos():
        for entry in [entry_clave, entry_nombre, entry_unidad, entry_peso, entry_cantidad, entry_fecha]:
            entry.configure(state="normal")
            entry.delete(0, "end")
            entry.configure(state="disabled")

    def seleccionar_producto(event):
        selected = tree.focus()
        if not selected:
            return
        valores = tree.item(selected, "values")
        for entry in [entry_clave, entry_nombre, entry_unidad, entry_peso, entry_cantidad]:
            entry.configure(state="normal")
            entry.delete(0, "end")

        entry_clave.insert(0, valores[1])
        entry_nombre.insert(0, valores[2])
        entry_unidad.insert(0, valores[3])
        entry_peso.insert(0, 'Peso')
        entry_cantidad.insert(0, 'Cantidad')
        

        # bloquear de nuevo excepto peso, cantidad y fecha
        entry_clave.configure(state="disabled")
        entry_nombre.configure(state="disabled")
        entry_unidad.configure(state="disabled")
        entry_peso.configure(state="normal")
        entry_cantidad.configure(state="normal")
        entry_fecha.configure(state="normal")

        nonlocal producto_id
        producto_id = valores[0]

    def actualizar_producto():
        try:
            peso = float(entry_peso.get())
            cantidad = float(entry_cantidad.get())
            fecha_val = entry_fecha.get()
        except Exception as e:
            messagebox.showwarning("Atención", f"Compruebe peso, cantidad y fecha:\n{e}", parent=app)
            return

        if peso < 0 or cantidad < 0:
            messagebox.showwarning("Atención", "Peso y cantidad no pueden ser negativos.", parent=app)
            return

        try:
            conn = conectar()
            sql_3 = f"SELECT id, peso, cantidad FROM productos WHERE id={producto_id}"
            conn.execute(sql_3)
            datos = conn.fetchall()
        except Exception as e:
            messagebox.showwarning("Atención", f"Fallo al conectarse a la BD:\n{e}", parent=app)
            return
        
        compr_inv = comprobar_inv(fecha_val,producto_id)

        if compr_inv ==0:
            inventario = datos[0][2]
            inv_peso = datos[0][1]            
        else:
            inventario = None
            inv_peso = None
        try:
            valores_0 = (peso, cantidad, fecha_val, producto_id, inventario, inv_peso)
            peso = peso + datos[0][1]
            cantidad = cantidad + datos[0][2]
            valores = (peso, cantidad, producto_id)
            conn = conectar()
            sql = """UPDATE productos
                     SET peso = %s, cantidad = %s
                     WHERE id = %s"""          

            sql_2 = """INSERT INTO vale_entrada (peso, cantidad, fecha, id_producto, inventario, inv_peso)
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            
            conn.execute(sql, valores)
            conn.execute(sql_2, valores_0)
            cerrar_conectar(conn)

            limpiar_campos()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.", parent=app)
            mostrar_productos()            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto:\n{e}", parent=app)

    def abrir_calendario():
        seleccionar_fecha(app, lambda f: entry_fecha.delete(0, "end") or entry_fecha.insert(0, f))

    # ---------- Interfaz ----------
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Recepción de productos")
    app.geometry("950x750")
    app.configure(fg_color="#649be2")
    app.attributes('-topmost', True)

    #direccion absoluta de recursos    
    icono = resource_path("imagenes/data_base.ico")
    try:
        app.iconbitmap(icono)
    except Exception:
        pass

    frame = ctk.CTkFrame(app, corner_radius=15, fg_color="white")
    frame.pack(pady=20, padx=20, fill="x")

    # Entradas
    entry_clave = ctk.CTkEntry(frame, placeholder_text="Clave", width=200, corner_radius=15, state="disabled")
    entry_clave.grid(row=0, column=0, padx=10, pady=10)

    entry_nombre = ctk.CTkEntry(frame, placeholder_text="Nombre", width=200, corner_radius=15, state="disabled")
    entry_nombre.grid(row=0, column=1, padx=10, pady=10)

    entry_unidad = ctk.CTkEntry(frame, placeholder_text="Unidad Medida", width=200, corner_radius=15, state="disabled")
    entry_unidad.grid(row=0, column=2, padx=10, pady=10)

    entry_peso = ctk.CTkEntry(frame, placeholder_text="Peso", width=200, corner_radius=15, state="disabled")
    entry_peso.grid(row=1, column=0, padx=10, pady=10)

    entry_cantidad = ctk.CTkEntry(frame, placeholder_text="Cantidad", width=200, corner_radius=15, state="disabled")
    entry_cantidad.grid(row=1, column=1, padx=10, pady=10)

    # Fecha
    entry_fecha = ctk.CTkEntry(frame, placeholder_text="Fecha", width=200, corner_radius=15, state="disabled")
    entry_fecha.grid(row=1, column=2, padx=10, pady=10)
    btn_fecha = ctk.CTkButton(frame, text="📅", width=50, command=abrir_calendario)
    btn_fecha.grid(row=1, column=3, padx=5, pady=10)

    # Botón Actualizar
    btn_actualizar = ctk.CTkButton(frame, text="Actualizar", command=actualizar_producto, corner_radius=20)
    btn_actualizar.grid(row=1, column=4, padx=10, pady=10)

   
    # Treeview
    tree_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="white")
    tree_frame.pack(padx=20, pady=20, fill="both", expand=True)

    columns = ("ID", "Clave", "Nombre", "Unidad", "Peso", "Cantidad", "Tipo Mat.", "Categoría")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    tree.pack(fill="both", expand=True)

    tree.bind("<<TreeviewSelect>>", seleccionar_producto)

    producto_id = None
    mostrar_productos()

    
    # ------------------- Footer -------------------
    footer = ctk.CTkLabel(
        app,
        text="© 2025 - Hecho para [Joyería Diamante Negro].\n"
               "Autor: Ing. Yolexis Herrera Espinosa\n"
             "Uso limitado y exclusivo. Contacto: 54813576",
        font=("Arial", 12),
        text_color="white",
        justify="center"
    )
    footer.pack(side="bottom", pady=15)

    app.mainloop()