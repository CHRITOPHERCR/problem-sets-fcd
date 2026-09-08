from conexion import (
    crear_base_datos,
    agregar_libro,
    mostrar_catalogo,
    buscar_libros,
    agregar_usuario,
    mostrar_usuarios
)


# =====================================================
# INICIALIZAR BASE DE DATOS
# =====================================================

crear_base_datos()


# =====================================================
# PROGRAMA PRINCIPAL
# =====================================================

print("Sistema de Gestión de Bibliotecas")
print("Problem Set 3")


while True:

    print("\n================================")
    print(" SISTEMA DE GESTIÓN DE BIBLIOTECA")
    print("================================")

    print("1. Agregar libro")
    print("2. Mostrar catálogo")
    print("3. Buscar libro")
    print("4. Registrar usuario")
    print("5. Mostrar usuarios")
    print("6. Salir")

    opcion = input(
        "Seleccione una opción: "
    ).strip()

    if opcion == "1":

        agregar_libro()

    elif opcion == "2":

        mostrar_catalogo()

    elif opcion == "3":

        buscar_libros()

    elif opcion == "4":

        agregar_usuario()

    elif opcion == "5":

        mostrar_usuarios()

    elif opcion == "6":

        print("\nPrograma finalizado.")

        break

    else:

        print("\nOpción no válida.")