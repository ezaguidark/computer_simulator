# Codigos de operaciones:
# Estos datos son de tipo int pero en forma Exadecimal.

LOAD  = 0x1  # carga el dato de la addr en la RAM al AC
STORE = 0x2  # almacena el valir del AC en la addr
ADD   = 0x3  # suma el dato en addr al AC
SUB   = 0x4  # resta el dato en addr al AC
JUMP  = 0x5  # cambia el PC a la direccion addr
JZ    = 0x6  # cambia el PC a addr si FLAG_Z es 1
IN    = 0x7  # Lee un caracter desde el teclado
OUT   = 0x8  # Muestra el valor del AC en "pantalla"
LOADI = 0x9  # carga un valir inmediato al AC
HALT  = 0xF  # Detener el programa.