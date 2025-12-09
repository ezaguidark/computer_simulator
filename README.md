Objetivo del programa:
Simular la estructura y funcionamiento básico de un computador sencillo, mediante la representación gráfica de sus elementos básicos:
•	CPU.
•	Memoria RAM.
•	Entrada y Salida.
Para posteriormente, implementar un programa simple que sume dos números y muestre el resultado en pantalla.
El programa estará en un “Almacenamiento persistente”, mientras que los datos se guardaran en la memoria RAM.

Requerimientos:
•	Python 3.X.X
•	Pygame
•	Programa.txt

Flujo general:
El simulador deberá cargar los datos de Programa.txt con las instrucciones en lenguaje máquina, y las escribirá en la memoria RAM. La CPU comenzara a ejecutar las instrucciones secuencialmente, esto incluye solicitar los datos para la suma y mostrar el resultado en pantalla.





Interface:
La interfaz gráfica, consta de 4 paneles en donde se muestra toda la información solicitada y se pide la entrada de datos al usuario:
 

•	Display: En este panel, se muestra una especie de pantalla que va mostrando los caracteres uno por uno, al estilo teletipo. El resultado se almacena en una posición fija de memoria para mayor facilidad y versatilidad al momento de mostrar el resultado en pantalla. Su valor por defecto es 0.

•	Estado de la CPU: En este panel, se muestra el estado de la CPU, lo que serían sus registros (PC, IC, AR, FLAG_Z), y su estado a tiempo real.

•	Controles: El programa consta de 3 botones básicos:
o	RUN: Inicia la secuencia de instrucciones del programa en el simulador.
o	STEP: Permite avanzar un solo paso del CPU el estado del programa.
o	RESET: Reinicia el programa a su estado inicial.

•	Memoria RAM: El panel más grande de la interfaz, muestra las 256 celdas correspondientes a los espacios en la memoria RAM. Se actualizan a tiempo real en función a los datos que se encuentran en ella.

Uso del simulador:
1.	Inicio del simulador:
 
Presionar el botón RUN, para que el simulador cargue e inicie el programa. El simulador comenzara a mostrar el mensaje de bienvenida. 
2.	Ingresar el primer número:
 
Cuando el mensaje de bienvenida termine de mostrarse, el programa solicitara el primer número. Para poder realizar esta operación, se deberá hacer “click” en el recuadro del INPUT, esto permitirá escribir el primer número. Cuando el número se haya ingresado, se deberá pulsar la tecla ENTER del teclado para almacenar el dato.
3.	Ingresar el segundo número:
 
El procedimiento es básicamente el mismo, luego de ingresar el primer número, se solicitará el segundo número. Se repite el procedimiento, hacer click en el recuadro del input, escribir el dato, y presionar ENTER.
4.	Visualizar el resultado y reiniciar.
 
El resultado se mostrará inmediatamente en el Display luego de ingresar el segundo número. El programa entrara en estado HALTED, y en la memoria se verán reflejados en donde están almacenados los resultados.
Opcionalmente se puede presionar el botón RESET para reiniciar el estado del programa, o simplemente cerrarlo y finalizar la ejecución del simulador.
Nota:
Actualmente, la ejecución del programa es continua. Pero si se desea ejecutarlo paso por paso, es posible cambiar la siguiente línea de código en el archivo main.py a False:
 
De esta forma, el programa se ejecutará por etapas, y se deberá presionar el botón RUN o STEP, cada vez que se realice una acción. Por ejemplo, al ingresar un número y presionar ENTER, se deberá presionar RUN nuevamente para reanudar el programa, o STEP para ver más a detalle el estado en memoria y en el CPU.


Flujo de funcionamiento:

1.	Fase de Inicialización y Bienvenida

La CPU carga el código ASCII de cada letra en el Acumulador (AC) y luego lo envía al buffer de pantalla, usando LOADI y OUT.

2.	Fase de Interacción
•	El programa muestra la solicitud, se detiene para la entrada del usuario y convierte el carácter a un valor numérico.
•	Muestra en pantalla la solicitud, usando LOADI y OUT. 
•	Detiene el ciclo de ejecución de la CPU, esperando que el usuario ingrese el input usando la operación IN. 
•	Muestra el carácter recién ingresado por el usuario con OUT. Recibe el valor
•	Como se recibe el valor ACSII del carácter, se convierte a valor numérico mediante la resta del valor ACSII de 0, utilizando SUB.
•	Se almacena en memoria el valor del input con STORE.
•	Se repite el procedimiento para el Numero 2.

3.	Fase de salida.
•	Se carga el valor del número 1 al acumulador con LOAD.
•	Se suma el valor del número 2 con ADD.
•	Se guarda el resultado en la posición designada en memoria para mostrarla en el Display, con STORE.
•	El programa se detiene, HALT.
