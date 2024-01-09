import random 
from collections import defaultdict

#------------------------------------------------------------------
    #Main Function
    #generates an random undirected graph with two parameters (desrciption in the comments in main)

def main():
    #Para1 num_of_nodes: Int
    #Para2 num_of_edges: Int
    #Keep in mind that the number of edges have to be low enough to generate such an graph, otherwise it raises an exception.
    graph = generate_random_graph(10,5)
    #print(graph)
    max_degree = get_maximum_degree(graph)
    #print(max_degree)

    simulate_distributed_coloring(graph, max_degree)


#------------------------------------------------------------------
    #Simulation of our distributed algorithm
    #every node just decides on the informations it would have in an distributed setup.

def simulate_distributed_coloring(graph, maximum_degree):
    num_of_colors = maximum_degree + 1
    uncolored_nodes = list()
    colored_nodes = dict()
    for i in range(len(graph)):
        uncolored_nodes.append(i)
    #print("Uncolored Nodes: " + str(uncolored_nodes))
    #print("Colored Nodes: " + str(colored_nodes))

    iterations = 0

    while uncolored_nodes:
        iterations += 1
        candidate_colors = dict()
        for node in uncolored_nodes:
            available_color = get_available_colors(graph, num_of_colors, colored_nodes, node)
            candidate_colors[node] = random.sample(available_color, 1)
            #print(candidate_colors[node])

        for node in uncolored_nodes:
            if check_if_color_is_unique_in_neigbours(graph, candidate_colors, node):
                uncolored_nodes.remove(node)
                colored_nodes[node] = candidate_colors[node]
        #print("Colored Nodes: " + str(colored_nodes))
                
    myKeys = list(colored_nodes.keys())
    myKeys.sort()
    sorted_colored_nodes = {i: colored_nodes[i] for i in myKeys}

    print("Result:")
    print("Iterations needed: " + str(iterations))
    print("Max Degree: " + str(maximum_degree))
    print("Graph: " + str(graph))
    print("Colors from 0 to " + str(maximum_degree) + " - (" + str(num_of_colors) + " Colors)")
    print("Colored Nodes: " + str(sorted_colored_nodes))

#------------------------------------------------------------------

def generate_random_graph(num_of_nodes, num_of_edges):
    if (num_of_edges > num_of_nodes * (num_of_nodes-1)):
        raise Exception("To many edges in comparison to nodes")
    
    edges = set()
    while len(edges) < num_of_edges:
        u, v = random.sample(range(num_of_nodes), 2)
        if u!=v:
            edges.add((u,v))

    graph = defaultdict(set)
    #print (edges)

    for edge in edges:
        graph[edge[0]].add(edge[1])
        graph[edge[1]].add(edge[0])

    #print(graph)
        
        
    for i in range(num_of_nodes):
       if not (i in graph):
           graph[i].add(None)

    myKeys = list(graph.keys())
    myKeys.sort()
    sorted_graph = {i: graph[i] for i in myKeys}
           
    return sorted_graph

def get_maximum_degree(graph):
    #print(graph)
    #print(len(graph))
    max_degree = 0
    for i in range(len(graph)):
        #print(graph[i])
        if len(graph[i]) > max_degree:
            max_degree = len(graph[i])
        #print(max_degree)
    return max_degree

def check_if_color_is_unique_in_neigbours(graph, candidate_colors, node):
    for neighbour in graph[node]:
        if neighbour in candidate_colors:
            if candidate_colors[neighbour] == candidate_colors[node]:
                return False
    return True

def get_available_colors(graph, num_of_colors, colored_nodes, node):
    colors = list()
    for i in range(num_of_colors):
        colors.append(i)
    #print(colors)
    for neighbour in graph[node]:
        if neighbour == None:
            continue
        if neighbour in colored_nodes:
            #print(colored_nodes)
            #print("color of neighbour: " + str(colored_nodes[neighbour][0]) )
            if colored_nodes[neighbour][0] in colors:
                colors.remove(colored_nodes[neighbour][0])
    #print(colors)
    return colors

if __name__ == '__main__':
    main()