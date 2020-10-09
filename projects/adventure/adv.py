from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


# We'll create a dictionary to store our rooms we've discovered; rooms will be our keys, connections our values
# Then, we need a list to store our path; this will store our backtracking for our dft.
visited = {}
bt = []

# We save our options for movements as k/v pairs. As we move, we can append the value of that key to our bt list
opps = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

# We start at 0 index of any given maze as our current id; 
# the value will be the initial ? values for each room
visited[player.current_room.id] = player.current_room.get_exits()

# Now we check the length of rooms we've visited against the total rooms we're receiving for our map size;
# as long as we have rooms left to visit:
while len(visited) < len(room_graph):

    # If our current room hasn't been visited yet
    if player.current_room.id not in visited:

        # We want to add our current room as visited
        # and set our previous room as the last room in our backtrack list
        visited[player.current_room.id] = player.current_room.get_exits()
        previousRoom = bt[-1]

        # Then we can remove our previous room as one of the possible exits we can go down
        visited[player.current_room.id].remove(previousRoom)

    # once the current room has been visited
    # and if we have exits left to visit
    elif len(visited[player.current_room.id]) > 0:
        # We'll pop off the next room we'll visit and add it to the path we're traversing over
        nextRoom = visited[player.current_room.id].pop()
        traversal_path.append(nextRoom)

        # For our backtracking, we'll add the opposite direction of where our next room is going.
        # Then, we'll move to the next room and do checks on it
        bt.append(opps[nextRoom])
        player.travel(nextRoom)

    # If we've iterated over all of our current room's exits
    elif len(visited[player.current_room.id]) == 0:
        # We'll grab our previous room from our backtrack
        previousRoom = bt.pop()

        # Then we'll add it to our path we've traversed over
        # and travel back to it
        traversal_path.append(previousRoom)
        player.travel(previousRoom)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited, path taken: {traversal_path}")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
