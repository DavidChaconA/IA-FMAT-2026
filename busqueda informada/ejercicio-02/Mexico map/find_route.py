"""A* en el grafo de México. Solo usa la biblioteca estándar de Python.

Adaptado de Búsqueda informada/project/search/astar.py y romania/node.py:
frontera por f = g + h, desempate por inserción, mejores costos y padres.
El estado ahora es el id entero de la ciudad. No se modifica el grafo.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import heapq
import json
import math
from pathlib import Path

GRAPH_PATH = Path(__file__).with_name("mexico_cities_graph.json")


def haversine(a: dict, b: dict) -> float:
    """Fórmula de generate_mexico_graph.py, sin ejecutar el generador."""
    p1, p2 = math.radians(a["lat"]), math.radians(b["lat"])
    dphi = math.radians(b["lat"] - a["lat"])
    dlmb = math.radians(b["lon"] - a["lon"])
    value = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(min(1.0, value)))


def prepare_graph(data: dict) -> tuple[dict, dict, float]:
    cities = {city["id"]: city for city in data["nodes"]}
    neighbors = {city_id: [] for city_id in cities}
    scale = 1.0
    for edge in data["edges"]:
        a, b, km = edge["source"], edge["target"], edge["km"]
        neighbors[a].append((b, km))
        neighbors[b].append((a, km))
        distance = haversine(cities[a], cities[b])
        if distance:
            scale = min(scale, km / distance)
    for items in neighbors.values():
        items.sort()  # Orden por id, igual en Python y JavaScript.
    # El JSON redondea km a dos decimales. Este factor garantiza que
    # scale * distancia(a,b) <= km(a,b), incluso si se redondeó hacia abajo.
    return cities, neighbors, scale * (1 - 1e-12)


def city_label(city: dict) -> str:
    return f'{city["name"]}, {city["state"]} [id={city["id"]}]'


def resolve_city(cities: dict, text: str, state: str | None = None) -> int:
    text = text.strip()
    matches = [
        city for city in cities.values()
        if (city["name"] == text or str(city["id"]) == text)
        and (state is None or city["state"] == state)
    ]
    if not matches:
        raise ValueError(f'Ciudad desconocida: {text!r}. Revisa nombre, acentos, estado o id.')
    if len(matches) > 1:
        options = "\n  ".join(city_label(city) for city in matches)
        raise ValueError(f'Nombre ambiguo: {text!r}. Usa el id o indica el estado:\n  {options}')
    return matches[0]["id"]


@dataclass
class Node:
    state: int
    parent: Node | None = None
    path_cost: float = 0.0

    def path(self) -> list[int]:
        ids = []
        node = self
        while node is not None:
            ids.append(node.state)
            node = node.parent
        return ids[::-1]


def a_star(cities: dict, neighbors: dict, start: int, goal: int, scale: float) -> dict:
    """A* del curso adaptado a ids y haversine; scale=0 permite comparar con UCS."""
    if start not in cities or goal not in cities:
        raise ValueError("El origen y el destino deben pertenecer al grafo.")

    def h(city_id: int) -> float:
        return scale * haversine(cities[city_id], cities[goal])

    frontier = [(h(start), 0, Node(start))]
    best_g = {start: 0.0}
    explored = set()
    counter = expanded = 0
    while frontier:
        _f, _order, node = heapq.heappop(frontier)
        if node.state in explored:
            continue
        if node.state == goal:
            path = node.path()
            return {"status": "success", "path": path, "depth": len(path) - 1,
                    "cost": node.path_cost, "expanded": expanded}
        explored.add(node.state)
        expanded += 1
        for city_id, km in neighbors[node.state]:
            cost = node.path_cost + km
            if city_id not in explored and cost < best_g.get(city_id, math.inf):
                best_g[city_id] = cost
                counter += 1
                child = Node(city_id, node, cost)
                heapq.heappush(frontier, (cost + h(city_id), counter, child))
    return {"status": "failure", "path": [], "depth": 0, "cost": None,
            "expanded": expanded}


def main() -> int:
    parser = argparse.ArgumentParser(description="Encuentra rutas con A* en el grafo de México.")
    parser.add_argument("--from-city", required=True, help="Nombre exacto o id del origen")
    parser.add_argument("--to", required=True, help="Nombre exacto o id del destino")
    parser.add_argument("--from-state", help="Estado del origen, si el nombre se repite")
    parser.add_argument("--to-state", help="Estado del destino, si el nombre se repite")
    parser.add_argument("--full-path", action="store_true", help="Imprime todas las ciudades de una ruta larga")
    args = parser.parse_args()
    cities, neighbors, scale = prepare_graph(json.loads(GRAPH_PATH.read_text(encoding="utf-8")))
    try:
        start = resolve_city(cities, args.from_city, args.from_state)
        goal = resolve_city(cities, args.to, args.to_state)
    except ValueError as error:
        parser.exit(2, f"Error: {error}\n")
    result = a_star(cities, neighbors, start, goal, scale)
    print("Algorithm: A* (f = g + h)")
    print(f"From: {city_label(cities[start])}")
    print(f"To: {city_label(cities[goal])}")
    print(f"Heuristic: haversine al destino x {scale:.9f} (ajuste por redondeo del JSON)")
    print(f'Status: {result["status"]}')
    names = [cities[i]["name"] for i in result["path"]]
    if len(names) > 14 and not args.full_path:
        names = names[:5] + [f"... ({len(names)} ciudades en total) ..."] + names[-5:]
    print("Path: " + " -> ".join(names))
    print(f'Depth: {result["depth"]} hops')
    if result["cost"] is not None:
        print(f'Cost: {result["cost"]:.2f} km')
    print(f'Expanded: {result["expanded"]} nodes')
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
