import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.constants import *

'''
esto sera para las ventanas emergentes
'''

def __ventanaDeRegistosfun__(titulo_WWII, accion):
        def decorador(funcion):
            def func_arg(*args,**kwargs):

                WWII = ttk.Toplevel(title = titulo_WWII, size=(250, 100), resizable=( 0, 0))

                for log in range(3):
                    WWII.columnconfigure(log, weight=1)
                    WWII.rowconfigure(log, weight=1)

                ttk.Label(WWII, bootstyle = SUCCESS, text='username >').grid(row = 0, column = 0)
                usr_entry = ttk.Entry(WWII, bootstyle = SECONDARY)
                usr_entry.grid(row = 0, column = 1)

                ttk.Label(WWII, bootstyle = SUCCESS, text='password >').grid(row = 1, column = 0)
                pass_entry = ttk.Entry(WWII, bootstyle = SECONDARY, show="*")
                pass_entry.grid(row = 1, column = 1)

                def ej():
                    funcion(*args, usr_entry=usr_entry, pass_entry=pass_entry, **kwargs)
                    WWII.destroy()

                ttk.Button(WWII, text=f"{accion}", command= lambda: ej()).grid(row = 3)
                
                return WWII
            
            return func_arg
        return decorador

def __ventanaDeProyectos__():
    def decorador(funcion):
        def func_arg(*args, **kwargs):
            Project_window = ttk.Toplevel(title="Nuevo proyecto", size=(700, 600))

            for c in range(5):
                Project_window.columnconfigure(c, weight=1)

            for r in range(7):
                Project_window.rowconfigure(r, weight=1)

            ttk.Label(Project_window, bootstyle=SUCCESS, text="Titulo", font=28).grid(row=0, column=0)
            title_entry = ttk.Entry(Project_window, bootstyle=SUCCESS)
            title_entry.grid(row=0, column=1, sticky="w")

            ttk.Label(Project_window, bootstyle=SUCCESS, text="Sinopsis", font=28).grid(row=1, column=0)
            sinop_entry = ttk.Entry(Project_window, bootstyle=SUCCESS)
            sinop_entry.grid(row=1, column=1, columnspan=2, sticky="nsew")

            ttk.Label(Project_window, bootstyle=DARK, text="Descripcion", font=28).grid(row=2, column=0, sticky="w")
            desc_entry = ScrolledText(Project_window, bootstyle=SUCCESS, height=25, width=40, font=20)
            desc_entry.grid(row=3, column=0, columnspan=2, rowspan=2, sticky="nsew")

            ttk.Label(Project_window, bootstyle=INFO, text="Fecha de entrega").grid(row=0, column=3)
            fecha_estimada = ttk.DateEntry(Project_window, bootstyle=SECONDARY)
            fecha_estimada.grid(row=1, column=3)

            ttk.Label(Project_window, bootstyle=INFO, text="fecha de creacion", font=30).grid(row=2, column=3)
            fecha_creacion = ttk.DateEntry(Project_window, bootstyle=SECONDARY)
            fecha_creacion.grid(row=3, column=3, sticky="n")

            estado_var = ttk.StringVar(value=0)
            def set_estado(valor):
                estado_var.set(valor)

            ttk.Label(Project_window, bootstyle=DARK, text="estado", font=30).grid(row=4, column=3, sticky="sw")
            ttk.Checkbutton(Project_window, bootstyle="danger-toolbutton", text="Finalizado", padding=(40, 5), variable=estado_var, onvalue=1, offvalue=0,command=lambda: set_estado(1)).grid(row=5, column=3, sticky="nw")
            ttk.Checkbutton(Project_window, bootstyle="success-toolbutton", text="Activo", padding=(40, 5), variable=estado_var, onvalue=0, offvalue=0, command=lambda: set_estado(0)).grid(row=5, column=4,sticky="nw")

            def ej():
                funcion(
                    *args,
                    title_entry=title_entry,
                    sinop_entry=sinop_entry,
                    desc_entry=desc_entry,
                    fecha_estimada=fecha_estimada,
                    fecha_creacion=fecha_creacion,
                    estado=estado_var.get(),
                    **kwargs
                )
                Project_window.destroy()

            ttk.Button(Project_window, bootstyle="SUCCESS", text="Guardar", command=ej).grid(row=6, column=0)

            return Project_window

        return func_arg
    return decorador

"""
Solo se crearon algunas
Pero en un futuro se iran agregando mas
ventanas emergentes
Para simplificar la logica en el modulo FunsLL.py
y en window.py
"""