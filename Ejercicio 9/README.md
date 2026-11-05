# Ejercicio 9 — Razonamiento lógico

Desde esta carpeta ejecuta:

```bash
python3 main.py
```

No necesita paquetes ni entorno virtual. Muestra las tres consultas con ambos
algoritmos y después el caso adicional de Luis con credencial. Cada corrida
reemplaza `evidencia.txt` con la salida de terminal.

- `biblioteca.json`: hechos, reglas y consultas, en el orden del enunciado.
- `main.py`: encadenamiento hacia adelante y hacia atrás.
- `evidencia.txt`: trazas y resultados de una ejecución real del programa.
- `reporte.md`: respuestas a las tres preguntas.

Se usa JSON porque Python ya lo puede leer; el enunciado permite un formato
equivalente a YAML. El código trabaja con los predicados de un argumento de
esta biblioteca. Las consultas hacia atrás son concretas, como
`AccesoNoche(Ana)`, y las variables de las premisas deben aparecer en la
conclusión de su regla. No es un motor general de lógica de primer orden.

Los diccionarios de sustituciones son locales a cada intento. Hacia adelante
se respeta el inicio de cada ronda; hacia atrás se prueban primero los hechos,
luego las reglas y se corta una rama si repite una meta en su pila.

El enunciado pide las trazas, no exige imágenes. Si quieres una captura de tu
propia ejecución, corre el comando y toma una captura de la terminal.
El proyecto del profesor se conserva como referencia, sin modificaciones.
