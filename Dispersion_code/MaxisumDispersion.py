from pyscipopt import Model, quicksum
import numpy as np
import matplotlib.pyplot as plt
from generateInstance import loadInstanceJSON, generateTablePdispersion

"""
Genera il modello Maxisum e lo ritorna 

Parametri:
I : insieme delle location 
p : numero di facilities da aprire
d : distanza euclidea tra le facilities i e j

Return:
model: modello completo
"""
def buildModel(I, p, d):
    #creazione modello
    model = Model()

    #definizione e inizializzazione variabili
    y, z = {}, {}
    for i in range(I):
        y[i] = model.addVar(vtype="B", name=f"y_{i}")
    
    for i in range(I):
        for j in range(i + 1, I):
            z[i, j] = model.addVar(vtype="B", name=f"z_{i}_{j}")

    # vincolo 2.12
    model.addCons(quicksum(y[i] for i in range(I)) == p, name="vincolo_2.12")

    # altri vincoli del modello matematico
    for i in range(I):
        for j in range(i + 1, I):
            model.addCons(z[i, j] <= y[i], name=f"z{i}_{j}")
            model.addCons(z[i, j] <= y[j], name=f"z{i}_{j}")
            model.addCons(z[i, j] >= y[i] + y[j] - 1, name=f"vincolo_2.15_{i}_{j}")
    
    #definizione funzione obiettivo
    model.setObjective(quicksum(d[i,j]*z[i,j] for i in range(I) for j in range(i+1, I)), sense="maximize")
    model.data = {'y': y, 'z': z, 'd': d}

    # modello SCIP configurato per la risoluzione
    return model

"""
Legge le istanze di input e ritorna i parametri richiesti dalla funzione buildModel()
Parametri:
filename : nome del file da leggere 

Return:
I : insieme delle location 
p: numero di facilities da aprire
d: distanza euclidea tra le facilities i e j
facilities: coordinate nel piano delle facilities
"""
def readInstances(filename):
    # estrazione dati dal file
    data = loadInstanceJSON(filename)

    #caricamento dati nelle variabili 
    I = data["I"]
    p = data["p"]
    facilities = data["facilities"]
    d = data["distanceMatrix"]

    return I, p, d, facilities

"""
Legge l'istanza, ottimizza il modello MaxiSum Dispersion e salva i risultati

Parametri:
filename : nome del file da leggere
resultPath : path del file csv su cui salvare i risultati
"""
def saveData(filename, resultPath):
    I, p, d, facilities = readInstances(filename)
    print(f"Facilities: {I}")
    print(f"facilities da aprire: {p}")

    # nome del modello
    typeModel = "MaxS"
    model = buildModel(I, p, d)
    model.optimize()
    y = model.data["y"]
    selectedFacilities = []
    openFacilities = 0
    for i in range(len(y)):
        if model.getVal(y[i]) > 0.5: 
            selectedFacilities.append(i)
            openFacilities+=1

    # visualizza graficamente l'unit square
    #plotMaxisumSolution(facilities, selectedFacilities, I)

    # numero di nodi esplorati per risolvere all'ottimo
    nodes = model.getNNodes()

    # generazione tabella CSV
    generateTablePdispersion(model, filename, resultPath,I,p,d,facilities,typeModel, nodes)

"""
Visualizza la soluzione del MaxiSum Dispersion problem

Parametri:
coordinates : coordinate delle facilities nel piano
selectedFacilities : lista degli indici delle facilities selezionate
I : numero totale di facilities

Return:
fig, ax : oggetti matplotlib per il grafico
"""
def plotMaxisumSolution(facilities, selectedFacilities, I):
    coords = np.array(facilities)
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title(f'MaxiSum Dispersion Solution (I = {I}, p={len(selectedFacilities)})\n')
    
    # Tutte le location generate
    ax.scatter(coords[:, 0], coords[:, 1], c='lightgray', s=100, alpha=0.6,
               marker='o', edgecolors='gray', linewidth=1, label='Available Locations')
    
    for i, (x, y) in enumerate(coords):
        ax.annotate(f'{i}', (x, y), xytext=(3, 3), textcoords='offset points',
                   fontsize=8, bbox=dict(boxstyle='round,pad=0.2', 
                   facecolor='white', alpha=0.7))
    
    # Facilities selezionate
    if selectedFacilities:
        selCoords = coords[list(selectedFacilities), :]
        ax.scatter(selCoords[:, 0], selCoords[:, 1], c='blue', s=200, alpha=0.9,
                   marker='s', edgecolors='blue', linewidth=1, label='Selected Facilities')
    
    ax.legend(loc='upper right')
    plt.show()
    return fig, ax

if __name__ == "__main__":

    #istanze da leggere e studiare
    instances = [
        "benchmark_instances/P_dispersion/SMALL_01.json",
        "benchmark_instances/P_dispersion/SMALL_02.json",
        "benchmark_instances/P_dispersion/SMALL_03.json",
        "benchmark_instances/P_dispersion/SMALL_04.json",
        "benchmark_instances/P_dispersion/SMALL_05.json",
        "benchmark_instances/P_dispersion/SMALL_06.json",
        "benchmark_instances/P_dispersion/SMALL_07.json",
        "benchmark_instances/P_dispersion/SMALL_08.json",
        "benchmark_instances/P_dispersion/SMALL_09.json",
        "benchmark_instances/P_dispersion/SMALL_10.json",

        "benchmark_instances/P_dispersion/MEDIUM_01.json",
        "benchmark_instances/P_dispersion/MEDIUM_02.json",
        "benchmark_instances/P_dispersion/MEDIUM_03.json",
        "benchmark_instances/P_dispersion/MEDIUM_04.json",
        "benchmark_instances/P_dispersion/MEDIUM_05.json",
        "benchmark_instances/P_dispersion/MEDIUM_06.json",
        "benchmark_instances/P_dispersion/MEDIUM_07.json",
        "benchmark_instances/P_dispersion/MEDIUM_08.json",
        "benchmark_instances/P_dispersion/MEDIUM_09.json",
        "benchmark_instances/P_dispersion/MEDIUM_10.json",

        "benchmark_instances/P_dispersion/LARGE_01.json",
        "benchmark_instances/P_dispersion/LARGE_02.json",
        "benchmark_instances/P_dispersion/LARGE_03.json",
        "benchmark_instances/P_dispersion/LARGE_04.json",
        "benchmark_instances/P_dispersion/LARGE_05.json",
        "benchmark_instances/P_dispersion/LARGE_06.json",
        "benchmark_instances/P_dispersion/LARGE_07.json",
        "benchmark_instances/P_dispersion/LARGE_08.json",
        "benchmark_instances/P_dispersion/LARGE_09.json",
        "benchmark_instances/P_dispersion/LARGE_10.json",
    ]

    for inst in instances:
        print(inst)
        saveData(inst, resultPath="results/P_dispersion/maxS_results.csv")
        


    


