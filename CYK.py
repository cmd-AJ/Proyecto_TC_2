# Python implementation for the
# CYK Algorithm 

#DISCLAIMER THIS CODE IS TAKEN BY MONI from https://www.geeksforgeeks.org/cocke-younger-kasami-cyk-algorithm/

import pandas as pd

# # Los no terminales y adaptar con el codigo de Z
# non_terminals = ["S0", "VP", "PP", "NP", "V", "P", "N", "Det"]
# terminals = ["cooks", "drinks", "eats", "cuts", "he", "she", "in", "with", "cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork", "knife", "oven", "spoon", "a", "the"]

# # Reglas gramaticas solo que hay que ver si necesitamos adaptar con el codigo de Z
# R = {
#     "S0": ["NP VP"],
#     "VP": ["V NP", "VP PP", "cooks", "drinks", "eats", "cuts"],
#     "PP": ["P NP"],
#     "NP": ["Det N", "he", "she"],
#     "V": ["cooks", "drinks", "eats", "cuts"],
#     "P": ["in", "with"],
#     "N": ["cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork", "knife", "oven", "spoon"],
#     "Det": ["a", "the"],
# }

def cyk_parse( R , w):
    words = w.split()
    n = len(words)

    # Crea la tabla en pandas como CYK table
    dict_list = {}
    contador = 1
    for e in words:
        dict_list[e] = ['']*contador + ['-']*(n-contador)
        contador = contador + 1
    table = pd.DataFrame(dict_list, index=words)

    # hace la identidad
    for i, word in enumerate(words):
        for non_terminal, productions in R.items():
            if word in productions:
                if table.iloc[i, i] == '':
                    table.iloc[i, i] = non_terminal
                else:
                    table.iloc[i, i] += ',' + non_terminal

   
    for length in range(2, n + 1): 
        for i in range(n - length + 1):
            j = i + length - 1
            cell_value = set()

            for k in range(i, j):
                B_values = table.iloc[i, k].split(',') if table.iloc[i, k] else []
                C_values = table.iloc[k + 1, j].split(',') if table.iloc[k + 1, j] else []

                for B in B_values:
                    for C in C_values:
                        for non_terminal, productions in R.items():
                            if f"{B} {C}" in productions:
                                cell_value.add(non_terminal)

            if cell_value:
                table.iloc[i, j] = ','.join(sorted(cell_value))

    # Revisa si es verdadero o no osea si tiene un estado inicial
    if 'S0' in table.iloc[0, n - 1]:
        print("The string is in the language (True).")
    else:
        print("The string is not in the language (False).")

    return table

