# Create Queue and Graph classes
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, vert_from, vert_to):
        """
        Add a directed edge to the graph.
        """
        if vert_from in self.vertices and vert_to in self.vertices:
            self.vertices[vert_from].add(vert_to)
        else:
            raise IndexError("Vertex is non-existent.")

    def get_neighbors(self, vert):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vert]


def earliest_ancestor(ancestors, starting_node):
    # Create a graph to store our ancestry tree
    g = Graph()
    
    # Assign our relationships and their connections. each pair is (p[0], c[1])
    # We'll add each parent of each pair to the graph, and then add the child to the graph if it hasn't already been added
    # Then, add our edge from child to parent
    for rel in ancestors:
        if rel[0] not in g.vertices:
            g.add_vertex(rel[0])
        if rel[1] not in g.vertices:
            g.add_vertex(rel[1])
        g.add_edge(rel[1], rel[0])

    # With our vertices graph set up, we want to create a queue,
    # and add our starting node to it as a list.
    q = Queue()
    q.enqueue([starting_node])

    # then we'll create a generation counter to keep track of how long our path is,
    # and a first_anc variable for when we find the first known ancestor

    gen = 1
    first_anc = -1

    # as long as we have items in our queue
    while q.size() > 0:

        # first, dequeue the current path we're working on, and get the last vertex from that list
        curr_path = q.dequeue()
        v = curr_path[-1]

        # Now that we have the vertex we're looking for,
        # we can check to see if the ancestor we're on is an older generation than previous
        if len(curr_path) > gen:
            gen = len(curr_path)
            first_anc = v
        # if the ancestor is the same generation, we'll check whether our current node is a lower ID than our last known earliest, as we want to return lowest ID between them
        elif len(curr_path) ==  gen:
            if v < first_anc:
                first_anc = v

        # now that we've determined the relationship of this node compared to our last known node,
        # we can iterate over all of its ancestors, creating a clone of our current path to include and append to our queue
        for anc in g.get_neighbors(v):
            q.enqueue(curr_path + [anc])

    # print(first_anc)
    return first_anc 