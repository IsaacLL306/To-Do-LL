<p align="center">
  <img src="src/Logo_LL.png" alt="Logo LL" width="150"/>
</p>
<h1 align="center">Python To Do LL</h1>
<p align="center">X IsaacLL</p>


***
# Python To Do LL

### 📌 Descripción
Aplicación en **Python** con interfaz gráfica basada en **Tkinter/ttkbootstrap** que permite:
- Gestión organizada de tareas personales.
- Creación y administración de proyectos asociados a cada usuario.
- Almacenamiento seguro de claves y credenciales de distintas plataformas.

### 🚀 Características principales
- Registro y login de usuarios.
- Panel de perfil con proyectos creados.
- Control de estado de tareas (pendiente / completada).
- Configuración guardada (último usuario, tema claro/oscuro).
- Base de datos integrada en **SQLite3**.

### ⚙️ Instalación
1. Clonar el repositorio o descargar los archivos.
2. Instalar dependencias:
   ```py
   pip install ttkbootstrap

   #Ejecutar programa desde consola
   python mani.py
    ```

### Modularizacion
#### La app se divide en modulos para mejor comprension de la logica utilizada
1. Mani.py - Modulo principal de ejecucion
2. Window.py - Modulo donde se construye la ventana//interfaz y algunas funciones varias
3. FunsLL.py - Modulo de las clases donde se ejecuta la mayor parte de la conexion con la BBDD
4. Modelslite_LL.py - Modulo donde se crea la BBDD y se generan los datos que tendra en un inicio
5. V.py - Modulo donde se crean las ventanas emergentes de algunas funciones con el proposito de organizar el codigo

- Nota: El Modulo FunsLL.py se divide en bloques los cuales se organizan segun la imersion del programa... Las propiedades del mismo, las diversas opciones sobre las tareas y 
  los proyecto etc...
- En caso de usar este Modulo Leer detenidamente los comentarios sobre cada bloque para mejor comprension

## 📁 Ubicación de la Base de Datos

La aplicación genera automáticamente la base de datos SQLite en:

**Documentos/LLTD/TD_LL_BBDD.db**

Esto garantiza que:
- Siempre se utilice una única base de datos.
- No se creen duplicados al ejecutar la app desde diferentes rutas.
- El usuario no tenga que configurar nada manualmente.

La carpeta `LLTD` se crea automáticamente si no existe.
  
### 📄 Licencia
Este proyecto está bajo la titularidad de **LL Proyecto / IsaacLL**.  
@Todos los derechos reservados.

### 👥 Autores y Colaboradores
- **IsaacLL / GioLL** – Desarrollo principal

### 🌐 Contacto
- Instagram: [Ir...](https://www.instagram.com/isaacll306)
- Facebook: [Ir...](https://www.facebook.com/IsaacLL306)
- Youtube: [Ir...](http://www.youtube.com/@elyolfrahd8001)
- Linkedin: [Ir...](https://www.linkedin.com/in/giovanni-leal-68b344324/)
- Tiktok: [Ir...](https://www.tiktok.com/@isaacll306)
- Github: [Ir...](https://github.com/IsaacLL306)
- Gmail personal - [Isaaclealga@gmail.com](mailto:Isaaclealga@gmail.com)
- Gmail LL proyecto - [llproyecto306@gmail.com](mailto:llproyecto306@gmail.com)

  

### URL´s
- [Versión descargable](https://drive.google.com/drive/folders/1KypqChIG68XZo9jA-2xdoSd2ZiWWqXZE?usp=drive_link)
- [Repositorio en GitHub](https://github.com/IsaacLL306/To-Do-LL)