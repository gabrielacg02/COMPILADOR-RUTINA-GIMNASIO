# ------------------------------------------------------------
# Ejecutor de FitLang
#
# Es el "programa pequeño" que pide el enunciado. Lee la lista de
# comandos que produce el compilador (un archivo .txt de la carpeta
# comandos/) y muestra la rutina paso a paso, como si fuera un
# entrenador. Al final muestra un resumen de toda la rutina.
#
# No necesita saber nada de variables ni de bloques: el generador ya
# le entrega todo listo, un comando por línea.
#
# Uso:   python ejecutor.py comandos/rutina1.txt
#        python ejecutor.py comandos/rutina1.txt --lento   (un paso cada medio segundo)
# ------------------------------------------------------------

import sys
import time


class ErrorEjecucion(Exception):
    pass


def ejecutar(comandos, lento=False):
    """Recibe la lista de comandos (textos como 'HACER FLEXIONES 10') y la ejecuta."""
    minutos_calentamiento = 0
    minutos_trote = 0
    segundos_descanso = 0
    repeticiones = {}            # ejercicio -> total de repeticiones

    print("=== Empieza la rutina ===")
    paso = 0
    for numero, linea in enumerate(comandos, start=1):
        partes = linea.split()
        if not partes:
            continue                                    # línea vacía
        if not partes[-1].lstrip("-").isdigit():
            raise ErrorEjecucion(f"Línea {numero} del archivo de comandos: '{linea}' no termina en un número")
        paso += 1
        comando = partes[0]

        if comando == "CALENTAR" and len(partes) == 2:
            minutos = int(partes[1])
            minutos_calentamiento += minutos
            print(f"Paso {paso}: Calienta {minutos} minutos")

        elif comando == "HACER" and len(partes) == 3:
            ejercicio = partes[1].lower()
            cantidad = int(partes[2])
            repeticiones[ejercicio] = repeticiones.get(ejercicio, 0) + cantidad
            print(f"Paso {paso}: Haz {cantidad} {ejercicio}")

        elif comando == "DESCANSAR" and len(partes) == 2:
            segundos = int(partes[1])
            segundos_descanso += segundos
            print(f"Paso {paso}: Descansa {segundos} segundos")

        elif comando == "TROTAR" and len(partes) == 2:
            minutos = int(partes[1])
            minutos_trote += minutos
            print(f"Paso {paso}: Trota {minutos} minutos")

        elif comando == "MOSTRAR" and len(partes) == 2:
            print(f"Paso {paso}: Resultado: {partes[1]}")

        else:
            raise ErrorEjecucion(f"Línea {numero} del archivo de comandos: no entiendo '{linea}'")

        if lento:
            time.sleep(0.5)

    print("=== Rutina terminada ===")
    print()
    print("Resumen:")
    print(f"  Calentamiento: {minutos_calentamiento} minutos")
    for ejercicio, total in repeticiones.items():
        print(f"  {ejercicio.capitalize()}: {total} en total")
    print(f"  Descanso: {segundos_descanso} segundos")
    print(f"  Trote: {minutos_trote} minutos")


# Esto solo se ejecuta si se corre este archivo directamente
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python ejecutor.py comandos/rutina1.txt [--lento]")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as archivo:
        lineas = archivo.read().splitlines()
    try:
        ejecutar(lineas, lento="--lento" in sys.argv)
    except ErrorEjecucion as e:
        print("ERROR DE EJECUCIÓN:", e)
