# Ejercicio 2: rutas con A* en México

David Efrain Chacon Ambrosio

Para este ejercicio adapté el A* del proyecto de Rumania para buscar rutas
en el grafo de las 1,000 ciudades de México. Se puede elegir un origen y un
destino desde la terminal o desde el mapa, y ver el camino y sus kilómetros.

## Cómo probarlo

Para usarlo en la terminal necesitas Python 3.10 o posterior. Abre CMD en
esta carpeta y ejecuta, por ejemplo:

```cmd
python find_route.py --from-city Tijuana --to Cancún
python find_route.py --from-city "Mexico City" --to Monterrey
```

Puedes cambiar las ciudades por otras del grafo. Escribe los nombres con
sus acentos y pon comillas si tienen espacios. En rutas largas se resume
el camino; agrega `--full-path` al comando si quieres ver todas las ciudades.

Si prefieres verlo en el mapa, abre `mexico_map.html` con doble clic o usa:

```cmd
start "" "mexico_map.html"
```

Elige el origen y el destino y pulsa **Calcular ruta**. El camino aparece
en azul y a la izquierda se muestran los kilómetros, los tramos y los nodos
expandidos. Con **Ver camino completo** puedes revisar todas las ciudades
por las que pasa.

No necesitas instalar paquetes ni iniciar un servidor. Mantén los archivos
de esta carpeta juntos para que el programa y el mapa puedan abrirlos.

## Si hay ciudades con el mismo nombre

En el mapa se muestra también el estado para distinguirlas. Si coinciden
el nombre y el estado, aparecen las coordenadas. En la terminal puedes
indicar el estado así:

```cmd
python find_route.py --from-city Puebla --from-state Puebla --to Monterrey
```

Para indicar el estado del destino usa `--to-state`. También puedes usar
el id que muestra el programa si todavía hay varias opciones.

El reporte y las cuatro capturas están en [Reporte.pdf](Reporte.pdf).
Probé las rutas Tijuana → Cancún y Mexico City → Monterrey.

Las conexiones del grafo son por cercanía entre ciudades, así que las rutas
no necesariamente corresponden a carreteras reales. 
