import json
import copy
import re

def convertir_CFG_a_CNF(ruta_cfg_json='CFG.json'):
    # Cargar la gramática CFG desde CFG.json
    with open(ruta_cfg_json, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    
    # Extraer variables, terminales y producciones
    variables = cfg['variables']
    terminales = cfg['simbolos']
    producciones = cfg['reglas']
    
    # Analizar las producciones en un diccionario
    def parsear_producciones(lista_producciones):
        prod_dict = {}
        for prod in lista_producciones:
            # Eliminar espacios en blanco adicionales
            prod = ' '.join(prod.split())
            # Usar una expresión regular para dividir en izquierda y derecha
            match = re.match(r'^(.*?)\s*(->|−→|→|–>|—>|~>|=>|==>|âˆ’â†’)\s*(.*)$', prod)
            if match:
                izquierda = match.group(1).strip()
                derecha = match.group(3).strip()
                derechas = [r.strip() for r in derecha.split('|')]
                if izquierda not in prod_dict:
                    prod_dict[izquierda] = []
                prod_dict[izquierda].extend(derechas)
            else:
                print(f"Error al analizar la producción: {prod}")
                continue
        return prod_dict

    prod_dict = parsear_producciones(producciones)

    # Paso 1: Agregar un nuevo símbolo inicial S0 -> S
    simbolo_inicial = 'S'
    nuevo_simbolo_inicial = 'S0'
    if nuevo_simbolo_inicial not in variables:
        variables.append(nuevo_simbolo_inicial)
    prod_dict[nuevo_simbolo_inicial] = [simbolo_inicial]

    # Paso 2: Eliminar producciones nulas (ε-producciones)
    # En este caso, no hay producciones nulas, así que no es necesario

    # Paso 3: Eliminar producciones unitarias
    def eliminar_producciones_unitarias(prod_dict):
        cambios = True
        while cambios:
            cambios = False
            for var in list(prod_dict.keys()):
                nuevas_producciones = []
                for prod in prod_dict[var]:
                    if prod in variables:
                        cambios = True
                        prod_dict[var].remove(prod)
                        prod_dict[var].extend(prod_dict[prod])
                        break  # Reiniciar el ciclo después de modificar
                else:
                    continue
                break
        return prod_dict

    prod_dict = eliminar_producciones_unitarias(prod_dict)

    # Paso 4: Reemplazar terminales en producciones con variables
    def reemplazar_terminales(prod_dict):
        nuevas_producciones = copy.deepcopy(prod_dict)
        nuevas_variables = {}
        indice_var = 1
        for var in prod_dict:
            for i, prod in enumerate(prod_dict[var]):
                simbolos = prod.split()
                if len(simbolos) > 1:
                    nuevos_simbolos = []
                    for simbolo in simbolos:
                        if simbolo in terminales:
                            if simbolo not in nuevas_variables:
                                nueva_var = f'T{indice_var}'
                                indice_var += 1
                                nuevas_variables[simbolo] = nueva_var
                                variables.append(nueva_var)
                                nuevas_producciones[nueva_var] = [simbolo]
                            nuevos_simbolos.append(nuevas_variables[simbolo])
                        else:
                            nuevos_simbolos.append(simbolo)
                    nuevas_producciones[var][i] = ' '.join(nuevos_simbolos)
        return nuevas_producciones

    prod_dict = reemplazar_terminales(prod_dict)

    # Paso 5: Convertir producciones a binarias
    def convertir_a_binario(prod_dict):
        nuevas_producciones = copy.deepcopy(prod_dict)
        indice_var = 1
        for var in list(prod_dict.keys()):
            for i, prod in enumerate(prod_dict[var]):
                simbolos = prod.split()
                while len(simbolos) > 2:
                    nueva_var = f'X{indice_var}'
                    indice_var += 1
                    variables.append(nueva_var)
                    ultimos_dos = simbolos[-2:]
                    simbolos = simbolos[:-2] + [nueva_var]
                    nuevas_producciones[nueva_var] = [' '.join(ultimos_dos)]
                    nuevas_producciones[var][i] = ' '.join(simbolos)
                nuevas_producciones[var][i] = ' '.join(simbolos)
        return nuevas_producciones

    prod_dict = convertir_a_binario(prod_dict)
    

    # Gather all values from the dictionary (excluding S0 key values)
    all_values = set()
    for key, values in prod_dict.items():
        if key != 'S0':  # Exclude 'S0'
            for value_list in values:
                # Split values if they contain spaces (like 'NP VP')
                all_values.update(value_list.split())

    # Remove keys that are not found in the values of other keys
    prod_dict = {key: values for key, values in prod_dict.items() if key == 'S0' or key in all_values}




    # Opcional: Guardar la gramática CNF en un archivo JSON
    gramatica_cnf = {
        'variables': variables,
        'terminales': terminales,
        'producciones': prod_dict
    }
    
    with open('CNF.json', 'w', encoding='utf-8') as f:
        json.dump(gramatica_cnf, f, indent=4, ensure_ascii=False)

    # Retornar la gramática en CNF
    return prod_dict

def imprimir_cnf(prod_dict):
    print("\nGramática en Forma Normal de Chomsky (CNF):")
    for var in prod_dict:
        prods = ' | '.join(prod_dict[var])
        print(f"{var} -> {prods}")
