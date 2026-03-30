import psycopg2
import customtkinter as ctk
from tkinter import ttk, messagebox
from models.conexion_sql import conectar, cerrar_conectar
from utilidades.recursos import resource_path
from utilidades.recursos import resource_path


# ---------- Insertar producto ----------
def insertar_productos():
    def insertar_producto():
        clave = entry_clave.get()
        nombre = entry_nombre.get()
        unidad = entry_unidad.get()
        peso = entry_peso.get()    
        cantidad = entry_cantidad.get()
        estado = estado_var.get()
        categoria = categoria_var.get()
        
        
        #Validando datos
        if not clave or not nombre or not unidad or not peso or not cantidad:
            messagebox.showwarning("Atención", "No pueden haber campos vacios.", parent=app)
            return
       
        try:
            float(peso)
            float(cantidad)            
        except Exception as ex:
            messagebox.showwarning("Atención", f"Compruebe el peso y la cantidad, deben ser números:\n{ex}", parent=app)
            return   
        
        if float(peso) < 0 or float(cantidad) < 0:
            messagebox.showwarning("Atención", f"Compruebe el peso y la cantidad, no pueden ser negativos.", parent=app)
            return
            
        try:
            conn = conectar()
            sql = f"""INSERT INTO productos (clave, nombre, unidad_medida, peso, cantidad, estado, categoria)
              VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            valores = (clave, nombre, unidad, peso, cantidad, estado, categoria)
            conn.execute(sql, valores)
            cerrar_conectar(conn)
            messagebox.showinfo("Éxito", "Producto insertado correctamente.", parent=app)
            mostrar_productos()
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar productooo: \n{e}", parent=app)

    # ---------- Mostrar productos en Treeview ----------
    def mostrar_productos():
        for item in tree.get_children():
            tree.delete(item)

        conn = conectar()
        sql_2 = ("SELECT id, clave, nombre, unidad_medida, peso, cantidad, estado, categoria FROM productos ORDER BY id DESC")
        conn.execute(sql_2)
        for row in conn.fetchall():
            tree.insert("", "end", values=row)
        cerrar_conectar(conn)

    # ---------- Limpiar formulario ----------
    def limpiar_campos():
        entry_clave.delete(0, "end")
        entry_nombre.delete(0, "end")
        entry_unidad.delete(0, "end")
        entry_peso.delete(0, "end")
        entry_cantidad.delete(0, "end")
        estado_var.set("8k")
        categoria_var.set("Ferretería")

    # ---------- Interfaz ----------
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Formulario de Productos")
    app.geometry("900x700")
    app.configure(fg_color="#649be2")  # Fondo azul a toda la ventana
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
    entry_clave = ctk.CTkEntry(frame, placeholder_text="Clave", width=200, corner_radius=15)
    entry_clave.grid(row=0, column=0, padx=10, pady=10)

    entry_nombre = ctk.CTkEntry(frame, placeholder_text="Nombre", width=200, corner_radius=15)
    entry_nombre.grid(row=0, column=1, padx=10, pady=10)

    entry_unidad = ctk.CTkEntry(frame, placeholder_text="Unidad Medida", width=200, corner_radius=15)
    entry_unidad.grid(row=0, column=2, padx=10, pady=10)

    entry_peso = ctk.CTkEntry(frame, placeholder_text="Peso", width=200, corner_radius=15)
    entry_peso.grid(row=1, column=0, padx=10, pady=10)

    entry_cantidad = ctk.CTkEntry(frame, placeholder_text="Cantidad", width=200, corner_radius=15)
    entry_cantidad.grid(row=1, column=1, padx=10, pady=10)

    # Radiobuttons Estado
    estado_var = ctk.StringVar(value="8k")
    estado_frame = ctk.CTkFrame(frame, fg_color="white")
    estado_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(estado_frame, text="Tipo material:").pack(anchor="w")
    ctk.CTkRadioButton(estado_frame, text="8k", variable=estado_var, value="8k").pack(anchor="w")
    ctk.CTkRadioButton(estado_frame, text="10k", variable=estado_var, value="10k").pack(anchor="w")
    ctk.CTkRadioButton(estado_frame, text="Ag", variable=estado_var, value="Ag").pack(anchor="w")

    # Radiobuttons Categoría
    categoria_var = ctk.StringVar(value="Ferreteria")
    categoria_frame = ctk.CTkFrame(frame, fg_color="white")
    categoria_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(categoria_frame, text="Categoría:").pack(anchor="w")
    ctk.CTkRadioButton(categoria_frame, text="Alimentos", variable=categoria_var, value="Alimentos").pack(anchor="w")
    ctk.CTkRadioButton(categoria_frame, text="Joyería", variable=categoria_var, value="Joyeria").pack(anchor="w")
    ctk.CTkRadioButton(categoria_frame, text="Ferretería", variable=categoria_var, value="Ferreteria").pack(anchor="w")

    # Botón Guardar
    btn_guardar = ctk.CTkButton(frame, text="Guardar", command=insertar_producto, corner_radius=20)
    btn_guardar.grid(row=2, column=2, padx=10, pady=10)

    # Treeview estilizado
    tree_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="white")
    tree_frame.pack(padx=20, pady=20, fill="both", expand=True)

    columns = ("ID", "Clave", "Nombre", "Unidad", "Peso", "Cantidad", "Estado", "Categoría")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    tree.pack(fill="both", expand=True)

    mostrar_productos()

    # ------------------- Footer -------------------
    footer = ctk.CTkLabel(
        app,
        text="© 2025 - Trabajo desarrollado para [Diamante Negro].\n"
               "Autor: Ing. Yolexis Herrera Espinosa\n"
             "Uso limitado y exclusivo. Contacto: yohepoli@gmail.com",
        font=("Arial", 12),
        text_color="white",
        justify="center"
    )
    footer.pack(side="bottom", pady=15)

    app.mainloop()
