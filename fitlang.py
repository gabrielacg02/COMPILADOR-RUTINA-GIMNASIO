# ------------------------------------------------------------
# Compilador de FitLang - programa principal
# Hecho por: Juan Esteban Rada Salcedo
#
# Une las dos fases de la Actividad 5: primero el léxico (lexico.py)
# y después el sintáctico (sintactico.py).
#
# Uso:
#   python fitlang.py programas/rutina1.fit            revisa el programa
#   python fitlang.py programas/rutina1.fit --tokens   además muestra los tokens
# ------------------------------------------------------------

import sys

import lexico
import sintactico


def compilar(texto):
    """
    Pasa el texto por el léxico y por el sintáctico.
    Devuelve (tokens, error, fase): si no hubo error, error y fase quedan en None.
    """
    try:
        tokens = lexico.analizar(texto)
    except lexico.ErrorLexico as e:
        return None, str(e), "léxico"

    try:
        sintactico.analizar(tokens)
    except sintactico.ErrorSintactico as e:
        return tokens, str(e), "sintáctico"

    return tokens, None, None


def main():
    if len(sys.argv) < 2:
        print("Uso: python fitlang.py programas/rutina1.fit [--tokens]")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as archivo:
        texto = archivo.read()

    tokens, error, fase = compilar(texto)

    if tokens and "--tokens" in sys.argv:
        print(lexico.tabla_tokens(tokens))
        print()

    if error:
        print(f"ERROR {fase.upper()}")
        print(error)
        sys.exit(1)

    print(f"Análisis léxico: correcto ({len(tokens)} tokens)")
    print("Análisis sintáctico: correcto, el programa cumple la gramática")


if __name__ == "__main__":
    main()
