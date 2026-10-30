"use strict";

// Puerto de find_route.py, adaptado del A* de
// Búsqueda informada/project/search/astar.py. Estado = id de ciudad.
const MexicoRoutes = (() => {
  function haversine(a, b) {
    const rad = Math.PI / 180;
    const value = Math.sin((b.lat - a.lat) * rad / 2) ** 2 +
      Math.cos(a.lat * rad) * Math.cos(b.lat * rad) *
      Math.sin((b.lon - a.lon) * rad / 2) ** 2;
    return 2 * 6371 * Math.asin(Math.sqrt(Math.min(1, value)));
  }

  function prepareGraph(data) {
    const cities = new Map(data.nodes.map(city => [city.id, city]));
    const neighbors = new Map(data.nodes.map(city => [city.id, []]));
    let scale = 1;
    for (const {source, target, km} of data.edges) {
      neighbors.get(source).push([target, km]);
      neighbors.get(target).push([source, km]);
      const distance = haversine(cities.get(source), cities.get(target));
      if (distance) scale = Math.min(scale, km / distance);
    }
    for (const items of neighbors.values()) items.sort((a, b) => a[0] - b[0]);
    return {cities, neighbors, scale: scale * (1 - 1e-12)};
  }

  function aStar(graph, start, goal) {
    const {cities, neighbors, scale} = graph;
    const h = id => scale * haversine(cities.get(id), cities.get(goal));
    const frontier = [{state: start, parent: null, g: 0, f: h(start), order: 0}];
    const bestG = new Map([[start, 0]]);
    const explored = new Set();
    let counter = 0, expanded = 0;
    while (frontier.length) {
      // Con 1,000 ciudades una lista ordenada basta y es fácil de leer.
      // El orden es el mismo del heap de Python: primero f, luego inserción.
      frontier.sort((a, b) => a.f - b.f || a.order - b.order);
      const node = frontier.shift();
      if (explored.has(node.state)) continue;
      if (node.state === goal) {
        const path = [];
        for (let current = node; current; current = current.parent) path.push(current.state);
        path.reverse();
        return {status: "success", path, depth: path.length - 1, cost: node.g, expanded};
      }
      explored.add(node.state);
      expanded++;
      for (const [id, km] of neighbors.get(node.state)) {
        const g = node.g + km;
        if (!explored.has(id) && g < (bestG.get(id) ?? Infinity)) {
          bestG.set(id, g);
          frontier.push({state: id, parent: node, g, f: g + h(id), order: ++counter});
        }
      }
    }
    return {status: "failure", path: [], depth: 0, cost: null, expanded};
  }

  return {haversine, prepareGraph, aStar};
})();
