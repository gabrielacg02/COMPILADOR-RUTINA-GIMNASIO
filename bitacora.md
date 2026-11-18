# Bitácora del grupo · FitLang

**Proyecto:** Mi lenguaje, mi compilador (Compiladores)
**Tema asignado:** Rutina de gimnasio
**Integrantes:** Gabriela Córdoba González, Yoisi Yarlenis Palacios Moreno, Juan Esteban Rada Salcedo
**Docente:** Hasler Gamboa

En este archivo vamos anotando lo que decidimos como grupo, por qué lo decidimos, quién hizo qué y si usamos IA.


## Actividad 3 · Conceptualización básica
### Qué decidimos y por qué

- **Nombre del lenguaje: FitLang.** Es corto y se relaciona con el gimnasio. Los programas se guardan con la extensión `.fit`.
- **Palabras en español y en minúscula.** Queríamos que cualquier persona del gimnasio pudiera leer una rutina aunque no sepa programar.
- **Cinco instrucciones propias del tema:** `calentar`, `hacer`, `descansar`, `trotar` y `mostrar`. Las cuatro primeras son las partes de una rutina real: calentar, hacer el ejercicio, descansar y hacer cardio. `mostrar` la agregamos para ver en pantalla el resultado de una cuenta, como el total de repeticiones. El enunciado pedía mínimo tres.
- **Los ejercicios son palabras del lenguaje:** flexiones, sentadillas, abdominales, burpees y zancadas. Así el compilador puede avisar si alguien escribe un ejercicio que no existe.
- **Unidades:** minutos para `calentar` y `trotar`, segundos para `descansar` y repeticiones para `hacer`, que es como se maneja en el gimnasio.
- **Solo números enteros.** Repeticiones, minutos y segundos no llevan decimales.
- **Una instrucción por línea y sin punto y coma.** El salto de línea separa una instrucción de otra. Por eso el `;` lo usamos como ejemplo de error léxico.
- **Repetición y condición con `fin`:** `repetir ... veces ... fin` y `si ... entonces ... sino ... fin`, como el ejemplo del enunciado. El `sino` se puede quitar.
- **Operaciones `+`, `-`, `*` y comparaciones `>`, `<`, `==`.** La multiplicación se hace primero, como en matemáticas. Las comparaciones solo van dentro de un `si`.
- **Comentarios con `#`**, para poner notas en las rutinas.
- **Cómo contar líneas y columnas:** las dos empiezan en 1 y las columnas cuentan los espacios. Lo decidimos para que los mensajes de error coincidan con lo que se ve en el archivo.
- **Resultado del compilador:** una lista de comandos como `CALENTAR 5` o `HACER FLEXIONES 10`, que un programa pequeño va mostrando paso a paso. Nos pareció más fácil de explicar que traducir a Python.
- **Los seis programas:** tres correctos (brazos y abdomen, piernas según el nivel y un circuito por rondas) y tres con un error a propósito: un `;` (léxico), un `repetir` sin `fin` (sintáctico) y una variable que nunca se creó (semántico).

### Quién hizo qué

| Integrante | Qué hizo |
|---|---|
| Gabriela | Subió el documento de la Actividad 3, los programas `rutina1.fit` y `rutina2.fit`, y esta bitácora |
| Yoisi | Subió los programas `rutina3.fit` y `error_lexico.fit` |
| Juan Esteban | Subió los programas `error_sintactico.fit` y `error_semantico.fit` |

Las instrucciones y los programas los decidimos entre los tres antes de repartir quién subía cada cosa.

### Retroalimentación del profesor y qué corregimos

El profesor revisó la Actividad 3 y nos pidió:
1. Subir los seis programas como archivos `.fit` y no solo dentro del Word, porque se usan en la Actividad 5. **Hecho:** quedaron en la carpeta `programas/`.
2. Agregar esta bitácora al repositorio. **Hecho.**
3. Que Yoisi y Juan Esteban hicieran sus propios commits y que fuéramos subiendo a medida que avanzamos. **Hecho:** cada uno subió sus dos programas desde su cuenta, y de aquí en adelante vamos a subir por partes.


   ## Actividad 5 · Análisis léxico y sintáctico

### Qué decidimos y por qué

- **Programamos el compilador en Python 3**, sin instalar librerías extra. Es el lenguaje que más manejamos los tres y se puede correr en cualquier computador. Cada uno lo trabajó en Visual Studio Code.
- **Primero nos pusimos de acuerdo en los nombres de los tokens** (`CALENTAR`, `HACER`, `EJERCICIO`, `IDENTIFICADOR`, `NUMERO`, `ASIGNACION`, `MAS`, `MENOS`, `POR`, `MAYOR`, `MENOR`, `IGUAL_IGUAL`, `SALTO`, `FIN_ARCHIVO`...), porque el léxico los produce, el sintáctico los recibe y la gramática los nombra. Si cada uno les ponía un nombre distinto, las partes no iban a encajar.
- **Trabajamos en orden:** primero el léxico, porque el sintáctico lo necesita para funcionar; la gramática se hizo al mismo tiempo, porque no depende del código; y las pruebas al final, cuando ya estaban las dos fases.
- **El léxico lee el programa carácter por carácter** y lleva la cuenta de la línea y la columna. Las dos empiezan en 1 y las columnas cuentan los espacios, como decidimos en la Actividad 3.
- **El salto de línea es un token (`SALTO`)**, porque en FitLang va una instrucción por línea y el sintáctico necesita saber dónde termina cada una. Los espacios y la sangría no son tokens.
- **Los ejercicios se reconocen en el léxico** (token `EJERCICIO`). Así el sintáctico puede avisar "se esperaba un ejercicio" si alguien escribe `hacer pesas 10`.
- **Una mayúscula, una tilde o un símbolo como `;`, `%` o `@` es error léxico.** El léxico se detiene en el primer error, porque sin la lista completa de tokens no se puede seguir.
- **La gramática no tiene recursividad izquierda.** Las cuentas se escriben con la forma "locomotora y vagones" de la clase (`Expr → Termino RestoExpr`), porque `Expr → Expr + Termino` haría que el analizador descendente se quedara dando vueltas sin leer nada.
- **La multiplicación va más abajo en la gramática que la suma y la resta**, para que se haga primero: `2 + 3 * 4` da 14.
- **El sintáctico es descendente recursivo:** una función por cada regla de la gramática, como lo vimos en clase. Encima de cada función está la regla que revisa (R1, R2...), y cada `RestoExpr` y `RestoTermino` se programó con un `while`.
- **Los errores dicen qué pasó, la línea y la columna**, por ejemplo «Línea 4, columna 13: se esperaba 'entonces', pero llegó un salto de línea». El sintáctico también se detiene en el primer error. Cuando falta un `fin`, el error se marca justo después de la última instrucción del archivo y dice en qué línea se abrió el bloque, así coincide con lo que explicamos en la Actividad 3 (línea 7, columna 10).
- **`descansar -30` es error de sintaxis**, porque FitLang no tiene números negativos escritos directamente. Que una cuenta dé negativo (como `series - 5`) lo va a revisar el semántico en la Actividad 7.
- **Los tres programas nuevos:** `error_lexico2.fit` (un `%` en la línea 3, columna 16), `error_sintactico2.fit` (un `si` sin `entonces` en la línea 4) y `rutina4.fit` (correcto, con un `si` dentro de un `repetir` y una cuenta para probar la precedencia).
- **Pruebas:** `pruebas.py` pasa los 9 programas por el compilador, compara lo que salió con lo que esperábamos y guarda un archivo por programa en la carpeta `resultados/`, más un `resumen.txt`. Las 9 pruebas dieron lo esperado. `error_semantico.fit` pasa estas dos fases, y así debe ser: está bien escrito y bien armado, y su error (usar una variable que no existe) se detecta en la Actividad 7.
- **Formato de los archivos:** Gabriela quitó los comentarios de "Hecho por" de los archivos para dejarlos todos con el mismo formato. La autoría de cada parte queda en los commits de cada uno.


