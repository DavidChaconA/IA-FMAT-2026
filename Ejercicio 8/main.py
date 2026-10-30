import argparse
import csv
import random
from pathlib import Path

CARPETA = Path(__file__).resolve().parent

# Mapa fijo del ejercicio. Cada estado es una pareja (fila, columna).
FILAS = 4
COLUMNAS = 12
INICIO = (3, 0)
META = (3, 11)
ACANTILADO = {(3, columna) for columna in range(1, 11)}
ACCIONES = ("N", "E", "S", "W")
MOVIMIENTOS = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}

ALPHA = 0.5
GAMMA = 1.0
EPSILON = 0.1
EPISODIOS = 500
MAX_PASOS = 200
SEMILLA = 1


def paso(estado, accion):
    """Devuelve (estado siguiente, recompensa, terminó en la meta)."""
    df, dc = MOVIMIENTOS[accion]
    fila = max(0, min(estado[0] + df, FILAS - 1))
    columna = max(0, min(estado[1] + dc, COLUMNAS - 1))
    siguiente = (fila, columna)

    if siguiente in ACANTILADO:
        return INICIO, -100, False
    if siguiente == META:
        return META, -1, True
    return siguiente, -1, False


def tabla_inicial():
    q = {}
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            estado = (fila, columna)
            if estado != META and estado not in ACANTILADO:
                q[estado] = {accion: 0.0 for accion in ACCIONES}
    return q


def accion_greedy(q, estado):
    # max conserva la primera acción en caso de empate: N, E, S, W.
    return max(ACCIONES, key=lambda a: q[estado][a])


def epsilon_greedy(q, estado, rng):
    if rng.random() < EPSILON:
        return rng.choice(ACCIONES)
    return accion_greedy(q, estado)


def actualizar_q(q, estado, accion, siguiente, recompensa, terminado):
    # Una caída NO es terminal: siguiente es el inicio y conserva valor futuro.
    futuro = 0.0 if terminado else max(q[siguiente].values())
    objetivo = recompensa + GAMMA * futuro
    q[estado][accion] += ALPHA * (objetivo - q[estado][accion])


def entrenar(episodios=EPISODIOS):
    rng = random.Random(SEMILLA)
    q = tabla_inicial()
    registros = []

    for episodio in range(1, episodios + 1):
        estado = INICIO
        retorno = 0.0
        for pasos in range(1, MAX_PASOS + 1):
            accion = epsilon_greedy(q, estado, rng)
            siguiente, recompensa, terminado = paso(estado, accion)
            actualizar_q(q, estado, accion, siguiente, recompensa, terminado)
            retorno += recompensa
            estado = siguiente
            if terminado:
                break
        # El tope corta el episodio, pero no convierte su último estado en meta.
        registros.append((episodio, retorno, pasos, terminado))
    return q, registros


def evaluar(q):
    """Evaluación con epsilon=0; no modifica la tabla Q."""
    estado = INICIO
    camino = [estado]
    acciones = []
    retorno = 0.0
    for _ in range(MAX_PASOS):
        accion = accion_greedy(q, estado)
        estado, recompensa, terminado = paso(estado, accion)
        camino.append(estado)
        acciones.append(accion)
        retorno += recompensa
        if terminado:
            break
    return camino, acciones, retorno, estado == META


def politica_texto(q):
    flechas = {"N": "↑", "E": "→", "S": "↓", "W": "←"}
    filas = []
    for f in range(FILAS):
        celdas = []
        for c in range(COLUMNAS):
            estado = (f, c)
            if estado == META:
                simbolo = "G"
            elif estado in ACANTILADO:
                simbolo = "C"
            else:
                simbolo = flechas[accion_greedy(q, estado)]
            celdas.append(simbolo)
        filas.append(" ".join(celdas))
    return "\n".join(filas)


def main():
    parser = argparse.ArgumentParser(description="Q-learning en Cliff Walking")
    parser.add_argument(
        "--episodios", "--episodes", type=int, default=EPISODIOS,
        help="Número de episodios de entrenamiento (por defecto: 500)",
    )
    args = parser.parse_args()
    if args.episodios <= 0:
        parser.error("El número de episodios debe ser mayor que cero.")

    q, registros = entrenar(args.episodios)
    camino, acciones, retorno, llego = evaluar(q)

    with (CARPETA / "recompensas.csv").open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["episodio", "recompensa", "pasos", "meta_alcanzada", "media_movil_10"])
        for i, registro in enumerate(registros):
            ventana = registros[max(0, i - 9):i + 1]
            media = sum(r[1] for r in ventana) / len(ventana)
            escritor.writerow([*registro, round(media, 2)])

    resultado = (
        f"Semilla: {SEMILLA}\n"
        f"Alpha: {ALPHA}; gamma: {GAMMA}; epsilon: {EPSILON}\n"
        f"Episodios: {args.episodios}; tope de pasos: {MAX_PASOS}\n"
        f"Q inicial: 0; desempate: {', '.join(ACCIONES)}\n\n"
        f"Política greedy (inicio en la esquina inferior izquierda):\n{politica_texto(q)}\n\n"
        f"Acciones: {', '.join(acciones)}\n"
        f"Camino: {' → '.join(map(str, camino))}\n"
        f"Pasos: {len(acciones)}\nRetorno greedy: {retorno:g}\nMeta alcanzada: {llego}\n"
        f"Episodios cortados por el tope: {sum(not r[3] for r in registros)}\n"
    )
    print(resultado)


if __name__ == "__main__":
    main()
