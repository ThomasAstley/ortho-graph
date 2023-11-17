#!/bin/env python
# License: GNU GPL version 3

import sys
import yaml
import pprint
import json
import statistics
import numpy as np
import random
import copy
from   optparse import OptionParser

HORIZONTAL = True
X_AXIS     = 0
Y_AXIS     = 1

def load_graphs(file_path):
    with open(file_path) as stream:
        try:
            graph_descriptions = yaml.safe_load(stream)
        except yaml.YAMLError as exception:
            print(exception)
            exit(10)
    
    return parse_graph_descriptions(graph_descriptions)


def parse_graph_descriptions(graph_descriptions):
    graphs = {}

    for graph_name in graph_descriptions:
        graph                 = graph_descriptions[graph_name]

        edges                 = []
        discovered_node_names = {*graph}
        connected_nodes       = dict()

        for node_name in graph:
            node = graph[node_name]

            if connected_nodes.get(node_name) == None:
                connected_nodes[node_name] = []

            for target_node_name in node:
                edges.append({node_name: target_node_name})

                if connected_nodes.get(target_node_name) == None:
                    connected_nodes[target_node_name] = []

                connected_nodes[node_name].append(target_node_name)

                if target_node_name not in discovered_node_names:
                    discovered_node_names.add(target_node_name)
                    connected_nodes[target_node_name].append(node_name)
                else:
                    connected_nodes[target_node_name].append(node_name)
        
        for node_name in discovered_node_names.difference({*graph}):
            graph[node_name] = []

        graphs[graph_name] = { 'edges': edges, 'nodes': connected_nodes } 

    return graphs 


def print_graph(data):
    pt = PrettyPrintTree()
    pt.print_json(data, orientation=PrettyPrintTree.Horizontal)


def new_coordinate(src_coordinate, node_name, used_coordinates):    
    offsets        = [(0,3), (3,0), (0,-3), (-3,0)]
    offset_index   = 0

    new_coordinate = src_coordinate

    while new_coordinate in used_coordinates:
        new_coordinate = (src_coordinate[0] + offsets[offset_index][0], src_coordinate[1] + offsets[offset_index][1])
        offset_index += 1
        
        if offset_index > 3:
            for position, offset in enumerate(offsets):
                if offset[0] > 0:
                    offset_x = offset[0] + 3
                elif offset[0] < 0:
                    offset_x = offset[0] - 3
                else:
                    offset_x = 0

                if offset[1] > 0:
                    offset_y = offset[1] + 3
                elif offset[1] < 0:
                    offset_y = offset[1] - 3
                else:
                    offset_y = 0

                offsets[position] = (offset_x, offset_y)

            offset_index = 0

    return new_coordinate


def place_nodes(graphs):
    simulate_annealing(graphs)


def simulate_annealing(graphs):
    for graph_name, graph in graphs.items():
        min_grid_size       = 10 * np.sqrt(len(graph['nodes']))
        grid_upper_boundary = int(2.5 * min_grid_size)
        grid_lower_boundary = int(-2.5 * min_grid_size)

        place_nodes_random(graph, grid_upper_boundary, grid_lower_boundary)
        debug_to_file('randomly placed nodes:       ' + str(graph['placed nodes']))

        temperature          = 2 * min_grid_size
        cooling_rate         = 0.95
        compact_direction    = HORIZONTAL

        while temperature > 1:
            move_nodes_to_neighbours_median(graph, temperature, grid_lower_boundary, grid_upper_boundary)

            temperature *= cooling_rate

        # compact_grid(graph, HORIZONTAL, 1)
        # compact_grid(graph, not HORIZONTAL, 1)

        debug_to_file('placed nodes:                 ' + str(graph['placed nodes']))
        
        graphs_copy = copy.deepcopy(graphs)
        placed_nodes_copy = graphs_copy[graph_name]['placed nodes']
        canonize_placed_nodes(placed_nodes_copy)

        debug_to_file('canonized placed nodes:       ' + str(placed_nodes_copy))

        if options.json_before_sizing: generate_json(graphs_copy, options.json_before_sizing)
        
        remove_empty_spaces(graph['placed nodes'])

        # Transform nodes to their true size
        place_according_to_size(graph['placed nodes'])

        # compact resized nodes

        if options.debug: print('placed nodes sized:  ', graph['placed nodes'])

        canonize_placed_nodes(graph['placed nodes'])
        debug_to_file('canonized placed nodes sized: ' + str(graph['placed nodes']))
        

def get_nodes_to_the_right(pivot_node, nodes, placed_nodes):
    for node in nodes:
        if placed_nodes.get(node) == None:
            placed_nodes[node] = copy.deepcopy(nodes[node])
    
    return filter(lambda node: placed_nodes[pivot_node][0] < placed_nodes[node][0], placed_nodes)


def get_nodes_below(pivot_node, nodes, placed_nodes):
    for node in nodes:
        if placed_nodes.get(node) == None:
            placed_nodes[node] = copy.deepcopy(nodes[node])
    
    return filter(lambda node: placed_nodes[pivot_node][1] > placed_nodes[node][1], placed_nodes)


def place_according_to_size(nodes):
    processed_x = {}
    processed_y = {}
    
    placed_nodes = {}

    for pivot_node in nodes:
        # move any nodes to the right by the width of the pivot_node in the x direction
        if processed_x.get(nodes[pivot_node][0]) == None:
            for node_right in get_nodes_to_the_right(pivot_node, nodes, placed_nodes):
                org = str(placed_nodes[node_right])
                placed_nodes[node_right][0] += 4

        processed_x[nodes[pivot_node][0]] = True

        # move any nodes under by the height of the pivot_node in the y direction
        if processed_y.get(nodes[pivot_node][1]) == None:
            for node_under in get_nodes_below(pivot_node, nodes, placed_nodes):
                org = str(placed_nodes[node_under])
                placed_nodes[node_under][1] -= 2

        processed_y[nodes[pivot_node][1]] = True

    for placed_node in placed_nodes:
        nodes[placed_node] = placed_nodes[placed_node]
        

def compact_grid(graph, direction, distance_between_nodes):
    nodes = graph['placed nodes']

    # make nodes equidistant using distance_between_nodes
    if direction == HORIZONTAL:
        for node in nodes:
            nodes_same_y      = filter(lambda filtered_node: nodes[filtered_node][1] == nodes[node][1] , nodes)
            x_sorted_nodes    = sorted(nodes_same_y, key = lambda x_node: nodes[x_node][0])
            middle_node_index = round(len(x_sorted_nodes) / 2)
            
            # move nodes to the right
            for index in range(middle_node_index + 1, len(x_sorted_nodes)):
                node           = x_sorted_nodes[index]
                previous_node  = x_sorted_nodes[index - 1]
                nodes[node][0] = nodes[previous_node][0] + distance_between_nodes

            # move nodes to the left
            for index in reversed(range(0, middle_node_index)):
                node           = x_sorted_nodes[index]
                previous_node  = x_sorted_nodes[index - 1]
                nodes[node][0] = nodes[previous_node][0] - distance_between_nodes
    else:
        for node in nodes:
            nodes_same_x      = filter(lambda filtered_node: nodes[filtered_node][0] == nodes[node][0] , nodes)
            y_sorted_nodes    = sorted(nodes_same_x, key = lambda y_node: nodes[y_node][1])
            middle_node_index = round(len(y_sorted_nodes) / 2)
            
            # move nodes to above
            for index in range(middle_node_index + 1, len(y_sorted_nodes)):
                node           = y_sorted_nodes[index]
                previous_node  = y_sorted_nodes[index - 1]
                nodes[node][1] = nodes[previous_node][1] + distance_between_nodes

            # move nodes to the left
            for index in reversed(range(0, middle_node_index)):
                node           = y_sorted_nodes[index]
                previous_node  = y_sorted_nodes[index - 1]
                nodes[node][1] = nodes[previous_node][1] - distance_between_nodes


def remove_empty_spaces(nodes):
    remove_empty_spaces_on_axis(nodes, X_AXIS)
    remove_empty_spaces_on_axis(nodes, Y_AXIS)


def remove_empty_spaces_on_axis(nodes, axis):
    sorted_nodes = sorted(nodes, key = lambda node: nodes[node][axis])
    minimum      = nodes[sorted_nodes[0]][axis]
    maximum      = nodes[sorted_nodes[-1]][axis]

    empty_lines = 0
    for line in range(minimum, maximum + 1):
        nodes_in_line = list(get_nodes_at_axis(nodes, axis, line))

        if not nodes_in_line:
            empty_lines += 1
        else:
            for node in nodes_in_line:
                nodes[node][axis] -= empty_lines


def get_nodes_at_axis(nodes, axis, coordinate):
    return filter(lambda node: nodes[node][axis] == coordinate, nodes)
        

def compact_coefficient(annealing_iterations, current_iteration):
    magic = 1 + ( (2 * (annealing_iterations - current_iteration - 30)) / (0.5 * annealing_iterations) )

    return max(1, magic)


def move_nodes_to_neighbours_median(graph, temperature, grid_lower_boundary, grid_upper_boundary):
    for node_name, neighbours in graph['nodes'].items():
        if len(neighbours) == 0:
            continue

        neighbours_x = []
        neighbours_y = []
        
        for neighbour in neighbours:
            neighbours_x.append(graph['placed nodes'][neighbour][0])
            neighbours_y.append(graph['placed nodes'][neighbour][1])
        
        random_x = random.uniform(-temperature, temperature)
        x        = np.clip(int(statistics.median(neighbours_x) + random_x ), grid_lower_boundary, grid_upper_boundary)

        random_y = random.uniform(-temperature, temperature)
        y        = np.clip(int(statistics.median(neighbours_y) + random_y ), grid_lower_boundary, grid_upper_boundary)

        place_nearby(graph, node_name, int(x), int(y), grid_lower_boundary, grid_upper_boundary)
        

def place_nearby(graph, node_name, x, y, grid_lower_boundary, grid_upper_boundary):
    coordinates_in_use = graph['placed nodes'].values()

    radius = 0

    while True:
        surrounding_coordinates_list = surrounding_coordinates(x, y, radius, grid_lower_boundary, grid_upper_boundary)
        coordinates_not_in_use       = []

        for coordinate in surrounding_coordinates_list:
            if coordinate not in coordinates_in_use:
                coordinates_not_in_use.append(coordinate)

        if len(coordinates_not_in_use) > 0:
            graph['placed nodes'][node_name] = coordinates_not_in_use[0]
            return

        radius += 1


def move_nodes_to_neighbours_median2(graph, temperature, grid_lower_boundary, grid_upper_boundary):
    for node_name, neighbours in graph['nodes'].items():
        
        if len(neighbours) == 0:
            continue

        # height = node['height']
        # width = node['width']
        height = 3 
        width = 5

        neighbours_x = []
        neighbours_y = []

        # todo - avoid looping through neighbours repeatedly  

        for neighbour in neighbours:
            neighbours_x.append(graph['placed nodes'][neighbour][0])
            neighbours_y.append(graph['placed nodes'][neighbour][1])
        
        random_x = random.uniform(-temperature * width, temperature * width)
        x        = np.clip(int(statistics.median(neighbours_x) + random_x), grid_lower_boundary, grid_upper_boundary)

        random_y = random.uniform(-temperature * height, temperature * height)
        y        = np.clip(int(statistics.median(neighbours_y) + random_y), grid_lower_boundary, grid_upper_boundary)

        place_nearby(graph, node_name, int(x), int(y), grid_lower_boundary, grid_upper_boundary)


def place_nodes_random(graph, grid_upper_boundary, grid_lower_boundary):
    used_coordinates      = set()
    graph['placed nodes'] = {}
    
    for node in graph['nodes']:
        node_placed = False

        while not node_placed: 
            x = int(random.uniform(grid_lower_boundary, grid_upper_boundary))
            y = int(random.uniform(grid_lower_boundary, grid_upper_boundary))
            
            if (x,y) not in used_coordinates:
                graph['placed nodes'][node] = [x, y]
                used_coordinates.add((x, y))
                node_placed = True


def place_nodes_in_circles(graphs):
    for graph in graphs.values():

        used_coordinates = set()
        placed_nodes     = {}

        for node_name, connected_nodes in graph['nodes'].items():
            if placed_nodes.get(node_name) == None:
                node_coordinate = new_coordinate((0, 0), node_name, used_coordinates)

                placed_nodes[node_name] = node_coordinate
                used_coordinates.add(node_coordinate)
            
            for connected_node in connected_nodes:
                if placed_nodes.get(connected_node) == None:
                    connected_node_coordinates = new_coordinate(placed_nodes[node_name], connected_node, used_coordinates)

                    placed_nodes[connected_node] = connected_node_coordinates
                    used_coordinates.add(connected_node_coordinates)
                   
        graph['placed nodes'] = {}

        for node_name, coordinate in placed_nodes.items():
            graph['placed nodes'][node_name] = list(coordinate)


def surrounding_coordinates(x, y, radius, grid_lower_boundary, grid_upper_boundary):
    surrounding_coordinates = []

    if radius == 0: return [[x, y]]

    for s_x in range(x - radius, x + radius + 1):
        if grid_lower_boundary <= y + radius <= grid_upper_boundary and grid_lower_boundary <= s_x <= grid_upper_boundary:
            surrounding_coordinates.append([s_x, y + radius])

        if grid_lower_boundary <= y - radius <= grid_upper_boundary and grid_lower_boundary <= s_x <= grid_upper_boundary:
            surrounding_coordinates.append([s_x, y - radius])
    
    for s_y in range((y - radius) + 1, y + radius):
        if grid_lower_boundary <= x + radius <= grid_upper_boundary and grid_lower_boundary <= s_y <= grid_upper_boundary:
            surrounding_coordinates.append([x + radius, s_y])

        if grid_lower_boundary <= x - radius <= grid_upper_boundary and grid_lower_boundary <= s_y <= grid_upper_boundary:
            surrounding_coordinates.append([x - radius, s_y])

    return surrounding_coordinates


def canonize_graphs_placed_nodes(graphs):
    for graph in graphs.values():
        canonize_placed_nodes(graph['placed nodes'])


def canonize_placed_nodes(placed_nodes):
    min_x = 0
    min_y = 0

    for coordinate in placed_nodes.values():
        if coordinate[0] < min_x: min_x = coordinate[0]

        if coordinate[1] < min_y: min_y = coordinate[1]

    for coordinate in placed_nodes.values():
        coordinate[0] -= min_x
        coordinate[1] -= min_y


def debug_to_file(text):
    if options.debug_file:
        f = open(options.debug_file, "a")
        f.write(text + '\n')
        f.close()


def debug(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def generate_json(graphs, file='stdout'):
    if file == 'stdout':
        print(json.dumps(graphs))
    else:
        f = open(file, "w")
        f.write(json.dumps(graphs))
        f.close()


def main():
    parser = OptionParser()

    parser.add_option("-f",                   "--file",                  dest="file_path", metavar="graph_description.yaml")
    parser.add_option("--json",               action="store_true",       dest="json",      help="Output json to stdout")
    parser.add_option("--debug",              action="store_true",       dest="debug",     help="Debug output")
    parser.add_option("--json_before_sizing", dest="json_before_sizing", help="Output json to file before sizing")
    parser.add_option("--debug_file",         dest="debug_file",         help="debug output to file")

    global options
    (options, args) = parser.parse_args()

    if options.file_path is None:
        print("Usage: ortho-graph graph_description.yaml")
        exit(2)

    graphs = load_graphs(options.file_path)

    place_nodes(graphs)
    canonize_graphs_placed_nodes(graphs)

    if options.json:
        generate_json(graphs)
    

if __name__ == '__main__':
    main()

