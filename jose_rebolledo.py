def validar_codigo(codigo, juegos):
    if not codigo or codigo.isspace():
        return False

    for key in juegos.keys():
        if key.lower() == codigo.lower():
            return False
    return True

def validar_titulo(titulo):
    return titulo.strip() != ""

def validar_plataforma(plataforma):
    return plataforma.strip() != ""

def validar_genero(genero):
    return genero.strip() != ""

def validar_clasificacion(clasificacion):
    return clasificacion in ['E', 'T', 'M']

def validar_multiplayer(multiplayer):
    return multiplayer.lower() in ['s', 'n']

def validar_editor(editor):
    return editor.strip() != ""

def validar_precio(precio_str):
    try:
        val = int(precio_str)
        return val > 0
    except ValueError:
        return False

def validar_stock(stock_str):
    try:
        val = int(stock_str)
        return val >= 0
    except ValueError:
        return False



def mostrar_menu():
    print("\n========== MENÚ PRINCIPAL ==========")
    print("1. Stock por plataforma")
    print("2. Búsqueda de juegos por rango de precio")
    print("3. Actualizar precio de juego")
    print("4. Agregar juego")
    print("5. Eliminar juego")
    print("6. Salir")
    print("=====================================")

def leer_opcion():
    while True:
        try:
            opcion = int(input("Seleccione una opción: "))
            if 1 <= opcion <= 6:
                return opcion
            else:
                print("Debe seleccionar una opción válida")
                mostrar_menu()
        except ValueError:
            print("Debe seleccionar una opción válida")
            mostrar_menu()

def stock_plataforma(plataforma, juegos, inventario):
    total_stock = 0
  
    for codigo, datos in juegos.items():
        if datos[1].lower() == plataforma.lower():
            if codigo in inventario:
                total_stock += inventario[codigo][1]
    print(f"\nStock total para la plataforma '{plataforma}': {total_stock}")

def busqueda_precio(p_min, p_max, juegos, inventario):
    resultados = []
    
    for codigo, datos_inv in inventario.items():
        precio = datos_inv[0]
        stock = datos_inv[1]
        if p_min <= precio <= p_max and stock > 0:
            if codigo in juegos:
                titulo = juegos[codigo][0]
                resultados.append(f"{titulo}--{codigo}")
    
    if resultados:
       
        resultados.sort()
        print("\n--- Juegos encontrados ---")
        for juego in resultados:
            print(juego)
    else:
        print("\nNo hay juegos en ese rango de precios.")

def buscar_codigo(codigo, diccionario):
    
    for key in diccionario.keys():
        if key.lower() == codigo.lower():
            return True
    return False

def actualizar_precio(codigo, nuevo_precio, juegos, inventario):
    if buscar_codigo(codigo, inventario):
        for key in inventario.keys():
            if key.lower() == codigo.lower():
                inventario[key][0] = nuevo_precio
                return True
    return False

def agregar_juego(codigo, titulo, plataforma, genero, clasificacion, multiplayer, editor, precio, stock, juegos, inventario):
    
    cod_upper = codigo.upper()
    if cod_upper in juegos:
        return False
    
    mp_bool = True if multiplayer.lower() == 's' else False
    
    juegos[cod_upper] = [titulo, plataforma, genero, clasificacion, mp_bool, editor]
    inventario[cod_upper] = [precio, stock]
    return True

def eliminar_juego(codigo, juegos, inventario):
    if buscar_codigo(codigo, juegos):
        key_to_del = None
        for key in juegos.keys():
            if key.lower() == codigo.lower():
                key_to_del = key
                break
        if key_to_del:
            juegos.pop(key_to_del)
            inventario.pop(key_to_del, None)
            return True
    return False



def main():
    
    juegos = {
        'G001': ['Eclipse Runner', 'PC', 'accion', 'T', True, 'NovaStudio'],
        'G002': ['Puzzle Atlas', 'Switch', 'puzzle', 'E', False, 'BrightWorks'],
        'G003': ['Sky Legends', 'PS5', 'aventura', 'T', True, 'OrionGames'],
        'G004': ['Racing Pulse', 'PC', 'carreras', 'E', True, 'VelocityLab'],
        'G005': ['Mystic Farm', 'Switch', 'simulacion', 'E', False, 'GreenSeed'],
        'G006': ['Shadow Tactics', 'Xbox', 'estrategia', 'M', False, 'IronGate']
    }

    inventario = {
        'G001': [9990, 7],
        'G002': [19990, 0],
        'G003': [42990, 3],
        'G004': [14990, 5],
        'G005': [17990, 9],
        'G006': [39990, 2]
    }

    
    opcion = 0
    while opcion != 6:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == 1:
            plat = input("Ingrese el nombre de la plataforma: ")
            stock_plataforma(plat, juegos, inventario)

        elif opcion == 2:
            print("\n--- Búsqueda por Rango de Precios ---")
            p_min_str = input("Ingrese el precio mínimo: ")
            p_max_str = input("Ingrese el precio máximo: ")
            
            
            if validar_precio(p_min_str) and validar_precio(p_max_str):
                p_min = int(p_min_str)
                p_max = int(p_max_str)
                
                if p_min <= p_max:
                    busqueda_precio(p_min, p_max, juegos, inventario)
                else:
                    print("Error: El precio mínimo no puede ser mayor al precio máximo.")
            else:
                print("Error: Los precios deben ser valores numéricos mayores a 0.")

        elif opcion == 3:
            print("\n--- Actualizar Precio de Juego ---")
            cod = input("Ingrese el código del juego: ")
            
            if buscar_codigo(cod, inventario):
                nuevo_p_str = input("Ingrese el nuevo precio: ")
                if validar_precio(nuevo_p_str):
                    nuevo_p = int(nuevo_p_str)
                    if actualizar_precio(cod, nuevo_p, juegos, inventario):
                        print("Precio actualizado con éxito.")
                    else:
                        print("Ocurrió un error al intentar actualizar el precio.")
                else:
                    print("Error: El precio debe ser un número entero mayor a 0.")
            else:
                print("Error: El código ingresado no existe en el inventario.")

        elif opcion == 4:
            print("\n--- Agregar Nuevo Juego ---")
            cod = input("Ingrese el código del juego: ")
            
            
            if not validar_codigo(cod, juegos):
                print("Error: El código está vacío o ya pertenece a otro juego.")
            else:
                tit = input("Ingrese el título: ")
                plat = input("Ingrese la plataforma: ")
                gen = input("Ingrese el género: ")
                clas = input("Ingrese la clasificación (E, T, M): ").upper()
                mp = input("¿Tiene multiplayer? (S/N): ").lower()
                edit = input("Ingrese el editor/developer: ")
                prec_str = input("Ingrese el precio: ")
                stk_str = input("Ingrese el stock inicial: ")

                
                if (validar_titulo(tit) and validar_plataforma(plat) and 
                    validar_genero(gen) and validar_clasificacion(clas) and 
                    validar_multiplayer(mp) and validar_editor(edit) and 
                    validar_precio(prec_str) and validar_stock(stk_str)):
                    
                    prec = int(prec_str)
                    stk = int(stk_str)
                    
                    if agregar_juego(cod, tit, plat, gen, clas, mp, edit, prec, stk, juegos, inventario):
                        print(f"¡Juego '{tit}' agregado con éxito de manera correcta!")
                    else:
                        print("Error: No se pudo agregar el juego.")
                else:
                    print("Error: Uno o más datos ingresados no cumplen con el formato válido.")

        elif opcion == 5:
            print("\n--- Eliminar Juego ---")
            cod = input("Ingrese el código del juego a eliminar: ")
            
            if eliminar_juego(cod, juegos, inventario):
                print(f"El juego con código '{cod.upper()}' ha sido eliminado correctamente.")
            else:
                print("Error: El código ingresado no corresponde a ningún juego existente.")

        elif opcion == 6:
            print("\n¡Gracias por utilizar el sistema de inventario! Saliendo...")

if __name__ == '__main__':
    main()
           