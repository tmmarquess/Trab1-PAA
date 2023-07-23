"""
####################################################################################################
classes
####################################################################################################
"""


class Vertex:
    def __init__(self, edge_name: str) -> None:
        self.edge_name = edge_name
        self.adjacency_list = []

    def __str__(self) -> str:
        return f"({self.edge_name})"

    def add_edge(self, destination, cost: float, transportation: str) -> None:
        self.adjacency_list.append(Edge(self, destination, cost, transportation))

    def print_edges(self) -> None:
        print(f"{self}: ", end="")
        for edge in self.adjacency_list:
            print(edge, end=" | ")
        print()


class Edge:
    def __init__(
        self, origin: Vertex, destination: Vertex, cost: float, transportation: str
    ) -> None:
        self.origin = origin
        self.destination = destination
        self.cost = cost
        self.transportation = transportation

    def __str__(self) -> str:
        return (
            f"{self.origin} -> {self.destination} [{self.cost}] {self.transportation}"
        )


"""
####################################################################################################
Funções
####################################################################################################
"""


def create_vertex(vertex_name):
    new_vertex = Vertex(vertex_name)
    vertex_list.update({vertex_name: new_vertex})
    return new_vertex


def print_graph(graph):
    for key in graph.keys():
        graph.get(key).print_edges()


def dijkstra(vertexes: dict, start: Vertex, end: Vertex):
    distance = {key: float("inf") for key in vertexes.keys()}
    visited = {key: False for key in vertexes.keys()}

    distance[start.edge_name] = 0

    while False in list(visited.values()):
        minimal_distance = float("inf")
        minimal_key: str

        for unvisited_vertex in [
            key for key, visited in visited.items() if not visited
        ]:
            if distance[unvisited_vertex] <= minimal_distance:
                minimal_distance = distance[unvisited_vertex]
                minimal_key = unvisited_vertex

        visited[minimal_key] = True

        if distance[minimal_key] != float("inf"):
            for adjacent in vertexes[minimal_key].adjacency_list:
                if (
                    not visited[adjacent.destination.edge_name]
                    and distance[minimal_key] + adjacent.cost
                    < distance[adjacent.destination.edge_name]
                ):
                    distance[adjacent.destination.edge_name] = (
                        distance[minimal_key] + adjacent.cost
                    )

    print("====================================================")
    print(f"{start} ==> {end} {distance[end.edge_name]}")


"""
####################################################################################################
Função principal
####################################################################################################
"""

vertex_list = dict()
temp_list = []
bus_waiting_list = []

# Reading distances input
while True:
    try:
        edge = input()
    except EOFError:
        break

    if len(edge) == 0:
        break

    origin, destination, transportation, cost = edge.split()
    temp_list.append(
        dict(
            origin=origin,
            destination=destination,
            transportation=transportation,
            cost=float(cost),
        )
    )

# Reading Bus time input
while True:
    try:
        edge = input()
    except EOFError:
        break

    if len(edge) == 0:
        break

    bus_line, cost = edge.split()
    bus_waiting_list.append(dict(bus_line=bus_line, cost=float(cost)))


# Reading source and destination
source, destination = input().split()

# Adding bus waiting time to final cost
for bus_waiting in bus_waiting_list:
    for edge in temp_list:
        if edge["transportation"] == bus_waiting["bus_line"]:
            edge["cost"] += bus_waiting["cost"]

# Creating graph
for edge in temp_list:
    origin_vertex = vertex_list.get(edge["origin"], None)
    destination_vertex = vertex_list.get(edge["destination"], None)

    if not origin_vertex:
        origin_vertex = create_vertex(edge["origin"])

    if not destination_vertex:
        destination_vertex = create_vertex(edge["destination"])

    origin_vertex.add_edge(destination_vertex, edge["cost"], edge["transportation"])


print_graph(vertex_list)

dijkstra(vertex_list, vertex_list[source], vertex_list[destination])
