# -*- coding: utf-8 -*-
"""
Created on Wed Agosto 19 13:41:12 2025

@author: yolexis
"""

import tkinter as tk
from tkinter import messagebox
from models.conexion_sql import conectar
from models.conexion import conexion_db
from utilidades.decisiones import cancelar
from utilidades.criptografia import encripntar
import subprocess
import datetime
import os
import logging
from typing import Optional
from utilidades.recursos import resource_path
from pathlib import Path
import shutil
import fnmatch


def ejecutar_editar_usuario(usuario, usuario_nuevo,contrasena,ventana_0,ventana_principal):
    try:
        conexion = conectar()
        clave = encripntar(contrasena)
        sql=f"UPDATE usuarios  SET nombre='{usuario_nuevo}', clave='{clave}' WHERE nombre='{usuario}';"
        conexion.execute(sql)
        conexion.close()
        titulo = "Editar usuarios"
        mensaje = f'Los cambios en el usuario {usuario_nuevo}\n ha sido guardado con exitos'
        messagebox.showinfo(titulo,mensaje)
        ventana_0.destroy()
        ventana_principal.destroy()
        titulo = "Editar usuarios"
        mensaje = f'Vuelva a abrir el programa con las nuevas credenciales'
        messagebox.showinfo(titulo,mensaje)
    except Exception as ex:
        titulo = "Editar usuarios"
        mensaje = f'!!!!Error los cambios\n no se han guardado: \n {ex}'
        messagebox.showinfo(titulo,mensaje)   


def editar_usuario(usuario,ventana_principal):
    ventana_0 = tk.Tk()
    ventana_0.geometry("500x150")
    ventana_0.title("Editar usuario")
    #ventana_0.iconbitmap("imagenes/data_base.ico")
    ventana_0.config(bg="PowderBlue")
    ventana_0.resizable(0, 0)   
    icono = resource_path("imagenes/data_base.ico")
    ventana_0.iconbitmap(icono)
    
    def obtener_datos():
        nombre = campo_0.get()
        contrasena = campo_00.get()
        ejecutar_editar_usuario(usuario,nombre,contrasena,ventana_0,ventana_principal)
        
    #Usuario_editar
    etiqueta_0 = tk.Label(ventana_0, text='Usuario: ')
    etiqueta_0.config(font=("arial", 14, "bold"), bg="PowderBlue")
    etiqueta_0.grid(row=0, column=0, padx=10, pady=10)
    
    campo_0 = tk.Entry(ventana_0, textvariable=usuario)
    campo_0.config(font=("arial", 14), bg="White", width=30)
    campo_0.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
    
    etiqueta_00 = tk.Label(ventana_0, text='Clave: ')
    etiqueta_00.config(font=("arial", 14, "bold"), bg="PowderBlue")
    etiqueta_00.grid(row=1, column=0, padx=10, pady=10)
    
    campo_00 = tk.Entry(ventana_0)
    campo_00.config(font=("arial", 14), bg="White", width=30, show="*")
    campo_00.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
            
    boton_0 = tk.Button(ventana_0, command=obtener_datos)
    boton_0.config(bg="LimeGreen", activebackground="SpringGreen", fg="White", relief="groove", font=("arial", 12, 'bold')
                   , width=15,justify='center', border=5, text='Guardar')
    boton_0.grid(row=2, column=0, padx=15, pady=10, columnspan=2)
           
    
    titulo = "Cancelar BD"
    mensaje = "Desea cancelar la creación de la base de datos"
    boton_0 = tk.Button(ventana_0, text='Cancelar', width=15,justify='center', border=5, command=lambda:cancelar(ventana_0,titulo,mensaje))
    boton_0.config(bg="Crimson", activebackground="Red", fg="White", relief="groove", font=("arial", 12, 'bold'))
    boton_0.grid(row=2, column=2, padx=15, pady=10, columnspan=2)

    ventana_0.mainloop()
    
def datos_globales():
    conexion_0 = conexion_db()
    sql = "SELECT * FROM variables_globales"
    try:
        cursor = conexion_0.cursor()
        cursor.execute(sql)
        datos =cursor.fetchall()
        return datos
    except:
        titulo = "Conexion BD"
        mensaje = "No se han podido encontrar la variables globales.\n Compruebe q las ha creado correctamente."
        messagebox.showerror(titulo,mensaje)
    conexion_0.cerrar_db()
    
       

def encontrar_pg_dump(db_host: str) -> Optional[str]:
    """
    Busca pg_dump.exe primero en el PATH y luego en rutas locales y de red.
    """
    # 1️⃣ Buscar en PATH
    pg_dump_path = shutil.which("pg_dump")
    if pg_dump_path:
        return pg_dump_path

    # 2️⃣ Posibles rutas estándar (locales y red)
    rutas_comunes = [
        rf"C:\Program Files\PostgreSQL",
        rf"C:\Program Files (x86)\PostgreSQL",
        rf"\\{db_host}\PostgreSQL",           # Ruta en red
        rf"\\{db_host}\C$\Program Files\PostgreSQL",   # Admin share en red
        rf"\\{db_host}\C$\Program Files (x86)\PostgreSQL"
    ]

    for ruta_base in rutas_comunes:
        if os.path.exists(ruta_base):
            for root, dirs, files in os.walk(ruta_base):
                for filename in fnmatch.filter(files, "pg_dump.exe"):
                    return os.path.join(root, filename)

    return None

def salva_database():
    datos_glob = datos_globales()  # ← Tu función que obtiene datos
    db_user = datos_glob[0][0]
    db_password = datos_glob[0][1]
    db_host = datos_glob[0][2]
    db_port = datos_glob[0][3]
    db_name = datos_glob[0][4]

    # Buscar pg_dump automáticamente
    pg_dump_path = encontrar_pg_dump(db_host)
    if not pg_dump_path:
        raise FileNotFoundError(
            "No se encontró 'pg_dump'. "
            "Instala PostgreSQL o asegúrate de que la carpeta 'bin' esté accesible."
        )

    output_dir = Path("C:/Diamantes_salvaDB")
    custom_filename: Optional[str] = None

    try:
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = custom_filename or f"backup_{db_name}_{timestamp}.sql"
        backup_path = output_dir / backup_filename

        env = os.environ.copy()
        env["PGPASSWORD"] = db_password

        pg_dump_cmd = [
            pg_dump_path,
            "-h", db_host,
            "-p", str(db_port),
            "-U", db_user,
            "-d", db_name,
            "-F", "p",
            "-f", str(backup_path)
        ]

        logging.info(f"Iniciando backup de la base de datos {db_name}")

        result = subprocess.run(pg_dump_cmd, env=env, capture_output=True, text=True)

        if result.stdout:
            print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        result.check_returncode()

        logging.info(f"Backup completado exitosamente en: {backup_path}")
        titulo='Salva'
        mensaje=f'Salva creada correctamente en: \n{output_dir}'
        messagebox.showinfo(titulo,mensaje)
        return str(backup_path)

    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar pg_dump: {e}")
        raise RuntimeError(f"Error ejecutando pg_dump: {e.stderr}") from e
    except Exception as e:
        logging.error(f"Error inesperado durante el backup: {e}")
        raise