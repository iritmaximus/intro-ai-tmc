import json
import os
from collections import deque

def load_data(source_file):
    """Reading JSON from the file and deserializing it
    :param source_file: JSON map of tram stops (str)
    :return: obj (array)
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, '..', source_file)) as file:
        return json.load(file)


class State:
    """ State lets you trace back the route from the last stop
    :attr stop: Code of the stop (str)
    :attr previous: Previous state of the route (State)
    """
    def __init__(self, stop, previous=None):
        self.stop = stop
        self.previous = previous

    """ Returns route as a string from the last stop to the beginning. 
        Format: 1030423 -> 1010420 -> 1010427 
    """
    def __str__(self):
        result = self.stop
        state = self.previous
        while state is not None:
            result += " -> " + state.stop
            state = state.previous

        return result

    def get_stop(self):
        return self.stop

    def get_previous(self):
        return self.previous


class CityMap:
    """Storage of the tram network stops
    :attr data: (obj)
    :attr stops: dictionary {stop_code: stop}
    """
    def __init__(self, source_file):
        self.data = load_data(source_file)
        self.stops = {}
        for stop in self.data:
            self.stops[stop["code"]] = stop

    def get_neighbors(self, stop_code):
        """Returns dictionary containing all neighbor stops """
        return self.stops.get(stop_code)["neighbors"]

    def get_neighbors_codes(self, stop_code):
        """Returns codes of all neighbor stops """
        return list(self.stops.get(stop_code)["neighbors"].keys())

    def search(self, start, goal):
        """Implement breadth-first search. Return the answer as a linked list of States
        where the first node contains the goal stop code and each node is linked to the previous node in the path.
        The last node in the list is the starting stop and its previous node is None.

        :param start: Code of the initial stop (str)
        :param goal: Code of the last stop (str)
        :returns (obj)
        """

        # 0. check if current node is goal? create new state with current stop and return State
        # 1. remove current stop from not visited nodes
        # 2. get neighboring stops of current stop
        # 3. add current stop to visited stops
        # 4. add neighbors to not visited nodes
        # 5. set current stop to next not visited node

        visited_node_codes = set()
        nodes = deque([State(start, None)])

        while nodes:
            # queue.pop() pops from the right...
            node = nodes.popleft()

            if node.get_stop() == goal:
                return node

            if node.get_stop() not in visited_node_codes:
                visited_node_codes.add(node.get_stop())

                for neighbor_code in self.get_neighbors_codes(node.get_stop()):
                    nodes.append(State(neighbor_code, node))

        # No routes found
        return None

    def heuristic(self, stop: State):
        """
        1. Implement a State class (the python TMC extension already has a template for this) with method 
           heuristic(Stop s), which calculates a lower bound on the time required to reach the destination from stop s. 
           A lower bound can be obtained by computing the distance between the two stops, and dividing it by the 
           maximum speed of the tram which you can assume to be 260 coordinate points per minute.
        2. Also implement method __lt__(self, other) in class State so that it can be used to order the nodes in 
           the priotity queue based on cost + h(node) as described in Part 1. Here the nodes are states that are 
           defined by the stop and the time since departure.
        3. Implement the A* search in class CityMap. The PriorityQueue data structure comes in handy. 
           An instance of the State class should be given as an argument to the search method.
        """
        return

if __name__ == "__main__":
        citymap = CityMap("network.json")
        results = str(citymap.search("1250429", "1121480"))
        print(results)

        print()

        citymap = CityMap("network.json")
        results = str(citymap.search("1010427", "1220425"))
        print(results)
