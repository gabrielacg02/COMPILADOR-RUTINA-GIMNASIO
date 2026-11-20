# ------------------------------------------------------------
# Compilador de FitLang - programa principal
#
# Pasa un programa .fit por las cuatro fases del compilador:
#   1. Léxico       (lexico.py)        separa en tokens
#   2. Sintáctico   (sintactico.py)    revisa la estructura y arma el árbol
#   3. Semántico    (semantico.py)     revisa que tenga sentido (variables y reglas)
#   4. Generación   (generador.py)     produce la lista de comandos
# Si no hay errores, guarda los comandos en la carpeta comandos/
# y, si se pide, los ejecuta con ejecutor.py.
#
# Uso:
#   python fitlang.py programas/rutina1.fit              compila y muestra los comandos
#   python fitlang.py programas/rutina1.fit --ejecutar   además ejecuta la rutina
#   python fitlang.py programas/rutina1.fit --tokens     además muestra los tokens
#   python fitlang.py programas/rutina1.fit --arbol      además muestra el árbol
# ------------------------------------------------------------

import os
import sys

import lexico
import sintactico
import semantico
import generador
import ejecutor

CARPETA = os.path.dirname(os.path.abspath(__file__))
CARPETA_COMANDOS = os.path.join(CARPETA, "comandos")


def compilar(texto):
    """
    Pasa el texto por las cuatro fases.
    Devuelve un diccionario con lo que salió de cada una; si hubo error,
    trae el mensaje y en qué fase pasó.
    """
    r = {"tokens": None, "arbol": None, "tabla": None, "comandos": None, "error": None, "fase": None}

    try:
        r["tokens"] = lexico.analizar(texto)
    except lexico.ErrorLexico as e:
        r["error"], r["fase"] = str(e), "léxico"
        return r

    try:
        r["arbol"] = sintactico.analizar(r["tokens"])
    except sintactico.ErrorSintactico as e:
        r["error"], r["fase"] = str(e), "sintáctico"
        return r

    try:
        r["tabla"] = semantico.analizar(r["arbol"])
    except semantico.ErrorSemantico as e:
        r["error"], r["fase"] = str(e), "semántico"
        return r

    r["comandos"] = generador.generar(r["arbol"])
    return r


def guardar_comandos(nombre_programa, comandos):
    """Guarda los comandos en comandos/<nombre>.txt y devuelve la ruta."""
    os.makedirs(CARPETA_COMANDOS, exist_ok=True)
    nombre = os.path.basename(nombre_programa).replace(".fit", ".txt")
    ruta = os.path.join(CARPETA_COMANDOS, nombre)
    generador.guardar(comandos, ruta)
    return ruta


def main():
    if len(sys.argv) < 2:
        print("Uso: python fitlang.py programas/rutina1.fit [--ejecutar] [--tokens] [--arbol]")
        sys.exit(1)

    ruta_programa = sys.argv[1]
    with open(ruta_programa, encoding="utf-8") as archivo:
        texto = archivo.read()

    r = compilar(texto)

    if r["tokens"] and "--tokens" in sys.argv:
        print(lexico.tabla_tokens(r["tokens"]))
        print()
    if r["arbol"] and "--arbol" in sys.argv:
        print("programa")
        print("\n".join(sintactico.texto_arbol(r["arbol"]["instrucciones"])))
        print()

    if r["error"]:
        print(f"ERROR {r['fase'].upper()}")
        print(r["error"])
        sys.exit(1)

    print(f"1. Análisis léxico:     correcto ({len(r['tokens'])} tokens)")
    print("2. Análisis sintáctico: correcto, cumple la gramática")
    print("3. Análisis semántico:  correcto, cumple las reglas del lenguaje")
    print(f"4. Generación:          {len(r['comandos'])} comandos")
    print()
    for comando in r["comandos"]:
        print("   " + comando)
    ruta = guardar_comandos(ruta_programa, r["comandos"])
    print()
    print(f"Comandos guardados en: comandos/{os.path.basename(ruta)}")

    if "--ejecutar" in sys.argv:
        print()
        ejecutor.ejecutar(r["comandos"])


if __name__ == "__main__":
    main()
