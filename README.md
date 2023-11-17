
# NAME

	ortho-graph - compute orthogonal routing

![Simple Graph](https://github.com/ThomasAstley/ortho-graph/blob/main/examples/simple_graph.png)

# SYNOPSIS

	ortho-graph --file graph_description.yaml

	cat graph_description.yaml | ortho-graph 

    cat yaml/json/perl/xml/dot | translator | ortho-graph --json | visualisation-tool

# DESCRIPTION

Given a graph description, compute orthogonal routes between the graphs nodes.

A graph ‘G’ is a set of nodes 'n' connected by directional edges 'e': G = (n, e)

An edge is either:

- uni-directional, from one node to another
- bi-directional, between two nodes
- from one node to itself

There can be multiple edges:

- between each pair of nodes
- from a node to itself

## Computation

- minimal edge turns
- minimal edge overlap

# OPTIONS      

--json -gives json format as output

--file -graph description file path 

# INPUT

The graph description is in YAML format. (https://yaml.org/)

## node

- no coordinates, default case
- specify node coordinates
- computed given another node as origin and direction
- node shape
    - size width/ length
    - size computed based on label

## edge

```
A: { B, C, ... }
```

Defines edges AB, AC, ...

- uni-directional, from one node to another
- bi-directional, between two nodes
- from one node to itself
- edge start, end

Multiple edges:

- for each pair of nodes
- for each node

## user attributes

passed as-is to output

```
user_attributes = { ... }
```

# OUTPUT 

The output is in JSON format

```
{"Graph": {"placed nodes": {"A": [0, 0], "B": [0, 3], "D": [3, 0], "C": [0, 6]}}}
```

# EXIT STATUS  

| code | description |
| ---- | ----------- |
|  0   | graph routed ok |
|  2   | wrong number of arguments |
|  10  | invalid graph description |

# DOCUMENTATION

# EXAMPLES

# COPYRIGHT AND LICENSE  

Thomas Astley 2023

GNU GPL Version 3, see *LICENSE.txt* file

# SEE ALSO

## Orthogonal Layouts Lecture 

[Lecture](https://www.youtube.com/watch?v=v-epJF7KAOY)

## Graph::Easy

[cpan](https://metacpan.org/pod/Graph::Easy)

[documentation](http://bloodgate.com/perl/graph/manual/overview.html)

## Orthogonal Connector Routing

[module](https://github.com/Bukk94/OrthogonalConnectorRouting)

## Orthogonal edge router

[documentation](http://docs.yworks.com/yfiles/doc/developers-guide/orthogonal_edge_router.html)

## Orthogonal Layout Algorithm Research papers

[paper 1](https://arxiv.org/pdf/1807.09368.pdf)

[paper 2](https://rtsys.informatik.uni-kiel.de/~biblio/downloads/theses/ocl-bt.pdf)
