#  Sistema de Gestión de Bibliotecas

El sistema permite administrar libros, autores y usuarios desde una consola.

---

##  Estructura del proyecto

```text
 biblioteca
│
├──  biblioteca.py
├──  conexion.py
└──  biblioteca.db
```

### `biblioteca.py`

Es el **archivo principal** del proyecto.

Contiene únicamente:

* Inicio del programa.
* Menú principal.
* Ejecución de las funciones.

Desde aquí se ejecuta todo el sistema.

### `conexion.py`

Contiene la **lógica del sistema**:

* Conexión con SQLite.
* Creación automática de la base de datos.
* Creación de las tablas.
* Consultas SQL.
* Registro de libros.
* Registro de usuarios.
* Búsqueda de libros.
* Mostrar catálogo y usuarios.

### `biblioteca.db`

Es la **base de datos SQLite**.

Se genera automáticamente al ejecutar `biblioteca.py` por primera vez.

Contiene las tablas:

```text
Autor
Libro
Usuario
```

---

##  ¿Cómo funciona?

Al ejecutar:

```bash
python biblioteca.py
```

el programa primero ejecuta:

```python
crear_base_datos()
```

Esta función:

1. Se conecta a SQLite.
2. Crea `biblioteca.db` si no existe.
3. Crea las tablas `Autor`, `Libro` y `Usuario`.
4. Inicia el menú principal.

Las tablas utilizan **claves primarias y foráneas** para mantener la relación entre autores y libros.

---

##  ¿Cómo vamos a ejecutar el proyecto?

### 1. Abrir la carpeta del proyecto

Abrir la carpeta `biblioteca` en Visual Studio Code.

### 2. Abrir la terminal

En VS Code:

**Terminal → New Terminal**

### 3. Ejecutar

```bash
python biblioteca.py
```

Aparecerá el menú:

```text
================================
 SISTEMA DE GESTIÓN DE BIBLIOTECA
================================

1. Agregar libro
2. Mostrar catálogo
3. Buscar libro
4. Registrar usuario
5. Mostrar usuarios
6. Salir
```

---

##  Ejemplo de prueba

### Agregar un libro

Seleccionar:

```text
1
```

Ingresar:

```text
ISBN: 9780307476463
Título: Cien años de soledad
Año: 1967
Autor: Gabriel García Márquez
Fecha de nacimiento: 1927-03-06
Copias: 5
```

Luego seleccionar:

```text
2
```

para comprobar que el libro aparece en el catálogo.

---

##  Buscar un libro

Seleccionar:

```text
3
```

y escribir:

```text
garcia
```

El sistema buscará coincidencias tanto por **título como por autor**.

Además, la búsqueda ignora los acentos, por lo que se puede escribir `garcia` aunque el nombre almacenado sea `García`.

---

##  Registrar un usuario

Seleccionar:

```text
4
```

Ejemplo:

```text
DNI: 71234567
Nombre: Christopher
Apellido: Paul
Email: christopher@gmail.com
Teléfono: 987654321
```

El DNI es único, por lo que no se permite registrar dos usuarios con el mismo DNI.

---

##  Funcionalidades

| Opción | Función           |
| ------ | ----------------- |
| 1      | Agregar libro     |
| 2      | Mostrar catálogo  |
| 3      | Buscar libro      |
| 4      | Registrar usuario |
| 5      | Mostrar usuarios  |
| 6      | Salir             |

---

##  Persistencia de datos

Los datos se almacenan directamente en:

```text
biblioteca.db
```

Por eso, al cerrar y volver a ejecutar el programa, **los datos registrados permanecen guardados**.

---

##  Tecnologías utilizadas

* Python
* SQLite
* Visual Studio Code
* Módulo `sqlite3`
* Módulo `unicodedata`

---

##  Administración de préstamos

breve descripción:

* Crear una tabla **Préstamo** relacionada con **Usuario** y **Libro**.
* Verificar que el libro tenga **copias disponibles** antes de realizar el préstamo.
* Controlar que cada usuario tenga como máximo **3 libros prestados simultáneamente**, mediante un **trigger** o validación.
* Registrar la fecha del préstamo y devolución.
* Actualizar la cantidad disponible del libro al prestar y devolver.
* Utilizar **transacciones (`BEGIN`, `COMMIT`, `ROLLBACK`)** para garantizar que todas las operaciones se realicen correctamente o se reviertan en caso de error.

No se considera penalidad por devolución fuera de plazo.

