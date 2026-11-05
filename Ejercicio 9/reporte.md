# Ejercicio 9 — Encadenamiento en la biblioteca

El programa revisa quién puede entrar de noche a la biblioteca usando los
hechos y las reglas del ejercicio. Con la base original, los dos métodos
prueban el acceso de Ana y Marta, pero no el de Luis. A Luis le falta la
credencial y tampoco hay un hecho que diga que es profesor. Que no se pueda
probar su acceso significa que no alcanza la información de esta base.

**¿Por qué aparece Becario(Ana) hacia adelante y no hacia atrás?**

Hacia adelante se aplica todo lo que se pueda deducir, aunque no haga falta
para responder la pregunta. Como Ana es estudiante y tiene credencial,
también sale que es becaria. En la primera ronda aparecen `Miembro(Ana)`,
`Miembro(Marta)` y `Becario(Ana)`. Hasta la segunda se usan los miembros nuevos
para obtener `AccesoNoche(Ana)` y `AccesoNoche(Marta)`.

Hacia atrás va directo a lo que necesita comprobar. Para el acceso de Ana
busca que sea miembro y que haya horario nocturno. Ser becaria no es un
requisito para entrar, así que ni intenta esa regla.

**¿Por qué intenta la regla de estudiante con Marta si es profesora?**

Porque las reglas se revisan en el orden de la base. La primera que puede
concluir `Miembro(Marta)` es `R_miembro_est`, así que la intenta. Falla al
buscar `Estudiante(Marta)` y pasa a `R_miembro_prof`. Ahí sí encuentra
`Profesor(Marta)` y puede seguir hasta probar el acceso. El programa no
escoge de antemano la regla que sabe que va a funcionar.

**¿Qué cambia si Luis tiene credencial?**

El programa también corre ese caso, separado de la base original. Al agregar
`TieneCredencial(Luis)`, hacia adelante aparecen tres conclusiones adicionales:
`Miembro(Luis)`, `Becario(Luis)` y `AccesoNoche(Luis)`. Su acceso queda probado
con ambos métodos. Hacia atrás usa que Luis es estudiante y tiene credencial,
y después comprueba el horario nocturno; no necesita deducir que es becario.
Las trazas completas de las ejecuciones están en `evidencia.txt`.
