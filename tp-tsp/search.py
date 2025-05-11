"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem

# cantidad_reinicios = int(input('Ingree la cantidad de reinicios: '))
class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)
        print(f'Actual: {actual}')
        print(f'Value: {value}')

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""
    def __init__(self, reset_quantity):
        super().__init__()
        self.reset_quantity = reset_quantity

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas de reinicio aleatorio.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj y configuracion inicial
        start = time()
        # best_tour = None
        # best_value = float('-inf')

        # Arrancamos del estado inicial
        best_tour = None
        best_value = float('-inf')
        # print(f'Actual: {actual}')
        # print(f'Value: {value}')

        for restart in range(self.reset_quantity +1):
            print(f'Restart: {restart}')
            # Usamos el estado inicial o uno de reinicio aleatorio
            if restart == 0:
                actual = problem.init
            else:
                actual = problem.random_reset()
            value = problem.obj_val(problem.init)
            while True:
                # Buscamos la acción que genera el sucesor con mayor valor objetivo
                act, succ_val = problem.max_action(actual)

                # Retornar si estamos en un maximo local:
                # el valor objetivo del sucesor es menor o igual al del estado actual
                if succ_val <= value:
                    break

                # Sino, nos movemos al sucesor
                actual = problem.result(actual, act)
                value = succ_val
                self.niters += 1

            if value > best_value:
                best_tour = actual
                best_value = value

        self.tour = best_tour
        self.value = best_value
        end = time()
        self.time = end-start

class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""
    def __init__(self, max_iters, max_without_improve, max_tabu_size):
        super().__init__()
        self.max_iters = max_iters
        self.max_without_improve = max_without_improve
        self.max_tabu_size = max_tabu_size

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con busqueda Tabu.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj y configuracion inicial
        start = time()
        actual = problem.init
        best_tour = actual
        value = problem.obj_val(actual)
        best_value = value
        tabu_list = []

        # Cambiar una vez terminada
        # iters = 100
        iters_without_improve = 0

        # for iteracion in range(self.max_iters + 1):
        #     print(iteracion)
        while True:
            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual, tabu_list)

            print(f'act: {act}')
            print(f'TAbu list: {tabu_list}')

            if act is None:
                break

            succ = problem.result(actual, act)

            if succ_val > best_value:
                best_tour = succ
                best_value = succ_val
                iters_without_improve = 0
                print('Mejora')
            else:
                iters_without_improve += 1
                print('No mejora')

            tabu_list.append(act)
            actual = succ
            value = succ_val
            self.niters += 1

            if len(tabu_list) == self.max_tabu_size: # 20
                tabu_list.pop(0)
                print('ACORTAR LISTA TABU')

            if iters_without_improve >= self.max_without_improve: # 1000
                print('MAXIMA CANTIDAD DE ITERACIONES SIN MEJORA')
                break

        self.tour = best_tour
        self.value = best_value
        end = time()
        self.time = end-start


# function BÚSQUEDA-TABÚ(problema) return estado
#   actual ← problema.estado-inicial
#   mejor ← actual
#   tabu ← inicialmente vacía
#   while no se cumpla el criterio de parada do
#       accion ← MAX-ACCION(problema, actual, tabu)
#       sucesor ← problema.resultado(actual, accion)


#       if problema.f(mejor) < problema.f(sucesor) then mejor ← sucesor
#       actualizar la lista tabú
#       actual ← sucesor
#   return mejor




# Se puede agregar criterio de aspiracion PERO no es obligatorio
# a la hora de elegir el sucesor, aplicamos el criterio de aspiracion
# si no hay ninguno que verifique este criterio se sigue con la busqueda taboo