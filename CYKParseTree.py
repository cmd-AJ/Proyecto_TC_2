import pandas as pd
import graphviz
import CYK as cyk

import graphviz

def build_parse_tree(R, parse_table, words):

    n = len(words) 
    tree = graphviz.Digraph()


    words_set = set(words)
    word_counts = dict.fromkeys(words_set, 0)
    
    for e in words:
        word_counts[e] = word_counts[e] + 1
        


    def add_nodes(non_terminal, i, j, parent=None):

        node_name = f"{non_terminal}_{i}_{j}"
        label = f"{non_terminal}"
        tree.node(node_name, label)

        if parent:
            tree.edge(parent, node_name)

        cell_value = parse_table.iloc[i, j]

        if cell_value == '-' or cell_value == '':  
            return

        non_terminals_in_cell = cell_value.split(',') 
        if non_terminal not in non_terminals_in_cell:
            return


        if non_terminal in R:
            productions = R[non_terminal]

            for prod in productions:
                prod_parts = prod.split()

                # Check for terminal productions
                if len(prod_parts) == 1 and prod_parts[0] in word_counts:
                    word_node = f"{prod_parts[0]}_{i}_{i}"
                    tree.node(word_node, prod_parts[0])
                    tree.edge(node_name, word_node)
                    if word_counts[prod_parts[0]] == 0:
                        words_set.remove(prod_parts[0])
                    else:
                        word_counts[prod_parts[0]] = word_counts[prod_parts[0]] - 1
                    
                    return 

                else:
        
                    for k in range(i, j):
                        B_values = parse_table.iloc[i, k].split(',') if parse_table.iloc[i, k] != '-' else []
                        C_values = parse_table.iloc[k + 1, j].split(',') if parse_table.iloc[k + 1, j] != '-' else []

                    
                        for B in B_values:
                            for C in C_values:
                                if f"{B} {C}" == prod:
                                   
                                    add_nodes(B, i, k, node_name)
                                    add_nodes(C, k + 1, j, node_name)
                                    return 

   
    if 'S0' in parse_table.iloc[0, n - 1]:
        add_nodes('S0', 0, n - 1)

    return tree

