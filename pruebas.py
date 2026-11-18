# ------------------------------------------------------------
# Pruebas del compilador de FitLang
# Hecho por: Juan Esteban Rada Salcedo
#
# Pasa los 9 programas de la carpeta programas/ por el compilador
# y guarda el resultado de cada uno en la carpeta resultados/.
# También compara lo que salió con lo que esperábamos.
#
# Uso:   python pruebas.py
# ------------------------------------------------------------

import os

import lexico
from fitlang import compilar

CARPETA = os.path.dirname(os.path.abspath(__file__))
PROGRAMAS = os.path.join(CARPETA, "programas")
RESULTADOS = os.path.join(CARPETA, "resultados")

# Programa -> lo que esperamos que pase en esta actividad
ESPERADO = {
    # Los seis de la Actividad 3
    "rutina1.fit": "correcto",
    "rutina2.fit": "correcto",
    "rutina3.fit": "correcto",
    "error_lexico.fit": "léxico",
    "error_sintactico.fit": "sintáctico",
    "error_semantico.fit": "correcto",   # su error es semántico: se detecta en la Actividad 7
    # Los tres nuevos de la Actividad 5
    "error_lexico2.fit": "léxico",
    "error_sintactico2.fit": "sintáctico",
    "rutina4.fit": "correcto",
}


def numerar(texto):
    """Devuelve el programa con el número de cada línea a la izquierda."""
    lineas = texto.rstrip("\n").split("\n")
    return "\n".join(f"{n:>3} | {linea}" for n, linea in enumerate(lineas, start=1))


def main():
    os.makedirs(RESULTADOS, exist_ok=True)
    resumen = ["RESUMEN DE PRUEBAS - FitLang, Actividad 5 (léxico y sintáctico)", ""]
    bien = 0

    for nombre, esperado in ESPERADO.items():
        with open(os.path.join(PROGRAMAS, nombre), encoding="utf-8") as f:
            texto = f.read()

        tokens, error, fase = compilar(texto)
        obtenido = fase if error else "correcto"
        coincide = obtenido == esperado
        if coincide:
            bien += 1

        # Archivo con el detalle de esta prueba
        detalle = [f"PROGRAMA: {nombre}", "", numerar(texto), ""]
        if tokens:
            detalle += [f"TOKENS ({len(tokens)}):", lexico.tabla_tokens(tokens), ""]
        if error:
            detalle += [f"RESULTADO: error {fase}", error]
        else:
            detalle += ["RESULTADO: correcto, pasa el análisis léxico y el sintáctico"]
        if nombre == "error_semantico.fit":
            detalle += ["", "NOTA: este programa está bien escrito y bien armado. Su error (usar la",
                        "variable 'repeticiones' que nunca se creó) es semántico: se detecta en la Actividad 7."]
        with open(os.path.join(RESULTADOS, nombre.replace(".fit", ".txt")), "w", encoding="utf-8") as f:
            f.write("\n".join(detalle) + "\n")

        # Línea del resumen
        resumen.append(f"[{'OK' if coincide else 'FALLA'}] {nombre}")
        resumen.append(f"     esperado: {esperado}  |  obtenido: {obtenido}")
        resumen.append(f"     {error if error else 'correcto'}")

    resumen += ["", f"{bien} de {len(ESPERADO)} pruebas dieron lo esperado."]
    with open(os.path.join(RESULTADOS, "resumen.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(resumen) + "\n")
    print("\n".join(resumen))
    print()
    print("Los resultados quedaron guardados en la carpeta 'resultados'.")


if __name__ == "__main__":
    main()
