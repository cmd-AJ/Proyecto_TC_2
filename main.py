# Primero juntar variables simbolos terminales 

#   "N −→ cat | dog",
#     "N −→ beer | cake | juice | meat | soup",


# a   "N −→ cat | dog | beer | cake | juice | meat | soup"


#Luego hacer cfg a cnf entonces
#Agregar S0 -> S  lo denotamos como $ como S0 porque no

#revisar que sean dos variables y revisar si ningun terminal (minusculas)  tienen variables

#eliminar producciones unarias osea el S0 tiene que tener todo lo que tiene S
# "S0 -> NP VP"

#Eliminar si no llegan a ningun lado
 
#  Ya tenemos chomskys


#Implementar cyk
# https://www.geeksforgeeks.org/cocke-younger-kasami-cyk-algorithm/

# Importar cyk_parse_tree y build_parse_tree desde CYKParseTree.py
from CYKParseTree import cyk_parse_tree, build_parse_tree

import CYK as cyk

import CFG_to_CNF


# Importar la función convertir_CFG_a_CNF del módulo CFG_to_CNF
from CFG_to_CNF import convertir_CFG_a_CNF, imprimir_cnf

# Llamar a la función para convertir la gramática CFG a CNF
prod_dict_cnf = convertir_CFG_a_CNF()

# Imprimir la gramática en CNF
imprimir_cnf(prod_dict_cnf)


w = "he drinks a beer with she"


table = cyk.cyk_parse(w)

print("\nCYK Parse Table:")
print(table)