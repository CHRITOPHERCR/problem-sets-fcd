from database import create_tables, add_dream, close_connection, get_dreams, buscar_dream_por_palabra , buscar_dream_por_fecha
bienvenida = "Bienvenido al aplicativo registra suenios"

menu = """ DIME QUE QUIERES HACER
1) agregar un suenio
2) leer nuestros suenios
3) buscar un suenio por alguna palabra
4) buscar suenios por fecha
5) salir


Selecciona una opcion: 
"""

create_tables()

def inserta_suenio():
    dream = input("escribe tu suenio: ")
    fecha = input("registra la fecha (YYYY-MM-DD): ")
    add_dream(dream, fecha)

def buscar_suenio_por_fecha():
    fecha = input("registra la fecha a buscar (YYYY-MM-DD:")
    dreams = buscar_dream_por_fecha (fecha)
    for dream in dreams:
        print(dream['dream'],dream['fecha'])

def buscar_suenio(): 
    palabra_clave = input("coloca tu palabra clave: ")
    dreams = buscar_dream_por_palabra(palabra_clave)
    for dream in dreams:
        print(dream['dream'], dream['fecha'])    


def leer_suenios():
    dreams = get_dreams()
    for dream in dreams:
        print(dream['dream'], dream['fecha'])

while (input_usuario := input(menu)) != "5":
    if input_usuario == "1":
        inserta_suenio()
    elif input_usuario == "2":
        leer_suenios()
    elif input_usuario == "3":
        buscar_suenio()    
    elif input_usuario == "4":
        buscar_suenio_por_fecha()
    else:
        print("invalido")

print("hasta luego")


close_connection()