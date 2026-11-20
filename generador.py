# ------------------------------------------------------------
# Generador de comandos de FitLang
#
# Es la última fase del compilador. Cuando el programa ya pasó el
# léxico, el sintáctico y el semántico, el generador recorre el árbol
# y lo convierte en una lista de comandos sencillos, uno por línea:
#
#   CALENTAR 5
#   HACER FLEXIONES 10
#   DESCANSAR 45
#   TROTAR 10
#   MOSTRAR 60
#
# Las variables ya se reemplazan por su valor, los repetir se
# "desenrollan" (si dice 3 veces, los comandos salen 3 veces) y de
# cada si solo sale el bloque que se cumple. Así el ejecutor no tiene
# que saber nada de variables ni de bloques: solo sigue la lista.
#
# Para probarlo solo:   python generador.py programas/rutina1.fit
# ------------------------------------------------------------

import sys

import lexico
import sintactico
import semantico
from tabla_simbolos import TablaSimbolos


class Generador:

    def __init__(self):
        self.tabla = TablaSimbolos()
        self.comandos = []

    def valor(self, expresion):
        return semantico.evaluar(expresion, self.tabla)

    def generar(self, instrucciones):
        for ins in instrucciones:
            tipo = ins["tipo"]

            if tipo == "asignacion":
                # Las asignaciones no producen comandos: solo cambian la tabla
                self.tabla.definir(ins["nombre"], self.valor(ins["valor"]), ins["linea"])

            elif tipo == "hacer":
                reps = self.valor(ins["repeticiones"])
                self.comandos.append(f"HACER {ins['ejercicio'].upper()} {reps}")

            elif tipo in ("calentar", "descansar", "trotar", "mostrar"):
                cantidad = self.valor(ins["cantidad"])
                self.comandos.append(f"{tipo.upper()} {cantidad}")

            elif tipo == "repetir":
                for _ in range(self.valor(ins["veces"])):
                    self.generar(ins["cuerpo"])

            elif tipo == "si":
                if self.valor(ins["condicion"]):
                    self.generar(ins["entonces"])
                else:
                    self.generar(ins["sino"])


def generar(arbol):
    """Recibe el árbol (ya revisado por el semántico) y devuelve la lista de comandos."""
    generador = Generador()
    generador.generar(arbol["instrucciones"])
    return generador.comandos


def guardar(comandos, ruta):
    """Guarda los comandos en un archivo de texto, uno por línea."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(comandos) + "\n")


# Esto solo se ejecuta si se corre este archivo directamente
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python generador.py programas/rutina1.fit")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as archivo:
        texto = archivo.read()
    try:
        arbol = sintactico.analizar(lexico.analizar(texto))
        semantico.analizar(arbol)
        for comando in generar(arbol):
            print(comando)
    except (lexico.ErrorLexico, sintactico.ErrorSintactico, semantico.ErrorSemantico) as e:
        print("El programa tiene errores, no se generan comandos:")
        print(e)
