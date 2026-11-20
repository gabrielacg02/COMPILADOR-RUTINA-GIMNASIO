# ------------------------------------------------------------
# Pruebas del compilador de FitLang (Actividad 7: compilador completo)
#
# Pasa los 14 programas de la carpeta programas/ por las cuatro fases
# y guarda el resultado de cada uno en la carpeta resultados_actividad7/.
# A los programas correctos además les guarda sus comandos en comandos/.
# Al final compara lo que salió con lo que esperábamos.
#
# Uso:   python pruebas.py
# ------------------------------------------------------------

import os

import sintactico
from fitlang import compilar, guardar_comandos

CARPETA = os.path.dirname(os.path.abspath(__file__))
PROGRAMAS = os.path.join(CARPETA, "programas")
RESULTADOS = os.path.join(CARPETA, "resultados_actividad7")

# Programa -> lo que esperamos que pase con el compilador completo
ESPERADO = {
    # Actividad 3
    "rutina1.fit": "correcto",
    "rutina2.fit": "correcto",
    "rutina3.fit": "correcto",
    "error_lexico.fit": "léxico",
    "error_sintactico.fit": "sintáctico",
    "error_semantico.fit": "semántico",      # ahora sí se detecta: la variable no existe
    # Actividad 5
    "error_lexico2.fit": "léxico",
    "error_sintactico2.fit": "sintáctico",
    "rutina4.fit": "correcto",
    # Actividad 7
    "error_variable2.fit": "semántico",      # Yoisi: variable que no existe en un si
    "error_regla1.fit": "semántico",         # Gabriela: rompe la regla R1
    "error_regla2.fit": "semántico",         # Gabriela: rompe la regla R2
    "error_regla3.fit": "semántico",         # Gabriela: rompe la regla R3
    "rutina5.fit": "correcto",               # Juan Esteban
}


def numerar(texto):
    """Devuelve el programa con el número de cada línea a la izquierda."""
    lineas = texto.rstrip("\n").split("\n")
    return "\n".join(f"{n:>3} | {linea}" for n, linea in enumerate(lineas, start=1))


def main():
    os.makedirs(RESULTADOS, exist_ok=True)
    resumen = ["RESUMEN DE PRUEBAS - FitLang, Actividad 7 (compilador completo)", ""]
    bien = 0

    for nombre, esperado in ESPERADO.items():
        with open(os.path.join(PROGRAMAS, nombre), encoding="utf-8") as f:
            texto = f.read()

        r = compilar(texto)
        obtenido = r["fase"] if r["error"] else "correcto"
        coincide = obtenido == esperado
        if coincide:
            bien += 1

        # Archivo con el detalle de esta prueba
        detalle = [f"PROGRAMA: {nombre}", "", numerar(texto), ""]
        if r["error"]:
            detalle += [f"RESULTADO: error {r['fase']}", r["error"]]
        else:
            ruta = guardar_comandos(nombre, r["comandos"])
            detalle += ["RESULTADO: correcto, pasa las cuatro fases", "",
                        "VARIABLES (tabla de símbolos):", r["tabla"].como_texto(), "",
                        f"COMANDOS GENERADOS ({len(r['comandos'])}), guardados en comandos/{os.path.basename(ruta)}:"]
            detalle += ["  " + c for c in r["comandos"]]
        if r["arbol"]:
            detalle += ["", "ÁRBOL SINTÁCTICO:", "programa"] + sintactico.texto_arbol(r["arbol"]["instrucciones"])
        with open(os.path.join(RESULTADOS, nombre.replace(".fit", ".txt")), "w", encoding="utf-8") as f:
            f.write("\n".join(detalle) + "\n")

        # Líneas del resumen
        resumen.append(f"[{'OK' if coincide else 'FALLA'}] {nombre}")
        resumen.append(f"     esperado: {esperado}  |  obtenido: {obtenido}")
        if r["error"]:
            for linea in r["error"].split("\n"):
                resumen.append(f"     {linea}")
        else:
            resumen.append(f"     correcto: {len(r['comandos'])} comandos generados")

    resumen += ["", f"{bien} de {len(ESPERADO)} pruebas dieron lo esperado."]
    with open(os.path.join(RESULTADOS, "resumen.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(resumen) + "\n")
    print("\n".join(resumen))
    print()
    print("Los resultados quedaron en la carpeta 'resultados_actividad7' y los comandos en la carpeta 'comandos'.")


if __name__ == "__main__":
    main()
