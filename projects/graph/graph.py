"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

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

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """

        bft_q = Queue()
        visited = set()

        #  Add the starting vert to the queue
        bft_q.enqueue(starting_vertex)

        #  As long as there are items in the queue
        while bft_q.size() > 0:
            # Remove the first item from our queue, 
            # and check if we've visited it
            vertex = bft_q.dequeue()

            if vertex not in visited:
                # If this is a newly visited node,
                # add it to our visited list
                # and add new neighbors to queue
                print(f'{vertex}')
                visited.add(vertex)

                for neighbor in self.get_neighbors(vertex):
                    bft_q.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """

        bft_s = Stack()

        visited = set()

        #  Add the starting node to the stack
        bft_s.push(starting_vertex)

        #  As long as there are items in the stack,
        while bft_s.size() > 0:
            # Pop the last item from our stack, 
            # and check if we've visited it
            vertex = bft_s.pop()

            #  If we haven't
            if vertex not in visited:
                # Print the node
                # Add to visited list
                # And then add all neighbors to the stack
                print(f'{vertex}')
                visited.add(vertex)
                for neighbor in self.get_neighbors(vertex):
                    bft_s.push(neighbor)

    def dft_recursive(self, starting_vertex, visited = None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        This should be done using recursion.
        """

        # We first check whether we have a visited set
        # if we get one from our params, we'll use that, otherwise create a new one
        if visited is None:
            visited = set()

        # for each node, print out the vertex location and get all of that vertex's neighbors
        # then add this node to our visited list
        print(f'{starting_vertex}')

        neighbors = self.get_neighbors(starting_vertex)
        visited.add(starting_vertex)

        # with that done, for every node we receive from our get_neighbors function (as long as it's not already visited), run recursion on that node, passing in our visited set
        for vertex in neighbors:
            if vertex not in visited:
                self.dft_recursive(vertex, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """

        path = Queue()
        visited = set()

        # Add the starting vert to the path queue
        # this vert will be made into a list which we'll append and subscript over
        path.enqueue([starting_vertex])


        # As long as we have items in our queue
        while path.size() > 0:
            # Remove our first path item
            # and grab the last vertex from that path
            check_path = path.dequeue()
            lv = check_path[-1]
            
            # If that vertex hasn't been visited
            if lv not in visited:
                # check if it's the vertex we're searching for
                if lv is destination_vertex:
                    # if it is we'll return our whole path
                    return check_path
                # if not, add the vertex to our visited set
                # then get the neighbors for it.
                visited.add(lv)
                neighbors = self.get_neighbors(lv)

                # finally for each neighbor we get back
                for neighbor in neighbors:
                    # we'll use the path we are currently checking to create unique paths,
                    # and append the    neighbor to the ends of their corresponding copies
                    # then add the clone to the end of our queue
                    cp_clone = check_path + [neighbor]
                    path.enqueue(cp_clone)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """   
        path = Stack()
        visited = set()

        if starting_vertex == destination_vertex:
            visited.add(starting_vertex)
            return list(visited)

        # Add the starting vertex to the path queue
        path.push(starting_vertex)

        # As long as our stack isn't empty
        while path.size() > 0:
            # Pop the most recently added vertex and 
            # Add it to the visited set
            vert_check = path.pop()
            visited.add(vert_check)

            # Use the get_neighbors method to find all next nodes
            neighbors = self.get_neighbors(vert_check)

            # For each node in our list
            for neighbor in neighbors:
                # if we haven't visited the neighbor before, push it onto our stack
                if neighbor not in visited:
                   path.push(neighbor)
                # before escaping the loop, check if the neighbor is our destination;
                # if it is, append it to the end of visited and return visited as a list
                if neighbor is destination_vertex:
                    visited.add(neighbor)
                    return list(visited)

    def dfs_recursive(self, starting_vertex, destination_vertex, visited = None, path= None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        # We first check whether we have a visited set
        # if we get one from our params, we'll use that, otherwise create a new one
        if visited is None:
            visited = set()
        # then do the same with our path
        if path is None:
            path = []

        # first add our starting vertex to our visited set and path list
        #NOTE: for our path, we want to create copies during each iteration.
        # that way if we encounter a dead end we don't break the path we were on
        visited.add(starting_vertex)
        path = path + [starting_vertex] 

        # then check if our current starting vertex is our search. if it is return our path to get here.
        if starting_vertex == destination_vertex:
            return path

        # after we've checked our search we want to get all of our neighbors and iterate over them
        neighbors = self.get_neighbors(starting_vertex)

        for neighbor in neighbors:
            # if we encounter a neighbor that we havent visited we'll run recursion to include it in our path. if we encounter our destination, we'll return it. if not then we will return None and go back along our search until we do
            if neighbor not in visited:
                path_check = self.dfs_recursive(neighbor, destination_vertex, visited, path)
                if path_check is not None:
                    return path_check
        return None

        
if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
