from pyscipopt import Model, quicksum
import numpy as np
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from generateInstance import loadInstanceJSON, generateTable

"""
Genera il modello e lo ritorna 

Parametri:
I : insieme delle possibili location per le facilities
J : insieme dei clienti
f : costi fissi di apertura facility
c : costi di assegnazione client - facility 

Return:
model: modello completo
"""

def buildFLPModel(I, J, f, c):

    # creazione modello
    model = Model()

    #definizione e inizializzazione variabili
    x, y = {}, {}

    for i in range(I):
        y[i] = model.addVar(vtype='B', name=f"y_{i}")
        for j in range(J):
            x[i, j] = model.addVar(vtype='B', name=f"x_{i}_{j}")

    #Definizione dei vincoli
    for j in range(J):
        model.addCons(quicksum(x[i, j] for i in range(I)) == 1,name=f'vincolo_2.3_{j}')

    for i in range(I):
        for j in range(J):
            model.addCons(x[i, j] <= y[i], name=f'vincolo_2.4_{i}_{j}')

    # definizione funzione obiettivo
    model.setObjective(
        quicksum(f[i] * y[i] for i in range(I)) +
        quicksum(c[i, j] * x[i, j] for i in range(I) for j in range(J)),
        sense="minimize"
    )

    # Memorizzazione delle variabili per l'accesso successivo
    model.data = x, y

    # modello SCIP configurato per la risoluzione
    return model

"""
Legge le istanze di input e ritorna i parametri richiesti dalla funzione buildModel()

Parametri:
filename : nome del file da leggere 

Return:
I : insieme delle possibili location per le facilities
J : insieme dei clienti
f : costi fissi di apertura facility
c : costi di assegnazione client - facility 
"""
def readInstances(filename):

    # estrazione dati dal file
    data = loadInstanceJSON(filename)

    #caricamento dati nelle variabili 
    I = data["I"]
    J = data["J"]
    c = data["costMatrix"]
    f = data["fixedCosts"]

    return I, J, f, c

"""
Legge l'istanza, ottimizza il modello UFLP e salva i risultati

Parametri:
filename : nome del file da leggere
resultPath : path del file csv su cui salvare i risultati
"""
def saveData(filename, resultPath):
    I, J, fixedCost, c = readInstances(filename)
    i = 0
    print(f"Facilities: {I}")
    print(f"Clients: {J}")
    print("COSTI FISSI FACILITY: ")
    # lettura costi fissi e assegnazione valori ad array f
    f = {}
    for value in fixedCost.values():
        print(f"f[{i}]", value)
        f[i] = value
        i+=1

    # calcolo distanza media e costo fisso medio 
    avgFixedCost = sum(f.values()) / len(f) 
    avgCostMatrix = sum(c.values())/ len(c) 

    # nome del modello
    typeModel = "UFLP"

    model = buildFLPModel(I=I, J=J, f=f, c=c)
    model.optimize()
    nodes = model.getNNodes()

    # generazione tabella CSV
    generateTable(model, filename, resultPath, I, J, typeModel, avgFixedCost, avgCostMatrix, 0, nodes)


if __name__ == "__main__": 
    
    # istanze da leggere e studiare    
    instances = [
        "benchmark_instances/FLP/SMALL_01.json",
        "benchmark_instances/FLP/SMALL_02.json",
        "benchmark_instances/FLP/SMALL_03.json",
        "benchmark_instances/FLP/SMALL_04.json",
        "benchmark_instances/FLP/SMALL_05.json",
        "benchmark_instances/FLP/SMALL_06.json",
        "benchmark_instances/FLP/SMALL_07.json",
        "benchmark_instances/FLP/SMALL_08.json",
        "benchmark_instances/FLP/SMALL_09.json",
        "benchmark_instances/FLP/SMALL_10.json",

        "benchmark_instances/FLP/MEDIUM_01.json",
        "benchmark_instances/FLP/MEDIUM_02.json",
        "benchmark_instances/FLP/MEDIUM_03.json",
        "benchmark_instances/FLP/MEDIUM_04.json",
        "benchmark_instances/FLP/MEDIUM_05.json",
        "benchmark_instances/FLP/MEDIUM_06.json",
        "benchmark_instances/FLP/MEDIUM_07.json",
        "benchmark_instances/FLP/MEDIUM_08.json",
        "benchmark_instances/FLP/MEDIUM_09.json",
        "benchmark_instances/FLP/MEDIUM_10.json",

        "benchmark_instances/FLP/LARGE_01.json",
        "benchmark_instances/FLP/LARGE_02.json",
        "benchmark_instances/FLP/LARGE_03.json",
        "benchmark_instances/FLP/LARGE_04.json",
        "benchmark_instances/FLP/LARGE_05.json",
        "benchmark_instances/FLP/LARGE_06.json",
        "benchmark_instances/FLP/LARGE_07.json",
        "benchmark_instances/FLP/LARGE_08.json",
        "benchmark_instances/FLP/LARGE_09.json",
        "benchmark_instances/FLP/LARGE_10.json",
    ]

    for inst in instances:
        saveData(inst, resultPath="results/uflp_results.csv")