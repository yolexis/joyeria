import tkinter as tk
from utilidades.recursos import resource_path
from tkinter import ttk

def informacion(root):
    #ventana = tk.Toplevel(root)
    ventana = tk.Tk()
    ventana.title("Información de contacto")
    ventana.resizable(False, False)
    ventana.geometry("420x260")

    icono = resource_path("imagenes/data_base.ico")
    try:
        ventana.iconbitmap(icono)
    except Exception:
        pass

    # Centrar la ventana
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (420 // 2)
    y = (ventana.winfo_screenheight() // 2) - (260 // 2)
    ventana.geometry(f"420x260+{x}+{y}")

    # Marco principal
    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    texto = (
        "Este software fue desarrollado por:\n\n"
        "Ing. Yolexis Herrera Espinosa\n"
        "Teléfono: +53 54813576\n"
        "Correo: yohepoli@gmail.com\n\n"
        "Uso exclusivo de Joyería Diamante Negro\n"
        "Todos los derechos reservados"
    )

    lbl_info = ttk.Label(
        frame,
        text=texto,
        justify="center",
        anchor="center",
        font=("Segoe UI", 10)
    )
    lbl_info.pack(expand=True)

    # Botón cerrar
    btn_cerrar = ttk.Button(frame, text="Cerrar", command=ventana.destroy)
    btn_cerrar.pack(pady=10)

    #ventana.transient(root)
    ventana.grab_set()