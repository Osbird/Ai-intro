import collections
import heapq
import math


class SimpleGraph:
    def __init__(self):
        self.edges = {}

    def neighbors(self, id):
        return self.edges[id]

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    def empty(self):
        return len(self.elements) == 0
    def put(self, x):
        self.elements.append(x)
    def get(self):
        return self.elements.popleft()


#Class for making a square-grid object
class SquareGrid:
    def __init__(self, width, height, choice):
        self.width = width
        self.height = height
        self.walls = []

    #Building the walls-array for problem 1
        if list(choice)[0]=='1':
            boardstring = "boards/board-" + choice + ".txt"
            print(boardstring)
            walls = []


            with open(boardstring, "r") as file:
                lines = file.readlines()
                y = 0
                for line in lines:
                    x = 0
                    for tile in line:
                        if tile == '\n':
                            break
                        if tile == '#':
                            self.walls.append((x,y))
                        if tile == 'A':
                            self.start = (x, y)
                        elif tile == 'B':
                            self.end = (x, y)
                        x += 1
                    y += 1

#the cost of all nodes in the basic squareGrid problem is 1
    def cost(self, from_node, to_node):
        if to_node not in self.walls:
            return 1
        return 0

#Help functions for the squaregrid
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    def passable(self, id):
        return id not in self.walls
    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() #Detta kommer til å se mer spennende ut
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

#The class for a squaregrid with weights
class GridWithWeights(SquareGrid):
    def __init__(self, width, height, choice):
        super().__init__(width,height, choice)
        self.weights, self.end, self.start = self.createBoard(choice)

    #help-function to convert letter to corresponding int
    def convertLetterToCost(letter):
        if letter == 'r': return 1
        if letter == 'g': return 5
        if letter == 'f': return 10
        if letter == 'm': return 50
        if letter == 'w': return 100
        if letter == 'A': return 1
        if letter == 'B': return 1

    #creating the board
    def createBoard(self, choice):
        boardstring = "boards/board-" + choice + ".txt"
        print(boardstring)
        board = {}
        goal = None
        start = None


        with open(boardstring, "r") as file:
            lines = file.readlines()
            y = 0
            for line in lines:
                x = 0
                for tile in line:

                    if tile == '\n':
                        break

                    board[x,y]=GridWithWeights.convertLetterToCost(tile)

                    if tile == 'A':
                        start = (x, y)
                    elif tile == 'B':
                        goal = (x, y)

                    x += 1

                y += 1
        return board, goal, start

    def cost(self, from_node, to_node):
        return self.weights.get(to_node)

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

# utility functions for visualizing square grids
def from_id_width(id, width):
    return (id % width, id // width)

#returning corresponding string for visualization of the tile. Depending on what sort of problem it is,
#and what we want to visualize. Style decides if we show "come_from graph
def draw_tile(graph, id, style, width):
    r = "."
    if 'number' in style and id in style['number']: r = "%d" % style['number'][id]
    if 'map' in style and type(graph) is GridWithWeights : r = GridWithWeights.cost(graph, 'a', id)
    if 'map' in style and type(graph) is SquareGrid and id not in graph.walls: r = '.'
   #if 'openNo' in style and id in openNo: r = 'o'
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = "\u2192"
        if x2 == x1 - 1: r = "\u2190"
        if y2 == y1 + 1: r = "\u2193"
        if y2 == y1 - 1: r = "\u2191"
    if 'start' in style and id == style['start']: r = "A"
    if 'goal' in style and id == style['goal']: r = "Z"
    if 'path' in style and id in style['path']: r = "@"
    if id in graph.walls: r = "#" * width
    return r

def draw_grid(graph, width=2, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print()





class Main:

    example_graph = SimpleGraph()
    example_graph.edges = {'a':['b'],
                               'b':['a','c','d'],
                               'c':['a'],
                               'd':['e','a'],
                               'e':['b']}

    DIAGRAM1_WALLS = [from_id_width(id, width=30) for id in
                      [21, 22, 51, 52, 81, 82, 93, 94, 111, 112, 123, 124, 133, 134, 141, 142, 153, 154, 163, 164, 171,
                       172, 173, 174, 175, 183, 184, 193, 194, 201, 202, 203, 204, 205, 213, 214, 223, 224, 243, 244,
                       253, 254, 273, 274, 283, 284, 303, 304, 313, 314, 333, 334, 343, 344, 373, 374, 403, 404, 433,
                       434]]



    def bfs(graph, start, goal):
        frontier = Queue()
        frontier.put(start)
        came_from = {}
        came_from[start] = None

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in graph.neighbors(current):
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current
        return came_from





    def dijkstra_search(graph, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far


    def reconstruct_path(came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        path.append(start)  # optional
        path.reverse()  # optional
        return path

    #def reconstructOpenNodes(open_nodes):


    diagram4 = GridWithWeights(40, 10, "2-1")
   # diagram4.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]


#    came_from, cost_so_far = dijkstra_search(diagram4, (1, 4), (7, 8))
#    draw_grid(diagram4, width=3, point_to=came_from, start=(1, 4), goal=(7, 8))
#    print()
#    draw_grid(diagram4, width=3, number=cost_so_far, start=(1, 4), goal=(7, 8))
#    print()
#    draw_grid(diagram4, width=3, path=reconstruct_path(came_from, start=(1, 4), goal=(7, 8)))
#    print()

    #The a star algorithm
    def a_star_search(graph, start, goal):
        def heuristic(a, b):
            (x1, y1) = a
            (x2, y2) = b
            return abs(x1 - x2) + abs(y1 - y2)
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far, frontier

    came_from, cost_so_far, open_nodes = a_star_search(diagram4, diagram4.start, diagram4.end)
    print("Came_from graph: ")
    draw_grid(diagram4, width=3, point_to=came_from, start=diagram4.start, goal=diagram4.end)
    print("\nCost_so_far graph: ")
    draw_grid(diagram4, width=4, number=cost_so_far, start=diagram4.start, goal=diagram4.end)
    print("\nMap_by_numbers graph: ")
    draw_grid(diagram4, width=3, map=diagram4, start=diagram4.start, goal=diagram4.end)
   # print("Open nodes: ")
   # draw_grid(diagram4, width=3, openNo=reconstructOpenNodes(), start=diagram4.start, goal=diagram4.end)
    print("\nReconstruct path: ")
    draw_grid(diagram4, width=3, path=reconstruct_path(came_from, start=diagram4.start, goal=diagram4.end))
    print()

    g = GridWithWeights(40, 10, "2-1")
    # g.walls = DIAGRAM1_WALLS  # long long list this is

    came_from, cost_so_far = dijkstra_search(g, g.start, g.end)
    print("Came_from graph: ")
    draw_grid(g, width=3, point_to=came_from, start=g.start, goal=g.end)
    print("\nCost_so_far graph: ")
    draw_grid(g, width=4, number=cost_so_far, start=g.start, goal=g.end)
    print("\nMap: ")
    draw_grid(g, width=3, map=g, start=g.start, goal=g.end)
    print("\nReconstruct path: ")
    draw_grid(g, width=3, path=reconstruct_path(came_from, start=g.start, goal=g.end))
    print()

    parents = bfs(g, g.start, g.end)
    print("BFS on board 2-1\nCame_from graph")
    draw_grid(g, width=2, point_to=parents, start=g.start, goal=g.end)
    print("Reconstruct path")
    draw_grid(g, width=2, path=reconstruct_path(came_from, start=g.start, goal=g.end))
    print()