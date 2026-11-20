# ------------------------------------------------------------
# Analizador semántico de FitLang
#
# El sintáctico ya revisó que el programa esté bien ARMADO.
# El semántico revisa que tenga SENTIDO. Para eso recorre el árbol
# como si ejecutara la rutina: va anotando las variables en la tabla
# de símbolos, calcula cuánto vale cada cantidad y revisa las reglas
# del lenguaje:
#
#   Variables  Toda variable tiene que crearse antes de usarse
#   R1  repetir tiene que ser mayor que 0
#   R2  las repeticiones de hacer tienen que ser mayores que 0
#   R3  descansar tiene que estar entre 10 y 300 segundos
#
# No se detiene en el primer error: revisa todo el programa y al
# final avisa todos los errores que encontró, cada uno con su línea.
#
# Para probarlo solo:   python semantico.py programas/rutina1.fit
# ------------------------------------------------------------

import sys

import lexico
import sintactico
from tabla_simbolos import TablaSimbolos, VariableNoDefinida

DESCANSO_MINIMO = 10      # segundos
DESCANSO_MAXIMO = 300     # segundos (5 minutos)


class ErrorSemantico(Exception):
    def __init__(self, errores):
        self.errores = errores
        super().__init__("\n".join(errores))


def evaluar(expresion, tabla):
    """
    Calcula cuánto vale una expresión (un número, una variable o una cuenta).
    Si usa una variable que no existe, la tabla lanza VariableNoDefinida.
    """
    tipo = expresion["tipo"]
    if tipo == "numero":
        return expresion["valor"]
    if tipo == "variable":
        return tabla.usar(expresion["nombre"], expresion["linea"], expresion["columna"])

    izquierda = evaluar(expresion["izq"], tabla)
    derecha = evaluar(expresion["der"], tabla)
    op = expresion["op"]
    if op == "+":
        return izquierda + derecha
    if op == "-":
        return izquierda - derecha
    if op == "*":
        return izquierda * derecha
    if op == ">":
        return izquierda > derecha
    if op == "<":
        return izquierda < derecha
    if op == "==":
        return izquierda == derecha


class AnalizadorSemantico:

    def __init__(self):
        self.tabla = TablaSimbolos()
        self.errores = []

    def anotar(self, mensaje):
        """Guarda un error. Si ya estaba (por ejemplo, dentro de un repetir), no lo repite."""
        if mensaje not in self.errores:
            self.errores.append(mensaje)

    def valor_de(self, expresion):
        """Calcula una expresión. Si usa una variable que no existe, anota el error y devuelve None."""
        try:
            return evaluar(expresion, self.tabla)
        except VariableNoDefinida as e:
            self.anotar(str(e))
            return None

    def revisar(self, instrucciones):
        for ins in instrucciones:
            tipo = ins["tipo"]

            if tipo == "asignacion":
                valor = self.valor_de(ins["valor"])
                self.tabla.definir(ins["nombre"], valor, ins["linea"])

            elif tipo == "hacer":
                reps = self.valor_de(ins["repeticiones"])
                # R2: las repeticiones de hacer tienen que ser mayores que 0
                if reps is not None and reps <= 0:
                    self.anotar(f"Línea {ins['linea']}: se rompió la regla R2 (las repeticiones de "
                                f"hacer deben ser mayores que 0): aquí se piden {reps} {ins['ejercicio']}")

            elif tipo == "descansar":
                segundos = self.valor_de(ins["cantidad"])
                # R3: descansar tiene que estar entre 10 y 300 segundos
                if segundos is not None and not (DESCANSO_MINIMO <= segundos <= DESCANSO_MAXIMO):
                    self.anotar(f"Línea {ins['linea']}: se rompió la regla R3 (descansar debe estar "
                                f"entre {DESCANSO_MINIMO} y {DESCANSO_MAXIMO} segundos): "
                                f"aquí se piden {segundos} segundos")

            elif tipo in ("calentar", "trotar", "mostrar"):
                self.valor_de(ins["cantidad"])          # solo se revisa que sus variables existan

            elif tipo == "repetir":
                veces = self.valor_de(ins["veces"])
                # R1: repetir tiene que ser mayor que 0
                if veces is not None and veces <= 0:
                    self.anotar(f"Línea {ins['linea']}: se rompió la regla R1 (repetir debe ser "
                                f"mayor que 0): aquí se pide repetir {veces} veces")
                if veces is not None and veces > 0:
                    for _ in range(veces):              # se recorre el bloque como si se ejecutara
                        self.revisar(ins["cuerpo"])
                else:
                    self.revisar(ins["cuerpo"])         # igual se revisa lo de adentro una vez

            elif tipo == "si":
                cumple = self.valor_de(ins["condicion"])
                if cumple is None:                      # no se sabe: se revisan los dos bloques
                    self.revisar(ins["entonces"])
                    self.revisar(ins["sino"])
                elif cumple:
                    self.revisar(ins["entonces"])
                else:
                    self.revisar(ins["sino"])


def analizar(arbol):
    """
    Revisa el sentido del programa. Si todo está bien, devuelve la tabla de símbolos.
    Si hay errores, lanza ErrorSemantico con la lista de todos.
    """
    analizador = AnalizadorSemantico()
    analizador.revisar(arbol["instrucciones"])
    if analizador.errores:
        raise ErrorSemantico(analizador.errores)
    return analizador.tabla


# Esto solo se ejecuta si se corre este archivo directamente
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python semantico.py programas/rutina1.fit")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as archivo:
        texto = archivo.read()
    try:
        tabla = analizar(sintactico.analizar(lexico.analizar(texto)))
        print("Sentido correcto: el programa cumple las reglas del lenguaje")
        print()
        print(tabla.como_texto())
    except lexico.ErrorLexico as e:
        print("ERROR LÉXICO:", e)
    except sintactico.ErrorSintactico as e:
        print("ERROR SINTÁCTICO:", e)
    except ErrorSemantico as e:
        print("ERROR SEMÁNTICO:")
        for error in e.errores:
            print("  -", error)
