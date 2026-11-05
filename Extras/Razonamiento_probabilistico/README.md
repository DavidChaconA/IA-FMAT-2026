# ¿La IA me deja sin chamba en 2031?

Red bayesiana de escenarios: relaciona avance de IA, automatización, nuevos
proyectos, demanda, experiencia y habilidad con conseguir una oferta de software.
**Todos los porcentajes de la red son supuestos didácticos, no predicciones
validadas.** Los estudios fundamentan la estructura, no sus valores numéricos.

## Ejecutar

```bash
cd /Users/davidchacon/Documents/IA/IA-FMAT-2026/Extras/Razonamiento_probabilistico
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python 05_escenarios_ia.py
```

Las siguientes veces basta activar `.venv`. Para cambiar el supuesto de avance:

```bash
python 05_escenarios_ia.py --p-avance 0.8
```

Esto supone 80 % de probabilidad de A; no significa que la IA haga 80 % del trabajo.

## Usar los programas de clase

Los scripts 01–03 ahora cargan por defecto `networks/empleo_ia_2031.yaml`.

```bash
python 01_show_network.py
python 02_joint.py
python 03_query.py
python 03_query.py --query O --evidence A=true E=true H=true
python 03_query.py --query O --evidence A=false E=true H=true
python 03_query.py --query A --evidence O=false
```

`03_query.py` sin opciones calcula P(O) sin evidencia. `02_joint.py` muestra
las 128 combinaciones posibles de las siete variables.

- `A`: avance alto de IA en 2031.
- `T`: automatización alta de tareas.
- `N`: expansión de nuevos proyectos por IA.
- `D`: demanda favorable de desarrolladores.
- `E`: al menos un año de experiencia remunerada.
- `H`: supera una evaluación técnica con IA.
- `O`: recibe una oferta de software en seis meses.

[MODELO.md](MODELO.md) define cada evento y justifica los supuestos.
[INVESTIGACION.md](INVESTIGACION.md) incluye los datos reales y sus fuentes.

Los ejemplos originales siguen disponibles:

```bash
python 03_query.py --network networks/wet_grass.yaml
python 03_query.py --network networks/alarm.yaml
python 04_explaining_away.py
```

El programa 04 conserva el ejemplo del pasto: requiere L, A y P, y no corresponde
a la estructura de la nueva red. El motor `bn/` y los programas de base proceden
del proyecto del profesor; se adaptó el valor por defecto y se añadió la red
propia y el comparador 05. El repositorio original quedó intacto.
