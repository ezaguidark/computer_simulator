import constantes as op

# Costantes:

DIR_ASCII_48 = 251
DIR_NUM1 = 252       # Dirección para Num1:
DIR_NUM2 = 253       # Dirección para Num2:
DIR_RESULTADO = 254  # Dirección para Resultado:


# Todas son instrucciones en ACSII:
# Funcionamiento: la operacion se dezplaza 12 bits a la izquierda y se opera con or binario el dato en ACSII,
# Eso guarda en los primeros 4 bits la instruccion y en el otro lado el dato. pero Python lo traduce a lenguaje maquina.

programa = [
   
    # Dir 0-25: Muestra "BIENVENIDOS"
    (op.LOADI << 12) | 66, (op.OUT << 12) | 0,  # B
    (op.LOADI << 12) | 73, (op.OUT << 12) | 0,  # I
    (op.LOADI << 12) | 69, (op.OUT << 12) | 0,  # E
    (op.LOADI << 12) | 78, (op.OUT << 12) | 0,  # N
    (op.LOADI << 12) | 86, (op.OUT << 12) | 0,  # V
    (op.LOADI << 12) | 69, (op.OUT << 12) | 0,  # E
    (op.LOADI << 12) | 78, (op.OUT << 12) | 0,  # N
    (op.LOADI << 12) | 73, (op.OUT << 12) | 0,  # I
    (op.LOADI << 12) | 68, (op.OUT << 12) | 0,  # D
    (op.LOADI << 12) | 79, (op.OUT << 12) | 0,  # O
    (op.LOADI << 12) | 10, (op.OUT << 12) | 0,  # Salto de línea
    
    
    # Dir 26-41: Muestra "NUMERO 1: " y un espacio (32)
    (op.LOADI << 12) | 78, (op.OUT << 12) | 0,  # N
    (op.LOADI << 12) | 85, (op.OUT << 12) | 0,  # U
    (op.LOADI << 12) | 77, (op.OUT << 12) | 0,  # M
    (op.LOADI << 12) | 69, (op.OUT << 12) | 0,  # E
    (op.LOADI << 12) | 82, (op.OUT << 12) | 0,  # R
    (op.LOADI << 12) | 79, (op.OUT << 12) | 0,  # O
    (op.LOADI << 12) | 32, (op.OUT << 12) | 0,  # Espacio
    (op.LOADI << 12) | 49, (op.OUT << 12) | 0,  # 1
    (op.LOADI << 12) | 58, (op.OUT << 12) | 0,  # :
    (op.LOADI << 12) | 32, (op.OUT << 12) | 0,  # Espacio Final antes del input
    (op.LOADI << 12) | 10, (op.OUT << 12) | 0,  # Salto de línea
    
    
    (op.IN << 12) | 0,
    # 11. SUB 251 (AC = 50 - 48 = 2)
    (op.SUB << 12) | DIR_ASCII_48, 
    # 12. STORE 252 (Guarda el 2 numérico en Num1)
    (op.STORE << 12) | DIR_NUM1, 
    

    # Dir 48-63: Muestra "NUMERO 2: " y un espacio
    (op.LOADI << 12) | 78, (op.OUT << 12) | 0,  # N
    (op.LOADI << 12) | 85, (op.OUT << 12) | 0,  # U
    (op.LOADI << 12) | 77, (op.OUT << 12) | 0,  # M
    (op.LOADI << 12) | 69, (op.OUT << 12) | 0,  # E
    (op.LOADI << 12) | 82, (op.OUT << 12) | 0,  # R
    (op.LOADI << 12) | 79, (op.OUT << 12) | 0,  # O
    (op.LOADI << 12) | 32, (op.OUT << 12) | 0,  # Espacio
    (op.LOADI << 12) | 50, (op.OUT << 12) | 0,  # 2
    (op.LOADI << 12) | 58, (op.OUT << 12) | 0,  # :
    (op.LOADI << 12) | 32, (op.OUT << 12) | 0,  # Espacio Final antes del input
    (op.LOADI << 12) | 10, (op.OUT << 12) | 0,  # Salto de línea


    
    (op.IN << 12) | 0,
    # 14. SUB 251 (AC = 50 - 48 = 2)
    (op.SUB << 12) | DIR_ASCII_48, 
    # 15. STORE 253 (Guarda el 2 numérico en Num2)
    (op.STORE << 12) | DIR_NUM2, 
    
    # 16. LOAD 252 (Carga 2 en AC)
    (op.LOAD << 12) | DIR_NUM1, 
    # 17. ADD 253 (Suma 2 + 2)
    (op.ADD << 12) | DIR_NUM2, 
    
    # 18. STORE 254 (Resultado 4)
    (op.STORE << 12) | DIR_RESULTADO, 
    
    # 19. HALT 0
    (op.HALT << 12) | 0
]


def guardar_programa_en_txt(programa_lista, ruta_archivo='programa.txt'):
    
    try:
        with open(ruta_archivo, 'w') as archivo:
            for instruccion in programa_lista:
                
                archivo.write(f"{instruccion}\n")
        print(f"El programa de máquina ha sido guardado en: {ruta_archivo}")
    except Exception as e:
        print(f"Error al intentar guardar el archivo: {e}")


guardar_programa_en_txt(programa)


# Antigua forma de escribir la memoria con una lista normal (ya no se usa).
"""
for i, instruccion in enumerate(programa):
    ram.write(i, instruccion)
"""