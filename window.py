import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
import funsLL
import sqlite3
from modelslite_LL import db_path

LL = funsLL.app_LL()
BBDD_op = db_path

app = ttk.Window(
    title = LL.title,
    themename = LL.theme_df,
    size=(700, 700),
    resizable=( 0, True),
    minsize=(500, 500),
    iconphoto='src/LL.png'
)
LL.set_app(app)

#Configuracion de filas y columnas general

app.columnconfigure(0, weight=0)
app.columnconfigure(1, weight=2)
app.rowconfigure(0, weight=0)
app.rowconfigure(1, weight=0)
app.rowconfigure(2, weight=3)

### Configuracion general

#Header

header = ttk.Frame(app, bootstyle=INFO)
header.grid(column=0, row=0, columnspan=2, sticky="nswe")

ttk.Label( #Titulo de Header LL
    header,
    bootstyle = "success",
    text="To Do LL",
    font=("Impact", 22),
    padding = (25, 5)
).pack()

#############################
#      Funciones main
#############################

def MenusAPP(frame, name, estilo, list_op): #Funcion para crear los menus de la navbar
    "Aqui se simplifica la logica"
    btt = ttk.Menubutton(
            frame,
            text = f"{name}",
            bootstyle = estilo,
            padding = (30, 5)
        )
    btt.pack(side = "left")

    menu_add = ttk.Menu(btt, tearoff = 0)

    for ss, func in list_op:
        menu_add.add_command(label = ss, command=func)
    btt['menu'] = menu_add
    return menu_add

def crear_menu_usr(): #Funcion para crear el menu de usuario en la navbar
    "Aqui se despliegan las opciones del menu segun el estado del usuario"

    # limpiar navbar del menú anterior
    for w in centerNav.winfo_children():
        w.destroy()

    # elegir opciones según estado del usuario
    if LL.usr_log == 0:
        lista_usr = [
            ("Login", lambda: log_LL(LL.Login_LL())),
            ("Crear", lambda: LL.crear_usr()),
            ("info...", lambda: LL.__ventana_explicacion__())
        ]
    else:
        lista_usr = [
            ("Perfil", lambda: LL.ver_datos_perfil()),
            ("Logout", lambda: logout_LL()),
            ("Guia", lambda: LL.__ventana_guia_breve__())
        ]

    # Crear el Menubutton con las opciones correctas
    MenusAPP(centerNav, 'User', PRIMARY, lista_usr)
    
    
    lista_secciones = [
        ("ver Proyectos",lambda: LL.ver_proyectos()),
        ("Ver usuarios", lambda: LL.ver_usuarios_claves())
    ]
    MenusAPP(centerNav, "Secciones", "SUCCESS-outline", lista_secciones)

    lista_app = [
            ('cambiar tema', lambda: LL.cambiar_tema()),
            ('About LL', lambda: LL.about_LL()),
            ('refresh', lambda: refrescar_todo()),            
            ('exit', lambda: LL.exit_app(app))
        ]
    MenusAPP(centerNav, "app", PRIMARY, lista_app)
    
def log_LL(win): #Complementacion del Login
    win.wait_window()
    refrescar_todo()

def logout_LL(): #Complementacion del Logout
    LL.logout_user()
    refrescar_todo()
    
def refrescar_todo(): # Refresca todo el contenido de la app segun el estado del usuario
    global frame_proyectos, usr_frame, s, add_frame

    # 1. limpiar frames
    for w in frame_proyectos.winfo_children():
        w.destroy()

    for w in usr_frame.winfo_children():
        w.destroy()
    
    for w in s.winfo_children():
        w.destroy()
    
    for w in add_frame.winfo_children():
        w.destroy()

    crear_barra_superior_proyectos()
    crear_barra_superior_usuarios()
    crear_menu_usr()
    
    # 2. volver a cargar según login
    if LL.usr_log == 1 or LL.var_log_dinamica == 1:
        desplegar_proyecto(frame_proyectos)
        desplegar_usuarios(usr_frame)
    else:
        peticicion_pro_log()
        peticicion_log()

    # 3. actualizar título
    app.title(LL.title)

#############################
#         Navbar
#############################

navbar = ttk.Frame(app, bootstyle=INFO)
navbar.grid(column=1, row=1, sticky="nsew", padx=0, pady=0)

for nBar in range(2):
    navbar.columnconfigure(nBar, weight=0)

ttk.Label(navbar, text = "NAVEGA >", padding = (30, 5), bootstyle = 'INVERSE-SUCCESS').grid(row = 0, column = 0) #Estilo nada mas

centerNav = ttk.Frame(navbar) #Aqui se desplegaran los botones de ls opciones en el navbar
centerNav.grid(row = 0, column = 1)

crear_menu_usr()

#############################
#         Contenido
#############################

contenido = ttk.Frame(
    app,
    bootstyle = DARK
    )
contenido.grid(column=0, row=2, sticky="nsew", columnspan=2)

contenido.rowconfigure(0, weight=1)
contenido.rowconfigure(1, weight=1)
contenido.columnconfigure(0, weight=1)
contenido.columnconfigure(1, weight=4)

#############################
#         Notebook
#############################

note = ttk.Notebook(contenido, bootstyle = SUCCESS)
note.grid(column = 0, row = 0, sticky="nsew", rowspan= 2, columnspan=2)

#Tareas Notebook
opcion_task = ttk.Frame(note)
note.add(opcion_task, text = "Tareas")

opcion_task.rowconfigure(0, weight=1)
opcion_task.rowconfigure(1, weight=1)
opcion_task.columnconfigure(0, weight=1)
opcion_task.columnconfigure(1, weight=4)

contenedor_tareas = ttk.Frame(opcion_task)
contenedor_tareas.grid(column=1, row=0, sticky="nsew", rowspan=2)

"""
Aqui se despliegan las tareas en el contenedor de tareas
"""

def desplegar_tareas(contenedor): #Funcion para desplegar las tareas en el contenedor
    from tkinter import BooleanVar
    import textwrap    

    for widget in contenedor.winfo_children():
        widget.destroy()

    conn = sqlite3.connect(BBDD_op)
    cursor = conn.cursor()
    cursor.execute("SELECT ID, tarea, estado FROM tareas_programa")
    tareas = cursor.fetchall()
    conn.close()

    contenedor.rowconfigure(0, weight=1)
    contenedor.columnconfigure(0, weight=1)

    sf = ScrolledFrame(contenedor, autohide=True)
    sf.grid(column=0, row=0, sticky="nsew", rowspan=2)

    for idx, (task_id, descripcion, estado) in enumerate(tareas):
        estado_var = BooleanVar(value=bool(estado))
        descripcion_wrapped = "\n".join(textwrap.wrap(descripcion, width=50))

        def actualizar_estado(var=estado_var, id=task_id):
            nuevo_estado = int(var.get())
            conn = sqlite3.connect(BBDD_op)
            cursor = conn.cursor()
            cursor.execute("UPDATE tareas_programa SET estado=? WHERE ID=?", (nuevo_estado, id))
            conn.commit()
            conn.close()

        chk = ttk.Checkbutton(
            sf,
            text=descripcion_wrapped,
            variable=estado_var,
            bootstyle="success-round-toggle",
            command=actualizar_estado
        )
        chk.grid(row=idx, column=2, sticky="w", padx=10, pady=5)

        ttk.Button(sf, text = "X", bootstyle = DANGER, padding=(5, 1),
                    command= lambda id=task_id, titulo=descripcion: eliminar_y_actualizar(id, titulo)).grid(row = idx, column = 0, padx = 10, sticky='s', pady = 10)
        
        ttk.Button(sf, text = "E", bootstyle = SECONDARY, padding=(5, 1),      
                   command= lambda pid = task_id: editar_y_actualizar(pid)).grid(row = idx, column = 1, padx = 10, sticky='s', pady = 10)

sidebar = ttk.Frame(opcion_task, bootstyle = DARK)
sidebar.grid(column = 0, row = 0, sticky="nsew", rowspan = 2)

sidebar.rowconfigure(0, weight=1)
sidebar.rowconfigure(1, weight=1)

ttk.Button(
    sidebar,
    text = "Nueva tarea",
    bootstyle = "LIGHT,",
    command = lambda: tareas_nuevas(contenedor_tareas),
    padding = (10, 5)
    ).grid(column = 0, row = 0, sticky="n", padx = 20, pady = 10)

def tareas_nuevas(contenedor): #Funcion para agregar nuevas tareas
    win = LL.add_task()
    win.wait_window()
    desplegar_tareas(contenedor)

def editar_y_actualizar(id): #Funcion para editar tareas
    win = LL.edit_task(id)
    win.wait_window()
    desplegar_tareas(contenedor_tareas)

def eliminar_y_actualizar(id, titulo): #Funcion para eliminar tareas
    LL.delete_task(id, titulo)
    desplegar_tareas(contenedor_tareas)

desplegar_tareas(contenedor_tareas)


# Yo ordene a mi alma que borrara
# Que no te amara
# y se rio en mi cara
# cronica de una muerte anunciada
# Sin ti mi vida, no conduce a nada


#Proyectos Notebook
opciones_proyectos = ttk.Frame(note)
note.add(opciones_proyectos, text = "Proyectos")

opciones_proyectos.rowconfigure(0, weight=0)
opciones_proyectos.rowconfigure(1, weight=1)
opciones_proyectos.columnconfigure(0, weight=0)
opciones_proyectos.columnconfigure(1, weight=1)

frame_proyectos = ttk.Frame(opciones_proyectos)
frame_proyectos.grid(column=0, row=1, columnspan=2, sticky="nsew")

"""Aqui se despliegan los proyectos en el contenedor de proyectos"""

def desplegar_proyecto(contenedor):
    for widget in contenedor.winfo_children():
        widget.destroy()

    conn = sqlite3.connect(BBDD_op)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ID_proyecto, Titulo, Sipnosis, Descripcion, FechaCreacion, FechaEntrega, Estado, usr_propietario, ID_usr_propietario 
        FROM proyectos_usr
        WHERE ID_usr_propietario = ?
    """, (LL.usr_ID,))
    data = cursor.fetchall()
    conn.close()

    contenedor.rowconfigure(0, weight=1)
    contenedor.columnconfigure(0, weight=1)

    sf = ScrolledFrame(contenedor, autohide=True)
    sf.grid(column=0, row=0, sticky="nsew", rowspan=2, padx=10, pady=5)

    for idx, (id_proyecto, ss, sipnosis, descripcion, fecha_creacion, fecha_entrega, estado, usr_p, usr_id_p) in enumerate(data):
        dios = ttk.Labelframe(
            sf,
            text=ss,
            bootstyle=SUCCESS
        )
        dios.grid(row=idx, column=0, sticky="ew", padx=10, pady = 5)

        ttk.Button(sf, text = "Editar", bootstyle = SECONDARY, padding=(25, 5),      
                   command=lambda pid = id_proyecto: editar_p(pid)).grid(row = idx, column = 1, padx = 10, sticky='N', pady = 15)
        

        ttk.Button(sf, text = "borrar", bootstyle = DANGER, padding=(25, 5),
                    command= lambda id=id_proyecto, titulo=ss: eliminar_p(id, titulo)).grid(row = idx, column = 1, padx = 10, sticky='s', pady = 10)

        ttk.Label(dios,
            text=f"{sipnosis}",
            wraplength=300,
            bootstyle=INFO,
            font = 22, padding=(20, 5)
        ).pack(anchor="w", padx=10, pady=5)

        ttk.Button(
            dios,
            text="ver más...",
            bootstyle="INFO",
            command= lambda id = id_proyecto: LL.vermasproyectos(id)
        ).pack(anchor="e", padx=10, pady=5)

s = ttk.Frame(opciones_proyectos, bootstyle = DARK)
s.grid(column=0, row=0, sticky="nsew", columnspan=2)

def crear_barra_superior_proyectos(): #Funcion para crear la barra superior de proyectos segun el estado del usuario
    # Limpiar la barra
    for w in s.winfo_children():
        w.destroy()

    # Si hay sesión → botón de Nuevo Proyecto
    if LL.usr_log == 1 or LL.var_log_dinamica == 1:
        ttk.Button(
            s,
            text="Nuevo Proyecto",
            bootstyle="LIGHT",
            command=lambda: proyecto_nuevo(frame_proyectos)
        ).pack(padx=10, pady=10, side=LEFT)

    # Si NO hay sesión → botón de Iniciar Sesión
    else:
        ttk.Button(
            s,
            text="Iniciar Sesion",
            bootstyle="INFO",
            command=lambda: log_LL(LL.Login_LL())
        ).pack(pady=10)

def peticicion_pro_log(): #Mensaje para pedir iniciar sesion en proyectos en caso de no haber sesion iniciada
    for w in frame_proyectos.winfo_children():
        w.destroy()

    ttk.Label(
        frame_proyectos,
        text="Debes iniciar sesion para ver tu proyectos\nQue te corresponden.",
        bootstyle="INVERSE-DANGER",
        font = ("Arial", 16),
        padding = (20, 20)
    ).pack()

def proyecto_nuevo(contenedor): #Funcion para agregar nuevos proyectos
    if LL.usr_log == 1 or LL.var_log_dinamica == 1:
        win = LL.add_proyecto()
        win.wait_window()
        desplegar_proyecto(contenedor)
    else:
        Messagebox.show_error("Debes iniciar sesion para agregar proyectos.", "Error de permisos")

def editar_p(id): #Funcion para editar proyectos
    if LL.usr_log == 1 or LL.var_log_dinamica == 1:
        win = LL.edit_proyecto(id)
        win.wait_window()
        desplegar_proyecto(frame_proyectos)
    else:
        Messagebox.show_error("Debes iniciar sesion para editar proyectos.", "Error de permisos")

def eliminar_p(id, titulo): #Funcion para eliminar proyectos
    if LL.usr_log == 1 or LL.var_log_dinamica == 1:
        LL.delete_proyecto(id, titulo)
        desplegar_proyecto(frame_proyectos)
    else:
        Messagebox.show_error("Debes iniciar sesion para eliminar proyectos.", "Error de permisos")

if LL.usr_log == 1 or LL.var_log_dinamica == 1:
    desplegar_proyecto(frame_proyectos)
    crear_barra_superior_proyectos()  
else:
    peticicion_pro_log()
    crear_barra_superior_proyectos()

    """
    Esta estructura condicional evalua
    si hay una sesion iniciada o no 
    y despliega los proyectos correspondientes
    o un mensaje pidiendo iniciar sesion
    """

#Usuarios&claves Notebook
Opciones_Claves = ttk.Frame(note)
note.add(Opciones_Claves, text = "User & Claves")

Opciones_Claves.rowconfigure(0, weight=0)
Opciones_Claves.rowconfigure(1, weight=1)
Opciones_Claves.columnconfigure(0, weight=0)
Opciones_Claves.columnconfigure(1, weight=1)

usr_frame = ttk.Frame(Opciones_Claves)
usr_frame.grid(column=0, row=1, columnspan=2, sticky="nsew")

"""Aqui se despliegan los usuarios en el contenedor de usuarios"""

def desplegar_usuarios(contenedor):
    for widget in contenedor.winfo_children():
        widget.destroy()

    conn = sqlite3.connect(BBDD_op)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ID, dominio, username, password, email
        FROM claves_personales 
        WHERE ID_usr_propietario = ?
    """, (LL.usr_ID,))
    usuarios = cursor.fetchall()
    conn.close()

    contenedor.rowconfigure(0, weight=1)
    contenedor.columnconfigure(0, weight=1)

    sf = ScrolledFrame(contenedor, autohide=True)
    sf.grid(column=0, row=0, sticky="nsew", padx=10, pady=5)
        
    for idx, (IDd, dominio, username, password, email) in enumerate(usuarios):
        usuario_frame = ttk.Labelframe(
            sf,
            text=dominio,
            bootstyle="SUCCESS"
        )
        usuario_frame.grid(row=idx, column=0, sticky="ew", padx=10, pady=5)

        ttk.Label(
            usuario_frame,
            text=f"Username: {username}\nemail: {email}",
            wraplength=300,
            bootstyle="PRIMARY"
        ).pack(anchor="w", padx=10, pady=5)       

        ttk.Button(
            usuario_frame,
            text="Mostrar Password",
            bootstyle="INFO",
            command= lambda usrid= IDd: LL.ver_detaller_usr_clave(usrid)
        ).pack(anchor="e", padx=10, pady=5)

        ttk.Button(
            sf,
            text="Borrar",
            bootstyle="DANGER",
            command= lambda ID_usr=IDd, user_name=username: eliminar_usr(ID_usr, user_name)
        ).grid(row=idx, column=1, padx=10, sticky='e', pady=10)

        ttk.Button(
            sf,
            text="Editar",
            bootstyle="SECONDARY",
            command= lambda ID_usr=IDd: actualizar_usr(ID_usr)
        ).grid(row=idx, column=2, padx=10, sticky='w', pady=10)
    

add_frame = ttk.Frame(Opciones_Claves, bootstyle=DARK)
add_frame.grid(column=0, row=0, columnspan=2, sticky="nsew")

def crear_barra_superior_usuarios(): #Funcion para crear la barra superior de usuarios segun el estado del usuario
    # Limpiar la barra
    for w in add_frame.winfo_children():
        w.destroy()

    if LL.usr_log == 1 or LL.var_log_dinamica == 1:
        ttk.Button(add_frame, text="Agregar Usuario", bootstyle="LIGHT", command=lambda: usr_nuevo(usr_frame)).pack(padx=10, pady=10, side = LEFT)
        ttk.Label(add_frame, text=f"{LL.usrname}", bootstyle="INVERSE-DARK", font=("Arial", 16)).pack(padx=10, pady=10, side = LEFT)
    else:
        ttk.Button(add_frame, text="Iniciar Sesion", bootstyle="INFO", command=lambda: log_LL(LL.Login_LL())).pack(pady=10)    

def peticicion_log(): #Mensaje para pedir iniciar sesion en usuarios en caso de no haber sesion iniciada
    ttk.Label(
        usr_frame,
        text="Debes iniciar sesion para ver los usuarios y claves\nQue te corresponden.",
        bootstyle="INVERSE-DANGER",
        font = ("Arial", 16),
        padding = (20, 20)
    ).pack()

def usr_nuevo(contenedor): #Funcion para agregar nuevos usuarios
    if LL.usr_log == 1 or LL.var_log_dinamica == 1 or LL.usr_state:
        win = LL.add_userkey()
        win.wait_window()
        desplegar_usuarios(contenedor)
    else:
        Messagebox.show_error("Debes iniciar sesion para agregar usuarios y claves.", "Error de permisos")

def actualizar_usr(id): #Funcion para editar usuarios
    if LL.usr_log == 1 or LL.var_log_dinamica == 1:
        win = LL.editar_usr_clave(id)
        win.wait_window()
        desplegar_usuarios(usr_frame)
    else:
        Messagebox.show_error("Esto no deberia ni de aparecer xD", "Error de permisos")

def eliminar_usr(id, titulo): #Funcion para eliminar usuarios
    if LL.usr_log == 1 or LL.var_log_dinamica == 1:
        LL.delete_usr(id, titulo)
        desplegar_usuarios(usr_frame)
    else:
        Messagebox.show_error("Esto no deberia ni de aparecer xD", "Error de permisos")

if LL.usr_log or LL.var_log_dinamica == 1:
    desplegar_usuarios(usr_frame)
    crear_barra_superior_usuarios()
elif not LL.usr_log:
    peticicion_log()
    crear_barra_superior_usuarios()

    """
    Esta estructura condicional evalua
    si hay una sesion iniciada o no
    y despliega los usuarios y claves correspondientes
    o un mensaje pidiendo iniciar sesion
    """