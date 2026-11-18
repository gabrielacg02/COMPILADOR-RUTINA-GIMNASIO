import sys

# Palabras reservadas. El tipo del token es la misma palabra en mayúscula.
PALABRAS_CLAVE = [
    "calentar", "hacer", "descansar", "trotar", "mostrar",
    "repetir", "veces", "si", "entonces", "sino", "fin",
]

# Ejercicios que acepta la instrucción "hacer"
EJERCICIOS = ["flexiones", "sentadillas", "abdominales", "burpees", "zancadas"]

# Símbolos de un solo carácter (el "=" se revisa aparte porque puede ser "==")
SIMBOLOS = {
    "+": "MAS",
    "-": "MENOS",
    "*": "POR",
    ">": "MAYOR",
    "<": "MENOR",
}


class Token:
    """Un pedacito del programa: qué tipo es, qué decía y dónde estaba."""

    def __init__(self, tipo, texto, linea, columna):
        self.tipo = tipo
        self.texto = texto
        self.linea = linea
        self.columna = columna


class ErrorLexico(Exception):
    pass


def es_letra(c):
    return "a" <= c <= "z" or c == "_"


def analizar(codigo):
    """Recibe el texto del programa y devuelve la lista de tokens."""
    tokens = []
    i = 0            # posición dentro del texto
    linea = 1
    columna = 1
    # Dónde termina el último token "de verdad". Sirve para decir dónde
    # quedó el final del programa si al sintáctico le falta algo al final.
    fin_linea, fin_columna = 1, 1

    while i < len(codigo):
        c = codigo[i]

        # Salto de línea: separa una instrucción de otra, por eso es un token
        if c == "\n":
            tokens.append(Token("SALTO", "\\n", linea, columna))
            i += 1
            linea += 1
            columna = 1
            continue

        # Espacios y tabulaciones: no son tokens, solo se avanza
        if c in " \t\r":
            i += 1
            columna += 1
            continue

        # Comentario: desde el # hasta el final de la línea se ignora
        if c == "#":
            while i < len(codigo) and codigo[i] != "\n":
                i += 1
                columna += 1
            continue

        # Número: se juntan todos los dígitos seguidos
        if c.isdigit():
            inicio = columna
            numero = ""
            while i < len(codigo) and codigo[i].isdigit():
                numero += codigo[i]
                i += 1
                columna += 1
            tokens.append(Token("NUMERO", numero, linea, inicio))
            fin_linea, fin_columna = linea, columna
            continue

        # Palabra: empieza con letra minúscula y sigue con letras, dígitos o _
        if es_letra(c):
            inicio = columna
            palabra = ""
            while i < len(codigo) and (es_letra(codigo[i]) or codigo[i].isdigit()):
                palabra += codigo[i]
                i += 1
                columna += 1
            if palabra in PALABRAS_CLAVE:
                tipo = palabra.upper()          # calentar -> CALENTAR
            elif palabra in EJERCICIOS:
                tipo = "EJERCICIO"
            else:
                tipo = "IDENTIFICADOR"          # nombre de una variable
            tokens.append(Token(tipo, palabra, linea, inicio))
            fin_linea, fin_columna = linea, columna
            continue

        # "=" es asignación y "==" es comparación: hay que mirar el siguiente
        if c == "=":
            if i + 1 < len(codigo) and codigo[i + 1] == "=":
                tokens.append(Token("IGUAL_IGUAL", "==", linea, columna))
                i += 2
                columna += 2
            else:
                tokens.append(Token("ASIGNACION", "=", linea, columna))
                i += 1
                columna += 1
            fin_linea, fin_columna = linea, columna
            continue

        # Los demás símbolos que sí existen
        if c in SIMBOLOS:
            tokens.append(Token(SIMBOLOS[c], c, linea, columna))
            i += 1
            columna += 1
            fin_linea, fin_columna = linea, columna
            continue

        # Si llega aquí, es algo que FitLang no conoce
        if c.isalpha():
            raise ErrorLexico(f"Línea {linea}, columna {columna}: la letra '{c}' no es válida "
                              f"(FitLang se escribe en minúscula y sin tildes)")
        raise ErrorLexico(f"Línea {linea}, columna {columna}: símbolo '{c}' no reconocido")

    # Token final: queda justo después del último token del programa
    tokens.append(Token("FIN_ARCHIVO", "", fin_linea, fin_columna))
    return tokens


def tabla_tokens(tokens):
    """Arma un texto con todos los tokens en columnas, para mostrarlos."""
    filas = [f"{'LÍNEA':<7}{'COLUMNA':<9}{'TIPO':<15}TEXTO"]
    for t in tokens:
        filas.append(f"{t.linea:<7}{t.columna:<9}{t.tipo:<15}{t.texto}")
    return "\n".join(filas)


# Esto solo se ejecuta si se corre este archivo directamente
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python lexico.py programas/rutina1.fit")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as archivo:
        texto = archivo.read()
    try:
        print(tabla_tokens(analizar(texto)))
    except ErrorLexico as e:
        print("ERROR LÉXICO:", e)
