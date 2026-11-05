import json
from pathlib import Path

CARPETA = Path(__file__).resolve().parent


def separar(atomo):
    # En esta base todos los predicados tienen un solo argumento.
    nombre, argumento = atomo[:-1].split("(")
    return nombre, argumento


def sustituir(atomo, valores):
    nombre, argumento = separar(atomo)
    return f"{nombre}({valores.get(argumento, argumento)})"


def unificar(patron, hecho, valores):
    """Compara un patrón como Miembro(x) con un hecho concreto como Miembro(Ana)."""
    nombre, argumento = separar(patron)
    nombre_hecho, constante = separar(hecho)
    if nombre != nombre_hecho:
        return None
    copia = dict(valores)
    if argumento[0].islower():
        if argumento in copia and copia[argumento] != constante:
            return None
        copia[argumento] = constante
    elif argumento != constante:
        return None
    return copia


def cumplir_premisas(premisas, hechos, valores):
    """Prueba las premisas y los hechos en su orden, conservando la misma x."""
    if not premisas:
        return [valores]
    respuestas = []
    for hecho in hechos:
        nuevos_valores = unificar(premisas[0], hecho, valores)
        if nuevos_valores is not None:
            respuestas.extend(cumplir_premisas(premisas[1:], hechos, nuevos_valores))
    return respuestas


def hacia_adelante(hechos, reglas, consulta):
    conocidos = list(hechos)
    inferidos = []
    traza = [f"Consulta: {consulta}", "Hechos iniciales: " + ", ".join(conocidos)]
    ronda = 1

    while True:
        nuevos = []
        traza.append(f"Ronda {ronda}:")
        for regla in reglas:
            for valores in cumplir_premisas(regla["si"], conocidos, {}):
                conclusion = sustituir(regla["entonces"], valores)
                if conclusion not in conocidos and conclusion not in nuevos:
                    nuevos.append(conclusion)
                    traza.append(f"  {regla['id']} con {valores} -> {conclusion}")
        if not nuevos:
            traza.append("  No hay hechos nuevos. Terminó el razonamiento.")
            break
        # Solo después de revisar TODAS las reglas se incorporan los nuevos hechos.
        conocidos.extend(nuevos)
        inferidos.extend(nuevos)
        ronda += 1

    respuesta = None
    for hecho in conocidos:
        respuesta = unificar(consulta, hecho, {})
        if respuesta is not None:
            break
    probada = respuesta is not None
    traza.append("Resultado: " + ("PROBADA" if probada else "NO PROBADA"))
    return probada, inferidos, traza


def probar_meta(meta, hechos, reglas, pila, traza, nivel=0):
    """Búsqueda hacia atrás para las consultas concretas de esta biblioteca."""
    espacio = "  " * nivel
    traza.append(f"{espacio}Meta: {meta}")
    if meta in pila:
        traza.append(f"{espacio}Ciclo: la meta ya está en la pila. Se corta esta rama.")
        return False

    # Primero se buscan hechos; no se imprimen los que no coinciden.
    for hecho in hechos:
        if unificar(meta, hecho, {}) is not None:
            traza.append(f"{espacio}Hecho encontrado: {hecho}")
            return True

    for regla in reglas:
        valores = unificar(regla["entonces"], meta, {})
        if valores is None:
            continue
        traza.append(f"{espacio}Intentar {regla['id']} con {valores}")
        cumple = True
        for premisa in regla["si"]:
            siguiente = sustituir(premisa, valores)
            if not probar_meta(siguiente, hechos, reglas, pila + [meta], traza, nivel + 1):
                cumple = False
                traza.append(f"{espacio}Falló {regla['id']}")
                break
        if cumple:
            traza.append(f"{espacio}Probada con {regla['id']}: {meta}")
            return True

    traza.append(f"{espacio}No se pudo probar: {meta}")
    return False


def hacia_atras(hechos, reglas, consulta):
    # Las consultas son concretas y todas las variables de cada regla están
    # en su conclusión. Cada intento tiene su propio diccionario de valores.
    # Así no se comparten variables entre reglas ni se necesitan índices x_1, x_2.
    traza = []
    probada = probar_meta(consulta, hechos, reglas, [], traza)
    traza.append("Resultado: " + ("PROBADA" if probada else "NO PROBADA"))
    return probada, traza


def ejecutar_caso(hechos, reglas, consultas, titulo):
    salida = [titulo, "=" * 65]
    for consulta in consultas:
        salida.extend(["", "HACIA ADELANTE"])
        _, nuevos, traza = hacia_adelante(hechos, reglas, consulta)
        salida.extend(traza)
        salida.append("Átomos nuevos: " + ", ".join(nuevos))
        salida.extend(["", "HACIA ATRÁS"])
        _, traza = hacia_atras(hechos, reglas, consulta)
        salida.extend(traza)
    return salida


def main():
    with (CARPETA / "biblioteca.json").open(encoding="utf-8") as archivo:
        base = json.load(archivo)

    hechos = base["hechos"]
    reglas = base["reglas"]
    salida = ejecutar_caso(hechos, reglas, base["consultas"], "BASE ORIGINAL")

    # Caso adicional pedido por el reporte, separado de las tres consultas iniciales.
    hechos_extra = hechos + ["TieneCredencial(Luis)"]
    salida.extend(["", ""])
    salida.extend(ejecutar_caso(hechos_extra, reglas, ["AccesoNoche(Luis)"],
                               "CASO ADICIONAL: LUIS TIENE CREDENCIAL"))
    texto = "\n".join(salida) + "\n"
    print(texto, end="")
    (CARPETA / "evidencia.txt").write_text(texto, encoding="utf-8")
    print("\nTraza guardada en evidencia.txt.")


if __name__ == "__main__":
    main()
