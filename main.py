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
from CYKParseTree import build_parse_tree

import CYK as cyk

import json


# Importar la función convertir_CFG_a_CNF del módulo CFG_to_CNF
from CFG_to_CNF import convertir_CFG_a_CNF, imprimir_cnf

# Llamar a la función para convertir la gramática CFG a CNF
prod_dict_cnf = convertir_CFG_a_CNF()

# Imprimir la gramática en CNF
imprimir_cnf(prod_dict_cnf)

print(' ')


w = input('Ingresa la cadena que deseas realizar\n Ejemplos: \n he drinks a beer with she \n the cat cooks\n Cadena: ')



with open('CNF.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    
    # Extraer variables, terminales y producciones
variables = cfg['variables']
terminales = cfg['terminales']
producciones = cfg['producciones']


verif = w.split(' ')

esterminal = True

for d in verif:
    if d not in terminales:
        print('\033[31mError la palabra encontrada no pertenece a los terminales \npalabra: '+ d + '\033[0m')
        esterminal = False
        


if esterminal == True:
    table = cyk.cyk_parse(producciones, w)

    print("\nCYK Parse Tabla con el algoritmo CYK:")
    print(table)

    parse_tree = build_parse_tree(producciones, table, w.split())

    # Renderiza el árbol de análisis como un PNG
    parse_tree.render(filename="./CYK_Parse_Tree", format="png", cleanup=False)
    print("Generando el arbol 'CYK_Parse_Tree.png'.")
