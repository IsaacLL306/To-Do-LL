from sqlite3 import *
import sqlite3 as sql
import os

carpeta = os.path.join(os.path.expanduser("~"), "Documents", "LLTD")
os.makedirs(carpeta, exist_ok=True)
db_path = os.path.join(carpeta, "TD_LL_BBDD.db")

connect_LL = sql.connect(db_path)
point = connect_LL.cursor()


def crear_Todas():
    TABLA_USR = """CREATE TABLE IF NOT EXISTS users(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    clave VARCHAR(100) NOT NULL
    )"""

    TAREAS_PROGRAMA = """CREATE TABLE IF NOT EXISTS tareas_programa(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    tarea varchar(250),
    estado INTEGER DEFAULT 0  -- 0 = pendiente, 1 = completada
    )"""

    PROYECTOS_USR = """CREATE TABLE IF NOT EXISTS proyectos_usr(
    ID_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
    UserKey INTEGER,
    Titulo VARCHAR(100),
    Sipnosis VARCHAR(500),
    descripcion TEXT,
    FechaCreacion DATE,
    FechaEntrega DATE,
    Estado VARCHAR(50),
    usr_propietario VARCHAR(50),
    ID_usr_propietario INTEGER,

    FOREIGN KEY (ID_usr_propietario) REFERENCES users(ID),
    FOREIGN KEY (usr_propietario) REFERENCES users(username)
    )"""
    
    TABLA_PROGRAM_CONFIG = """CREATE TABLE IF NOT EXISTS config_programa (
    ID_config INTEGER, 
    usr_log INTEGER,
    usr_save VARCHAR(50),
    usr_save_ID INTEGER,
    title VARCHAR(100) default 'To Do LL',
    theme_last VARCHAR(50) default 'light')"""

    TABLA_CLAVES_PERSONALES = """CREATE TABLE IF NOT EXISTS claves_personales (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        dominio VARCHAR(100) NOT NULL,
        username VARCHAR(100) NOT NULL,
        email VARCHAR(100),
        password VARCHAR(100) NOT NULL,
        auth1 VARCHAR(100),
        auth2 VARCHAR(100),
        auth3 VARCHAR(100),
        usr_propietario VARCHAR(50),
        ID_usr_propietario INTEGER,

        FOREIGN KEY (ID_usr_propietario) REFERENCES users(ID),
        FOREIGN KEY (usr_propietario) REFERENCES users(username)
        )"""

    

    tablas = [TABLA_USR, TAREAS_PROGRAMA, PROYECTOS_USR, TABLA_PROGRAM_CONFIG, TABLA_CLAVES_PERSONALES]

    for tabla in tablas:
        point.execute(tabla)

    connect_LL.commit()

    # 👇 Inicializar config_programa solo si está vacía
    point.execute("SELECT COUNT(*) FROM config_programa")
    cantidad = point.fetchone()[0]

    if cantidad == 0:
        point.execute("""
            INSERT INTO config_programa (ID_config, usr_log, usr_save, usr_save_ID, theme_last)
            VALUES (1, 0, 'NONE', NULL, 'lumen')
        """)
        connect_LL.commit()

#point.execute("INSERT iNTO config_programa (ID_config, usr_log, usr_save, usr_save_ID, theme_last) VALUES (1, 0, 'NONE', NULL, 'lumen')")

connect_LL.commit()



def eliminar_tabla(valor):
    point.execute(f"DROP TABLE IF EXISTS {valor}")
    connect_LL.commit()

#eliminar_tabla('proyectos_usr')

"""
Aqui se crean los modelos y tablas necesarias
para el correcto funcionamiento del programa
Solo se ejecuta una vez al iniciar el programa
y si las tablas ya existen no se vuelven a crear

La unica funcion exportada es crear_Todas()
que se encarga de crear todas las tablas necesarias

Todo lo demas es solo codigo basura para pruebas
que no eliminare

Por favor, en caso de hacer algo
Verificar detenidamente en que puede afectar
"""
