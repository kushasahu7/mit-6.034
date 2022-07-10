# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    True values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    q = [];
    q.append((start, [start]))
    v= {}
    if start == goal:
        return [start]
    while len(q) >0:
        node, path = q.pop(0)
        if v.get(node, False) == False:
            v[node] = True;
            #print("Running for", node , "now for goal", goal)
            #print("rest of q",q)
            nodes = graph.get_connected_nodes(node)
            #print("chilren", nodes)
            for n in nodes:
                #print("v[n[", v.get(n, False))
                if v.get(n, False) == False:
                    #print(n,"not visited")
                    q.append((n, path+[n]))
                    #print("added in Q", q)
                    #v[n] = True;
                    if(n == goal):
                        #print("found yay", n, path)
                        return path+[n]

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    q = [];
    q.append((start, [start]))
    v= {}
    if start == goal:
        return [start]
    while len(q) >0:
        node, path = q.pop(0)
        if v.get(node, False) == False:
            v[node] = True;
            #print("Running for", node , "now for goal", goal)
            #print("rest of q",q)
            nodes = graph.get_connected_nodes(node)
            #print("chilren", nodes)
            for n in nodes:
                #print("v[n[", v.get(n, False))
                if v.get(n, False) == False:
                    #print(n,"not visited")
                    q.insert(0,(n, path+[n]))
                    #print("added in Q", q)
                    #v[n] = True;
                    if(n == goal):
                        #print("found yay", n, path)
                        return path+[n]


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    q = [];
    q.append((start, [start]))
    v= {}
    if start == goal:
        return [start]
    while len(q) >0:
        node, path = q.pop(0)
        if v.get(node, False) == False:
            v[node] = True;
            #print("Running for", node , "now for goal", goal)
            #print("rest of q",q)
            nodes = sorted(graph.get_connected_nodes(node), key=lambda x:graph.get_heuristic(x,goal), reverse=True)
            #print("chilren", sorted(graph.get_connected_nodes(node), key=lambda x:graph.get_heuristic(x,goal), reverse=True))
            for n in nodes:
                #print("v[n[", v.get(n, False))
                if v.get(n, False) == False:
                    #print(n,"not visited")
                    q.insert(0,(n, path+[n]))
                    #print("added in Q", q)
                    #v[n] = True;
                    if(n == goal):
                        #print("found yay", n, path)
                        return path+[n]

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    #print("goal, bw", goal, beam_width)
    q = [];
    level = 0
    q.append((start, [start], level))
    v= {}
    if start == goal:
        return [start]
    while len(q) >0:
        node, path,level = q.pop(0)
        if(node==goal):
            return path
        if v.get(node, False) == False:
            v[node] = True;
            #print("Running for", node , "now for goal", goal)
            #print("rest of q",q)
            nodes = graph.get_connected_nodes(node);

            #print("chilren", nodes)
            for n in nodes:
                #print("v[n[", v.get(n, False))
                if v.get(n, False) == False:
                    #print(n,"not visited")
                    q.append((n, path+[n], level+1))
                    #print("added in Q", q)
                    #v[n] = True;
                    # if(n == goal):
                    #     #print("found yay", n, path)
                    #     return path+[n]
            q = sorted(q, key=lambda x:(x[2],graph.get_heuristic(x[0],goal)))[0:beam_width]
            #print("now q", q)
    return []                    

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    prev = None
    sum = 0
    #print("finding path le in", node_names)
    for n in node_names:
        if prev is not None:
            edge = graph.get_edge(prev,n)
            #print(edge.length)
            sum+=edge.length
        prev= n
    return sum


def branch_and_bound(graph, start, goal):
    #print("goal, bw", goal)
    q = [];
    q.append((start, [start], 0))
    v= {}
    if start == goal:
        return [start]
    while len(q) >0:
        node, path,cost = q.pop(0)
        if(node==goal):
            return path
        if v.get(node, False) == False:
            v[node] = True;
            #print("Running for", node , "now for goal", goal)
            #print("rest of q",q)
            nodes = graph.get_connected_nodes(node);

            #print("chilren", nodes)
            for n in nodes:
                #print("v[n[", v.get(n, False))
                if v.get(n, False) == False:
                    #print(n,"not visited")
                    q.append((n, path+[n], cost+graph.get_edge(node,n).length))
                    #print("added in Q", q)
                    #v[n] = True;
                    # if(n == goal):
                    #     #print("found yay", n, path)
                    #     return path+[n]
            q = sorted(q, key=lambda x:(x[2]))
            #print("now q", q)
    return []

def a_star(graph, start, goal):
    #print("goal, bw", goal)
    q = [];
    q.append((start, [start], 0))
    v= {}
    if start == goal:
        return [start]
    while len(q) >0:
        node, path,cost = q.pop(0)
        if(node==goal):
            return path
        if v.get(node, False) == False:
            v[node] = True;
            #print("Running for", node , "now for goal", goal)
            #print("rest of q",q)
            nodes = graph.get_connected_nodes(node);

            #print("chilren", nodes)
            for n in nodes:
                #print("v[n[", v.get(n, False))
                if v.get(n, False) == False:
                    #print(n,"not visited")
                    q.append((n, path+[n], cost+graph.get_edge(node,n).length+graph.get_heuristic(n,goal)))
                    #print("added in Q", q)
                    #v[n] = True;
                    # if(n == goal):
                    #     #print("found yay", n, path)
                    #     return path+[n]
            q = sorted(q, key=lambda x:(x[2]))
            #print("now q", q)
    return []


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    nodes = graph.nodes
    for n in nodes:
        paths = branch_and_bound(graph, n, goal)
        if path_length(graph, paths) < graph.get_heuristic(n,goal):
            return False
    return True

def is_consistent(graph, goal):
    edges = graph.edges
    for e in edges:
        if e.length < abs(graph.get_heuristic(e.node1, goal)-graph.get_heuristic(e.node2, goal)):
            return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '4'
WHAT_I_FOUND_INTERESTING = 'NA'
WHAT_I_FOUND_BORING = 'NA'
