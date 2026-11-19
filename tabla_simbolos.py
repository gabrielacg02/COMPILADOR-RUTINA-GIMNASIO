# ------------------------------------------------------------
# Tabla de símbolos (tabla de variables) de FitLang
#
# Es la "libreta" del compilador: cada vez que el programa crea o
# cambia una variable (series = 3), aquí se anota su nombre, su valor
# y la línea donde se definió por primera vez.
#
# Cuando el programa USA una variable (repetir series veces), se busca
# en la libreta. Si no está, es porque nunca se creó, y se avisa el
# error con la línea y la columna donde se intentó usar.
# ------------------------------------------------------------


class VariableNoDefinida(Exception):
    pass


class TablaSimbolos:

    def __init__(self):
        # nombre de la variable -> {"valor": ..., "linea": ...}
        self.variables = {}

    def definir(self, nombre, valor, linea):
        """Anota una variable nueva, o le cambia el valor si ya existía."""
        if nombre in self.variables:
            self.variables[nombre]["valor"] = valor
        else:
            self.variables[nombre] = {"valor": valor, "linea": linea}

    def existe(self, nombre):
        return nombre in self.variables

    def usar(self, nombre, linea, columna):
        """
        Devuelve el valor de una variable.
        Si nunca se creó, lanza VariableNoDefinida con la línea y la columna.
        """
        if nombre not in self.variables:
            raise VariableNoDefinida(
                f"Línea {linea}, columna {columna}: la variable '{nombre}' "
                f"se usa pero nunca se creó")
        return self.variables[nombre]["valor"]

    def como_texto(self):
        """La tabla en columnas, para mostrarla en pantalla o en los resultados."""
        if not self.variables:
            return "(el programa no usa variables)"
        filas = [f"{'VARIABLE':<12}{'VALOR FINAL':<14}DEFINIDA EN LA LÍNEA"]
        for nombre, datos in self.variables.items():
            filas.append(f"{nombre:<12}{str(datos['valor']):<14}{datos['linea']}")
        return "\n".join(filas)


# Prueba rápida de la tabla sola:   python tabla_simbolos.py
if __name__ == "__main__":
    tabla = TablaSimbolos()
    tabla.definir("series", 3, 2)
    tabla.definir("reps", 10, 3)
    tabla.definir("reps", 15, 6)          # cambia el valor, la línea sigue siendo 3
    print(tabla.como_texto())
    print()
    print("Valor de series:", tabla.usar("series", 4, 9))
    try:
        tabla.usar("rondas", 5, 9)
    except VariableNoDefinida as e:
        print("Error esperado ->", e)
