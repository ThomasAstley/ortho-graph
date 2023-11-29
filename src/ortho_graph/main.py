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
import subprocess
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
        graphs[graph_name]    = {} 

        graph                 = graph_descriptions[graph_name]

        discovered_node_names = {*graph}
        connected_nodes       = dict()

        for node_name in graph:
            node = graph[node_name]

            if connected_nodes.get(node_name) == None:
                connected_nodes[node_name] = []

            for target_node_name in node:
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

        for node_name in discovered_node_names:
            node = {'name': node_name, 
                    'edges': list(graph[node_name]),
                    'neighbours': connected_nodes[node_name]}

            graphs[graph_name][node_name] = node 

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
        min_nodes_grid       = np.sqrt(len(graph))
        min_grid_size       = 2 * min_nodes_grid

        grid_upper_boundary = int(2.5 * min_grid_size)
        grid_lower_boundary = int(-2.5 * min_grid_size)

        place_nodes_random(graph, grid_upper_boundary, grid_lower_boundary)
        # debug_to_file('randomly placed nodes:       ' + str(graph))

        temperature          = 2 * min_grid_size
        cooling_rate         = 0.80
        compact_direction    = HORIZONTAL

        while temperature > 1:
            move_nodes_to_neighbours_median(graph, temperature, grid_lower_boundary, grid_upper_boundary)
            
            # display_graph_in_asciio(graph, grid_upper_boundary)

            temperature *= cooling_rate

        debug_to_file('placed nodes:                 ' + str(graph))
        
        graphs_copy = copy.deepcopy(graphs)
        graph_copy = graphs_copy[graph_name]
        canonize_node_positions(graph_copy)

        debug_to_file('canonized placed nodes:       ' + str(graph_copy))

        if options.json_before_sizing: generate_json(graphs_copy, options.json_before_sizing)
        
        compact_graph(graph)

        # Transform nodes to their true size
        place_according_to_size(graph)

        # compact resized nodes

        if options.debug: print('placed nodes sized:  ', str(graph))

        canonize_node_positions(graph)
        debug_to_file('canonized placed nodes sized: ' + str(graph))
        
import time
def display_graph_in_asciio(graph, grid_upper_boundary, current_node, median_x, median_y):
    script  = bytes("stop_updating_display ;", 'utf-8')
    script += bytes("select_all_elements ; delete_selected_elements ;", 'utf-8')

    info = {}
    info['grid_upper_boundary'] = grid_upper_boundary
    info['current_node'] = current_node
    info['median_x'] = median_x
    info['median_y'] = median_y

    result = subprocess.run(
                ["json_dtd_to_asciio_script", "info:", "30", "0", "", "1"], 
                input=bytes(json.dumps(info), 'utf-8'), 
                capture_output = True)

    script += result.stdout

    script += graph_to_asciio_script(graph, grid_upper_boundary, 0)

    median_node = {}
    median_node['x'] = {'name': 'x', 'position': [median_x, median_y]}

    script += graph_to_asciio_script(median_node, grid_upper_boundary, 0)
    
    script += bytes("start_updating_display ;", 'utf-8')

    subprocess.run(["xh", "-f", "POST", "http://localhost:4444/script",  bytes("script=", 'utf-8') + script])

    time.sleep(0.005)


def graph_to_asciio_script(graph, boundary, box):
    object_type = 'new_box' if box else 'new_text'

    script = bytes(
                "create_undo_snapshot ;\n" +
                "delete_all_ruler_lines ;\n" +
                "add_ruler_line 'vertical',"   + str(boundary)     + ";\n" +
                "add_ruler_line 'horizontal'," + str(boundary + 1) + ";\n", 'utf-8') 

    for node in graph.values():
        position  = node['position']
        node_name = node['name']

        script += bytes(
                    ("add '%s', " + object_type + "(TEXT_ONLY =>'%s'), %d, %d ;\n") % 
                        (node_name, node_name, position[0] + boundary, -position[1] + boundary ), 
                    'utf-8')

    return script


def get_nodes_to_the_right(pivot_node, placed_nodes):
    return filter(lambda node: placed_nodes[pivot_node['name']][X_AXIS] < placed_nodes[node][X_AXIS], placed_nodes)


def get_nodes_below(pivot_node, placed_nodes):
    return filter(lambda node: placed_nodes[pivot_node['name']][Y_AXIS] > placed_nodes[node][Y_AXIS], placed_nodes)


def place_according_to_size(graph):
    processed_x  = {}
    processed_y  = {}
    placed_nodes = {}
    
    for node_name in graph:
        placed_nodes[node_name] = copy.deepcopy(graph[node_name]['position'])

    nodes = []
    for node_name in graph:
        nodes.append(graph[node_name])

    for pivot_node in nodes:
        # move any nodes to the right by the width of the pivot_node in the x direction
        if processed_x.get(pivot_node['position'][X_AXIS]) == None:
            for node_right in get_nodes_to_the_right(pivot_node, placed_nodes):
                placed_nodes[node_right][X_AXIS] += 4

        processed_x[pivot_node['name']] = True

        # move any nodes under by the height of the pivot_node in the y direction
        if processed_y.get(pivot_node['position'][Y_AXIS]) == None:
            for node_under in get_nodes_below(pivot_node, placed_nodes):
                placed_nodes[node_under][Y_AXIS] -= 2

        processed_y[pivot_node['name']] = True

    for placed_node_name in placed_nodes:
        graph[placed_node_name]['position'] = placed_nodes[placed_node_name]
        

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


def compact_graph(graph):
    compact_graph_on_axis(graph, X_AXIS)
    compact_graph_on_axis(graph, Y_AXIS)


def compact_graph_on_axis(graph, axis):
    nodes = []
    for node_name in graph:
        nodes.append(graph[node_name])

    sorted_nodes = sorted(nodes, key = lambda node: node['position'][axis])
    minimum      = sorted_nodes[0]['position'][axis]
    maximum      = sorted_nodes[-1]['position'][axis]

    empty_lines = 0
    for line in range(minimum, maximum + 1):
        nodes_in_line = list(get_nodes_at_axis(nodes, axis, line))

        if not nodes_in_line:
            empty_lines += 1
        else:
            for node in nodes_in_line:
                node['position'][axis] -= empty_lines


def get_nodes_at_axis(nodes, axis, coordinate):
    return filter(lambda node: node['position'][axis] == coordinate, nodes)
        

def compact_coefficient(annealing_iterations, current_iteration):
    magic = 1 + ( (2 * (annealing_iterations - current_iteration - 30)) / (0.5 * annealing_iterations) )

    return max(1, magic)


def move_nodes_to_neighbours_median(graph, temperature, grid_lower_boundary, grid_upper_boundary):
    for node_name, node in graph.items():
        if not node['neighbours']:
            # debug('Node: ', node_name, ' has no neighbours')
            place_nearby(graph, node_name, 0, 0, grid_lower_boundary, grid_upper_boundary)
            continue

        neighbours_x = []
        neighbours_y = []
        
        for neighbour in node['neighbours']:
            neighbours_x.append(graph[neighbour]['position'][X_AXIS])
            neighbours_y.append(graph[neighbour]['position'][Y_AXIS])
        
        random_x = random.uniform(-temperature, temperature)
        median_x = statistics.median(neighbours_x)
        x        = np.clip(int(median_x + random_x), grid_lower_boundary, grid_upper_boundary)

        random_y = random.uniform(-temperature, temperature)
        median_y = statistics.median(neighbours_y)
        y        = np.clip(int(median_y + random_y), grid_lower_boundary, grid_upper_boundary)

        display_graph_in_asciio(graph, grid_upper_boundary, node_name, median_x, median_y)

        place_nearby(graph, node_name, int(x), int(y), grid_lower_boundary, grid_upper_boundary)
        
        display_graph_in_asciio(graph, grid_upper_boundary, node_name, median_x, median_y)


def place_nearby(graph, node_name, x, y, grid_lower_boundary, grid_upper_boundary):
    coordinates_in_use = []
    # todo - node_name overwritten
    for x_node_name in graph:
        coordinates_in_use.append(graph[x_node_name]['position'])

    radius = 0

    while True:
        surrounding_coordinates_list = surrounding_coordinates(x, y, radius, grid_lower_boundary, grid_upper_boundary)
        coordinates_not_in_use       = []

        for coordinate in surrounding_coordinates_list:
            if coordinate not in coordinates_in_use:
                coordinates_not_in_use.append(coordinate)

        if len(coordinates_not_in_use) > 0:
            graph[node_name]['position'] = coordinates_not_in_use[0]
            return

        radius += 1


def place_nodes_random(graph, grid_upper_boundary, grid_lower_boundary):
    # todo - very unoptimised
    used_coordinates = set()
    
    for node_name in graph:
        node_placed = False
    
        while not node_placed: 
            x = int(random.uniform(grid_lower_boundary, grid_upper_boundary))
            y = int(random.uniform(grid_lower_boundary, grid_upper_boundary))
            
            if (x,y) not in used_coordinates:
                graph[node_name]['position'] = [x, y]
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
        canonize_node_positions(graph)


def map_node_positions(graph, grid_upper_boundary):
    for node_name in graph:
        graph[node_name]['position'][X_AXIS] += grid_upper_boundary
        graph[node_name]['position'][Y_AXIS] += grid_upper_boundary


def canonize_node_positions(graph):
    min_x = 0
    min_y = 0
    
    for node_name in graph:
        if graph[node_name]['position'][X_AXIS] < min_x: min_x = graph[node_name]['position'][X_AXIS]
        if graph[node_name]['position'][Y_AXIS] < min_y: min_y = graph[node_name]['position'][Y_AXIS]

    for node_name in graph:
        graph[node_name]['position'][X_AXIS] -= min_x
        graph[node_name]['position'][Y_AXIS] -= min_y


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

    pp = pprint.PrettyPrinter(indent=4)

    graphs = load_graphs(options.file_path)
    # pp.pprint(graphs)

    place_nodes(graphs)
    # canonize_graphs_placed_nodes(graphs)
    # pp.pprint(graphs)

    if options.json:
        generate_json(graphs)
    

if __name__ == '__main__':
    main()
