import constantes as op

class RAM:
    def __init__(self):
        # Aqui se inician las celdas de memoria.
        self.mem = [0] * 256

    # Esta funcion recibe una direcccion y un valor para agregar a memoria.
    def write(self, addr, value):
        if 0 <= addr < 256:
            self.mem[addr] = value

    # Se recibe una direccion y regresa el valor.
    def read(self, addr):
        if 0 <= addr < 256:
            return self.mem[addr]
        return 0
    
    def bootloader(self, ruta_archivo, dir_inicio=0):
        # Lee un archivo txt, lo escribe en la ram y guarda una copia para el reset.

        instrucciones_leidas = [] # Lista para almacenar el programa
        
        try:
            with open(ruta_archivo, 'r') as f:
                for linea in f:
                    linea_limpia = linea.strip()
                    if linea_limpia:
                        instruccion = int(linea_limpia)
                        
                        # 1. Almacenar en la lista
                        instrucciones_leidas.append(instruccion)
            
            # 2. Escribir la lista completa en la RAM
            direccion_actual = dir_inicio
            for instruccion in instrucciones_leidas:
                self.write(direccion_actual, instruccion)
                direccion_actual += 1
            
            # 3. Devolver la lista
            return instrucciones_leidas 
            
        except FileNotFoundError:
            print(f"Error: Archivo de programa '{ruta_archivo}' no encontrado.")
            return None # Devolver None si hay un error
        except ValueError:
            print(f"Error de formato. Asegúrese que solo hay números en el TXT.")
            return None
    

class CPU:
    def __init__(self, memoriaRAM, salida):
        self.ram = memoriaRAM
        self.pantalla = salida

        # Estos serian los registros:
        self.pc = 0  # Program Counter
        self.ir = 0  # Instruction Register
        self.ac = 0  # Acumulador
        self.flag_z = 0 # actualmente en 0

        self.halted = False # para saber si la instruccion es True
        self.waiting_for_input = False # Para la instruccion IN
    
    # Esta seria la parte de la Unidad de control (CU)
    def step(self):
        if self.halted or self.waiting_for_input:
            return
        # Representando las etapas del CPU:

        # 1. FETCH:
        # Traer la instrucción de la RAM usando el PC
        self.ir = self.ram.read(self.pc)
        self.pc += 1 # Avanzamos el PC

        if self.ir == 0 and self.pc > 0:
             self.halted = True
             return

        # 2. DECODE:
        # Operaciones y operadores de bits:
        # se separa la instrucción de 16 bits en 4 bits la instruccion y 12 bits el operador o valor, etc.
        # por ejemplo si la instruccion es 0x1 en binario se desplaza 12 posiciones
        opcode = self.ir >> 12         # Desplazamiento a la derecha para obtener los 4 bits del Opcode
        operand = self.ir & 0xFFF      # Máscara 0xFFF (12 unos) para obtener solo el Operando equivale a 1111 1111 1111 en binario
        
        # 3. EXECUTE:
        self.ejecutar(opcode, operand)

    def ejecutar(self, opcode, operand):

        # Estas serian las instrucciones ISA:

        # ALU unidad aritmetrica logica:
        if opcode == op.LOAD:
            self.ac = self.ram.read(operand)

        elif opcode == op.LOADI: # Cargar valor inmediato
            self.ac = operand

        elif opcode == op.STORE:
            self.ram.write(operand, self.ac)

        elif opcode == op.ADD:
            self.ac += self.ram.read(operand)
            self.flag_z = 1 if self.ac == 0 else 0

        elif opcode == op.SUB:
            self.ac -= self.ram.read(operand)
            self.flag_z = 1 if self.ac == 0 else 0

        # Control de Flujo:
        elif opcode == op.JUMP:
            self.pc = operand # iguala pc a la direccion
            
        elif opcode == op.JZ:
            if self.flag_z == 1:
                self.pc = operand # solo si Flag Z está activo

        # E/S y Control:
        elif opcode == op.IN:
            self.waiting_for_input = True
            #self.pc -= 1 
            return
            
        elif opcode == op.OUT:
            self.pantalla.append(self.ac)

        elif opcode == op.HALT:
            self.halted = True

    def reset(self, programa_inicial, datos_iniciales):
        
        # 1. Reiniciar registros de la CPU
        self.pc = 0
        self.ir = 0
        self.ac = 0
        self.flag_z = 0
        self.halted = False
        self.waiting_for_input = False
        
        # 2. Reiniciar la pantalla de salida
        self.pantalla.clear() # Limpiamos el output
        
        # 3. Limpiar toda la RAM a ceros
        self.ram.data = [0] * 256 # Asume que RAM.data es la lista de 256 celdas
        
        # 4. Recargar el programa
        for i, instruccion in enumerate(programa_inicial):
            self.ram.write(i, instruccion)
            
        # 5. Recargar los datos
        for direccion, valor in datos_iniciales.items():
            self.ram.write(direccion, valor)

    