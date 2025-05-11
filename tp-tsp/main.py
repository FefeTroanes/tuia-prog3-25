"""Modulo principal.

Autor: Mauro Lucci.
Fecha: 2023.
Materia: Prog3 - TUIA
"""

import parse
import load
import search
import plot
import problem

# Algoritmos involucrados
HILL_CLIMBING = "hill"
HILL_CLIMBING_RANDOM_RESET = "hill_reset"
TABU_SEARCH = "tabu"
ALGO_NAMES = [HILL_CLIMBING, HILL_CLIMBING_RANDOM_RESET, TABU_SEARCH]


def main() -> None:
    """Funcion principal."""
    # Parsear los argumentos de la linea de comandos
    args = parse.parse()

    # Leer la instancia
    G, coords = load.read_tsp(args.filename)

    # Construir la instancia de TSP
    p = problem.TSP(G)

    # inputs
    print('HILL CLIMBING DE REINICIO ALEATORIO')
    reset_quantity = int(input('Ingrese la cantidad de veces que desea reiniciar aleatoriamente: '))

    print('BUSQUEDA TABU')
    max_iters = int(input('Ingrese la cantidad limite de iteraciones: '))
    max_without_improve = int(input('Ingrese la cantidad limite de iteraciones sin mejora: '))
    max_tabu_size = int(input('Ingrese el largo maximo de la lista tabu: '))

    # Construir las instancias de los algoritmos
    algos = {HILL_CLIMBING: search.HillClimbing(),
             HILL_CLIMBING_RANDOM_RESET: search.HillClimbingReset(reset_quantity),
             TABU_SEARCH: search.Tabu(max_iters, max_without_improve, max_tabu_size)}

    # Resolver el TSP con cada algoritmo
    for algo in algos.values():
        algo.solve(p)

    # Mostrar resultados por linea de comandos
    print("Valor:", "Tiempo:", "Iters:", "Algoritmo:", sep="\t\t")
    for name, algo in algos.items():
        print(algo.value, "%.2f" % algo.time, algo.niters, name, sep="\t\t")

    # Graficar los tours
    tours = {}
    tours['init'] = (p.init, p.obj_val(p.init))  # estado inicial
    for name, algo in algos.items():
        tours[name] = (algo.tour, algo.value)
    plot.show(G, coords, args.filename, tours)


if __name__ == "__main__":
    main()
