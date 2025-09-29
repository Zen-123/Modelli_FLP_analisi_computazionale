import random
import numpy as np
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import time
from pyscipopt import Model
import pandas as pd
import psutil

# dimensioni istanze UFLP e CFLP
INSTANCE_GROUPS = {
    'small': {
        'name': 'Small',
        'I_range': [10, 15],
        'J_range': [20, 100],
        'C_range': [5,10],
        'f_range': [5, 10]
    },
    'medium': {
        'name': 'Medium',
        'I_range': [20, 40],
        'J_range': [100, 300],
        'C_range': [8, 12],
        'f_range': [50, 100]
    },
    'large': {
        'name': 'Large',
        'I_range': [40, 60],
        'J_range': [350, 450],
        'C_range': [12, 16],
        'f_range': [200, 400]
    }
}

# dimensioni istanze Pdispertion e Maxisum
INSTANCE_GROUPS_P_DISPERSION = {
    'small': {
        'name': 'Small',
        'I_range': [8, 12],
        'p_range': [3, 7]
    },
    'medium': {
        'name': 'Medium',
        'I_range': [13, 18],
        'p_range': [7, 12],
    },
    'large': {
        'name': 'Large',
        'I_range': [18, 25],
        'p_range': [10, 15],
    }
}

"""
Genera le istanze per i problemi CFLP/UFLP
Parametri:
IRange : range di valori per le facilities
JRange : range di valori per i clienti

Return:
I : num. facility 
J : num. clienti
facilities : coordinate facilities
clients : coordinate clienti
costMatrix : matrice dei costi di assegnazione
"""
def generateInstanceFLP(IRange, JRange):
    
    # Genera casualmente il numero di facilities e clienti nei range specificati
    I = random.randint(IRange[0], IRange[1])  # numero facilities
    J = random.randrange(JRange[0], JRange[1]+1, 10)  # numero clienti
    
    print(f"#facilities: {I}")
    print(f"#clienti: {J}")
    print()
    
    # Genera coordinate facilities tramite una distribuzione uniforme
    facilities = []
    for i in range(I):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        facilities.append((x, y))
    
    # Genera coordinate clienti tramite distribuzione uniforme
    clients = []
    for j in range(J):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        clients.append((x, y))
    
    # Calcola matrice dei costi c_ij (distanza euclidea tra facility i e cliente j)
    costMatrix = {}
    for i in range(I):
        for j in range(J):
            # Calcola distanza euclidea tra facility i e cliente j
            fx, fy = facilities[i]
            cx, cy = clients[j]
            distance = round(np.sqrt((fx - cx)**2 + (fy - cy)**2), 4)
            costMatrix[(i,j)] = distance
    
    return I, J, facilities, clients, costMatrix

"""
Genera capacità per le facilities nel range specificato
Parametri: 
I : num. facility 
J : num. clienti
CRange: range di valori per le capacità

Return:
C: array delle capacità
"""
def generateCapacity(I,J, CRange):

    count = 0
    while True:
        # Genera capacità casuali per ogni facility
        C = {i: random.randint(CRange[0], CRange[1]) for i in range(I)}
        count +=1
        totalCapacity = sum(C.values())

        if totalCapacity >= J:
            print(f"Cicli ripetuti: {count}")
            return C
        

"""
Genera costi fissi per le facilities nel range specificato
Parametri: 
I : num. facility 
J : num. clienti
fRange: range di costi fissi di apertura

Return:
f: array dei costi fissi
"""
def generateFixedCosts(I, fRange):
   
    f = {}
    for i in range(I):
        f[i] = round(random.uniform(fRange[0], fRange[1]), 2)
    return f

"""
Salva i dati dell'istanza generata in un file JSON specificato
Parametri: 
instanceData : dizionario contenente tutti i dati generati
filename: nome del file in cui salvare i dati

"""
def saveInstanceJSON(instanceData, filename):
    
    # converte tuple e altri tipi non serializzabili
    serializableData = {}
    
    for key, value in instanceData.items():
        if isinstance(value, dict):
            # Converte chiavi tuple in stringhe per JSON
            if key in ['costMatrix', 'distanceMatrix']:
                serializableData[key] = {str(k): v for k, v in value.items()}
            else:
                serializableData[key] = value
        else:
            serializableData[key] = value
    
    with open(filename, 'w') as f:
        json.dump(serializableData, f, indent=4)
    
    print(f"Istanza salvata in formato JSON: {filename}")


"""
Carica i dati dal file JSON specificato

Parametri:
filename: nome del file in cui sono salvati i dati

Return:
data : ritorna i dati estratti dal file JSON
"""
def loadInstanceJSON(filename):

    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Riconverte le chiavi delle matrici da stringhe a tuple
    if 'costMatrix' in data:
        costMatrix = {}
        for keystr, value in data['costMatrix'].items():
            keyTuple = eval(keystr) 
            costMatrix[keyTuple] = value
        data['costMatrix'] = costMatrix
    
    if 'distanceMatrix' in data:
        distanceMatrix = {}
        for keystr, value in data['distanceMatrix'].items():
            keyTuple = eval(keystr)
            distanceMatrix[keyTuple] = value
        data['distanceMatrix'] = distanceMatrix
    
    return data

"""
Genera tutti i gruppi di istanze di benchmark

Parametri:
instanceRange : numero di istance per gruppo da generare
outputDir : directory in cui salvare i risultati

Return:
allInstances : ritorna tutte le istanze generate
"""
def generateAllInstancesFLP(instanceRange, outputDir="benchmark_instances/FLP", ):
    # Crea directory se non esiste
    os.makedirs(outputDir, exist_ok=True)
    
    allInstances = []
    instanceCounter = 0
    print("=" * 60)
    print("GENERAZIONE ISTANZE BENCHMARK UFLP/CFLP")
    print("=" * 60)
    
    # genera i gruppi di istanze e le singole istanze 
    for groupKey, groupParams in INSTANCE_GROUPS.items():
        print(f"\nGENERAZIONE GRUPPO {groupParams['name'].upper()}:")
        print("-" * 40)
        print(f"Facilities: {groupParams['I_range']}")
        print(f"Clienti: {groupParams['J_range']}")
        print(f"Capacità: {groupParams['C_range']}")
        print(f"Costi fissi: {groupParams['f_range']}")
        print()
        
        for i in range(instanceRange):
            print(f"Generazione istanza {instanceCounter} ({groupParams['name']}_{i+1}):")
            # Genera dati comuni
            I, J, facilities, clients, costMatrix = generateInstanceFLP(
                groupParams['I_range'], 
                groupParams['J_range']
            )
            
            # Genera costi fissi e capacità 
            fixedCosts = generateFixedCosts(I, groupParams['f_range'])
            capacities = generateCapacity(I,J, groupParams['C_range'])
            
            # Calcola statistiche 
            avgCapacity = sum(capacities.values()) / len(capacities)
            avgFixedCost = sum(fixedCosts.values()) / len(fixedCosts)
            
            # dizionario di istanza
            instanceData = {
                'instance_id': f'{groupKey.upper()}_{i+1:02d}',
                'group': groupParams['name'],
                'group_key': groupKey,
                'instance_number_in_group': i+1,
                'parameters': {
                    'I_range': groupParams['I_range'],
                    'J_range': groupParams['J_range'],
                    'C_range': groupParams['C_range'],
                    'f_range': groupParams['f_range']
                },
                'I': I,
                'J': J,
                'facilities': facilities,
                'clients': clients,
                'costMatrix': costMatrix,
                'fixedCosts': fixedCosts,
                'capacities': capacities,
                'statistics': {
                    'avg_capacity': round(avgCapacity, 2),
                    'avg_fixed_cost': round(avgFixedCost, 2),
                    'total_capacity': sum(capacities.values()),
                    'min_capacity': min(capacities.values()),
                    'max_capacity': max(capacities.values())
                },
            }
            
            allInstances.append(instanceData)
            
            # Salva istanza singola
            filename = f"{outputDir}/{instanceData['instance_id']}.json"
            saveInstanceJSON(instanceData, filename)
            
            instanceCounter += 1
    
    # Genera file riepilogativo
    summaryData = {
        'generation_info': {
            'total_instances': len(allInstances),
            'instances_per_group': 3
        },
        'groups': {
            groupKey: {
                'name': groupParams['name'],
                'parameters': groupParams,
                'instances': [inst['instance_id'] for inst in allInstances 
                             if inst['group_key'] == groupKey]
            } for groupKey, groupParams in INSTANCE_GROUPS.items()
        },
        'instances_summary': [
            {
                'instance_id': inst['instance_id'],
                'group': inst['group'],
                'I': inst['I'],
                'J': inst['J'],
                'avg_capacity': inst['statistics']['avg_capacity'],
                'avg_fixed_cost': inst['statistics']['avg_fixed_cost']
            } for inst in allInstances
        ]
    }
    
    summaryFilename = f"{outputDir}/benchmark_summary.json"
    with open(summaryFilename, 'w') as f:
        json.dump(summaryData, f, indent=4)
    
    print("=" * 60)
    print(" GENERAZIONE COMPLETATA!")
    print("=" * 60)
    print()
    
    return allInstances

"""
Mostra a video le coordinate delle facilities e dei clienti nello Unit Square
Parametri:
facilities : coordinate facilities nell'Unit Square
clients : coordinate clients nell'Unit Square
title : titolo del grafico
"""
def plotInstance(facilities, clients=None, title="Istanza"):
    plt.figure(figsize=(10, 8))

    if facilities:
        f_x, f_y = zip(*facilities)
        plt.scatter(f_x, f_y, c='red', s=100, marker='s', label='Facilities', alpha=0.8)

        if len(facilities) <= 20:
            for i, (x, y) in enumerate(facilities):
                plt.annotate(f'F{i+1}', (x, y), xytext=(5, 5), 
                            textcoords='offset points', fontsize=8, fontweight='bold')
    
    if clients:
        c_x, c_y = zip(*clients)
        plt.scatter(c_x, c_y, c='blue', s=50, marker='o', label='Clienti', alpha=0.6)
        
        if len(clients) <= 50:
            for j, (x, y) in enumerate(clients):
                plt.annotate(f'C{j+1}', (x, y), xytext=(5, 5), 
                            textcoords='offset points', fontsize=6, alpha=0.7)
    
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.grid(True, alpha=0.3)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.legend()
    plt.gca().set_aspect('equal', adjustable='box')
    
    plt.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], 'k--', alpha=0.5, linewidth=2)
    plt.tight_layout()
    plt.show()

"""
Genera le tabelle CSV contenenti i risultati del benchmark

Parametri: 
model : modello ottimizzato
filename : nome del file da leggere per generare la tabella
resultPath : path in cui salvare la tabella
I : num. facilities
J : num. clienti
typeModel : identifica il tipo di modello 
avgFixedCost : costo fisso medio
avgCostMatrix : costo di assegnazione medio
avgCapacity : capacità media 
nodes : numero di nodi esplorati
"""
def generateTable(model, filename, resultPath, I, J, typeModel,avgFixedCost,avgCostMatrix, avgCapacity, nodes):
    """Genera tabella risultati per benchmark"""
    x, y = model.data
    status = model.getStatus()
    obj = model.getObjVal()
    operFacilities = sum(1 for i in range(I) if model.getVal(y[i]) > 0.5)


    result = {
        "instance": os.path.basename(filename),
        "model": typeModel,
        "I": I,
        "J": J,
        "status": status,
        "objective_value": obj,
        "num_open_facilities": operFacilities,
        "runtime_s": model.getTotalTime(),
        "avg_fixedCosts": avgFixedCost,
        "avg_costMatrix": avgCostMatrix,
        "avg_capacity": avgCapacity,
        "nodes_explored": nodes,
        "gap": model.getGap(),
    }

    os.makedirs(os.path.dirname(resultPath), exist_ok=True)
    df = pd.DataFrame([result])

    if not os.path.exists(resultPath):
        df.to_csv(resultPath, index=False)
    else:
        df.to_csv(resultPath, mode="a", header=False, index=False)
    print(f"[OK] Risultati salvati in {resultPath}")
    print(df)


"""
Genera le istanze per i problemi Pdispertion / Maxisum Dispertion
Parametri:
IRange : range di valori per le facilities
PRange : range di valori per p

Return:
I : num. facility 
facilities : coordinate facilities
p : num. facilities da aprire
distanceMatrix : matrice delle distanze
"""
def generateInstanceDispersion(IRange, PRange):

    I = random.randint(IRange[0], IRange[1]) 
    print(f"#facilities: {I}")

    facilities = []
    for i in range(I):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        facilities.append((x, y))

    distanceMatrix = {}
    for i in range(I):
        for j in range(i + 1, I):
            dist = np.sqrt((facilities[i][0] - facilities[j][0])**2 + 
                          (facilities[i][1] - facilities[j][1])**2)
            distanceMatrix[(i, j)] = dist
            distanceMatrix[(j, i)] = dist
            

    p = random.randint(PRange[0], PRange[1])
    
    return I, facilities, p, distanceMatrix

"""
Genera tutti i gruppi di istanze di benchmark

Parametri:
instanceRange : numero di istance per gruppo da generare
outputDir : directory in cui salvare i risultati

Return:
allInstances : ritorna tutte le istanze generate
"""
def generateAllInstancesPdispertion(instanceRange, outputDir="benchmark_instances/P_dispersion" ):
    os.makedirs(outputDir, exist_ok=True)
    
    allInstances = []
    instanceCounter = 1
    
    print("=" * 60)
    print("GENERAZIONE ISTANZE BENCHMARK P_Dispersion/Maxisum Dispersion")
    print("=" * 60)
    
    for groupKey, groupParams in INSTANCE_GROUPS_P_DISPERSION.items():
        print(f"\nGENERAZIONE GRUPPO {groupParams['name'].upper()}:")
        print("-" * 40)
        print(f"Facilities: {groupParams['I_range']}")
        print(f"Num. facilities da aprire (p): {groupParams['p_range']}")
        print()
        
        for i in range(instanceRange):
            print(f"Generazione istanza {instanceCounter} ({groupParams['name']}_{i+1}):")
            # Genera istanza base
            I, facilities, p, distanceMatrix = generateInstanceDispersion(
                groupParams['I_range'], 
                groupParams['p_range'], 
            )
            
            # Calcola statistiche per verifica
            avgDistance = sum(distanceMatrix.values()) / len(distanceMatrix)
            
            instanceData = {
                'instance_id': f'{groupKey.upper()}_{i+1:02d}',
                'group': groupParams['name'],
                'group_key': groupKey,
                'instance_number_in_group': i+1,
                'parameters': {
                    'I_range': groupParams['I_range'],
                    'p_range': groupParams['p_range']
                },
                'I': I,
                'p': p,
                'facilities': facilities,
                'distanceMatrix': distanceMatrix,
                'statistics': {
                    'avg_distance': round(avgDistance, 2),
                    'min_distance': min(distanceMatrix.values()),
                    'max_distance': max(distanceMatrix.values())
                },
            }
            
            allInstances.append(instanceData)
            
            # Salva istanza 
            filename = f"{outputDir}/{instanceData['instance_id']}.json"
            saveInstanceJSON(instanceData, filename)
            
            instanceCounter += 1
    
    # Genera file riepilogativo
    summaryData = {
        'generation_info': {
            'total_instances': len(allInstances),
            'instances_per_group': 3
        },
        'groups': {
            groupKey: {
                'name': groupParams['name'],
                'parameters': groupParams,
                'instances': [inst['instance_id'] for inst in allInstances 
                             if inst['group_key'] == groupKey]
            } for groupKey, groupParams in INSTANCE_GROUPS_P_DISPERSION.items()
        },
        'instances_summary': [
            {
                'instance_id': inst['instance_id'],
                'group': inst['group'],
                'I': inst['I'],
                'avg_distance': inst['statistics']['avg_distance'],
                'min_distance': inst['statistics']['min_distance'],
                'max_distance': inst['statistics']['max_distance'],
            } for inst in allInstances
        ]
    }
    
    summaryFilename = f"{outputDir}/benchmark_summary_Pdispertion.json"
    with open(summaryFilename, 'w') as f:
        json.dump(summaryData, f, indent=4)
    
    print("=" * 60)
    print(" GENERAZIONE COMPLETATA!")
    print("=" * 60)
    print()
    
    return allInstances


"""
Genera le tabelle CSV contenenti i risultati del benchmark

Parametri: 
model : modello ottimizzato
filename : nome del file da leggere per generare la tabella
resultPath : path in cui salvare la tabella
I : num. facilities
p : num. facilities da aprire
d : matrice delle distanze
facilities : coordinate delle facilities
typeModel : identifica il tipo di modello 
nodes : numero di nodi esplorati
"""
def generateTablePdispersion(model, filename, resultPath, I,p,d,facilities,typeModel , nodes):
    
    y = model.data['y']

    # calcolo memoria totale utilizzata
    proc = psutil.Process(os.getpid())
    mem = proc.memory_info().rss / 1024**2

    # estrazione variabili
    if typeModel == "Pdisp":
        D = model.data['D']
        M = model.data['M']
        optimalMinDistance = model.getVal(D)

    else:
        z = model.data['z']


    status = model.getStatus()
    obj = model.getObjVal()


    #  lista delle facilities aperte
    selectedFacilities = []
    openFacilities = 0
    for i in range(len(y)):
        if model.getVal(y[i]) > 0.5:  
            selectedFacilities.append(i)
            openFacilities+=1

    # lista delle distanze tra le facilities aperte
    selectedDistances = []
    for i in range(len(selectedFacilities)):
        for j in range(i + 1, len(selectedFacilities)):
            facI, facJ = selectedFacilities[i], selectedFacilities[j]
            # Cerca la distanza nel dizionario
            if (facI, facJ) in d:
                selectedDistances.append(d[(facI, facJ)])
            elif (facJ, facI) in d:
                selectedDistances.append(d[(facJ, facI)])

    # calcolo statistiche
    avgDistance = sum(selectedDistances) / len(selectedDistances)
    minDistance = min(selectedDistances)
    maxDistance = max(selectedDistances)
    stdDistribution = np.std(selectedDistances)


    print(f"Facilities selezionate: {selectedFacilities}")

    result = {
        "instance": os.path.basename(filename),
        "model": typeModel,
        "I": I,
        "p": p,
        "M": M if typeModel == "Pdisp" else None,
        "min_distance": round(minDistance,5),
        "max_distance": round(maxDistance,5),
        "status": status,
        "objective_value": round(obj, 4),
        "D": round(optimalMinDistance,4) if typeModel == "Pdisp" else None,
        "num_open_facilities": openFacilities,
        "avg_distanceMatrix": round(avgDistance,4),
        "std_Distribution" : round(stdDistribution,3),
        "nodes_explored": nodes,
        "runtime_s": round(model.getTotalTime(),5),
        "mem_MB": round(mem,2),
        "gap": model.getGap()
    }


    os.makedirs(os.path.dirname(resultPath), exist_ok=True)
    df = pd.DataFrame([result])

    if not os.path.exists(resultPath):
        df.to_csv(resultPath, index=False)
    else:
        df.to_csv(resultPath, mode="a", header=False, index=False)

    print(f"[OK] Risultati salvati in {resultPath}")
    print(df)


if __name__ == "__main__":
    
    # genera le istanze 
    allInstancesFLP = generateAllInstancesFLP(instanceRange=10)
    allInstances = generateAllInstancesPdispertion(instanceRange=10)