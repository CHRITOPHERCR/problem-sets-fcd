import sqlite3
import unicodedata


# =====================================================
# CONEXIÓN A LA BASE DE DATOS
# =====================================================

def conectar():
    conexion = sqlite3.connect("biblioteca.db")
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


# =====================================================
# CREACIÓN DE LA BASE DE DATOS Y TABLAS
# =====================================================

def crear_base_datos():

    conexion = conectar()

    cursor = conexion.cursor()

    try:

        # =================================================
        # TABLA AUTOR
        # =================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Autor (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nombre TEXT NOT NULL,
                Apellido TEXT NOT NULL,
                "Fecha de nacimiento" TEXT
            )
        """)

        # =================================================
        # TABLA LIBRO
        # =================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Libro (
                IDlibro INTEGER PRIMARY KEY AUTOINCREMENT,
                ISBN TEXT NOT NULL UNIQUE,
                Título TEXT NOT NULL,
                "Año de publicación" INTEGER,
                cantidad_disponible INTEGER NOT NULL DEFAULT 0,
                AutorID INTEGER NOT NULL,

                FOREIGN KEY (AutorID)
                    REFERENCES Autor(ID)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            )
        """)

        # =================================================
        # TABLA USUARIO
        # =================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuario (
                IDusuario INTEGER PRIMARY KEY AUTOINCREMENT,
                DNI TEXT NOT NULL UNIQUE,
                Nombre TEXT NOT NULL,
                Apellido TEXT NOT NULL,
                email TEXT,
                teléfono TEXT,
                fecha_membresía TEXT DEFAULT CURRENT_DATE
            )
        """)

        conexion.commit()

        print("Base de datos inicializada correctamente.")

    except sqlite3.Error as error:

        conexion.rollback()

        print("Error al crear la base de datos:")
        print(error)

    finally:

        conexion.close()


# =====================================================
# QUITAR ACENTOS
# =====================================================

def quitar_acentos(texto):

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    return texto.lower()


# =====================================================
# MOSTRAR CATÁLOGO
# =====================================================

def mostrar_catalogo():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            L.IDlibro,
            L.ISBN,
            L.Título,
            L."Año de publicación",
            L.cantidad_disponible,
            A.Nombre || ' ' || A.Apellido AS Autor

        FROM Libro AS L

        INNER JOIN Autor AS A
            ON L.AutorID = A.ID

        ORDER BY L.Título;
    """)

    libros = cursor.fetchall()

    print("\n================ CATÁLOGO ================")

    if not libros:

        print("No existen libros registrados.")

    else:

        for libro in libros:

            print(
                f"\nID: {libro[0]}"
                f"\nISBN: {libro[1]}"
                f"\nTítulo: {libro[2]}"
                f"\nAño: {libro[3]}"
                f"\nCopias disponibles: {libro[4]}"
                f"\nAutor: {libro[5]}"
            )

    conexion.close()


# =====================================================
# BUSCAR LIBROS
# =====================================================

def buscar_libros():

    print("\n================ BUSCAR LIBRO ================")

    texto = input(
        "Ingrese título, autor o parte del nombre: "
    ).strip()

    texto_busqueda = quitar_acentos(texto)

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            L.IDlibro,
            L.ISBN,
            L.Título,
            L."Año de publicación",
            L.cantidad_disponible,
            A.Nombre || ' ' || A.Apellido AS Autor

        FROM Libro AS L

        INNER JOIN Autor AS A
            ON L.AutorID = A.ID

        ORDER BY L.Título;
    """)

    libros = cursor.fetchall()

    resultados = []

    for libro in libros:

        titulo = quitar_acentos(libro[2])
        autor = quitar_acentos(libro[5])

        if (
            texto_busqueda in titulo
            or texto_busqueda in autor
        ):

            resultados.append(libro)

    print("\n================ RESULTADOS ================")

    if not resultados:

        print("No se encontraron libros.")

    else:

        for libro in resultados:

            print(
                f"\nISBN: {libro[1]}"
                f"\nTítulo: {libro[2]}"
                f"\nAño: {libro[3]}"
                f"\nCopias disponibles: {libro[4]}"
                f"\nAutor: {libro[5]}"
            )

    conexion.close()


# =====================================================
# AGREGAR USUARIO
# =====================================================

def agregar_usuario():

    print("\n================ REGISTRAR USUARIO ================")

    dni = input("Ingrese el DNI: ").strip()

    nombre = input("Ingrese el nombre: ").strip()

    apellido = input("Ingrese el apellido: ").strip()

    email = input("Ingrese el email: ").strip()

    telefono = input("Ingrese el teléfono: ").strip()

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        # Verificar DNI

        cursor.execute("""
            SELECT IDusuario
            FROM Usuario
            WHERE DNI = ?
        """, (dni,))

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            print("\nERROR: El DNI ya está registrado.")

            return

        # Insertar usuario

        cursor.execute("""
            INSERT INTO Usuario (
                DNI,
                Nombre,
                Apellido,
                email,
                teléfono
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            dni,
            nombre,
            apellido,
            email,
            telefono
        ))

        conexion.commit()

        print("\nUsuario registrado correctamente.")
        print(f"ID de usuario: {cursor.lastrowid}")
        print(f"DNI: {dni}")
        print(f"Nombre: {nombre} {apellido}")

    except sqlite3.IntegrityError as error:

        conexion.rollback()

        print("\nERROR DE INTEGRIDAD:")
        print(error)

    except Exception as error:

        conexion.rollback()

        print("\nERROR:")
        print(error)

    finally:

        conexion.close()


# =====================================================
# MOSTRAR USUARIOS
# =====================================================

def mostrar_usuarios():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            IDusuario,
            DNI,
            Nombre,
            Apellido,
            email,
            teléfono,
            fecha_membresía

        FROM Usuario

        ORDER BY Apellido, Nombre;
    """)

    usuarios = cursor.fetchall()

    print("\n================ USUARIOS ================")

    if not usuarios:

        print("No existen usuarios registrados.")

    else:

        for usuario in usuarios:

            print(
                f"\nID: {usuario[0]}"
                f"\nDNI: {usuario[1]}"
                f"\nNombre: {usuario[2]} {usuario[3]}"
                f"\nEmail: {usuario[4]}"
                f"\nTeléfono: {usuario[5]}"
                f"\nFecha de membresía: {usuario[6]}"
            )

    conexion.close()


# =====================================================
# AGREGAR LIBRO
# =====================================================

def agregar_libro():

    print("\n========== AGREGAR LIBRO ==========")

    isbn = input("Ingrese el ISBN: ").strip()

    titulo = input("Ingrese el título: ").strip()

    anio = input(
        "Ingrese el año de publicación: "
    ).strip()

    nombre_autor = input(
        "Ingrese el nombre del autor: "
    ).strip()

    apellido_autor = input(
        "Ingrese el apellido del autor: "
    ).strip()

    fecha_nacimiento = input(
        "Ingrese la fecha de nacimiento del autor (YYYY-MM-DD): "
    ).strip()

    try:

        cantidad = int(
            input("Ingrese la cantidad de copias: ")
        )

    except ValueError:

        print("\nERROR: La cantidad debe ser un número entero.")

        return

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        conexion.execute("BEGIN")

        # =================================================
        # VERIFICAR ISBN
        # =================================================

        cursor.execute("""
            SELECT
                IDlibro,
                cantidad_disponible

            FROM Libro

            WHERE ISBN = ?
        """, (isbn,))

        libro_existente = cursor.fetchone()

        if libro_existente:

            id_libro = libro_existente[0]

            cantidad_actual = libro_existente[1]

            nueva_cantidad = (
                cantidad_actual + cantidad
            )

            cursor.execute("""
                UPDATE Libro

                SET cantidad_disponible = ?

                WHERE IDlibro = ?
            """, (
                nueva_cantidad,
                id_libro
            ))

            conexion.commit()

            print("\nEl ISBN ya existe.")

            print(
                f"Se agregaron {cantidad} copias."
            )

            print(
                f"Cantidad anterior: {cantidad_actual}"
            )

            print(
                f"Nueva cantidad: {nueva_cantidad}"
            )

            return

        # =================================================
        # BUSCAR AUTOR
        # =================================================

        cursor.execute("""
            SELECT ID

            FROM Autor

            WHERE LOWER(Nombre) = LOWER(?)

              AND LOWER(Apellido) = LOWER(?)
        """, (
            nombre_autor,
            apellido_autor
        ))

        autor_existente = cursor.fetchone()

        if autor_existente:

            autor_id = autor_existente[0]

            print(
                f"\nEl autor ya existe. "
                f"ID del autor: {autor_id}"
            )

        else:

            # =================================================
            # CREAR AUTOR
            # =================================================

            cursor.execute("""
                INSERT INTO Autor (
                    Nombre,
                    Apellido,
                    "Fecha de nacimiento"
                )

                VALUES (?, ?, ?)
            """, (
                nombre_autor,
                apellido_autor,
                fecha_nacimiento
            ))

            autor_id = cursor.lastrowid

            print(
                f"\nSe creó un nuevo autor "
                f"con ID: {autor_id}"
            )

        # =================================================
        # CREAR LIBRO
        # =================================================

        cursor.execute("""
            INSERT INTO Libro (
                ISBN,
                Título,
                "Año de publicación",
                cantidad_disponible,
                AutorID
            )

            VALUES (?, ?, ?, ?, ?)
        """, (
            isbn,
            titulo,
            anio,
            cantidad,
            autor_id
        ))

        conexion.commit()

        print("\nLibro agregado correctamente.")

        print(f"ISBN: {isbn}")

        print(f"Título: {titulo}")

        print(f"Copias: {cantidad}")

    except sqlite3.IntegrityError as error:

        conexion.rollback()

        print("\nERROR DE INTEGRIDAD:")
        print(error)

    except Exception as error:

        conexion.rollback()

        print("\nERROR:")
        print(error)

    finally:

        conexion.close()