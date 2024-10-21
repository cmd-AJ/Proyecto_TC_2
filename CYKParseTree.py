import pandas as pd
import graphviz

non_terminals = ["S0", "VP", "PP", "NP", "V", "P", "N", "Det"]
terminals = ["cooks", "drinks", "eats", "cuts", "he", "she", "in", "with", 
             "cat", "dog", "beer", "cake", "juice", "meat", "soup", 
             "fork", "knife", "oven", "spoon", "a", "the"]

# Reglas gramaticales
R = {
    "S0": ["NP VP"],
    "VP": ["V NP", "VP PP", "cooks", "drinks", "eats", "cuts"],
    "PP": ["P NP"],
    "NP": ["Det N", "he", "she"],
    "V": ["cooks", "drinks", "eats", "cuts"],
    "P": ["in", "with"],
    "N": ["cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork", "knife", "oven", "spoon"],
    "Det": ["a", "the"],
}

def cyk_parse_tree(w):
    words = w.split()
    n = len(words)

    # Crear la tabla CYK con datos adicionales para analizar el árbol
    parse_table = [{} for _ in range(n)]
    for i in range(n):
        parse_table[i] = [{} for _ in range(n)]

    # Inicializar tabla con coincidencias de terminal
    for i, word in enumerate(words):
        for non_terminal, productions in R.items():
            if word in productions:
                parse_table[i][i][non_terminal] = [(word,)]

    # Rellenar la tabla con coincidencias no terminales
    for length in range(2, n + 1): 
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for B in parse_table[i][k]:
                    for C in parse_table[k + 1][j]:
                        for non_terminal, productions in R.items():
                            if f"{B} {C}" in productions:
                                if non_terminal not in parse_table[i][j]:
                                    parse_table[i][j][non_terminal] = []
                                parse_table[i][j][non_terminal].append((B, C, i, k, j))

    # Comprobar si la frase pertenece a la lengua
    if 'S0' in parse_table[0][n - 1]:
        print("The string is in the language (True).")
    else:
        print("The string is not in the language (False).")

    return parse_table

def build_parse_tree(parse_table, words):
    """Builds a parse tree using the data from the CYK table."""
    n = len(words)
    tree = graphviz.Digraph()

    def add_nodes(non_terminal, i, j, parent=None):
        """Recursively add nodes to the graphviz tree."""
        node_name = f"{non_terminal}_{i}_{j}"
        label = f"{non_terminal}"
        tree.node(node_name, label)
        if parent:
            tree.edge(parent, node_name)

        # Obtener las producciones que llevaron a este no-terminal
        productions = parse_table[i][j].get(non_terminal)
        if productions:
            for prod in productions:
                if len(prod) == 1:  # Producción terminal
                    word = prod[0]
                    word_node = f"{word}_{i}_{i}"
                    tree.node(word_node, word)
                    tree.edge(node_name, word_node)
                else:
                    B, C, i, k, j = prod
                    add_nodes(B, i, k, node_name)
                    add_nodes(C, k + 1, j, node_name)

    # Empezar por la raíz del árbol de análisis sintáctico
    if 'S0' in parse_table[0][n - 1]:
        add_nodes('S0', 0, n - 1)

    return tree

# Ejemplo de uso:
w = "he drinks a beer with she"
table = cyk_parse_tree(w)
parse_tree = build_parse_tree(table, w.split())

# Renderiza el árbol de análisis como un PNG
parse_tree.render(filename="/mnt/data/CYK_Parse_Tree", format="png", cleanup=False)
print("Parse tree generated and saved as 'CYK_Parse_Tree.png'.")
