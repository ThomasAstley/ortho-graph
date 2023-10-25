Ortho-graph project
===================

Given a graph description, compute orthogonal routes between the graphs nodes.

```
ortho-graph graph_description.yaml

cat graph_description.yaml | ortho-graph 

cat yaml/json/perl/xml/dot | translator | ortho-graph | visualisation-tool
```

# Links

## Orthogonal Layouts (1/5): Topology - Shape - Metrics | Visualization of Graphs - Lecture 6

[Lecture](https://www.youtube.com/watch?v=v-epJF7KAOY)

## Graph::Easy

[cpan](https://metacpan.org/pod/Graph::Easy)

[documentation](http://bloodgate.com/perl/graph/manual/overview.html)

## Orthogonal Connector Routing

[module](https://github.com/Bukk94/OrthogonalConnectorRouting)

## Orthogonal edge router

[documentation](http://docs.yworks.com/yfiles/doc/developers-guide/orthogonal_edge_router.html)

# Input


## Format

- utf8
- '#' starts comment
- whitespace doesn't matter (freeform)

## Graph description

- Simple text description
- Future languages
	- Graphviz
	- Graph::Easy

### user attributes

passed as-is to output

- colour
- label
	- \n for new line
	- alignment
	- wrapping
- edge shape
- edge start, end
- edge length
- edge title/text
- node shape

    
```
user_attributes = { ... }
```

### node coordinates

- no coordinates, default case
- specify node coordinates
- computed given another node as origin and direction

### route    

- no route, default case
- specify an edge length

### types of object

- graph
- node
- edge
- group

See *definitions* file.

### edge specification

```
A,B,C-->D
```

Equivalent 

```
A-->D
B-->D
C-->D
```

# Computation

- minimal edge turns
- minimal edge overlap

```
options = 
	{
	A = { ... },
	'A -> B' = { ... }
	}
```

# Routed graph description

## Nodes

- top-left coordinate
- bottom-right coordinate
- name
- user attributes

## Edges

an edge consists of one or more legs
- user attributes

### Leg

- start coordinate
- end coordinate

