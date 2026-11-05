# ¿Habrá chamba de software en 2031?

Investigación consultada el 30 de octubre de 2026. Fundamento para una red
bayesiana de escenarios; no es un modelo calibrado ni una predicción personal.
Cinco años desde ahora corresponde a 2031, no a 2030.

## Idea recomendada

Comparar la posibilidad de recibir una oferta de desarrollo de software en
México durante seis meses de búsqueda activa en 2031. La población propuesta
son egresados de carreras relacionadas que buscan empleo en software.
Hay que mantener ese evento y esa población iguales en todas las tablas.

La pregunta permite contrastar escenarios: mercado favorable o difícil,
experiencia práctica previa y capacidad de resolver tareas con herramientas
actuales. No equivale a preguntar si desaparecerán los programadores.

## Evidencia y sus límites

### México: IMCO, edición 2026

La ficha de Desarrollo de software indica 96.8 % de ocupación, 3.2 % de
desempleo y 44.7 % de vinculación entre estudios y trabajo. Son indicadores
actuales, no probabilidades de contratación futura.

Fuente: [ficha de la carrera](https://comparacarreras.imco.org.mx/desarrollo_de_software/).

La metodología usa ENOE de 2T2025 a 1T2026. Ocupación se calcula sobre la
población económicamente activa; vinculación, sobre ocupados con información
válida de carrera y ocupación. No describe exclusivamente a recién egresados.

Fuente: [metodología](https://comparacarreras.imco.org.mx/metodologia/).

Por tanto, no pondríamos 0.968 como probabilidad de conseguir una oferta de
software en seis meses. Tampoco multiplicaríamos indicadores con universos
diferentes sin justificar los denominadores y los datos faltantes.

### Estados Unidos: BLS

La página vigente proyecta 10 % de crecimiento conjunto de desarrolladores,
analistas de calidad y testers entre 2025 y 2035, con 106,100 aperturas anuales
promedio, incluidas sustituciones. La proyección anterior de 15 % para
2024–2034 todavía aparece en búsquedas.

Fuente: [Occupational Outlook Handbook](https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm).

Esto describe cantidad de puestos en otro país. No proporciona la probabilidad
de contratación de un mexicano ni se puede dividir entre dos para obtenerla.

### Entrada al mercado: Stanford Digital Economy Lab

La revisión del 12 de agosto de 2026 usa nóminas ADP hasta junio de 2026.
Encuentra una brecha relativa de empleo de 19 % entre jóvenes de 22–25 años
en ocupaciones expuestas a IA y la trayectoria de sus pares menos expuestos.
No encuentra desplazamiento generalizado y presenta los resultados como
descriptivos, no causales.

Fuente: [Canaries in the Coal Mine](https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/).

No significa que 19 % de los programadores fueron despedidos por IA ni que
la probabilidad individual de obtener empleo cayó 19 puntos porcentuales.

### Productividad: METR

El experimento de principios de 2025 encontró tareas 19 % más lentas con IA.
La actualización del 24 de febrero de 2026 advierte que la nueva muestra tiene
sesgos de selección y no permite estimar con confianza la aceleración actual.

Fuente: [actualización metodológica](https://metr.org/blog/2026-02-24-uplift-update/).

No usaríamos ese 19 % como probabilidad de reemplazo ni asumiríamos que usar
IA siempre mejora el trabajo. Importa medir calidad, revisión y contexto.

### Expectativas de empleadores: WEF

El informe 2025 incluye desarrollo de software y aplicaciones entre los roles
de mayor crecimiento porcentual esperado hacia 2030.

Fuente: [Future of Jobs, Jobs Outlook](https://www.weforum.org/publications/the-future-of-jobs-report-2025/2-jobs-outlook/).

Son expectativas de empleadores y el horizonte termina antes de 2031. Sirve
para motivar escenarios, no para llenar una tabla de contratación individual.

## Red actualizada: el avance de IA es incierto

La implementación está en `networks/empleo_ia_2031.yaml`. Las variables,
las tablas y sus supuestos se explican en [MODELO.md](MODELO.md).
Se eligió un simulador de escenarios: TODOS sus parámetros numéricos son
supuestos didácticos. Las fuentes motivan las variables, no estiman las CPT.

### Medir capacidad no es medir sustitución laboral

METR define el horizonte de tareas por el tiempo que necesita un experto
humano y la tasa de éxito del agente, incluyendo umbrales de 50 % y 80 %.
Su página consultada indica última actualización el 8 de septiembre de 2026
y advierte que estimaciones superiores a 16 horas no son fiables con esa suite.

Fuente: [Task-Completion Time Horizons](https://metr.org/time-horizons/).

Una nota del investigador Thomas Kwa aclara que el horizonte no es el tiempo
que una IA trabaja sola y que cambia mucho según el tipo de tarea.

Fuente: [Limitaciones, 22 de enero de 2026](https://metr.org/notes/2026-01-22-time-horizon-limitations/).

Otra nota de METR señala incertidumbre por la distribución de tareas y por
las decisiones estadísticas, especialmente al saturarse la evaluación.

Fuente: [Supuestos del modelado, 20 de marzo de 2026](https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/).

**Decisión propia:** definir A mediante un umbral verificable de capacidad en
2031 y variar P(A). No extrapolar una curva exponencial hasta 2031 como si
su continuidad estuviera garantizada. El 80 % del umbral define éxito en
tareas; no es el prior de A ni una probabilidad de quedarse sin trabajo.

### Dos posibles efectos de IA sobre la demanda

El WEF reporta que 41 % de empleadores encuestados prevé reducir plantilla
donde la IA replique trabajo, mientras 49 % planea reorientar su negocio hacia
nuevas oportunidades de IA y 62 % contratar habilidades para trabajar con ella.
Son planes para 2025–2030, no tasas de éxito ni despido de personas.

Fuente: [Estrategias de plantilla, Future of Jobs 2025](https://www.weforum.org/publications/the-future-of-jobs-report-2025/4-workforce-strategies/).

**Decisión propia:** separar automatización T y expansión N. No son eventos
excluyentes: una industria puede experimentar ambos. Las cifras anteriores
no se usan como P(T|A), P(N|A) o P(O), pues no miden esos eventos.

## Alternativa: ¿quién gana la carrera de IA?

Hay que definir un resultado verificable. Ejemplo: una empresa concreta lidera
el gasto empresarial estadounidense en APIs de modelos al cierre de 2031,
según una fuente y una metodología fijadas. Esto no significa liderar usuarios,
rentabilidad, hardware y capacidades al mismo tiempo.

Menlo Ventures estimó para 2025 cuotas de gasto empresarial en APIs de 40 %
para Anthropic y 27 % para OpenAI, con una encuesta a 495 decisores y modelado
de mercado. Son estimaciones estadounidenses. Menlo es inversor en Anthropic.

Fuente: [State of Generative AI in the Enterprise 2025](https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/).

Artificial Analysis evalúa capacidades mediante un índice compuesto y señala
que sus métricas no aplican por igual a todos los usos.

Fuente: [metodología de evaluación](https://artificialanalysis.ai/methodology/intelligence-benchmarking).

Una cuota de mercado no es probabilidad de victoria futura. Para esa red se
necesitarían supuestos sobre capacidades, distribución, costos, financiación
y competencia. Es interesante, pero más especulativa que la de empleo.
Además, el código de clase solo admite booleanos: conviene preguntar por una
empresa específica, no representar ganadores mutuamente excluyentes como
varios nodos independientes.

## Estado de la implementación

La red de escenarios ya funciona con los scripts 01, 02 y 03. El script
`05_escenarios_ia.py` compara perfiles y valores de P(A). Se conservó la
alternativa de competencia empresarial arriba solo como referencia de la
investigación inicial. No se implementó como otra red.

Los resultados dependen de supuestos, no constituyen una predicción validada
para México ni un efecto causal medido. La siguiente mejora empírica sería
obtener datos de contratación con características de candidatos y horizontes
comparables. La incertidumbre futura seguiría necesitando escenarios.
