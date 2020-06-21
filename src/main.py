import sys
import networkx as nt

def highest_kcore(ppi_file):
    k_cores = {}        
    highest_kcore =0   

    ppi_graph = build_ppi_graph(ppi_file)         
    protein_cores = nt.core_number(ppi_graph)      
    for protein, k_core in protein_cores.items():
        if highest_kcore < k_core: 
            highest_kcore = k_core
        if k_core in k_cores:
            k_cores[k_core].append(protein)
        else:
            k_cores[k_core]=[protein]

    return highest_kcore,k_cores

def build_ppi_graph(ppi_file):
    with open(ppi_file, "r") as ppi:
        ppi_graph = nt.Graph()
        for interaction in ppi:
            nodes = interaction.rstrip("\n").split("\t")
            ppi_graph.add_edge(nodes[0], nodes[1])
    return ppi_graph

ppi_file = 'TestfilesforPPI/GRIDforhuman.txt'

highest_kcore,k_cores = highest_kcore(ppi_file) 
print("The highest k-core is a {0}-core and there are {1} proteins in that {0}-core. \n"
      "The proteins are: {2}".format(highest_kcore,len(k_cores[highest_kcore]),k_cores[highest_kcore]))