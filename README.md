
# NAME

	ortho-graph - compute orthogonal routing

![Simple Graph](https://github.com/ThomasAstley/ortho-graph/blob/main/examples/simple_graph.png)

# SYNOPSIS

	ortho-graph graph_description.yaml

	cat graph_description.yaml | ortho-graph 

# DESCRIPTION

Given a graph description, compute orthogonal routes between the graphs nodes.

## Definitions

### Graph 

A graph ‘G’ is a set of nodes 'n' connected by edges 'e': G = (n, e)

#### Synonyms

- node: vertex
- edge: link

### Edge

An edge can be:
- uni-directional, information flows from one node to another
- bi-directional, information flows between two nodes

### Group

Set of nodes sharing a common attribute

# OPTIONS      

# EXIT STATUS  

| code | description |
| ---- | ----------- |
|  0   | graph routed ok |
|  2   | wrong number of arguments |
|  10  | invalid graph description |

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

