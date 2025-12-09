import componentes
import constantes as op
import time
import pygame
import sys
from interfaz import Interfaz

# Iniciando pygame:
pygame.init()

X, Y = 1280, 720
SCREEN = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Simulador de un Computador. 💻")

# Colores iniciales (cambiar luego)
COLORES = {
    'BLANCO': (255, 255, 255),
    'NEGRO': (0, 0, 0),
    'GRIS_CLARO': (200, 200, 200),
    'GRIS_OSCURO': (50, 50, 50),
    'AMARILLO_PC': (255, 255, 0),
    'AZUL_RAM': (100, 100, 200),
    'ROJO_BOTON': (200, 50, 50),     # Para el botón PAUSE
    'VERDE_BOTON': (0, 150, 0),      # Para el botón RUN
    'GRIS_CLARO': (150, 150, 150)    # Para el botón STEP
}

# Fuente inicial (cambiar despues)
FUENTE_PEQ = pygame.font.SysFont("monospace", 14)
FUENTE_GRANDE = pygame.font.SysFont("monospace", 18, bold=True)
FUENTE_RAM = pygame.font.SysFont("monospace", 12)

# Pantalla inicial
pantalla = []

# Iniciamos los componentes.
ram = componentes.RAM()
cpu = componentes.CPU(ram, pantalla)
modo_run = False

# Carga el programa en lenguaje maquina y lo escribe en la ram.
# Tambien se guarda para el reset.
programa = ram.bootloader("programa.txt")

# NOTA: Todo funciona con operadores bits. como | y & y >> o <<

# Datos iniciales para el reset.
DATOS_INICIALES = {
    251: 48,
    252: 0, 
    253: 0, 
    254: 0,
}

for direccion, valor in DATOS_INICIALES.items():
    ram.write(direccion, valor)


"""   Prueba inicial en consola...

def imprimir_estado(paso):
    print(f"\n--- PASO {paso} ---")
    print(f"PC (Contador): {cpu.pc}")
    print(f"IR (Instrucción): {cpu.ir}")
    print(f"AC (Acumulador): {cpu.ac}")
    print(f"Flag Z: {cpu.flag_z}")


# --- Ejecución del Ciclo ---
paso = 1

# PASO 1: LOADI 5
imprimir_estado(paso)
cpu.step()
print("ACCIÓN: LOADI 5")
imprimir_estado(paso + 1)
paso += 1
# Debería: AC = 5, PC = 1, IR = (LOADI 5)

# PASO 2: ADD 250 (RAM[250] tiene 2)
imprimir_estado(paso)
cpu.step()
print("ACCIÓN: ADD 250 (5 + 2)")
imprimir_estado(paso + 1)
paso += 1
# Debería: AC = 7, PC = 2, IR = (ADD 250)

# PASO 3: OUT (Muestra el valor ASCII 7)
imprimir_estado(paso)
cpu.step()
print("ACCIÓN: OUT (Muestra chr(7))")
imprimir_estado(paso + 1)
paso += 1
# Debería: AC = 7, PC = 3, La pantalla simulada debe tener un carácter.

# PASO 4: HALT
imprimir_estado(paso)
cpu.step()
print("ACCIÓN: HALT")
imprimir_estado(paso + 1)
paso += 1
# Debería: halted = True

# --- RESULTADOS FINALES ---
print("\n==============================")
print(f"CPU DETENIDA: {cpu.halted}")
print(f"VALOR FINAL DEL AC: {cpu.ac}")
print(f"SALIDA EN PANTALLA SIMULADA: {pantalla}")
print("==============================")


"""

"""   Prueba usando Pygame   """
gui = Interfaz(SCREEN, cpu, ram, X, Y, FUENTE_PEQ, FUENTE_GRANDE, FUENTE_RAM, COLORES, programa, DATOS_INICIALES)


# Bucle para Pygame:

clock = pygame.time.Clock()
ejecutando = True

while ejecutando:
    # --- Manejo de Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        # Aquí se gestionará la pulsación de botones y la entrada IN

        # GESTIÓN DE CLICS DEL RATÓN
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = evento.pos # Obtiene la posición del clic (x, y)
            
            # --- LÓGICA DE ACTIVACIÓN DEL INPUT (NUEVO) ---
            # Si la CPU está esperando input, un clic puede activar la caja de texto
            if gui.input_box_rect and gui.input_box_rect.collidepoint(pos):
                gui.input_activo = True
                gui.input_color = COLORES['AMARILLO_PC'] # Resalta la caja al activarla
            else:
                gui.input_activo = False
                gui.input_color = COLORES['BLANCO']
            # -----------------------------------------------

            # Llama a la interfaz para que maneje el clic de los botones RUN/STEP/RESET
            nuevo_modo_run, accion_step = gui.gestionar_click(pos, modo_run) 
            
            # Actualiza el modo_run global si es necesario
            modo_run = nuevo_modo_run
            
            # Si se ejecutó un STEP, se puede añadir una pequeña pausa
            if accion_step:
                time.sleep(0.1)

        
        # GESTIÓN DE TECLADO 
        
        if evento.type == pygame.KEYDOWN:
            # Solo procesa las teclas si el campo de entrada está activo
            if gui.input_activo:
                if evento.key == pygame.K_RETURN:
                    # PROCESAR LA ENTRADA (Lógica de finalización de IN)
                    try:
                        # Este ya no se usa porque el profesor pide ACSII
                        #valor_ingresado = int(gui.texto_entrada)

                        if gui.texto_entrada: # Asegúrate de que haya algo escrito
                            caracter = gui.texto_entrada[0]
                            valor_ascii = ord(caracter) # La función ord() da el código ASCII
                            
                            cpu.ac = valor_ascii
                        
                        # Este ya no se usa porque el profesor pide ACSII
                        #cpu.ac = valor_ingresado

                        cpu.waiting_for_input = False
                        gui.input_activo = False
                        
                        # en True mientras tanto:
                        modo_run = True 
                        gui.texto_entrada = ""
                        
                    except ValueError:
                        print("Error: Ingrese solo números.")
                        gui.texto_entrada = ""
                        
                elif evento.key == pygame.K_BACKSPACE:
                    gui.texto_entrada = gui.texto_entrada[:-1]
                else:
                    # Aceptar solo dígitos
                    if evento.unicode.isdigit() or (evento.unicode == '-' and not gui.texto_entrada):
                        gui.texto_entrada += evento.unicode

    # --- Lógica de la Simulación (Modo RUN) ---
    if modo_run and not cpu.halted and not cpu.waiting_for_input:
        cpu.step()
        # Pequeña pausa para que la simulación no sea instantánea
        time.sleep(0.1) 

    # --- Dibujo ---
    gui.mostrar_interfaz(modo_run)
    
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Controla la velocidad de redibujado (no la velocidad de la CPU en modo RUN)
    clock.tick(60) 

pygame.quit()
sys.exit()