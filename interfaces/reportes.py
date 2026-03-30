import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image
from tkcalendar import Calendar
from datetime import datetime
from utilidades.recursos import resource_path
from utilidades.exportar_excel import reporte_mensual, reporte_ferreteria


# ---------- Seleccionar fecha ----------
def seleccionar_fecha(entry, callback):
    
    def devolver_fecha():
        fecha = cal.get_date()   # dd/mm/yyyy
        top.destroy()
        callback(fecha)

    hoy = datetime.today()

    top = ctk.CTkToplevel(entry)
    top.title("Calendario")
    top.resizable(False, False)

    top.transient(entry)
    #top.grab_set()

    entry.update_idletasks()
    x = entry.winfo_rootx()
    y = entry.winfo_rooty() + entry.winfo_height() + 5
    top.geometry(f"+{x}+{y}")

    cal = Calendar(
        top,
        selectmode="day",
        year=hoy.year,
        month=hoy.month,
        day=hoy.day,
        date_pattern="dd/mm/yyyy",
        background="#649be2",
        foreground="white",
        headersbackground="#4a7dc1",
        headersforeground="white",
        selectbackground="#ffb703",
        selectforeground="black"
    )

    cal.pack(padx=10, pady=10)

    ttk.Button(top, text="Aceptar", command=devolver_fecha).pack(pady=(0, 10))

# ------------------- Ventana de reportes -------------------
def ventana_reportes():
    app = ctk.CTkToplevel()
    app.title("Reportes")
    app.geometry("950x610")
    app.configure(fg_color="#649be2")
    app.attributes('-topmost', True)

    # Icono
    icono = resource_path("imagenes/data_base.ico")
    try:
        app.iconbitmap(icono)
    except Exception:
        pass
    
    # Frame principal
    frame = ctk.CTkFrame(app, corner_radius=15, fg_color="white")
    frame.pack(pady=40, padx=40, fill="both", expand=True)

    # ------------------- Entradas de fecha -------------------
    fechas_frame = ctk.CTkFrame(frame, fg_color="white")
    fechas_frame.grid(row=0, column=0, columnspan=3, pady=20)

    fecha_inicial = ctk.StringVar()
    fecha_final = ctk.StringVar()

    # Label + entry fecha inicial
    lbl_inicio = ctk.CTkLabel(fechas_frame, text="Fecha Inicial:", font=("Arial", 16, "bold"))
    lbl_inicio.grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w")

    entry_fecha_inicial = ctk.CTkEntry(
        fechas_frame, placeholder_text="Seleccione la fecha inicial",
        textvariable=fecha_inicial, width=200, corner_radius=15
    )
    entry_fecha_inicial.grid(row=1, column=0, padx=10, pady=5)

    btn_fecha_inicial = ctk.CTkButton(
                        fechas_frame,
                        text="📅",
                        width=50,
                        command=lambda: seleccionar_fecha(entry_fecha_inicial, fecha_inicial.set)
                    )

    btn_fecha_inicial.grid(row=1, column=1, padx=5, pady=5)

    # Label + entry fecha final
    lbl_final = ctk.CTkLabel(fechas_frame, text="Fecha Final:", font=("Arial", 16, "bold"))
    lbl_final.grid(row=0, column=2, padx=10, pady=(0, 5), sticky="w")

    entry_fecha_final = ctk.CTkEntry(
        fechas_frame, placeholder_text="Seleccione la fecha final",
        textvariable=fecha_final, width=200, corner_radius=15
    )
    entry_fecha_final.grid(row=1, column=2, padx=10, pady=5)

    btn_fecha_final = ctk.CTkButton(
    fechas_frame,
    text="📅",
    width=50,
    command=lambda: seleccionar_fecha(entry_fecha_final, fecha_final.set)
)

    btn_fecha_final.grid(row=1, column=3, padx=5, pady=5)

    # ------------------- Cargar imágenes -------------------
    img = resource_path("imagenes/reporte_mensual.png")
    img1 = ctk.CTkImage(Image.open(img), size=(120, 120))
    img2 = ctk.CTkImage(Image.open(img), size=(120, 120))
    img3 = ctk.CTkImage(Image.open(img), size=(120, 120))

    # ------------------- Botones -------------------
    def ejecutar_reporte_mensual():
        if not fecha_inicial.get() or not fecha_final.get():
            messagebox.showerror("Error", "Debe seleccionar ambas fechas antes de generar el reporte", parent=app)
            return
        reporte_mensual(fecha_inicial.get(), fecha_final.get(),app)

    btn1 = ctk.CTkButton(
        frame,
        text="Reporte X Intervalo\nde tiempo JOYERÍA",
        image=img1,
        compound="top",
        command=ejecutar_reporte_mensual,
        width=220,
        height=220,
        fg_color="#649be2",
        hover_color="#4a7dc1",
        corner_radius=20,
        font=("Arial", 16, "bold")
    )
    btn1.grid(row=2, column=0, padx=30, pady=30)

    def ejecutar_reporte_ferreteria():
        if not fecha_inicial.get() or not fecha_final.get():
            messagebox.showerror("Error", "Debe seleccionar ambas fechas antes de generar el reporte", parent=app)
            return
        reporte_ferreteria(fecha_inicial.get(), fecha_final.get(),app)

    btn2 = ctk.CTkButton(
        frame,
        text="Reporte X Intervalo\nde tiempo FERRETERÍA",
        image=img2,
        compound="top",
        command=ejecutar_reporte_ferreteria,
        width=220,
        height=220,
        fg_color="#649be2",
        hover_color="#4a7dc1",
        corner_radius=20,
        font=("Arial", 16, "bold")
    )
    btn2.grid(row=2, column=1, padx=30, pady=30)

    btn3 = ctk.CTkButton(
        frame,
        text="Reporte de venta\nde Alimentos",
        image=img3,
        compound="top",
        command=lambda: messagebox.showinfo("Reporte", "Hay que implementar el reporte de venta\nde Alimentos", parent=app),
        width=220,
        height=220,
        fg_color="#649be2",
        hover_color="#4a7dc1",
        corner_radius=20,
        font=("Arial", 16, "bold")
    )
    btn3.grid(row=2, column=2, padx=30, pady=30)

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

