# ------------------------------------------------------------
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
# Actividad 7: además de revisar, ahora ARMA EL ÁRBOL del programa.
# Cada función devuelve un "nodo" (un diccionario) con lo que
# encontró. El semántico y el generador recorren ese árbol.
#
# Para probarlo solo:   python sintactico.py programas/rutina1.fit
# Para ver el árbol:     python sintactico.py programas/rutina1.fit --arbol
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
        instrucciones = self.lista(cierres=[])
        self.exigir("FIN_ARCHIVO", "el final del archivo")
        return {"tipo": "programa", "instrucciones": instrucciones}

    # R2  Lista → SALTO Lista | Instruccion FinLinea Lista | ε
    # La lista se acaba (ε) cuando llega el final del archivo o la palabra
    # que cierra el bloque donde estamos ("fin", o "sino" dentro de un si).
    # Devuelve la lista de instrucciones que encontró.
    def lista(self, cierres):
        instrucciones = []
        while True:
            tipo = self.actual().tipo
            if tipo == "SALTO":
                self.consumir()                 # línea vacía o solo con comentario
            elif tipo == "FIN_ARCHIVO" or tipo in cierres:
                return instrucciones
            else:
                instrucciones.append(self.instruccion())
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
            return self.asignacion()
        elif t.tipo in ("CALENTAR", "DESCANSAR", "TROTAR", "MOSTRAR"):
            return self.instruccion_simple()
        elif t.tipo == "HACER":
            return self.hacer()
        elif t.tipo == "REPETIR":
            return self.repetir()
        elif t.tipo == "SI":
            return self.si()
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
        nombre = self.consumir()                         # el nombre de la variable
        self.exigir("ASIGNACION", "'='")
        valor = self.expr()
        return {"tipo": "asignacion", "linea": nombre.linea,
                "nombre": nombre.texto, "valor": valor}

    # R6  Calentar  → 'calentar' Expr
    # R8  Descansar → 'descansar' Expr
    # R9  Trotar    → 'trotar' Expr
    # R10 Mostrar   → 'mostrar' Expr
    # Las cuatro se arman igual: la palabra y después una cantidad.
    def instruccion_simple(self):
        palabra = self.consumir()
        cantidad = self.expr()
        return {"tipo": palabra.texto, "linea": palabra.linea, "cantidad": cantidad}

    # R7  Hacer → 'hacer' EJERCICIO Expr
    def hacer(self):
        palabra = self.consumir()                        # la palabra "hacer"
        ejercicio = self.exigir("EJERCICIO", "un ejercicio (flexiones, sentadillas, abdominales, burpees o zancadas)")
        repeticiones = self.expr()
        return {"tipo": "hacer", "linea": palabra.linea,
                "ejercicio": ejercicio.texto, "repeticiones": repeticiones}

    # R11  Repetir → 'repetir' Expr 'veces' SALTO Lista 'fin'
    def repetir(self):
        inicio = self.consumir()                         # la palabra "repetir"
        veces = self.expr()
        self.exigir("VECES", "'veces'")
        self.exigir("SALTO", "un salto de línea después de 'veces'")
        cuerpo = self.lista(cierres=["FIN"])
        self.cerrar_con_fin(inicio)
        return {"tipo": "repetir", "linea": inicio.linea, "veces": veces, "cuerpo": cuerpo}

    # R12  Si   → 'si' Comparacion 'entonces' SALTO Lista Sino 'fin'
    # R13  Sino → 'sino' SALTO Lista | ε
    def si(self):
        inicio = self.consumir()                         # la palabra "si"
        condicion = self.comparacion()
        self.exigir("ENTONCES", "'entonces'")
        self.exigir("SALTO", "un salto de línea después de 'entonces'")
        bloque_si = self.lista(cierres=["FIN", "SINO"])
        bloque_sino = []
        if self.actual().tipo == "SINO":
            self.consumir()
            self.exigir("SALTO", "un salto de línea después de 'sino'")
            bloque_sino = self.lista(cierres=["FIN"])
        self.cerrar_con_fin(inicio)
        return {"tipo": "si", "linea": inicio.linea, "condicion": condicion,
                "entonces": bloque_si, "sino": bloque_sino}

    def cerrar_con_fin(self, inicio):
        """Consume el 'fin' de un bloque. Si no está, dice cuál bloque quedó abierto."""
        if self.actual().tipo != "FIN":
            self.error(f"'fin' para cerrar el '{inicio.texto}' de la línea {inicio.linea}")
        self.consumir()

    # R14  Comparacion   → Expr OpComparacion Expr
    # R15  OpComparacion → '>' | '<' | '=='
    def comparacion(self):
        izquierda = self.expr()
        if self.actual().tipo not in ("MAYOR", "MENOR", "IGUAL_IGUAL"):
            self.error("una comparación (>, < o ==)")
        operador = self.consumir().texto
        derecha = self.expr()
        return {"tipo": "comparacion", "op": operador, "izq": izquierda, "der": derecha}

    # R16  Expr      → Termino RestoExpr
    # R17  RestoExpr → '+' Termino RestoExpr | '-' Termino RestoExpr | ε
    # El while hace el trabajo de RestoExpr: mientras llegue otro vagón (+ o -), se consume.
    # Cada vagón se va "colgando" del nodo anterior: así 10 - 4 - 3 queda (10 - 4) - 3.
    def expr(self):
        nodo = self.termino()
        while self.actual().tipo in ("MAS", "MENOS"):
            operador = self.consumir().texto
            derecha = self.termino()
            nodo = {"tipo": "operacion", "op": operador, "izq": nodo, "der": derecha}
        return nodo

    # R18  Termino      → Valor RestoTermino
    # R19  RestoTermino → '*' Valor RestoTermino | ε
    def termino(self):
        nodo = self.valor()
        while self.actual().tipo == "POR":
            self.consumir()
            derecha = self.valor()
            nodo = {"tipo": "operacion", "op": "*", "izq": nodo, "der": derecha}
        return nodo

    # R20  Valor → NUMERO | IDENTIFICADOR
    def valor(self):
        t = self.actual()
        if t.tipo == "NUMERO":
            self.consumir()
            return {"tipo": "numero", "valor": int(t.texto)}
        if t.tipo == "IDENTIFICADOR":
            self.consumir()
            # Se guarda dónde está escrita la variable, para que el semántico
            # pueda decir línea y columna si no existe.
            return {"tipo": "variable", "nombre": t.texto, "linea": t.linea, "columna": t.columna}
        self.error("un número o una variable")


def analizar(tokens):
    """Revisa la estructura y devuelve el árbol. Si algo está mal, lanza ErrorSintactico."""
    return AnalizadorSintactico(tokens).programa()


# ---------------- para ver el árbol en pantalla ----------------

def texto_expresion(e):
    """Escribe una expresión con paréntesis, para que se vea qué se agrupa primero."""
    if e["tipo"] == "numero":
        return str(e["valor"])
    if e["tipo"] == "variable":
        return e["nombre"]
    if e["tipo"] == "comparacion":
        return f"{texto_expresion(e['izq'])} {e['op']} {texto_expresion(e['der'])}"
    return f"({texto_expresion(e['izq'])} {e['op']} {texto_expresion(e['der'])})"


def texto_arbol(instrucciones, sangria="  "):
    lineas = []
    for ins in instrucciones:
        t = ins["tipo"]
        if t == "asignacion":
            lineas.append(f"{sangria}asignacion: {ins['nombre']} = {texto_expresion(ins['valor'])}")
        elif t == "hacer":
            lineas.append(f"{sangria}hacer: {ins['ejercicio']}, {texto_expresion(ins['repeticiones'])}")
        elif t == "repetir":
            lineas.append(f"{sangria}repetir: {texto_expresion(ins['veces'])} veces")
            lineas += texto_arbol(ins["cuerpo"], sangria + "    ")
        elif t == "si":
            lineas.append(f"{sangria}si: {texto_expresion(ins['condicion'])}")
            lineas.append(f"{sangria}  entonces:")
            lineas += texto_arbol(ins["entonces"], sangria + "    ")
            if ins["sino"]:
                lineas.append(f"{sangria}  sino:")
                lineas += texto_arbol(ins["sino"], sangria + "    ")
        else:   # calentar, descansar, trotar, mostrar
            lineas.append(f"{sangria}{t}: {texto_expresion(ins['cantidad'])}")
    return lineas


# Esto solo se ejecuta si se corre este archivo directamente
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python sintactico.py programas/rutina1.fit [--arbol]")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as archivo:
        texto = archivo.read()
    try:
        arbol = analizar(lexico.analizar(texto))
        print("Estructura correcta: el programa cumple la gramática")
        if "--arbol" in sys.argv:
            print()
            print("programa")
            print("\n".join(texto_arbol(arbol["instrucciones"])))
    except lexico.ErrorLexico as e:
        print("ERROR LÉXICO:", e)
    except ErrorSintactico as e:
        print("ERROR SINTÁCTICO:", e)
