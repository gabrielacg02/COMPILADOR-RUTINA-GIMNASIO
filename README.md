# FitLang · Compilador para rutinas de gimnasio

Proyecto de Compiladores **"Mi lenguaje, mi compilador"** · Ingeniería de Sistemas · Fundación Universitaria Claretiana

- **Tema asignado:** Rutina de gimnasio
- **Integrantes:** Gabriela Córdoba González, Yoisi Yarlenis Palacios Moreno y Juan Esteban Rada Salcedo
- **Docente:** Hasler Gamboa

FitLang es un lenguaje pequeño para escribir rutinas de gimnasio como si fueran programas. El compilador revisa la rutina en cuatro fases (léxico, sintáctico, semántico y generación) y, si está bien, la convierte en una lista de comandos que un programa pequeño ejecuta paso a paso, como lo diría un entrenador.

Así se ve un programa en FitLang (`programas/rutina1.fit`):

```
# Rutina 1: brazos y abdomen para principiantes
series = 3
calentar 5
repetir series veces
    hacer flexiones 10
    hacer abdominales 15
    descansar 45
fin
trotar 10
```

---

## 1. Qué se necesita

- **Python 3** (versión 3.8 o más nueva). No hay que instalar ninguna librería: el compilador solo usa lo que trae Python.
- Para comprobar que está instalado, abra una terminal y escriba `python --version`. Si dice que no lo encuentra, pruebe con `py --version`; si así funciona, use `py` en lugar de `python` en todos los comandos de este archivo.

## 2. Cómo descargarlo

**Opción A (sin Git):** en esta página, botón verde **Code → Download ZIP**, y descomprimir el ZIP.

**Opción B (con Git):**

```
git clone https://github.com/gabrielacg02/COMPILADOR-RUTINA-GIMNASIO.git
```

Después, abrir una terminal **dentro de la carpeta del proyecto** (la que tiene `fitlang.py`). Todos los comandos de este archivo se escriben desde ahí.

## 3. Inicio rápido

**Compilar y ejecutar una rutina:**

```
python fitlang.py programas/rutina1.fit --ejecutar
```

Muestra el resultado de las cuatro fases, la lista de comandos generados y la rutina ejecutada paso a paso con un resumen al final.

**Correr todas las pruebas:**

```
python pruebas.py
```

Pasa los 14 programas de la carpeta `programas/` por el compilador y al final debe decir **"14 de 14 pruebas dieron lo esperado"**. Los resultados se guardan en `resultados_actividad7/` y los comandos de los programas correctos en `comandos/`.

## 4. Todos los comandos

### El compilador completo

| Comando | Qué hace |
|---|---|
| `python fitlang.py programas/rutina1.fit` | Pasa el programa por las cuatro fases, muestra los comandos y los guarda en `comandos/rutina1.txt` |
| `python fitlang.py programas/rutina1.fit --ejecutar` | Lo mismo, y además ejecuta la rutina paso a paso |
| `python fitlang.py programas/rutina1.fit --tokens` | Además muestra la tabla de tokens del léxico |
| `python fitlang.py programas/rutina1.fit --arbol` | Además muestra el árbol sintáctico |
| `python pruebas.py` | Corre los 14 programas de prueba y guarda los resultados |

Las opciones se pueden combinar, por ejemplo: `python fitlang.py programas/rutina2.fit --arbol --ejecutar`.

### Cada fase por separado

Cada archivo del compilador también se puede correr solo, para ver qué hace esa fase:

| Comando | Qué muestra |
|---|---|
| `python lexico.py programas/rutina1.fit` | La tabla de tokens (línea, columna, tipo y texto), o el error léxico |
| `python sintactico.py programas/rutina1.fit` | Si la estructura cumple la gramática, o el error sintáctico |
| `python sintactico.py programas/rutina1.fit --arbol` | Además, el árbol del programa |
| `python tabla_simbolos.py` | Una prueba corta de la tabla de variables |
| `python semantico.py programas/rutina1.fit` | Si cumple las reglas del lenguaje y la tabla de variables, o los errores semánticos |
| `python generador.py programas/rutina1.fit` | La lista de comandos generados |
| `python ejecutor.py comandos/rutina1.txt` | Ejecuta un archivo de comandos ya generado |
| `python ejecutor.py comandos/rutina1.txt --lento` | Lo mismo, con un paso cada medio segundo |

## 5. Qué se ve en pantalla

### Un programa correcto

`python fitlang.py programas/rutina2.fit --ejecutar` (salida resumida):

```
1. Análisis léxico:     correcto (71 tokens)
2. Análisis sintáctico: correcto, cumple la gramática
3. Análisis semántico:  correcto, cumple las reglas del lenguaje
4. Generación:          14 comandos

   CALENTAR 8
   HACER SENTADILLAS 15
   HACER ZANCADAS 13
   DESCANSAR 60
   ...
   MOSTRAR 60

Comandos guardados en: comandos/rutina2.txt

=== Empieza la rutina ===
Paso 1: Calienta 8 minutos
Paso 2: Haz 15 sentadillas
Paso 3: Haz 13 zancadas
Paso 4: Descansa 60 segundos
...
Paso 14: Resultado: 60
=== Rutina terminada ===

Resumen:
  Calentamiento: 8 minutos
  Sentadillas: 60 en total
  Zancadas: 52 en total
  Descanso: 240 segundos
  Trote: 0 minutos
```

### Un programa con error

Cada error dice en qué fase pasó, qué pasó y dónde (línea y columna; en las reglas semánticas, la línea y la regla que se rompió):

```
> python fitlang.py programas/error_lexico.fit
ERROR LÉXICO
Línea 3, columna 10: símbolo ';' no reconocido

> python fitlang.py programas/error_sintactico2.fit
ERROR SINTÁCTICO
Línea 4, columna 13: se esperaba 'entonces', pero llegó un salto de línea

> python fitlang.py programas/error_regla1.fit
ERROR SEMÁNTICO
Línea 4: se rompió la regla R1 (repetir debe ser mayor que 0): aquí se pide repetir -2 veces
```

Las líneas y las columnas se cuentan desde 1. Las columnas cuentan cada carácter de la línea tal como está en el archivo, incluidos los espacios de sangría.

**Nota:** en la ventana de Windows PowerShell las tildes pueden verse mal (por ejemplo "lúxico" en vez de "léxico"). Es la forma en que esa ventana muestra las letras con tilde, no un error del compilador. En la terminal de Visual Studio Code se ven bien.

## 6. Probar un programa propio

1. Crear un archivo de texto dentro de `programas/`, por ejemplo `programas/mi_rutina.fit`.
2. Escribir la rutina con las instrucciones de la sección 7.
3. Correr:

```
python fitlang.py programas/mi_rutina.fit --ejecutar
```

## 7. El lenguaje FitLang

### Instrucciones del gimnasio

| Instrucción | Cómo se escribe | Qué hace |
|---|---|---|
| calentar | `calentar 5` | Calentar esa cantidad de minutos |
| hacer | `hacer flexiones 10` | Hacer un ejercicio con esa cantidad de repeticiones |
| descansar | `descansar 45` | Descansar esa cantidad de segundos |
| trotar | `trotar 10` | Trotar esa cantidad de minutos |
| mostrar | `mostrar total` | Mostrar en pantalla el resultado de una cuenta |

Los ejercicios que acepta `hacer` son: **flexiones, sentadillas, abdominales, burpees y zancadas**.

### Variables, cuentas, repetición y condición

| Qué | Cómo se escribe |
|---|---|
| Variable | `series = 3` |
| Cuentas | `+`, `-` y `*`; la multiplicación se hace primero: `base + serie * 2` |
| Comparaciones | `>`, `<` y `==`; solo dentro de un `si` |
| Repetición | `repetir series veces` ... `fin` |
| Condición | `si nivel > 2 entonces` ... `sino` ... `fin` (el `sino` es opcional) |
| Comentario | `# texto` (el compilador lo ignora) |

Donde va una cantidad se puede poner un número, una variable o una cuenta, por ejemplo `hacer zancadas reps - 2`.

### Reglas de escritura

- Una instrucción por línea, sin punto y coma.
- Todo en minúscula y sin tildes.
- Solo números enteros.
- Cada `repetir` y cada `si` se cierran con su propio `fin`.
- Los únicos símbolos válidos son `=  +  -  *  >  <  ==` y `#`.

### Reglas de sentido (las revisa el semántico)

| Regla | Qué revisa |
|---|---|
| Variables | Toda variable tiene que crearse antes de usarse |
| R1 | `repetir` tiene que ser mayor que 0 |
| R2 | Las repeticiones de `hacer` tienen que ser mayores que 0 |
| R3 | `descansar` tiene que estar entre 10 y 300 segundos |

Las reglas se revisan con el valor calculado, no con lo que está escrito: `repetir series - 5 veces` con `series = 3` rompe la R1 porque da -2.

## 8. Cómo está hecho el compilador

```
programa .fit → léxico → sintáctico → semántico → generador → lista de comandos → ejecutor
```

| Archivo | Fase | Qué hace | Quién lo hizo |
|---|---|---|---|
| `lexico.py` | 1. Léxico | Lee el programa carácter por carácter y lo separa en tokens, con su línea y columna. Avisa si hay un símbolo que no existe | Gabriela |
| `gramatica.txt` | — | Las reglas del lenguaje (la gramática), sin recursividad izquierda | Juan Esteban |
| `sintactico.py` | 2. Sintáctico | Analizador descendente recursivo: revisa con la gramática que los tokens estén en orden y arma el árbol del programa | Yoisi |
| `tabla_simbolos.py` | 3. Semántico | La tabla de variables: guarda cada variable con su valor y avisa si se usa una que no existe | Yoisi |
| `semantico.py` | 3. Semántico | Recorre el árbol calculando los valores y revisa las reglas R1, R2 y R3. Avisa todos los errores, no solo el primero | Gabriela |
| `generador.py` | 4. Generación | Convierte la rutina en una lista de comandos (`CALENTAR 5`, `HACER FLEXIONES 10`...) | Gabriela |
| `ejecutor.py` | Ejecución | Lee la lista de comandos y muestra la rutina paso a paso, con un resumen | Juan Esteban |
| `fitlang.py` | — | Programa principal: une las cuatro fases y el ejecutor | Juan Esteban (Act. 5) y Gabriela (Act. 7) |
| `pruebas.py` | — | Corre los 14 programas de prueba y guarda los resultados | Juan Esteban (Act. 5) y Gabriela (Act. 7) |

El léxico y el sintáctico se detienen en el primer error, porque sin tokens o sin árbol no se puede seguir. El semántico revisa todo el programa y muestra todos los errores que encuentra.

## 9. Programas de prueba

Todos están en la carpeta `programas/`.

| Programa | Qué tiene | Resultado esperado |
|---|---|---|
| `rutina1.fit` | Brazos y abdomen para principiantes | Correcto (11 comandos) |
| `rutina2.fit` | Piernas según el nivel (usa `si`) | Correcto (14 comandos) |
| `rutina3.fit` | Circuito por rondas (repetir dentro de repetir) | Correcto (23 comandos) |
| `rutina4.fit` | Cuerpo completo que sube de dificultad | Correcto (11 comandos) |
| `rutina5.fit` | Descanso que baja en cada serie | Correcto (12 comandos) |
| `error_lexico.fit` | Un `;` | Error léxico, línea 3, columna 10 |
| `error_lexico2.fit` | Un `%` | Error léxico, línea 3, columna 16 |
| `error_sintactico.fit` | Un `repetir` sin `fin` | Error sintáctico, línea 7, columna 10 (final del archivo) |
| `error_sintactico2.fit` | Un `si` sin `entonces` | Error sintáctico, línea 4, columna 13 |
| `error_semantico.fit` | Usa la variable `repeticiones`, que no existe | Error semántico, línea 5, columna 21 |
| `error_variable2.fit` | Usa la variable `experiencia`, que no existe | Error semántico, línea 4, columna 4 |
| `error_regla1.fit` | `repetir series - 5 veces` con `series = 3` | Error semántico, regla R1 |
| `error_regla2.fit` | `hacer abdominales reps - 12` con `reps = 12` | Error semántico, regla R2 |
| `error_regla3.fit` | `descansar 600` | Error semántico, regla R3 |

## 10. Qué hay en cada carpeta y archivo

| Carpeta o archivo | Qué tiene |
|---|---|
| `programas/` | Los 14 programas de prueba en FitLang |
| `resultados/` | Resultados de las pruebas de la Actividad 5 (solo léxico y sintáctico, 9 programas) |
| `resultados_actividad7/` | Resultados de las pruebas del compilador completo (14 programas): un archivo por programa y `resumen.txt` |
| `comandos/` | Los comandos generados para los 5 programas correctos |
| `Capturas pruebas/` | Documentos con las capturas de las pruebas que hizo cada integrante en su computador (Actividades 5 y 7) |
| `Actividad 3 - FitLang.docx` | El diseño del lenguaje (Actividad 3) |
| `gramatica.txt` | La gramática del lenguaje |
| `bitacora.md` | Lo que decidimos como grupo en cada actividad, quién hizo qué y el uso de IA |
| `media pagina.md` | Lo más difícil del proyecto y las decisiones que tomamos |
