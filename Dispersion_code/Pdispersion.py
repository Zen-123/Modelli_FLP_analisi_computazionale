from pyscipopt import Model, quicksum
import numpy as np
import matplotlib.pyplot as plt
from generateInstance import loadInstanceJSON, generateTablePdispersion

"""
Genera il modello Pdispertion e lo ritorna 

Parametri:
I : insieme delle location 
p: numero di facilities da aprire
d: distanza euclidea tra le facilities i e j

Return:
model: modello completo
"""


def buildModel(I, p, d):
    # creazione modello
    model = Model()

    # definizione e inizializzazione variabili
    y = {}
    for i in range(I):
        y[i] = model.addVar(vtype="B", name=f"y_{i}")

    # D: distanza minima tra le facilities selezionate, lb = lower bound
    D = model.addVar(vtype="C", name="D", lb=0)

    # vincolo 2.8
    model.addCons(quicksum(y[i] for i in range(I)) == p, name="vincolo_2.8")

    # big-M
    M = max(d.values())
    # vincolo 2.9
    for i in range(I):
        for j in range(i + 1, I):
            if (i, j) in d:
                model.addCons(D <= d[(i, j)] + M * (1 - y[i]) +
                              M * (1 - y[j]), name=f"vincolo_2.9_{i}_{j}")

    # definizione funzione obiettivo
    model.setObjective(D, sense="maximize")

    model.data = {'y': y, 'D': D, 'M': M}
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
    data = loadInstanceJSON(filename)
    I = data["I"]
    p = data["p"]
    facilities = data["facilities"]
    d = data["distanceMatrix"]
    return I, p, d, facilities




"""
Legge l'istanza, ottimizza il modello P-dispersion e salva i risultati

Parametri:
filename : nome del file da leggere
resultPath : path del file csv su cui salvare i risultati
"""

def saveData(filename, resultPath):

    I, p, d, facilities = readInstances(filename)
    print(f"Facilities: {I}")
    print(f"facilities da aprire: {p}")
    typeModel = "Pdisp"
    model = buildModel(I, p, d)
    model.optimize()
    nodes = model.getNNodes()
    y = model.data["y"]

    # Estrai le variabili y
    selectedFacilities = []
    operFacilities = 0
    for i in range(len(y)):
        if model.getVal(y[i]) > 0.5:
            selectedFacilities.append(i)
            operFacilities += 1

    # visualizza graficamente l'unit square
    plotSolution(facilities, selectedFacilities, model, I)

    # generazione tabella CSV
    generateTablePdispersion(model, filename, resultPath,
                             I, p, d, facilities, typeModel, nodes)

"""
Visualizza la soluzione del P-dispersion problem

Parametri:
facilities : coordinate delle facilities nel piano
selectedFacilities : lista degli indici delle facilities selezionate
model : modello ottimizzato
I : numero totale di facilities

Return:
fig, ax : oggetti matplotlib per il grafico
"""
def plotSolution(facilities, selectedFacilities, model, I):
    """
    Visualizza la soluzione del P-dispersion problem
    """
    coords = np.array(facilities)
    y = model.data["y"]

    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title(
        f'P-Dispersion Solution (I = {I}, p={len(selectedFacilities)})\n')

    # visualizza location
    ax.scatter(coords[:, 0], coords[:, 1], c='lightgray', s=100, alpha=0.6,
               marker='o', edgecolors='gray', linewidth=1, label='Available Locations')
    for i, (x, y) in enumerate(coords):
        ax.annotate(f'{i}', (x, y), xytext=(3, 3), textcoords='offset points',
                    fontsize=8, bbox=dict(boxstyle='round,pad=0.2',
                                          facecolor='white', alpha=0.7))

    # Facilities selezionate
    if selectedFacilities:
        selCoords = coords[list(selectedFacilities), :]
        ax.scatter(selCoords[:, 0], selCoords[:, 1], c='red', s=200, alpha=0.9,
                   marker='s', edgecolors='darkred', linewidth=2, label='Selected Facilities')

        # collegamento tra facilities selezionate
        distancesList = []
        minDistPair = None

        # Evidenzia la coppia con distanza minima
        if minDistPair:
            i, j = minDistPair
            ax.plot([coords[i, 0], coords[j, 0]],
                    [coords[i, 1], coords[j, 1]],
                    'r-', alpha=0.8, linewidth=0.3)

        if distancesList:
            info_text = (f'Selected: {selectedFacilities}\n'
                         )
            ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10,
                    verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5',
                                                       facecolor='lightblue', alpha=0.9))

    ax.legend(loc='upper right')
    plt.show()
    return fig, ax


if __name__ == "__main__":

    # istanze da leggere e studiare
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
        saveData(inst, resultPath="results/P_dispersion/pdisp_results.csv")
