# Lo más difícil y las decisiones que tomamos

**Proyecto FitLang · Actividad 7 · Gabriela Córdoba González, Yoisi Yarlenis Palacios Moreno y Juan Esteban Rada Salcedo**

Lo más difícil de todo el proyecto fue que cada parte del compilador depende de la anterior, así que no podíamos trabajar cada uno por su lado sin ponernos de acuerdo primero. Desde la Actividad 5 decidimos los nombres de los tokens entre los tres, y en esta actividad tuvimos que acordar cómo se veía el árbol y cómo se escribían los comandos (`HACER FLEXIONES 10`) antes de programar. Cuando no lo hicimos así, las piezas no encajaban.

**Yoisi (árbol y tabla de variables).** Lo más difícil fue cambiar el sintáctico para que, además de revisar, armara el árbol, sin dañar lo que ya funcionaba en la Actividad 5. Decidimos que cada función devuelva un nodo con lo que encontró, y que cada variable guarde su línea y su columna, para que después se pueda decir exactamente dónde se usó una que no existe. Para la tabla de variables decidimos guardar el valor y la línea donde se creó cada una, como una libreta.

**Gabriela (reglas, generador y unión de todo).** Lo más difícil fue que las reglas no se pueden revisar mirando solo el texto: en `repetir series - 5 veces` hay que saber cuánto vale `series` para darse cuenta de que da -2. Por eso decidimos que el semántico recorra el programa como si lo ejecutara, calculando los valores con la tabla de variables. También decidimos que no se detenga en el primer error, sino que avise todos, como vimos en clase. Las reglas las escogimos pensando en un gimnasio real, no tiene sentido repetir 0 veces, hacer 0 repeticiones ni descansar 10 minutos entre series.

**Juan Esteban (ejecutor).** Lo más difícil fue decidir cómo mostrar la rutina para que se entendiera como la diría un entrenador y no como una lista de código. Decidimos que el ejecutor solo lea comandos sencillos, uno por línea, sin variables ni bloques, porque el generador ya los deja listos. Así el ejecutor queda separado del compilador y se puede probar solo con un archivo de comandos. También agregamos un resumen al final con el total de cada ejercicio y el tiempo de descanso.

Al final, la decisión que más nos ayudó fue probar siempre con los mismos programas desde la Actividad 3 y agregar programas nuevos en cada actividad, así cada vez que cambiábamos algo sabíamos enseguida si se había dañado otra cosa.
