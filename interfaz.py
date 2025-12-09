import pygame

class Interfaz:
    def __init__(self, pantalla, cpu, ram, ancho, alto, fuente_peq, fuente_grande, fuente_ram, colores, programa_inicial, datos_iniciales):
        self.PANTALLA = pantalla
        self.cpu = cpu
        self.ram = ram
        self.ANCHO = ancho
        self.ALTO = alto

        self.programa_inicial = programa_inicial
        self.datos_iniciales = datos_iniciales
        
        # Fuentes y Colores
        self.FUENTE_PEQ = fuente_peq
        self.FUENTE_GRANDE = fuente_grande
        self.FUENTE_RAM = fuente_ram
        self.colores = colores
        self.BLANCO = colores['BLANCO']
        self.GRIS_OSCURO = colores['GRIS_OSCURO']
        self.AMARILLO_PC = colores['AMARILLO_PC']
        
        # Nuevos colores para el tema retro
        self.VERDE_FOSFORO = (30, 255, 30)
        self.FONDO_NEGRO_CONS = (10, 10, 10)
        
        self.FUENTE_CONS = pygame.font.Font(None, 24) 
        
        # --- Definición de la Geometría de la Consola ---
        
        # La consola empezará 40px debajo del título (que empieza en Y=10)
        self.Y_CONSOLA_START = 50 
        
        # Área de los botones para la gestión de clics (Rectángulos de Pygame)
        self.boton_run_rect = None
        self.boton_step_rect = None
        self.boton_reset_rect = None
        
        # Dimensiones para los paneles (precalculadas)
        self.X_IZQ_START = 10 # Margen izquierdo
        self.X_DER_START = self.ANCHO // 2 + 10 # Margen derecho
        self.Y_TERCIO = self.ALTO // 3
        self.Y_DOS_TERCIOS = 2 * self.ALTO // 3

        # --- Variables de Input ---
        self.input_box_rect = None  # Rectángulo del campo de texto
        self.texto_entrada = ""     # Texto que el usuario está escribiendo
        self.input_activo = False   # Bandera para saber si se puede escribir
        self.input_color = colores['BLANCO']

        # Define la posición y tamaño del recuadro
        self.REC_CONSOLA = pygame.Rect(self.X_IZQ_START, 
                                    self.Y_CONSOLA_START, 
                                    500, 150) # (X, Y, Ancho, Alto)

    def dibujar_registros(self):
        """ Dibuja los registros de la CPU en el panel central IZQUIERDO. """
        
        # Coordenadas de inicio del contenido dentro del panel
        X_START = self.X_IZQ_START + 10 
        Y_START = self.Y_TERCIO + 40
        Y_SPACING = 30
        
        # Título del Panel
        titulo = self.FUENTE_GRANDE.render("Estado de la CPU", True, self.BLANCO)
        self.PANTALLA.blit(titulo, (self.X_IZQ_START, self.Y_TERCIO + 10))
        
        # --- Formateo de los Registros ---
        
        # PC (Program Counter): Hexadecimal 0x00
        pc_hex = f"0x{self.cpu.pc:02X}"
        
        # IR (Instruction Register): Hexadecimal 0x0000
        ir_hex = f"0x{self.cpu.ir:04X}"
        
        # AC (Acumulador): Valor en Decimal
        ac_val = self.cpu.ac
        
        # --- Renderizado de Texto ---
        
        # 1. PC
        pc_texto = self.FUENTE_PEQ.render(f"PC (Next Instruction): {pc_hex}", True, self.BLANCO)
        self.PANTALLA.blit(pc_texto, (X_START, Y_START))
        
        # 2. IR
        ir_texto = self.FUENTE_PEQ.render(f"IR (Current Instr.): {ir_hex}", True, self.BLANCO)
        self.PANTALLA.blit(ir_texto, (X_START, Y_START + Y_SPACING))
        
        # 3. AC
        ac_texto = self.FUENTE_PEQ.render(f"AC (Accumulator): {ac_val}", True, self.BLANCO)
        self.PANTALLA.blit(ac_texto, (X_START, Y_START + 2 * Y_SPACING))
        
        # 4. FLAG Z (Se resalta si es 1)
        flag_color = self.AMARILLO_PC if self.cpu.flag_z == 1 else self.BLANCO
        flag_texto = self.FUENTE_PEQ.render(f"FLAG Z (Zero): {self.cpu.flag_z}", True, flag_color)
        self.PANTALLA.blit(flag_texto, (X_START, Y_START + 3 * Y_SPACING))
        
        # 5. ESTADO
        estado_msg = 'HALTED' if self.cpu.halted else ('WAITING INPUT' if self.cpu.waiting_for_input else 'PAUSED')
        estado_color = (255, 100, 100) if self.cpu.halted else self.BLANCO
        estado_texto = self.FUENTE_PEQ.render(f"ESTADO: {estado_msg}", True, estado_color)
        self.PANTALLA.blit(estado_texto, (X_START, Y_START + 5 * Y_SPACING))


    def dibujar_pantalla(self):
        """
        Dibuja el output usando un modelo HÍBRIDO (Consola Interactiva + Resultado Numérico),
        simulando una pantalla de fósforo verde.
        """
        # Direcciones de RAM
        DIR_RESULTADO = 254
        X_START = self.X_IZQ_START
        Y_START = 10
        
        # --- TÍTULO ---
        titulo = self.FUENTE_GRANDE.render("DISPLAY DE RESULTADOS", True, self.BLANCO)
        self.PANTALLA.blit(titulo, (X_START, Y_START))
        
        # -----------------------------------------------
        # --- 1. DIBUJAR EL RECUADRO RETRO DE LA CONSOLA ---
        # -----------------------------------------------
        
        # 1. Dibujar el fondo del recuadro (asumiendo que self.REC_CONSOLA se define en __init__)
        pygame.draw.rect(self.PANTALLA, self.FONDO_NEGRO_CONS, self.REC_CONSOLA)
        
        # 2. Dibujar un borde verde para el efecto CRT
        pygame.draw.rect(self.PANTALLA, self.VERDE_FOSFORO, self.REC_CONSOLA, 2)
        
        # --- 2. CONSOLA INTERACTIVA (Teletipo) ---
        
        # El texto comienza con un margen interno de 10px desde el borde superior e izquierdo del recuadro
        X_CONSOLA = self.REC_CONSOLA.left + 10 
        Y_CONSOLA = self.REC_CONSOLA.top + 10 
        
        # 2.1. Convertir Buffer ASCII a cadena de texto
        texto_consola_str = "".join([
            # Si el código es 10 (LF), lo reemplazamos por el salto de línea de Python ('\n').
            # Si no, usamos chr() para convertir el número a carácter.
            chr(codigo) if codigo != 10 else '\n' 
            for codigo in self.cpu.pantalla
        ])
        
        # 2.2. Añadir el texto que el usuario está escribiendo (Input activo)
        texto_consola_str += self.texto_entrada 
        
        # 2.3. Dividir la cadena por saltos de línea ('\n') para dibujar
        lineas_dibujadas = texto_consola_str.split('\n')

        # 2.4. Dibujar cada línea secuencialmente
        Y_ACTUAL = Y_CONSOLA # Inicializamos con el margen superior
        for i, linea in enumerate(lineas_dibujadas):
            # Usamos la fuente y el color verde de fósforo
            superficie_texto = self.FUENTE_CONS.render(linea, True, self.VERDE_FOSFORO)
            self.PANTALLA.blit(superficie_texto, (X_CONSOLA, Y_ACTUAL))
            Y_ACTUAL += 25  # Espacio entre líneas
        
        # ---------------------------------------------------
        # --- 3. RESULTADO NUMÉRICO FINAL (Dentro del Cuadro) ---
        # ---------------------------------------------------
    
        # Definimos las posiciones para la línea de resultado
        X_CONSOLA = self.REC_CONSOLA.left + 10 
        
        # Calculamos la posición Y. Debe estar cerca del fondo (.bottom) del rectángulo,
        # dejando un margen de unos 15px.
        Y_RESULTADO_FINAL = self.REC_CONSOLA.bottom - 25 
        
        # 3.1. Dibujar la Etiqueta "RESULTADO: "
        etiqueta_val = "RESULTADO: "
        # Usamos la FUENTE GRANDE para el resultado
        etiqueta_texto_surf = self.FUENTE_GRANDE.render(etiqueta_val, True, self.VERDE_FOSFORO)
        
        # Dibujamos la etiqueta
        self.PANTALLA.blit(etiqueta_texto_surf, (X_CONSOLA, Y_RESULTADO_FINAL))
        
        # 3.2. Leer y Dibujar el Valor (RAM[254])
        resultado_num = self.cpu.ram.read(DIR_RESULTADO)
        resultado_val = f"{resultado_num}"
        
        # Calculamos la X para que el número empiece después de la etiqueta
        X_RESULTADO = X_CONSOLA + etiqueta_texto_surf.get_width() 

        resultado_texto_surf = self.FUENTE_GRANDE.render(resultado_val, True, self.VERDE_FOSFORO)
        
        # Dibujamos el valor. Se alinea con la Y_RESULTADO_FINAL.
        self.PANTALLA.blit(resultado_texto_surf, (X_RESULTADO, Y_RESULTADO_FINAL))
        
        # Nota: Eliminamos la actualización de Y_ACTUAL en esta parte ya que es una posición fija.
        
        # --- FIN DE DIBUJO ---

    def gestionar_click(self, pos, modo_run):
        
        # 1. Clic en el botón STEP (mi_cpu.step())
        if self.boton_step_rect and self.boton_step_rect.collidepoint(pos):
            # Solo permitimos STEP si no estamos en modo RUN
            if not modo_run and not self.cpu.halted:
                self.cpu.step()
                return modo_run, True # Retorna modo_run y True para indicar que se avanzó
        
        # 2. Clic en el botón RUN/PAUSE
        if self.boton_run_rect and self.boton_run_rect.collidepoint(pos):
            # Cambia el modo_run a lo opuesto, activando/desactivando el ciclo automático
            return not modo_run, False # Retorna el nuevo modo_run
        
        # 3. Clic en el botón RESET
        if self.boton_reset_rect and self.boton_reset_rect.collidepoint(pos):
            # Llama al método reset de la CPU, pasándole las copias maestras
            self.cpu.reset(self.programa_inicial, self.datos_iniciales) 
            
            # Después del RESET, el simulador siempre debe estar en modo PAUSE (False)
            return False, False # Retorna modo_run=False y accion_step=False
            
        return modo_run, False # No hubo acción de la CPU
    
        


    def dibujar_botones(self, modo_run):
        """ Dibuja los rectángulos de los botones de control y sus textos. """
    
        # 1. Título del Panel (Ubicado en el tercio inferior izquierdo)
        titulo = self.FUENTE_GRANDE.render("Controles", True, self.BLANCO)
        self.PANTALLA.blit(titulo, (self.X_IZQ_START, self.Y_DOS_TERCIOS + 10))
        
        # Coordenadas y dimensiones comunes de los botones
        BTN_ANCHO = 120
        BTN_ALTO = 40
        BTN_Y = self.Y_DOS_TERCIOS + 50
        
        # --- BOTÓN RUN/PAUSE ---
        X_RUN = self.X_IZQ_START + 10
        
        # 1. Crear y guardar el Rectángulo para la detección de clics
        self.boton_run_rect = pygame.Rect(X_RUN, BTN_Y, BTN_ANCHO, BTN_ALTO)
        
        # 2. Definir el color y texto según el modo_run actual
        if modo_run:
            # Modo activo (el botón sirve para PAUSAR)
            color = self.colores['ROJO_BOTON']
            texto = "PAUSE"
        else:
            # Modo pausado (el botón sirve para EJECUTAR)
            color = self.colores['VERDE_BOTON']
            texto = "RUN"
            
        # 3. Dibujar el rectángulo y el texto
        pygame.draw.rect(self.PANTALLA, color, self.boton_run_rect, 0, 5) # 0 es para rellenar, 5 para bordes redondeados
        run_texto = self.FUENTE_GRANDE.render(texto, True, self.BLANCO)
        texto_rect = run_texto.get_rect(center=self.boton_run_rect.center)
        self.PANTALLA.blit(run_texto, texto_rect)


        # --- BOTÓN STEP ---
        X_STEP = X_RUN + BTN_ANCHO + 20 # 20 píxeles de separación del botón RUN
        
        # 1. Crear y guardar el Rectángulo para la detección de clics
        self.boton_step_rect = pygame.Rect(X_STEP, BTN_Y, BTN_ANCHO, BTN_ALTO)
        
        # 2. Definir el color según el estado de la CPU
        # Es gris claro si se puede dar un paso, gris oscuro si está detenido (HALTED)
        if self.cpu.halted:
            color = self.colores['GRIS_OSCURO']
            step_text_color = self.colores['BLANCO'] # Texto blanco en fondo oscuro
        else:
            color = self.colores['GRIS_CLARO']
            step_text_color = self.colores['NEGRO']  # Texto negro en fondo claro

        # 3. Dibujar el rectángulo y el texto
        pygame.draw.rect(self.PANTALLA, color, self.boton_step_rect, 0, 5) 
        step_texto = self.FUENTE_GRANDE.render("STEP", True, step_text_color)
        texto_rect = step_texto.get_rect(center=self.boton_step_rect.center)
        self.PANTALLA.blit(step_texto, texto_rect)

        # --- BOTÓN RESET ---
        X_RESET = X_STEP + BTN_ANCHO + 20 
        
        # 1. Crear y guardar el Rectángulo para la detección de clics
        self.boton_reset_rect = pygame.Rect(X_RESET, BTN_Y, BTN_ANCHO, BTN_ALTO)
        
        # 2. Dibujar el rectángulo y el texto
        color = self.colores['AZUL_RAM'] 
        pygame.draw.rect(self.PANTALLA, color, self.boton_reset_rect, 0, 5) 
        reset_texto = self.FUENTE_GRANDE.render("RESET", True, self.BLANCO)
        texto_rect = reset_texto.get_rect(center=self.boton_reset_rect.center)
        self.PANTALLA.blit(reset_texto, texto_rect)

    
    def dibujar_ram(self):
        """ Dibuja la cuadrícula de 16x16 de la RAM en el panel de la derecha. """
    
        # Título
        titulo = self.FUENTE_GRANDE.render("Memoria RAM (256 celdas)", True, self.BLANCO)
        self.PANTALLA.blit(titulo, (self.X_DER_START, 10)) 
        
        # --- Parámetros de la Cuadrícula ---
        X_INICIO = self.X_DER_START -20
        Y_INICIO = 40
        TAM_CELDA = 38  # Tamaño de cada celda (ajustado para caber en 640px)
        GAP = 2        # Espacio entre celdas
        
        # --- Bucle para dibujar las 256 celdas ---
        for i in range(256):
            
            # 1. Calcular coordenadas (Fila y Columna)
            col = i % 16
            fila = i // 16
            
            x = X_INICIO + col * (TAM_CELDA + GAP)
            y = Y_INICIO + fila * (TAM_CELDA + GAP)
            
            # 2. Obtener la Dirección, Valor y establecer el Color
            direccion = i
            valor = self.ram.read(direccion)
            
            # Determinar el color de fondo de la celda
            color_fondo = self.colores['GRIS_OSCURO']
            color_texto = self.colores['BLANCO']
            
            # Resaltado: Si la dirección es la apuntada por el PC
            if direccion == self.cpu.pc:
                color_fondo = self.colores['AMARILLO_PC']  # Resalta la instrucción actual
                color_texto = self.colores['NEGRO']
            elif valor != 0:
                # Si contiene algún valor (Código o Dato), usa otro color para distinguir
                color_fondo = self.colores['AZUL_RAM'] 
            
            # 3. Dibujar el Rectángulo de la celda
            rect = pygame.Rect(x, y, TAM_CELDA, TAM_CELDA)
            pygame.draw.rect(self.PANTALLA, color_fondo, rect)
            
            # 4. Mostrar la Dirección (Hexadecimal, Arriba a la izquierda)
            dir_texto = self.FUENTE_RAM.render(f"{direccion:02X}", True, color_texto)
            self.PANTALLA.blit(dir_texto, (x + 2, y))
            
            # 5. Mostrar el Valor (Hexadecimal, Centro)
            # Formato 0000 para la instrucción de 16 bits
            val_texto = self.FUENTE_RAM.render(f"{valor:04X}", True, color_texto)
            
            # Centrar el valor en la celda
            val_rect = val_texto.get_rect(center=rect.center)
            self.PANTALLA.blit(val_texto, val_rect)

    
    def dibujar_input(self):
        """ Dibuja la caja de input cuando la CPU está esperando una instrucción IN. """
        
        if not self.cpu.waiting_for_input:
            return # No dibujar nada si la CPU no está esperando
            
        X_START = self.X_IZQ_START + 10
        Y_START = self.Y_DOS_TERCIOS + 120 # Debajo de los botones
        ANCHO_CAJA = 200
        ALTO_CAJA = 30
        
        # 1. Indicador de Espera
        espera_texto = self.FUENTE_GRANDE.render("-> ESPERANDO INPUT (IN)", True, self.colores['AMARILLO_PC'])
        self.PANTALLA.blit(espera_texto, (X_START, Y_START - 25))
        
        # 2. Rectángulo de la caja de texto
        self.input_box_rect = pygame.Rect(X_START, Y_START, ANCHO_CAJA, ALTO_CAJA)
        
        # Dibujar el fondo de la caja
        pygame.draw.rect(self.PANTALLA, self.input_color, self.input_box_rect, 1) # Borde blanco
        pygame.draw.rect(self.PANTALLA, self.colores['NEGRO'], self.input_box_rect.inflate(-2, -2)) # Fondo negro

        # 3. Dibujar el texto escrito
        texto_superficie = self.FUENTE_GRANDE.render(self.texto_entrada, True, self.colores['BLANCO'])
        self.PANTALLA.blit(texto_superficie, (self.input_box_rect.x + 5, self.input_box_rect.y + 5))


    def mostrar_interfaz(self, modo_run):
        self.PANTALLA.fill(self.GRIS_OSCURO)
        
        # Dibuja la línea divisoria vertical (Mitad Izquierda vs. Mitad Derecha)
        pygame.draw.line(self.PANTALLA, self.BLANCO, (600, 0), (600, self.ALTO), 2)
        
        # Dibujar las líneas divisorias horizontales en la Mitad IZQUIERDA
        pygame.draw.line(self.PANTALLA, self.BLANCO, (0, self.Y_TERCIO), (600, self.Y_TERCIO), 1)
        pygame.draw.line(self.PANTALLA, self.BLANCO, (0, self.Y_DOS_TERCIOS), (600, self.Y_DOS_TERCIOS), 1)

        # Llama a todos los dibujos de componentes
        self.dibujar_registros()
        self.dibujar_pantalla()
        self.dibujar_input()
        self.dibujar_botones(modo_run)
        self.dibujar_ram()