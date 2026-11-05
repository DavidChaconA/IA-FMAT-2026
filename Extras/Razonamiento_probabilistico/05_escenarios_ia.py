"""Compara escenarios; las cifras son supuestos, no predicciones validadas."""

import argparse
from copy import deepcopy
from pathlib import Path

from bn.enumerate import enumerate_ask
from bn.load import load_yaml, parse_network


RED = Path(__file__).resolve().parent / "networks" / "empleo_ia_2031.yaml"


def probabilidad(texto):
    try:
        valor = float(texto)
    except ValueError:
        raise argparse.ArgumentTypeError("Usa un número entre 0 y 1.")
    if not 0 <= valor <= 1:
        raise argparse.ArgumentTypeError("La probabilidad debe estar entre 0 y 1.")
    return valor


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p-avance", type=probabilidad, default=None,
                        help="Supuesto P(avance alto de IA), entre 0 y 1.")
    args = parser.parse_args()
    datos = load_yaml(RED)
    if args.p_avance is not None:
        datos["cpts"]["A"] = args.p_avance
    red = parse_network(datos)
    print(red.name)
    print("Todos los porcentajes dependen de tablas elegidas para explorar escenarios.\n")
    print("E: experiencia remunerada >= 1 año; H: supera evaluación técnica con IA.")
    print("O: oferta de software en seis meses de búsqueda activa en México, en 2031.")
    print(f"Supuesto P(A=true): {datos['cpts']['A']:.0%}\n")
    # Escenarios separados: funcionan incluso si el prior elegido es 0 o 1.
    escenarios = []
    for p in (0.0, 1.0):
        variante = deepcopy(datos)
        variante["cpts"]["A"] = p
        escenarios.append(parse_network(variante))
    print(f"{'Perfil':<32} {'A=false':>10} {'A=true':>10} {'A incierto':>12}")
    for e, h in [(False, False), (False, True), (True, False), (True, True)]:
        evidencia = {"E": e, "H": h}
        valores = [enumerate_ask(escenario, "O", evidencia)[True]
                   for escenario in escenarios]
        valores.append(enumerate_ask(red, "O", evidencia)[True])
        perfil = f"E={'sí' if e else 'no'}, H={'sí' if h else 'no'}"
        print(f"{perfil:<32}" + "".join(f"{v:>11.1%}" for v in valores))

    print("\nSensibilidad de P(O), perfil E=true, H=true:")
    for p in (.2, .5, .8):
        variante = deepcopy(datos)
        variante["cpts"]["A"] = p
        valor = enumerate_ask(parse_network(variante), "O", {"E": True, "H": True})[True]
        print(f"  Si suponemos P(A)={p:.0%}: P(O)={valor:.1%}")
    print("\nTambién puedes cambiar T, N, D y O en el YAML: el efecto neto de IA")
    print("depende de esas decisiones. Esta tabla no prueba un efecto causal real.")


if __name__ == "__main__":
    main()
