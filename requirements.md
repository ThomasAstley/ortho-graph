Ortho-graph project
===================

Given a graph description, compute orthogonal routes between the graphs nodes.

```
ortho-graph graph_description.yaml

cat graph_description.yaml | ortho-graph 

cat yaml/json/perl/xml/dot | translator | ortho-graph | visualisation-tool
```

# Graph description (input)

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
A: { B, C, ... }
```
Defines edges AB, AC, ...

# Computation

- minimal edge turns
- minimal edge overlap

```
{
edges: 
  { 
  A: [ B ],        # node A has an edge to node B
  B: [ C, D ],     # node B has edges to nodes C and D
  C: [ D ]
  },
options:
    {
    node: 
        {
        A: { ... }
        },
    edges:
        {
        'A':
            {
            'B': {...},
            'C': {...} 
            }
        }
    }
}
```

# Routed graph description (output)

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

# Future ideas

- add new node to pre-rendered graph with minimal changes
	- pre-rendered graph rendered by ortho-graph
		- keep computation data to speedup new routing
	- manually rendered graph


