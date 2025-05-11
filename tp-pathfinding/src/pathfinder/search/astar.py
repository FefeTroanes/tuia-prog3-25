from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {}

        # Add the node to the explored dictionary
        explored[node.state] = True

        # Initialize the frontier with the initial node
        # In this example, the frontier is a priority queue
        frontier = PriorityQueueFrontier()
        frontier.add(node, (node.cost + grid.manhattan_distance(node.state, grid)))

        while True:
            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)

            # Remove a node from the frontier
            node = frontier.pop()

            # Return if the node contains a goal state
            # In this example, the goal test is run
            # after removing a new node from the frontier
            if node.state == grid.end:
                return Solution(node, explored)

            # GBFS
            successors = grid.get_neighbours(node.state)
            for neighbour in successors:
                new_state = successors[neighbour]
                cost = node.cost + grid.get_cost(new_state)

                if new_state not in explored or cost < explored[new_state]:
                    new_node = Node("",
                                    new_state,
                                    cost,
                                    parent=node,
                                    action=neighbour)
                    explored[new_state] = cost
                    frontier.add(new_node, (cost + grid.manhattan_distance(new_node.state, grid)))
