# Bitácora del grupo · FitLang

**Proyecto:** Mi lenguaje, mi compilador (Compiladores)
**Tema asignado:** Rutina de gimnasio
**Integrantes:** Gabriela Córdoba González, Yoisi Yarlenis Palacios Moreno, Juan Esteban Rada Salcedo
**Docente:** Hasler Gamboa

En este archivo vamos anotando lo que decidimos como grupo, por qué lo decidimos, quién hizo qué y si usamos IA.

---

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


