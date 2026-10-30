# Ejercicio 8 — Q-learning

La idea del ejercicio es que el agente aprenda a llegar a la meta sin caerse
al acantilado. El mapa tiene 4 filas y 12 columnas: empieza abajo a la
izquierda y la meta está abajo a la derecha.

El programa entrena durante 500 episodios con α = 0.5, γ = 1 y ε = 0.1.
La tabla Q empieza en ceros y la semilla es 1 para poder repetir el resultado.
Si hay empate entre acciones, se toma la primera en el orden N, E, S, W.
Cada episodio tiene un límite de 200 pasos para que no se quede dando vueltas.

Al probar lo aprendido sin movimientos al azar, el agente sube una casilla,
avanza once a la derecha y baja a la meta. En total son **13 pasos y una
recompensa de −13**. El camino sale en la terminal y las recompensas de los
500 episodios quedan en `recompensas.csv`. En esta corrida hubo tres episodios
que llegaron al límite de pasos.

**¿Por qué el camino de 13 pasos es el mejor?**

Porque es el más corto que evita el acantilado. Hay que avanzar once columnas,
pero no se puede ir directo por abajo sin caer. Entonces toca subir, cruzar
por la fila de arriba del acantilado y bajar al final. Son 11 + 1 + 1 = 13
pasos. Cada paso vale −1, incluso el de llegar a la meta. Dar más vueltas
solo suma más penalizaciones y caer cuesta −100.

**¿Por qué en el entrenamiento la recompensa puede ser peor que −13?**

Porque mientras entrena todavía prueba movimientos al azar el 10 % de las
veces. Aunque ya tenga aprendido el camino, uno de esos movimientos puede
hacer que se desvíe o se caiga. Por eso no todos los episodios salen igual
de bien. En la evaluación ya no explora: elige siempre la acción con mayor
valor Q, y ahí sí logra los 13 pasos.

**¿Qué pasa con la actualización de Q cuando se cae?**

El siguiente estado es el inicio, S = (3, 0). Caerse le cuesta −100, pero
no acaba el episodio: vuelve al inicio y sigue intentando. Entonces el
objetivo para actualizar Q es `−100 + γ × max Q(S, acción)`. Se toma el
mejor valor Q del inicio porque desde ahí todavía tiene que seguir jugando.
El valor futuro solo se pone en cero cuando llega a la meta, porque ahí
sí termina el episodio.
