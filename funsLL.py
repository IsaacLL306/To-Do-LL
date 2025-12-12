import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText, ScrolledFrame
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import sqlite3
from PIL import Image, ImageTk
from V import __ventanaDeRegistosfun__, __ventanaDeProyectos__
import webbrowser as www
from modelslite_LL import db_path

BBDD_op = db_path


conn = sqlite3.connect(BBDD_op)
cursor = conn.cursor()
config = cursor.execute("SELECT ID_config, usr_log, usr_save, usr_save_ID, theme_last, title FROM config_programa")
config = cursor.fetchone()
conn.close()

if config:
    ID_config, usr_log, usr_save, usr_save_ID, theme_last, title_v = config
else:
    ID_config = usr_log = usr_save_ID = 0
    usr_save = "None"
    theme_last = "solar"

class app_LL():
    

    def __init__(self): #Valores principales
        self.app = NONE
        self.usrname = usr_save
        self.usr_ID = usr_save_ID
        self.theme_df = theme_last
        self.usr_state = False
        self.usr_log = usr_log
        self.title = title_v

        self.var_log_dinamica = None
        self.version_app = "v1.0.0 LL"
    
    def set_app(self, app): #Funcion sobre la ventana
        """Asignar la ventana principal después de crearla"""
        self.app = app
        
        'No tocar de ser necesario'
        'Funciona para el cambio de tema dinámico'

    def cambiar_tema(self): #El mismo nombre lo indica
        # Cambia el tema a preferencia del usuario claro u oscuro
        connect_LL = sqlite3.connect(BBDD_op)
        point = connect_LL.cursor()
        point.execute("SELECT theme_last FROM config_programa WHERE ID_config = 1")
        tema = point.fetchone()
        connect_LL.close()

        if tema:
            tema_val = tema[0]
        else:
            return

        # Alternar tema
        if tema_val in ("darkly", "solar", "cyborg"):
            new_tema = "lumen"
            self.tema_dinamico = "oscuro"
        else:
            new_tema = "darkly"
            self.tema_dinamico = "SUCCESS"

        # Actualizar BD
        connect_LL = sqlite3.connect(BBDD_op)
        point = connect_LL.cursor()
        point.execute(
            "UPDATE config_programa SET theme_last = ? WHERE ID_config = 1",
            (new_tema,)
        )
        connect_LL.commit()
        connect_LL.close()

        # 🔄 Aplicar el tema dinámicamente
        if self.app:
            self.app.style.theme_use(new_tema)
        else:
            print("no se aplica el tema")

    ###########################
    # Seccion de tareas

    def add_task(self): #Añadir una tarea
        task_window = ttk.Toplevel(title="Añadir Tareas", size=(400, 150), resizable=(0, 0))

        ttk.Label(task_window, bootstyle="INVERSE-PRIMARY", text="Tarea nueva", font=20, padding = (25, 3)).grid(row=0, column=0, pady =10, sticky="E")
        task_entry = ttk.Entry(task_window, bootstyle=PRIMARY, width=30)
        task_entry.grid(row=0, column=1, sticky="W")

        def registrar():
            task_r = task_entry.get()
            if task_r:
                conn = sqlite3.connect(BBDD_op)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO tareas_programa (tarea, estado) VALUES (?, ?)", (task_r, 0))
                conn.commit()
                conn.close()

            task_window.destroy()

        ttk.Button(task_window, bootstyle=PRIMARY, text="Guardar", command=registrar).grid(row=1, column=0, pady=10)
        return task_window
    
    def edit_task(self, id_task): # Edita una tarea 'X' en caso de que el usuario quiera cambiarla o modificarla
        task_window = ttk.Toplevel(title="Añadir Tareas", size=(300, 100), resizable=(0, 0))

        conn = sqlite3.connect(BBDD_op)
        cursor = conn.cursor()
        cursor.execute("SELECT tarea, estado FROM tareas_programa WHERE ID = ?", (id_task,))
        datos = cursor.fetchone()
        conn.close()

        if datos:
            tarea_val, estado_val = datos
        else:
            tarea_val = estado_val = ""

        ttk.Label(task_window, bootstyle="INVERSE-SUCCESS", text="Tarea nueva", font=20).grid(row=0, column=0)
        task_entry = ttk.Entry(task_window, bootstyle=PRIMARY)
        task_entry.grid(row=0, column=1)
        task_entry.insert(0, tarea_val)

        def actualizar_task():
            task_r = task_entry.get()

            conn = sqlite3.connect(BBDD_op)
            cursor = conn.cursor()
            cursor.execute("UPDATE tareas_programa SET tarea = ? WHERE ID = ?", (task_r, int(id_task)))
            conn.commit()
            conn.close()

            Messagebox.ok(f"Tarea '{task_r}' actualizada correctamente", title="Done", alert=True)
            task_window.destroy()
        ttk.Button(task_window, bootstyle="SUCCESS", text="Guardar", command=actualizar_task).grid(row=1, column=0)
        return task_window

    
    def delete_task(self, id_task, name): # Elimina una tarea 'X' en caso de que el usuario quiera borrarla
        conn = sqlite3.connect(BBDD_op)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tareas_programa WHERE ID = ?", (id_task,))
        conn.commit()
        conn.close()
        Messagebox.ok(f"'{name}' eliminado correctamente", title="Done", alert=True)

    ###########################
    #Seccion de proyectos
        
    @__ventanaDeProyectos__() # Este decorador crea la ventana de proyectos, proviene del modulo V.py
    def add_proyecto(self, title_entry = None, sinop_entry = None, desc_entry = None, fecha_estimada = None, fecha_creacion = None, estado = 0): #Añade un nuevo proyecto
        connect_P = sqlite3.connect(BBDD_op)
        pointP = connect_P.cursor()

        title_r = title_entry.get()
        sinop_r = sinop_entry.get()
        desc_r = desc_entry.get("1.0", "end-1c")
        date_r = fecha_estimada.entry.get()
        date_create = fecha_creacion.entry.get()
        print(f"usr - {self.usr_log}")
        
        if self.usr_log == 0:
            pointP.execute("""
            INSERT INTO proyectos_usr (titulo, Sipnosis, descripcion, FechaEntrega, Estado, FechaCreacion, usr_propietario, ID_usr_propietario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (title_r, sinop_r, desc_r, date_r, estado, date_create, "ANONIMO", None))
            connect_P.commit()
            connect_P.close()
            Messagebox.ok(f"Proyecto '{title_r}' creado correctamente", title="Done", alert=True)
        elif self.usr_log == 1:
            pointP.execute("""
            INSERT INTO proyectos_usr (titulo, Sipnosis, descripcion, FechaEntrega, Estado, FechaCreacion, usr_propietario, ID_usr_propietario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (title_r, sinop_r, desc_r, date_r, estado, date_create, self.usrname, self.usr_ID))
            connect_P.commit()
            connect_P.close()
            Messagebox.ok(f"Proyecto '{title_r}' creado correctamente", title="Done", alert=True)
        
        " Con esta funcion se añade un nuevo proyecto a la base de datos"
        " Si el usuario no ha iniciado sesion, el proyecto se guarda como 'ANONIMO' y sin ID de usuario"
        " Si el usuario ha iniciado sesion, el proyecto se guarda con su nombre e ID de usuario"
        " Esto permite gestionar proyectos de usuarios registrados y anonimos"
    
    def edit_proyecto(self, id_proyecto): # Edita un proyecto 'X' en caso de que el usuario quiera cambiarlo o modificarlo
        Project_window = ttk.Toplevel(title="Editar proyecto", size=(700, 600))

        for c in range(5):
            Project_window.columnconfigure(c, weight=1)
        for r in range(7):
            Project_window.rowconfigure(r, weight=1)

        # --- Traer datos ---
        conn = sqlite3.connect(BBDD_op)
        cursor = conn.cursor()
        cursor.execute("""SELECT titulo, Sipnosis, descripcion, FechaEntrega, FechaCreacion, Estado 
                        FROM proyectos_usr WHERE ID_proyecto = ?""", (id_proyecto,))
        data = cursor.fetchone()
        conn.close()

        if data:
            titulo_val, sinop_val, desc_val, fecha_entrega_val, fecha_creacion_val, estado_val = data
        else:
            titulo_val = sinop_val = desc_val = fecha_entrega_val = fecha_creacion_val = estado_val = ""

        # --- Campos ---
        ttk.Label(Project_window, bootstyle=SUCCESS, text="Titulo", font=28).grid(row=0, column=0)
        title_entry = ttk.Entry(Project_window, bootstyle=SUCCESS)
        title_entry.grid(row=0, column=1, sticky="w")
        title_entry.insert(0, titulo_val)

        ttk.Label(Project_window, bootstyle=SUCCESS, text="Sinopsis", font=28).grid(row=1, column=0)
        sinop_entry = ttk.Entry(Project_window, bootstyle=SUCCESS)
        sinop_entry.grid(row=1, column=1, columnspan=2, sticky="nsew")
        sinop_entry.insert(0, sinop_val)

        ttk.Label(Project_window, bootstyle=DARK, text="Descripcion", font=28).grid(row=2, column=0, sticky="w")
        desc_entry = ScrolledText(Project_window, bootstyle=SUCCESS, height=25, width=40, font=20)
        desc_entry.grid(row=3, column=0, columnspan=2, rowspan=2, sticky="nsew")
        desc_entry.insert("1.0", desc_val)

        ttk.Label(Project_window, bootstyle=INFO, text="Fecha de entrega").grid(row=0, column=3)
        fecha_estimada = ttk.DateEntry(Project_window, bootstyle=SECONDARY)
        fecha_estimada.grid(row=1, column=3)
        fecha_estimada.entry.delete(0, "end")

        ttk.Label(Project_window, bootstyle=INFO, text="Fecha de creacion", font=30).grid(row=2, column=3)
        fecha_creacion = ttk.DateEntry(Project_window, bootstyle=SECONDARY)
        fecha_creacion.grid(row=3, column=3, sticky="n")
        fecha_creacion.entry.delete(0, "end")

        estado_var = ttk.StringVar(value=str(estado_val))

        ttk.Label(Project_window, bootstyle=DARK, text="Estado", font=30).grid(row=4, column=3, sticky="sw")
        ttk.Checkbutton(Project_window, bootstyle="danger-toolbutton", text="Finalizado",
                        padding=(40, 5), variable=estado_var, onvalue="1", offvalue="0").grid(row=5, column=3, sticky="nw")
        ttk.Checkbutton(Project_window, bootstyle="success-toolbutton", text="Activo",
                        padding=(40, 5), variable=estado_var, onvalue="0", offvalue="0").grid(row=5, column=4, sticky="nw")


        def actualizar_proyecto():
            title_r = title_entry.get()
            sinop_r = sinop_entry.get()
            desc_r = desc_entry.get("1.0", "end-1c")
            date_r = fecha_estimada.entry.get()
            date_create = fecha_creacion.entry.get()
            estado_r = estado_var.get()

            conn = sqlite3.connect(BBDD_op)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE proyectos_usr
                SET titulo = ?, Sipnosis = ?, descripcion = ?, FechaEntrega = ?, FechaCreacion = ?, Estado = ?
                WHERE ID_proyecto = ?""",
                (title_r, sinop_r, desc_r, date_r, date_create, estado_r, int(id_proyecto)))
            conn.commit()
            conn.close()

            Messagebox.ok(f"Proyecto '{title_r}' actualizado correctamente", title="Done", alert=True)
            Project_window.destroy()
        
        """
        Con esta funcion se edita un proyecto existente en la base de datos
        Se traen los datos actuales del proyecto y se muestran en una ventana
        El usuario puede modificar los campos y guardar los cambios

        A diferencia de añadir un proyecto, aqui se crea la ventana manualmente
        y se rellenan los campos con los datos actuales del proyecto
        Ya que el decorador no soporta editar proyectos existentes
        """

        ttk.Button(Project_window, bootstyle="SUCCESS", text="Guardar", command=actualizar_proyecto).grid(row=6, column=0)
        return Project_window

        

    def delete_proyecto(self, id_proyecto, name): # Elimina un proyecto 'X' en caso de que el usuario quiera borrarlo
        conn = sqlite3.connect(BBDD_op)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM proyectos_usr WHERE ID_proyecto = ?", (id_proyecto,))
        conn.commit()
        conn.close()
        Messagebox.ok(f"Proyecto {name} eliminado correctamente", title="Done", alert=True)

        "Evalua el ID del proyecto y lo elimina de la base de datos"
        "Sencillo"
    
    def vermasproyectos(self, id_proyecto): # Ver más detalles de un proyecto 'X'
        conn = sqlite3.connect(BBDD_op)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ID_proyecto, Titulo, Sipnosis, Descripcion, FechaCreacion, FechaEntrega, Estado, usr_propietario FROM proyectos_usr WHERE ID_proyecto = ?",
            (id_proyecto,)
        )
        proyecto = cursor.fetchone()
        conn.close()

        if not proyecto:
            return  # Si no existe el proyecto, no hace nada

        # Desempaquetar los datos
        id_p, titulo, sipnosis, descripcion, fecha_creacion, fecha_entrega, estado, propietario  = proyecto

        # Crear ventana emergente con los detalles
        detalle = ttk.Toplevel(title=f"Proyecto: {titulo}", size=(400, 300), resizable=(0, 0))

        ttk.Label(detalle, text=f"{titulo}", bootstyle="INVERSE-SUCCESS", font=34).pack(anchor="w", padx=10)
        ttk.Label(detalle, text=f"- {sipnosis}", wraplength=380, font=12, bootstyle="INVERSE-SUCCESS").pack(anchor="w", padx=10)
        ttk.Label(detalle, text=f"Descripción: {descripcion}", wraplength=380, font=16, bootstyle="INVERSE-DARK").pack(anchor="w", padx=10, pady=10)
        ttk.Label(detalle, text=f"Creado: {fecha_creacion or 'No especificado'}", bootstyle="INVERSE-INFO").pack(anchor="w", padx=10)
        ttk.Label(detalle, text=f"Entrega: {fecha_entrega or 'No especificado'}", bootstyle="INVERSE-INFO").pack(anchor="w", padx=10)
        estado_text = "En Progreso" if int(estado) == 0 else "Completado"
        ttk.Label(detalle, text=f"Estado: {estado_text}", bootstyle="INVERSE-INFO").pack(anchor="w", padx=10)
        ttk.Label(detalle, text=f"Hecho por: {propietario}", bootstyle="INVERSE-INFO").pack(anchor="w", padx=10)

        """ 
        Muestra una ventana con los detalles completos del proyecto seleccionado 
        Tanto su nombre, fechas asignadas y estatus, asi como el mismo creador de dicho proyecto

        Se pueden visualizar en la interfaz principal de proyectos, segun lo que tenga el usuario bajo sus datos
        Y en la ventana emergente de ver_proyectos, donde se listan todos los proyectos guardados, tanto en general como del usuario logeado
        """

    def ver_proyectos(self): # Ventana emergente para ver todos los proyectos guardados
        conn = sqlite3.connect(BBDD_op)
        cursor = conn.cursor()
        cursor.execute("SELECT ID_proyecto, Titulo, Sipnosis, Descripcion, FechaCreacion, FechaEntrega, Estado, usr_propietario, ID_usr_propietario FROM proyectos_usr")
        proyectos = cursor.fetchall()
        conn.close()

        if not proyectos:
            Messagebox.show_info("No hay proyectos guardados todavía", title="Info", alert=True)
            return
        
        show_p = ttk.Toplevel(title="Proyectos Guardados", size=(400, 400), resizable=(1, 1))
        proyectos_note = ttk.Notebook(show_p, bootstyle = SUCCESS)
        proyectos_note.pack(fill=BOTH, expand=YES)

        general = ttk.Frame(proyectos_note)
        proyectos_note.add(general, text="Proyectos")

        for c in range(2):
            general.columnconfigure(c, weight=1)      

        ttk.Label(general, text="Todos los Proyectos", font=("Arial", 14, "bold"), bootstyle="INVERSE-INFO").grid(row=0, column=0, sticky="nsew", columnspan=2)
        
        for i, py in enumerate(proyectos, start=1):
            estado_text = "Completado" if py[6] == 1 else "En Progreso"
            texto = f"* Título: {py[1]} | Estado: {estado_text}"

            lbl = ttk.Label(general, text=texto, anchor="w", padding=5, bootstyle="INVERSE-SUCCESS")
            lbl.grid(row=i, column=0, sticky="ew", pady=5)

            ttk.Button(general, text="Ver detalles", bootstyle="SUCCESS-outline",
            command=lambda pid=py[0]: self.vermasproyectos(pid)).grid(row=i, column=1, sticky="ew", pady=5)
        
        personal = ttk.Frame(proyectos_note)
        proyectos_note.add(personal, text="Mis Proyectos")

        for c in range(2):
            personal.columnconfigure(c, weight=1)
        
        if self.usr_log == 0:
            ttk.Label(personal, text="Debes iniciar sesión para ver tus proyectos guardados", bootstyle="INVERSE-DANGER", font=("Arial", 12), padding=(20, 20)).grid(row=0, column=0)
        elif self.usr_log == 1 or self.var_log_dinamica == 1:
            user_proyectos = [p for p in proyectos if p[8] == self.usr_ID]

            if not user_proyectos:
                ttk.Label(personal, text="No tienes proyectos guardados todavía", bootstyle="INVERSE-DANGER", font=("Arial", 12), padding=(20, 20)).grid(row=0, column=0)
            else:
                for i, py in enumerate(user_proyectos, start=1):
                    estado_text = "Completado" if py[6] == 1 else "En Progreso"
                    texto = f"* Título: {py[1]} | Estado: {estado_text}"

                    lbl = ttk.Label(personal, text=texto, anchor="w", padding=5, bootstyle="INVERSE-SUCCESS")
                    lbl.grid(row=i, column=0, sticky="ew", pady=5)

                    ttk.Button(personal, text="Ver detalles", bootstyle="SUCCESS-outline",
                    command=lambda pid=py[0]: self.vermasproyectos(pid)).grid(row=i, column=1, sticky="ew", pady=5)        
            ttk.Label(personal, text=f"proyectos {self.usrname}", font=("Arial", 14, "bold"), bootstyle="INVERSE-INFO").grid(row=0, column=0, sticky="nsew", columnspan=2)
        
        """
        Muestra una ventana con todos los proyectos guardados en la base de datos
        Se divide en dos pestañas: Todos los proyectos y Mis proyectos
        En "Todos los proyectos" se listan todos los proyectos guardados
        En "Mis proyectos" se listan solo los proyectos del usuario logeado
        """
        
    ###########################
    #Login & Registro Funciones

    def actualizar_datos_usuario(self, username, user_id, titulo): # Esta funcion funciona para insertar y leer datos
        self.usrname = username
        self.usr_ID = user_id
        self.title = titulo
        self.usr_state = True

        # Actualizar la ventana
        self.app.title(titulo)

        'No tocar de ser necesario'
        'Funciona para el Log_LL'

    @__ventanaDeRegistosfun__("Sign in", "REGISTRAR") # Este decorador crea la ventana de registro, proviene del modulo V.py
    def crear_usr(self, usr_entry=None, pass_entry=None): #Inserta un nuevo usuario en la base de datos
        connect_L = sqlite3.connect(BBDD_op)
        pointL = connect_L.cursor()
        getUsr = usr_entry.get()
        getPass = pass_entry.get()
        try: 
            REGISTRO_EJECUCION = f"""INSERT INTO users VALUES(
            NULL, '{getUsr}', '{getPass}')"""
            pointL.execute(REGISTRO_EJECUCION)
            connect_L.commit()
            Messagebox.ok(f"Registro hecho correctamente, {getUsr}", title = "Done", alert = True)
        except Exception as e:
            if "UNIQUE constraint failed: users.username" in str(e):
                Messagebox.show_error(f"El nombre de usuario '{getUsr}' ya está en uso. Por favor, elige otro.", title="Error", alert=True)
        finally:
            pointL.close()
            connect_L.close()
        
        """
        Con esta funcion se crea un nuevo usuario en la base de datos
        La unica validacion hasta el momento es que el nombre de usuario sea unico
        En caso de proseguir con el proyecto se añadira mas seguridad a las contraseñas y otro tipo de validaciones
        """
            

    @__ventanaDeRegistosfun__("Log in", "INGRESAR") # Este decorador crea la ventana de login, proviene del modulo V.py... Es el mismo de la funcion para crear usuario
    def Login_LL(self, *, usr_entry=None, pass_entry=None): #Inicia sesion con un usuario ya creado
        connect_L = sqlite3.connect(BBDD_op)
        pointL = connect_L.cursor()

        getUsr = usr_entry.get()
        getPass = pass_entry.get()

        # Seleccionar ID, username y clave
        pointL.execute("SELECT ID, username, clave FROM users WHERE username=? AND clave=?", (getUsr, getPass))
        user_data = pointL.fetchone()

        if user_data:
            user_id, username, clave = user_data  # desempaquetar resultados

            # Actualizar configuración con nombre e ID
            pointL.execute(
                """
                UPDATE config_programa
                SET usr_log = 1,
                    usr_save = ?,
                    usr_save_ID = ?,
                    title = ?
                WHERE ID_config = 1
                """,
                (username, user_id, f'To Do LL - {username}')
            )

            connect_L.commit()
            self.actualizar_datos_usuario(
                username,
                user_id,
                f"To Do LL - {username}",

            )
            self.var_log_dinamica = 1
            lista_cambio_provisional = [f"{user_id}"]

            self.usrname = username
            self.usr_log = 1
            self.usr_ID = lista_cambio_provisional[0]

            Messagebox.ok(f"Hola, {username}", title="Bienvenido", alert=True)

        else:
            Messagebox.retrycancel("Usuario no encontrado", title="Error", alert=True)
            print(f"Usuario {getUsr} no se encuentra registrado")

        connect_L.close()

        """
        Con esta funcion se inicia sesion con un usuario ya registrado en la base de datos
        Se valida que el nombre de usuario y la clave coincidan con un registro existente
        En caso de exito, se actualiza la configuracion del programa para reflejar el usuario logeado
        """
    #############################
    #Usuarios & Claves Funciones

    """
    Punto fuerte del programa
    Ya que existen multiples registros, ya sea un banco, una red social, una tienda online, etc
    Es comun que algunos olviden sus contraseñas o datos de acceso
    O que las guarden en cookies del navegador, lo cual no garantiza seguridad

    Con esta app se podran guardar usuarios y contraseñas de forma local y segura
    asi como algun otro tipo de autenticacion que pida dicho diminio o servicio y el usuario no quiera olvidar

    Se podran guardar multiples usuarios y claves, asociados a un usuario principal que haya iniciado sesion
    """

    def add_userkey(self): # Añadir un nuevo usuario y clave
        key_window = ttk.Toplevel(title="Añadir Usuario & Clave", size=(450, 500), resizable=(0, 0))

        for k in range(2):
            key_window.columnconfigure(k, weight=1)
        for l in range(9):
            key_window.rowconfigure(l, weight=1)

        ttk.Label(key_window, bootstyle="INVERSE-SUCCESS", text="Dominio", padding=(35,5)).grid(row=0, column=0, sticky = "e")
        dominio_entry = ttk.Entry(key_window, bootstyle=SUCCESS, width=30)
        dominio_entry.grid(row=0, column=1, sticky="w")

        ttk.Label(key_window, bootstyle="inverse-info", text="Username", padding=(25, 5)).grid(row=1, column=0, sticky = "e")
        username_entry = ttk.Entry(key_window, bootstyle=INFO, width=30)
        username_entry.grid(row=1, column=1, sticky="w")

        ttk.Label(key_window, bootstyle="inverse-info", text="Email", padding=(25, 5)).grid(row=2, column=0, sticky = "e")
        email_entry = ttk.Entry(key_window, bootstyle=INFO, width=30)
        email_entry.grid(row=2, column=1, sticky="w")

        ttk.Label(key_window, bootstyle="inverse-info", text="Password", padding=(25, 5)).grid(row=3, column=0, sticky = "e")
        password_entry = ttk.Entry(key_window, bootstyle=INFO, width=30)
        password_entry.grid(row=3, column=1, sticky="w")

        ttk.Label(key_window, bootstyle = "inverse-primary", text="En caso de tener otro tipo de autenticacion, puedes guardarlos aca", padding=(25, 5)).grid(row=4, column=0, columnspan=2)

        ttk.Label(key_window, bootstyle="inverse-danger", text="Auth1 (opcional)", padding=(25, 5)).grid(row=5, column=0, sticky = "e")
        auth1_entry =ttk.Entry(key_window, bootstyle=DANGER, width=30)
        auth1_entry.grid(row=5, column=1, sticky="w")

        ttk.Label(key_window, bootstyle="inverse-danger", text="Auth2 (opcional)", padding=(25, 5)).grid(row=6, column=0, sticky = "e")
        auth2_entry =ttk.Entry(key_window, bootstyle=DANGER, width=30)
        auth2_entry.grid(row=6, column=1, sticky="w")

        ttk.Label(key_window, bootstyle="inverse-danger", text="Auth3 (opcional)", padding=(25, 5)).grid(row=7, column=0, sticky = "e")
        auth3_entry =ttk.Entry(key_window, bootstyle=DANGER, width=30)
        auth3_entry.grid(row=7, column=1, sticky="w")

        def guardar_clave():
            dominio_r = dominio_entry.get()
            username_r = username_entry.get()
            email_r = email_entry.get()
            password_r = password_entry.get()
            auth1_r = auth1_entry.get()
            auth2_r = auth2_entry.get()
            auth3_r = auth3_entry.get()

            if self.usr_log == 1:
                if dominio_r and username_r and password_r:
                    conn = sqlite3.connect(BBDD_op)
                    cursor = conn.cursor()
                    cursor.execute("""
                    INSERT INTO claves_personales (dominio, username, email, password, auth1, auth2, auth3, usr_propietario, ID_usr_propietario)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (dominio_r, username_r, email_r, password_r, auth1_r, auth2_r, auth3_r, self.usrname, self.usr_ID))
                    conn.commit()
                    conn.close()
                    Messagebox.ok(f"Clave para '{dominio_r}' guardada correctamente", title="Done", alert=True)
                    key_window.destroy()
                else:
                    Messagebox.show_error("Dominio, Username y Password son obligatorios", title="Error", alert=True)
            else:
                Messagebox.show_error("Debes iniciar sesión para guardar claves LL", title="Error", alert=True)
            """
            Esta funcion crea una ventana para añadir un nuevo usuario y clave
            Se solicitan datos como dominio, username, email, password y autenticaciones adicionales en caso de tener alguna

            Sin decorador, porque no me dio tiempo de hacerlo
            """

        ttk.Button(key_window, bootstyle="SUCCESS", text="Guardar", command= lambda: guardar_clave()).grid(row=8, column=0, columnspan=2)
        return key_window        
    
    def delete_usr(self, ID_usr, user_name): # Elimina un usuario y clave 'X' en caso de que el usuario quiera borrarla
        conn = sqlite3.connect(BBDD_op)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM claves_personales WHERE ID = ?", (ID_usr,))
        conn.commit()
        conn.close()
        Messagebox.ok(f"Usuario {user_name} eliminado correctamente", title="Done", alert=True)
        
        'Elimina un usuario y clave de la base de datos segun su ID'
        'Sencillo' 

    # Hay una nave que perdida en altamar
    # Esta clamando que la vayan a buscar
    # Poues le ha azotado una fuerte tempestad
    # Y quiere regresar, y quiere regresar
    
    def ver_usuarios_claves(self): # Ventana emergente para ver todos los usuarios y claves guardados
        conn = sqlite3.connect(BBDD_op)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT ID, dominio, username, password, email 
        FROM claves_personales 
        WHERE ID_usr_propietario = ?
        """, (self.usr_ID,))
        data = cursor.fetchall()
        conn.close()
        
        if self.usr_log == 1:
            show_u = ttk.Toplevel(title="Usuarios & Claves Guardadas", size=(400, 400), resizable=(1, 1))
            st = ttk.Frame(show_u)
            st.pack(fill=BOTH, expand=YES)

            for c in range(2):
                st.columnconfigure(c, weight=1)

            ttk.Label(st, text="Usuarios guardados", font=("Arial", 14, "bold"), bootstyle="INVERSE-INFO").grid(row=0, column=0, sticky="nsew", columnspan=2)

            for i, usr in enumerate(data, start=1):
                # usr = (ID, dominio, username, email, password)
                texto = f"* {usr[1]} | Usuario: {usr[2]}"

                lbl = ttk.Label(st, text=texto, anchor="w", padding=5, bootstyle="INVERSE-SUCCESS")
                lbl.grid(row=i, column=0, sticky="ew", pady=5)

                ttk.Button(st, text="x", bootstyle="DANGER",
                command= lambda usrid = usr[0]: self.ver_detaller_usr_clave(usrid)).grid(row=i, column=1, sticky="ew", pady=5)
        elif self.usr_log == 0:
            Messagebox.show_error("Debes iniciar sesión para ver los usuarios y claves guardadas", title="Error", alert=True)
        
        """
        Muestra una ventana con todos los usuarios y claves guardados en la base de datos
        Solo se muestran los usuarios y claves del usuario que ha iniciado sesión
        En caso de no haber iniciado sesión, se muestra un mensaje de error
        """
    
    def ver_detaller_usr_clave(self, id_usr): # Ver más detalles de un usuario y clave 'X'
        conn = sqlite3.connect(BBDD_op)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ID, dominio, username, email, password, auth1, auth2, auth3 FROM claves_personales WHERE ID = ?",
            (id_usr,)
        )
        usr_data = cursor.fetchone()
        conn.close()

        if not usr_data and self.usr_log == 1:
            Messagebox.show_info("No tienes claves guardadas todavía", title="Info", alert=True)
            return

        # Desempaquetar los datos
        id_u, dominio, username, email, password, auth1, auth2, auth3 = usr_data
        
        ven = ttk.Toplevel(title="Password", size=(300, 200), resizable=(0, 0))

        kc = ttk.Frame(ven)
        kc.grid(column=0, row=0, sticky="nsew")

        for m in range(2):
            kc.columnconfigure(m, weight=1)
            kc.rowconfigure(m, weight=1)

        ttk.Label(kc, text=f"{dominio}", bootstyle="INVERSE-SUCCESS", font = 22).grid(column=0, row=0, sticky="nsew")

        param = f"""Username: {username}\nEmail: {email}\nPassword: {password}\nAuth1: {auth1}\nAuth2: {auth2}\nAuth3: {auth3}"""  
        texto = ttk.Text(ven, height=8, wrap="word", font=("Segoe UI", 12))
        texto.insert("1.0", param)
        texto.config(state="disabled")

        texto.grid(column=0, row=2, sticky="nsew", padx=10, pady=10)

        """
        Muestra una ventana con los detalles completos del usuario y clave seleccionado
        Tanto su dominio, username, email, password y autenticaciones adicionales
        Se pueden visualizar en la interfaz principal de usuarios y claves, segun lo que tenga el usuario bajo sus datos

        Y se podran copiar al portapapeles en caso de no querer escribirlos manualmente
        No hace falta que me agradezcas.
        """
    
    def editar_usr_clave(self, id_usr): # Edita un usuario y clave 'X' en caso de que el usuario quiera cambiarlo o modificarlo
        key_window = ttk.Toplevel(title="Añadir Usuario & Clave", size=(400, 400), resizable=(0, 0))

        for k in range(2):
            key_window.columnconfigure(k, weight=1)
        for l in range(7):
            key_window.rowconfigure(l, weight=1)

        conn = sqlite3.connect(BBDD_op)
        cursor = conn.cursor()
        cursor.execute("SELECT dominio, username, email, password, auth1, auth2, auth3 FROM claves_personales WHERE ID = ?", (id_usr,))
        datos = cursor.fetchone()
        conn.close()

        if datos:
            dominio_val, username_val, email_val, password_val, auth1_val, auth2_val, auth3_val = datos
        else:
            dominio_val = username_val = email_val = password_val = auth1_val = auth2_val = auth3_val = ""


        ttk.Label(key_window, bootstyle="INVERSE-SUCCESS", text="Dominio", padding=(35,5)).grid(row=0, column=0, sticky = "e")
        dominio_entry = ttk.Entry(key_window, bootstyle=SUCCESS, width=30)
        dominio_entry.grid(row=0, column=1, sticky="w")
        dominio_entry.insert(0, dominio_val)

        ttk.Label(key_window, bootstyle="inverse-info", text="Username", padding=(25, 5)).grid(row=1, column=0, sticky = "e")
        username_entry = ttk.Entry(key_window, bootstyle=INFO, width=30)
        username_entry.grid(row=1, column=1, sticky="w")
        username_entry.insert(0, username_val)

        ttk.Label(key_window, bootstyle="inverse-info", text="Email", padding=(25, 5)).grid(row=2, column=0, sticky = "e")
        email_entry = ttk.Entry(key_window, bootstyle=INFO, width=30)
        email_entry.grid(row=2, column=1, sticky="w")
        email_entry.insert(0, email_val)

        ttk.Label(key_window, bootstyle="inverse-info", text="Password", padding=(25, 5)).grid(row=3, column=0, sticky = "e")
        password_entry = ttk.Entry(key_window, bootstyle=INFO, width=30)
        password_entry.grid(row=3, column=1, sticky="w")
        password_entry.insert(0, password_val)

        ttk.Label(key_window, bootstyle="inverse-danger", text="Auth1 (opcional)", padding=(25, 5)).grid(row=4, column=0, sticky = "e")
        auth1_entry =ttk.Entry(key_window, bootstyle=DANGER, width=30)
        auth1_entry.grid(row=4, column=1, sticky="w")
        auth1_entry.insert(0, auth1_val if auth1_val is not None else "")

        ttk.Label(key_window, bootstyle="inverse-danger", text="Auth2 (opcional)", padding=(25, 5)).grid(row=5, column=0, sticky = "e")
        auth2_entry =ttk.Entry(key_window, bootstyle=DANGER, width=30)
        auth2_entry.grid(row=5, column=1, sticky="w")
        auth1_entry.insert(0, auth1_val if auth1_val is not None else "")

        ttk.Label(key_window, bootstyle="inverse-danger", text="Auth3 (opcional)", padding=(25, 5)).grid(row=6, column=0, sticky = "e")
        auth3_entry =ttk.Entry(key_window, bootstyle=DANGER, width=30)
        auth3_entry.grid(row=6, column=1, sticky="w")
        auth1_entry.insert(0, auth1_val if auth1_val is not None else "")

        def actualizar_usr():
            dominio_r = dominio_entry.get()
            username_r = username_entry.get()
            email_r = email_entry.get()
            password_r = password_entry.get()
            auth1_r = auth1_entry.get()
            auth2_r = auth2_entry.get()
            auth3_r = auth3_entry.get()

            if dominio_r and username_r and password_r:
                conn = sqlite3.connect(BBDD_op)
                cursor = conn.cursor()
                cursor.execute("""
                UPDATE claves_personales
                SET dominio = ?, username = ?, email = ?, password = ?, auth1 = ?, auth2 = ?, auth3 = ?
                WHERE ID = ?""", (dominio_r, username_r, email_r, password_r, auth1_r, auth2_r, auth3_r, int(id_usr)))
                conn.commit()
                conn.close()
                Messagebox.ok(f"Usuario '{dominio_r}' actualizado correctamente", title="Done", alert=True)
                key_window.destroy()
            else:
                Messagebox.show_error("Dominio, Username y Password son obligatorios", title="Error", alert=True)
        
        """
        Con esta funcion se edita un usuario y clave existente en la base de datos
        En caso de cambiar el username o contraseña de dicho dominio
        es primordial actualizar esto para mejor administracion de los datos
        y que no hayan perdidas de informacion
        """

        ttk.Button(key_window, bootstyle="SUCCESS", text="Guardar", command= lambda: actualizar_usr()).grid(row=7, column=0, columnspan=2)
        return key_window 

    ###########################
    #Funciones complementarias

    """
    Ya que hasta aqui llega lo primordial del programa
    Tareas, proyectos, usuarios y claves
    Ahora vienen funciones complementarias que mejoran la experiencia de usuario
    Y complementan la aplicacion en si

    Por favor no las toques si no es necesario
    Y si lo haces, asegúrate de entender bien su funcionamiento
    """
    
    def exit_app(self, cont): # Cierra la aplicacion, sin tantas vueltas
        cont.destroy()

    def _7_palabrasdasdasda(self): # 7 palabras E.S.E.N.C.I.A
        Tablos = ttk.Toplevel(title="Esencia")
        Tablos.geometry("450x550")

        try:
            # Cargar y redimensionar la imagen
            imagen = Image.open("src/Esencia.png")
            imagen = imagen.resize((350, 350))
            img_tk = ImageTk.PhotoImage(imagen)

            # Mantener referencia
            Tablos.img_tk = img_tk

            # Mostrar la imagen
            label_imagen = ttk.Label(master=Tablos, image=Tablos.img_tk)
            label_imagen.pack(padx=10, pady=10)

        except FileNotFoundError:
            error_label = ttk.Label(master=Tablos, text="No se encontró 'Esencia.png'")
            error_label.pack(padx=10, pady=10)

        # Texto de la canción
        esencia = (
            "(Wake me up) wake me up inside\n"
            "(I can't wake up) wake me up inside\n"
            "(Save me) call my name and save me from the dark\n"
            "(Wake me up) bid my blood to run\n"
            "(I can't wake up) before I come undone\n"
            "(Save me) save me from the nothing I've become"
        )

        # Widget Text para mostrar la letra
        texto = ttk.Text(master=Tablos, height=8, wrap="word")
        texto.insert("1.0", esencia)
        texto.config(state="disabled")
        texto.pack(padx=10, pady=10, fill="x")

        return Tablos           

    def _7_palabras(self):  # 7 palabras E.S.E.N.C.I.A
        Tablos = ttk.Toplevel(title="Esencia")
        Tablos.geometry("450x550")

        # --- TÍTULO ---
        titulo = ttk.Label(master=Tablos, text="E.S.E.N.C.I.A", font=("Arial", 18, "bold"), bootstyle = "INVERSE-SUCCESS")
        titulo.pack(pady=10)

        # --- IMAGEN ---
        try:
            imagen = Image.open("src/Esencia.png")
            imagen = imagen.resize((350, 350))
            img_tk = ImageTk.PhotoImage(imagen)

            Tablos.img_tk = img_tk  # Mantener referencia

            label_imagen = ttk.Label(master=Tablos, image=Tablos.img_tk)
            label_imagen.pack(padx=10, pady=10)

        except FileNotFoundError:
            error_label = ttk.Label(master=Tablos, text="No se encontró 'Esencia.png'")
            error_label.pack(padx=10, pady=10)

        # --- LETRA (como Label) ---
        esencia = (
            "(Wake me up) wake me up inside\n"
            "(I can't wake up) wake me up inside\n"
            "(Save me) call my name and save me from the dark\n"
            "(Wake me up) bid my blood to run\n"
            "(I can't wake up) before I come undone\n"
            "(Save me) save me from the nothing I've become"
        )

        label_letra = ttk.Label(master=Tablos, text=esencia, wraplength=400, justify="center", bootstyle="success")
        label_letra.pack(padx=10, pady=10)

        return Tablos      

    def logout_user(self): #Esta funcion deberia estar arriba, pero bueno aqui se queda
        connect_LL = sqlite3.connect(BBDD_op)
        point = connect_LL.cursor()
        point.execute(
            "UPDATE config_programa SET usr_log = 0, usr_save = 'NONE', usr_save_ID = NULL, title = 'To Do LL' WHERE ID_config = 1"
        )
        connect_LL.commit()
        connect_LL.close()
        self.usr_log = 0
        self.actualizar_datos_usuario(
            "ANONIMO",
            None,
            "To Do LL"
        )
        self.var_log_dinamica = None
        Messagebox.ok("Has cerrado sesión correctamente", title="Done", alert=True)

        """
        Con esta funcion se cierra la sesion del usuario logeado
        Se actualiza la configuracion del programa para reflejar que no hay ningun usuario logeado
        Y se restablecen los datos del usuario a valores por defecto

        Por favor, en caso de modificarla, considerar que tanto el Log_LL como otras funciones que dependen de esta
        puedan verse afectadas y causar errores en la aplicacion
        """
    
    def contar_registros(self): # Cuenta la cantidad de proyectos del usuario logeado
        conn = sqlite3.connect(BBDD_op)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM proyectos_usr WHERE ID_usr_propietario = ?", (self.usr_ID,))
        cantidad = cursor.fetchone()[0]
        conn.close()
        "Aqui no tiene mucha funcionalidad, pero se usa en ver_datos_perfil"
        return cantidad
    

    def contar_usuarios_claves(self): # Cuenta la cantidad de usuarios y claves del usuario logeado
        conn = sqlite3.connect(BBDD_op)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM claves_personales WHERE ID_usr_propietario = ?", (self.usr_ID,))
        cantidad = cursor.fetchone()[0]
        conn.close()
        "Aqui no tiene mucha funcionalidad, pero se usa en ver_datos_perfil"
        return cantidad
        
    def ver_datos_perfil(self):  # Ventana emergente para ver los datos del perfil del usuario 
        perfil_window = ttk.Toplevel(title="Mi Perfil", size=(300, 350), resizable=(0, 0))

        # Usuario
        ttk.Label(
            perfil_window, 
            bootstyle="INVERSE-info", 
            text=f"Usuario: {self.usrname}", 
            font=20, padding=(30, 7)
        ).grid(row=0, column=0, sticky="n")

        # Frame proyectos
        frame_bt_proyectos = ttk.Frame(perfil_window)
        frame_bt_proyectos.grid(row=1, column=0, pady=10)        

        cantidad_proyectos = self.contar_registros()
        cantidad_usrs_claves = self.contar_usuarios_claves()

        ttk.Label(
            frame_bt_proyectos,
            bootstyle="INVERSE-SUCCESS",
            text=f"Proyectos almacenados: {cantidad_proyectos}", 
            font=20, padding=(30, 7)
        ).grid(row=0, column=0, sticky="w")

        ttk.Button(
            frame_bt_proyectos,
            bootstyle="SUCCESS-outline",
            text="Ver",
            command=self.ver_proyectos
        ).grid(row=1, column=0, sticky="n")

        # Separador
        ttk.Separator(perfil_window, bootstyle="Danger").grid(row=3, column=0, sticky="ew", pady=5)
        
        # Usuarios & Claves
        ttk.Label(
            perfil_window, 
            bootstyle="INVERSE-PRIMARY", 
            text=f"Usuarios & Claves almacenadas: {cantidad_usrs_claves}", 
            font=20, padding=(25, 3)
        ).grid(row=4, column=0, sticky="E")

        ttk.Button(
            perfil_window,
            bootstyle="PRIMARY-outline",
            text="Ver",
            command=self.ver_usuarios_claves
        ).grid(row=5, column=0, sticky="n")

        # --- Frame inferior con botones extra ---
        frame_bottom = ttk.Frame(perfil_window)
        frame_bottom.grid(row=6, column=0, pady=15)

        ttk.Button(
            frame_bottom, 
            text="7 Palabras", 
            bootstyle="success-outline", 
            command=lambda: self._7_palabras()
        ).pack(side="left", padx=5)

        ttk.Button(
            frame_bottom, 
            text="Guía", 
            bootstyle="info-outline", 
            command=lambda: self.__ventana_guia_breve__()
        ).pack(side="left", padx=5)

        ttk.Button(
            frame_bottom, 
            text="About LL", 
            bootstyle="secondary-outline", 
            command=lambda: self.about_LL()
        ).pack(side="left", padx=5)

        return perfil_window

    
    def imprimir_datos(self): # Imprime en consola los datos del usuario logeado (para pruebas)
        print(f"login status: {self.usr_log}")
        print(f"Usuario: {self.usrname}, ID guardado: {self.usr_ID}, Título: {self.title}, Estado de sesión: {self.usr_state}")
        print(f"la dinamica es {self.var_log_dinamica}")

        """
        No hace nada importante, pero igual se queda
        En caso de eliminarla o modificarla, revisar en que se relaciona con otras partes del codigo
        Ya que puede causar errores si se elimina sin mas

        Por favor se responsable
        """

    def about_LL(self): # Ventana para mostrar redes de LL
        urls = {
            'instagram': "https://www.instagram.com/isaacll306/",
            'Facebook': "https://www.facebook.com/IsaacLL306",
            'Youtube': "http://www.youtube.com/@elyolfrahd8001",
            'Tiktok': "https://www.tiktok.com/@isaacll306",
            'Linkedin': "https://www.linkedin.com/in/giovanni-leal-68b344324/"
        }

        about_window = ttk.Toplevel(title="About To Do LL", size=(400, 300), resizable=(0, 0))
        about_window.columnconfigure(0, weight=1)

        ttk.Label(
            about_window,
            text="Siguenos para mas",
            font=("Arial", 16, "bold"),
            bootstyle="inverse-success",
            anchor="center"
        ).grid(row=0, column=0, pady=10, sticky='nsew')

        RedesFrame = ttk.Frame(about_window)
        RedesFrame.grid(row=1, column=0, sticky='nsew')
        RedesFrame.columnconfigure(0, weight=1)

        ttk.Button(
            RedesFrame, text="Tiktok - @isaacll306", bootstyle="dark", cursor="hand2",
            command=lambda: www.open(urls["Tiktok"]), padding=(40, 5)
        ).grid(row=0, column=0, sticky='n', pady=4)

        ttk.Button(
            RedesFrame, text="Youtube - IsaacLL", bootstyle="danger", cursor="hand2",
            command=lambda: www.open(urls["Youtube"]), padding=(40, 5)
        ).grid(row=1, column=0, sticky='n', pady=4)

        meta_redes = ttk.Frame(RedesFrame)
        meta_redes.grid(row=2, column=0, pady=10)
        for c in range(2):
            meta_redes.columnconfigure(c, weight=1)

        ttk.Button(
            meta_redes, text="Instagram\nLL proyecto", bootstyle="warning", cursor="hand2",
            command=lambda: www.open(urls["instagram"]), padding=(40, 5)
        ).grid(row=0, column=0, sticky='ew', padx=5)

        ttk.Button(
            meta_redes, text="Facebook\nLL proyecto", bootstyle="primary", cursor="hand2",
            command=lambda: www.open(urls["Facebook"]), padding=(40, 5)
        ).grid(row=0, column=1, sticky='ew', padx=5)

        ttk.Button(
            RedesFrame, text="Linkedin - IsaacLL", bootstyle=INFO, cursor="hand2",
            command= lambda: www.open(urls["Linkedin"]), padding=(40, 5)
        ).grid(row=3, column=0, sticky='n', pady=4)

        return about_window

    
    def __ventana_explicacion__(self): #Da un poco de contexto al usuiario sobre la app
        guia_window = ttk.Toplevel(title=f"To Do LL {self.version_app}", size=(500, 450))
        guia_window.columnconfigure(0, weight=1)

        # Título
        ttk.Label(
            guia_window,
            text="Proposito de To Do LL",
            font=("Arial", 16, "bold"),
            bootstyle="inverse-success",
            anchor="center"
        ).grid(row=0, column=0, pady=10)

        # Texto principal agrupado
        guia_texto = """Esta aplicación te permite gestionar tus tareas y proyectos,
    así como guardar tus claves de manera eficiente.

    Características principales:
    - Crear, editar y eliminar tareas.
    - Organizar tareas en proyectos.
    - Configurar preferencias de usuario.
    - Almacenar y gestionar claves personales de forma segura.
    - Interfaz intuitiva y fácil de usar.

    Para comenzar, inicia sesión o crea una cuenta nueva.
    """
        ttk.Label(
            guia_window,
            text=guia_texto,
            justify="left",
            wraplength=480
        ).grid(row=1, column=0, padx=20, pady=10)

        # Documentación
        ttk.Label(
            guia_window,
            text="Si tienes alguna duda, consulta la documentación completa en la siguiente opción:",
            font=("Arial", 10, "bold"),
            bootstyle="inverse-info",
            wraplength=480
        ).grid(row=2, column=0, pady=10)

        def abrir_guia(func):
            guia_window.destroy()
            func

        # Botones en la misma fila
        frame_botones = ttk.Frame(guia_window)
        frame_botones.grid(row=3, column=0, pady=5)
        ttk.Button(frame_botones, text="Doc.LL", bootstyle="info-link", command= lambda: abrir_guia(self.__ventana_guia_breve__())).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="GitHub", bootstyle="secondary", command= lambda: www.open('https://github.com/IsaacLL306/To-Do-LL')).pack(side="left", padx=5)

        fin = ttk.Frame(guia_window)
        fin.grid(row=4, column=0, pady=10)

        for r in range(1):
            fin.rowconfigure(r, weight=1)

        ttk.Label(
            fin,
            text="¡Gracias por usar To Do LL!",
            font=("Arial", 16, "bold"),
            bootstyle="inverse-success"
        ).grid(row=0, column=0,sticky="s")

        #7 PALABRAS
        
        ttk.Button(fin, text="7 Palabras", bootstyle="success-outline", command=lambda: abrir_guia(self._7_palabras())).grid(row=1, column=0, sticky='n')

        return guia_window
    
    def __ventana_guia_breve__(self): #Da una breve guia al usuario
        guia_breve_window = ttk.Toplevel(title="Guia Rápida - To Do LL", size=(500, 500))
        
        guia_breve_window.columnconfigure(0, weight=1)
        guia_breve_window.rowconfigure(0, weight=1)
        guia_breve_window.rowconfigure(1, weight=1)
        guia_breve_window.rowconfigure(2, weight=10)

        # Título principal
        ttk.Label(
            guia_breve_window,
            text="Guía Rápida de To Do LL",
            font=("Arial", 16, "bold"),
            bootstyle="inverse-success",
            anchor="center"
        ).grid(row=0, column=0, pady=10)

        ttk.Label(
            guia_breve_window,
            text=f"Versión: {self.version_app}",
            font=("Arial", 9),
            anchor="center"
        ).grid(row=1, column=0)

        # Crear ScrolledFrame
        scrolled_frame = ScrolledFrame(guia_breve_window)
        scrolled_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # --- Sección: Bienvenida / Tareas ---
        ttk.Label(
            scrolled_frame,
            text="Sección: Tareas",
            font=("Arial", 12, "bold"),
            bootstyle="inverse-success",
            anchor="w"
        ).pack(fill="x", pady=(10, 2))

        ttk.Label(
            scrolled_frame,
            text="- Inicia sesión o crea una cuenta nueva, para mantener tu entorno más personal\n"
                "- Crea, edita y elimina tareas que tengas por hacer de manera fácil",
            justify="left",
            wraplength=480,
            font=("Arial", 10)
        ).pack(anchor="w", padx=10)

        # --- Sección: Proyectos ---
        ttk.Label(
            scrolled_frame,
            text="Sección: Proyectos",
            font=("Arial", 12, "bold"),
            bootstyle="inverse-info",
            anchor="w"
        ).pack(fill="x", pady=(10, 2))

        ttk.Label(
            scrolled_frame,
            text="- Organiza tus tareas en proyectos para una mejor gestión\n"
                "- Crea una breve explicación para cada proyecto\n"
                "- Marca proyectos como 'en progreso' o 'completados'\n"
                "- Edita proyectos para añadir más elementos o pasos\n"
                "- Mientras más organizado y detallado, mejor será tu flujo de trabajo\n"
                "- Si un proyecto ya no es relevante, elimínalo para mantener tu lista limpia",
            justify="left",
            wraplength=480,
            font=("Arial", 10)
        ).pack(anchor="w", padx=10)

        # --- Sección: Usuarios y Claves ---
        ttk.Label(
            scrolled_frame,
            text="Sección: Usuarios y Claves",
            font=("Arial", 12, "bold"),
            bootstyle="inverse-primary",
            anchor="w"
        ).pack(fill="x", pady=(10, 2))

        ttk.Label(
            scrolled_frame,
            text="- Guarda tus claves personales de forma segura\n"
                "- Añade dominios, usernames, emails y passwords\n"
                "- Usa descripciones claras para diferenciar cuentas (ej: 'Facebook / principal')\n"
                "- Si no tienes correo o username, coloca 'N/A' o '---'\n"
                "- Añade autenticaciones adicionales como 2FA o preguntas de seguridad\n"
                "- Mantén tus datos actualizados y no los compartas con nadie",
            justify="left",
            wraplength=480,
            font=("Arial", 10)
        ).pack(anchor="w", padx=10)

        # --- Sección: Cierre ---
        ttk.Label(
            scrolled_frame,
            text="¡Gracias por usar To Do LL!",
            font=("Arial", 12, "bold"),
            bootstyle="inverse-warning",
            anchor="center"
        ).pack(fill="x", pady=(15, 5))

        ttk.Label(
            scrolled_frame,
            text="Si te gustó la aplicación, compártela con tus amigos o en redes sociales.\n"
                "Cualquier sugerencia, no dudes en contactarme a través de mis redes sociales o correo electrónico.",
            justify="left",
            wraplength=480,
            font=("Arial", 10)
        ).pack(anchor="w", padx=10)

        def abrir_g(func):
            guia_breve_window.destroy()
            func

        ttk.Button(
            guia_breve_window,
            text= "7 palabras",
            bootstyle = "SUCCESS_outline",
            command = lambda: abrir_g(self._7_palabras())
        ).grid(row = 3, column = 0)

        return guia_breve_window