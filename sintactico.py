# Analizador sintáctico de FitLang

#
# Revisa, con las reglas de gramatica.txt, que los tokens que
# entrega el léxico estén en un orden permitido.
#
# Es un analizador DESCENDENTE RECURSIVO, como el de la clase:
# hay una función por cada regla de la gramática (R1, R2, ...).
# Cada función mira el token actual para saber qué hacer y
# "consume" los tokens que ya revisó. Si llega algo que la regla
# no permite, se detiene y dice qué esperaba, con línea y columna.
#
# Para probarlo solo:   python sintactico.py programas/rutina1.fit
# ------------------------------------------------------------

import sys

import lexico


class ErrorSintactico(Exception):
    pass


class AnalizadorSintactico:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0          # cuál token toca revisar

    # ---------------- herramientas ----------------

    def actual(self):
        """El token que toca revisar ahora."""
        return self.tokens[self.pos]

    def consumir(self):
        """Este token ya quedó revisado: lo devuelve y pasa al siguiente."""
        token = self.tokens[self.pos]
        if token.tipo != "FIN_ARCHIVO":
            self.pos += 1
        return token

    def error(self, que_se_esperaba):
        """Para todo y arma el mensaje con la línea y la columna."""
        t = self.actual()
        if t.tipo == "FIN_ARCHIVO":
            raise ErrorSintactico(f"Línea {t.linea}, columna {t.columna} (final del archivo): "
                                  f"se esperaba {que_se_esperaba}")
        if t.tipo == "SALTO":
            llego = "un salto de línea"
        else:
            llego = f"'{t.texto}'"
        raise ErrorSintactico(f"Línea {t.linea}, columna {t.columna}: "
                              f"se esperaba {que_se_esperaba}, pero llegó {llego}")

    def exigir(self, tipo, que_se_esperaba):
        """Si el token actual es del tipo pedido lo consume; si no, es error."""
        if self.actual().tipo != tipo:
            self.error(que_se_esperaba)
        return self.consumir()

    # ------------- una función por regla -------------

    # R1  Programa → Lista FIN_ARCHIVO
    def programa(self):
        self.lista(cierres=[])
        self.exigir("FIN_ARCHIVO", "el final del archivo")

    # R2  Lista → SALTO Lista | Instruccion FinLinea Lista | ε
    # La lista se acaba (ε) cuando llega el final del archivo o la palabra
    # que cierra el bloque donde estamos ("fin", o "sino" dentro de un si).
    def lista(self, cierres):
        while True:
            tipo = self.actual().tipo
            if tipo == "SALTO":
                self.consumir()                 # línea vacía o solo con comentario
            elif tipo == "FIN_ARCHIVO" or tipo in cierres:
                return
            else:
                self.instruccion()
                self.fin_linea()

    # R3  FinLinea → SALTO | ε
    def fin_linea(self):
        if self.actual().tipo == "SALTO":
            self.consumir()
        elif self.actual().tipo != "FIN_ARCHIVO":
            self.error("un salto de línea (va una sola instrucción por línea)")

    # R4  Instruccion → Asignacion | Calentar | Hacer | Descansar | Trotar | Mostrar | Repetir | Si
    def instruccion(self):
        t = self.actual()
        if t.tipo == "IDENTIFICADOR":
            self.asignacion()
        elif t.tipo in ("CALENTAR", "DESCANSAR", "TROTAR", "MOSTRAR"):
            self.instruccion_simple()
        elif t.tipo == "HACER":
            self.hacer()
        elif t.tipo == "REPETIR":
            self.repetir()
        elif t.tipo == "SI":
            self.si()
        elif t.tipo == "FIN":
            raise ErrorSintactico(f"Línea {t.linea}, columna {t.columna}: "
                                  f"sobra este 'fin', no hay ningún repetir ni si abierto")
        elif t.tipo == "SINO":
            raise ErrorSintactico(f"Línea {t.linea}, columna {t.columna}: "
                                  f"este 'sino' no pertenece a ningún si")
        else:
            self.error("una instrucción")

    # R5  Asignacion → IDENTIFICADOR '=' Expr
    def asignacion(self):
        self.consumir()                                  # el nombre de la variable
        self.exigir("ASIGNACION", "'='")
        self.expr()

    # R6  Calentar  → 'calentar' Expr
    # R8  Descansar → 'descansar' Expr
    # R9  Trotar    → 'trotar' Expr
    # R10 Mostrar   → 'mostrar' Expr
    # Las cuatro se arman igual: la palabra y después una cantidad.
    def instruccion_simple(self):
        self.consumir()
        self.expr()

    # R7  Hacer → 'hacer' EJERCICIO Expr
    def hacer(self):
        self.consumir()                                  # la palabra "hacer"
        self.exigir("EJERCICIO", "un ejercicio (flexiones, sentadillas, abdominales, burpees o zancadas)")
        self.expr()                                      # las repeticiones

    # R11  Repetir → 'repetir' Expr 'veces' SALTO Lista 'fin'
    def repetir(self):
        inicio = self.consumir()                         # la palabra "repetir"
        self.expr()
        self.exigir("VECES", "'veces'")
        self.exigir("SALTO", "un salto de línea después de 'veces'")
        self.lista(cierres=["FIN"])
        self.cerrar_con_fin(inicio)

    # R12  Si   → 'si' Comparacion 'entonces' SALTO Lista Sino 'fin'
    # R13  Sino → 'sino' SALTO Lista | ε
    def si(self):
        inicio = self.consumir()                         # la palabra "si"
        self.comparacion()
        self.exigir("ENTONCES", "'entonces'")
        self.exigir("SALTO", "un salto de línea después de 'entonces'")
        self.lista(cierres=["FIN", "SINO"])
        if self.actual().tipo == "SINO":
            self.consumir()
            self.exigir("SALTO", "un salto de línea después de 'sino'")
            self.lista(cierres=["FIN"])
        self.cerrar_con_fin(inicio)

    def cerrar_con_fin(self, inicio):
        """Consume el 'fin' de un bloque. Si no está, dice cuál bloque quedó abierto."""
        if self.actual().tipo != "FIN":
            self.error(f"'fin' para cerrar el '{inicio.texto}' de la línea {inicio.linea}")
        self.consumir()

    # R14  Comparacion   → Expr OpComparacion Expr
    # R15  OpComparacion → '>' | '<' | '=='
    def comparacion(self):
        self.expr()
        if self.actual().tipo not in ("MAYOR", "MENOR", "IGUAL_IGUAL"):
            self.error("una comparación (>, < o ==)")
        self.consumir()
        self.expr()

    # R16  Expr      → Termino RestoExpr
    # R17  RestoExpr → '+' Termino RestoExpr | '-' Termino RestoExpr | ε
    # El while hace el trabajo de RestoExpr: mientras llegue otro vagón (+ o -), se consume.
    def expr(self):
        self.termino()
        while self.actual().tipo in ("MAS", "MENOS"):
            self.consumir()
            self.termino()

    # R18  Termino      → Valor RestoTermino
    # R19  RestoTermino → '*' Valor RestoTermino | ε
    def termino(self):
        self.valor()
        while self.actual().tipo == "POR":
            self.consumir()
            self.valor()

    # R20  Valor → NUMERO | IDENTIFICADOR
    def valor(self):
        if self.actual().tipo in ("NUMERO", "IDENTIFICADOR"):
            self.consumir()
        else:
            self.error("un número o una variable")


def analizar(tokens):
    """Revisa la estructura. Si algo está mal, lanza ErrorSintactico."""
    AnalizadorSintactico(tokens).programa()


# Esto solo se ejecuta si se corre este archivo directamente
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python sintactico.py programas/rutina1.fit")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as archivo:
        texto = archivo.read()
    try:
        analizar(lexico.analizar(texto))
        print("Estructura correcta: el programa cumple la gramática")
    except lexico.ErrorLexico as e:
        print("ERROR LÉXICO:", e)
    except ErrorSintactico as e:
        print("ERROR SINTÁCTICO:", e)
