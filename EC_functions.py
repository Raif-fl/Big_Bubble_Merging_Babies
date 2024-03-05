def condense_edges(input_list: list[tuple]):
    temp_dict = dict()
    suffix = lambda y : y[1:]

    for value in input_list:
        if temp_dict.get(value) is None:
            temp_dict[suffix(value[0])] = value[1]
        else:
            temp_dict[suffix(value[0])] += value[1]
    return(temp_dict)

def extend_edges(leftover_graph:dict ) -> dict:
    extended_graph = dict()
    prefix = lambda x : x[0:-1]

    for key in leftover_graph.keys():
        new_key = prefix(key)

        if extended_graph.get(new_key) is None:
            new_edges = condense_edges(leftover_graph[key])

            new_val = []
            for key in new_edges.keys():
                new_val.append((key, new_edges[key]))

        else:
            old_edges = {}
            for value in extended_graph[new_key]:
                if old_edges.get(value) is None:
                    old_edges[value[0]] = value[1]

            new_edges = condense_edges(leftover_graph[key])

            for edge in old_edges:
                if new_edges.get(edge) is None:
                    new_edges[edge] = old_edges[edge]
                else:
                    new_edges[edge] += old_edges[edge]

            new_val = []
            for key in new_edges.keys():
                new_val.append((key, new_edges[key]))

        extended_graph[new_key] = new_val

    return(extended_graph)
