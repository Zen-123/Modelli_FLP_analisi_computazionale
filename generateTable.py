import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
Carica i dati dal file CSV e li normalizza (rimuove spazi e converte in minuscolo).

Parametri:
filename (str): file CSV da cui estrarre i dati

Return:
df (DataFrame): struttura dati bidimensionale usata per salvare i dati di una tabella 
                e manipolarli, in questo caso salva i dati del file CSV
"""
def loadAndNormalize(filename):
    # carica i dati dal file csv
    df = pd.read_csv(filename)
    # normalizza i nomi delle colonne
    df.columns = df.columns.str.strip().str.lower()
    return df


"""
Mostra tabella riassuntiva del file CSV con tutti i dati per FLP.

Parametri:
df (DataFrame): contiene i dati del file CSV

Return:
summary (DataFrame): df contenente le colonne del file CSV da stampare a schermo 
                    per facilitare la lettura
"""
def createTableFLP(df):
    summary = df[["instance", "model", "i", "j",  "num_open_facilities", "avg_fixedcosts", "avg_capacity","objective_value",
                 ]].drop_duplicates().reset_index(drop=True)
    print(summary)
    return summary

"""
Mostra tabella riassuntiva del file CSV con tutti i dati per Dispersion.

Parametri:
df (DataFrame): contiene i dati del file CSV

Return:
summary (DataFrame): df contenente le colonne del file CSV da stampare a schermo 
                    per facilitare la lettura
"""
def createTableDispersion(df):
    summary = df[["instance", "model", "i", "p", "m", "min_distance", "max_distance", "status",
                  "objective_value", "d", "num_open_facilities", "avg_distancematrix","std_distribution" ,"nodes_explored", "runtime_s", "gap"]].drop_duplicates().reset_index(drop=True)
    print(summary)
    return summary

"""
Mostra tabella riassuntiva del file CSV con i dati riguardanti la distanza per Dispersion.

Parametri:
df (DataFrame): contiene i dati del file CSV

Return:
summary (DataFrame): df contenente le colonne del file CSV da stampare a schermo 
                    per facilitare la lettura
"""
def createTableDistanceDispersion(df):
    summary = df[["instance", "model", "i", "p", "min_distance" , "max_distance", "avg_distancematrix", "std_distribution"]].drop_duplicates().reset_index(drop=True)
    print(summary)
    return summary

"""
Genera un grafico che mostra la relazione tra num.clienti e tempo di runtime

Parametri:
df : contiene i dati del file csv

"""
def clientsRuntimeGraphFLP(df):
    for model in ["UFLP", "CFLP"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["j"], subset["runtime_s"], label=model)

    plt.xlabel("Numero clienti (J)")
    plt.ylabel("Runtime (s)")
    plt.title("Confronto runtime UFLP vs CFLP")
    plt.legend()
    plt.show()

"""
Genera grafico che mostra andamento medio tra numero di clienti e valore di funzione obiettivo

Parametri:
df : contiene i dati del file csv

"""
def clientsOptimalValueGraphFLP(df):

    group = df.groupby(['model', 'j'])['objective_value'].agg(['mean', 'std']).reset_index()
    for model in ["UFLP", "CFLP"]:
        g = group[group['model'] == model].sort_values('j')
        plt.plot(g['j'], g['mean'], marker='o', label=model)

    plt.xlabel("Numero clienti (j)")
    plt.ylabel("Valore funzione obiettivo")
    plt.title("Confronto numero clienti / funzione obiettivo")
    plt.legend()
    plt.show()

"""
Genera un grafico che mostra la relazione tra costo fisso medio di apertura e tempo di runtime

Parametri:
df : contiene i dati del file csv

"""
def avgFixedCostRuntimeGraphFLP(df):
    plt.figure()
    for model in ["UFLP", "CFLP"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["avg_fixedcosts"], subset["runtime_s"], label=model)
    plt.xlabel("Costo fisso medio")
    plt.ylabel("Runtime (s)")
    plt.legend()
    plt.title("Confronto costo fisso medio / runtime")
    plt.show()

"""
Genera un grafico che mostra la relazione tra costo di assegnazione medio e tempo di runtime

Parametri:
df : contiene i dati del file csv
"""
def avgCostMatrixRuntimeGraphFLP(df):
    for model in ["UFLP", "CFLP"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["avg_costmatrix"], subset["runtime_s"], label=model)

    plt.xlabel("distanza media ")
    plt.ylabel("Runtime (s)")

    plt.title("Confronto costo assegnazione medio / runtime")

    plt.legend()
    plt.show()

"""
Genera un grafico che mostra la relazione tra il valore big-M e il runtime 

Parametri:
df : contiene i dati del file csv
"""
def mValueRuntimeGraphDispersion(df):
    plt.figure(figsize=(8,5))
    for model in ["Pdisp"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["m"], subset["runtime_s"])
        
    plt.xlabel("Valore di M ")
    plt.ylabel("Runtime (s)")
    plt.xticks(np.arange(0, 110000, 10000))
    plt.show()

"""
Genera un grafico che mostra la relazione tra il valore big-M e i nodi esplorati 

Parametri:
df : contiene i dati del file csv
"""
def mValueNodesGraphDispersion(df):
    for model in ["Pdisp"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["m"], subset["nodes_explored"])
        
    plt.xlabel("Valore di M")
    plt.ylabel("Nodi esplorati")    
    plt.xticks(np.arange(0, 11000, 1000))
    plt.show()

"""
Genera un grafico che mostra la relazione tra il valore big-M e il valore della funzione obiettivo

Parametri:
df : contiene i dati del file csv
"""
def mValueObjValueGraphDispersion(df):
    for model in ["Pdisp"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["m"], subset["objective_value"])
        
    plt.xlabel("Valore di M")
    plt.ylabel("Valore funzione obiettivo")
    plt.xticks(np.arange(0, 11000, 1000))
    plt.show()

"""
Genera un grafico che mostra la relazione tra num.totale facilities e tempo di runtime

Parametri:
df : contiene i dati del file csv

"""
def totalFacilitiesRuntimeGraphFLP(df):
    for model in ["UFLP", "CFLP"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["i"], subset["runtime_s"], label=model)

    plt.xlabel("Numero facilities totali")
    plt.ylabel("Runtime (s)")
    plt.legend()
    plt.title("Confronto facilities totali / runtime")

    plt.show()

"""
Genera un grafico che mostra la relazione tra num.clienti e  num. facilities aperte

Parametri:
df : contiene i dati del file csv

"""
def clientsOpenFacilitiesGraphFLP(df):

    for model in ["UFLP", "CFLP"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["j"], subset["num_open_facilities"], label=model)

    plt.xlabel("Numero clienti")
    plt.ylabel("Numero facilities aperte")

    plt.axline((0, 0), slope=0.075, color="gray", linestyle="--")
    plt.axhline(y=1, color="red", linestyle="--") 

    plt.legend()
    plt.show()

"""
Genera un grafico che mostra la relazione tra costo di assegnazione medio e numero facilities aperte

Parametri:
df : contiene i dati del file csv

"""
def avgCostMatrixNumOpenFacGraphFLP(df):

    for model in ["UFLP", "CFLP"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["avg_costmatrix"],subset["num_open_facilities"], label=model)

    plt.xlabel("Distanza media")
    plt.ylabel("Numero facilities aperte")
    plt.title("Confronto costo assegnazione medio / numero facilities aperte")

    plt.legend()
    plt.show()


"""
Genera grafico che mostra andamento medio tra numero di facilities aperte e valore di funzione obiettivo

Parametri:
df : contiene i dati del file csv
"""
def openFacilitiesOptimalValueGraphFLP(df):

    for model in ["UFLP", "CFLP"]:
        subset = df[df["model"] == model]
        grouped = subset.groupby("num_open_facilities")["objective_value"].mean().reset_index()
        x = grouped["num_open_facilities"]
        y = grouped["objective_value"]
        plt.plot(x, y, "o-", label=f"{model}")

    plt.xlabel("Numero facilities aperte")
    plt.ylabel("Valore funzione obiettivo")
    plt.title("Confronto facilities aperte / valore ottimo")

    plt.legend()
    plt.show()

"""
Genera grafico che mostra relazione tra costo fisso medio e valore funzione obiettivo

Parametri:
df : contiene i dati del file csv

"""
def avgFixedCostOptimalValueGraphFLP(df):
    for model in ["UFLP", "CFLP"]:
        subset = df[df["model"] == model]
        grouped = subset.groupby("avg_fixedcosts")["objective_value"].mean().reset_index()
        
        x = grouped["avg_fixedcosts"]
        y = grouped["objective_value"]
        
        plt.plot(x, y, "o-", label=model)

    plt.xlabel("Costo fisso medio")
    plt.ylabel("Valore medio della funzione obiettivo")
    plt.title("Confronto costo fisso medio / valore ottimo")

    plt.legend()
    plt.show()

"""
Genera grafico che mostra relazione tra costo di assegnazione medio e valore funzione obiettivo

Parametri:
df : contiene i dati del file csv

"""
def avgCostMatrixOptimalValueGraphFLP(df):
    for model in ["UFLP", "CFLP"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["avg_costmatrix"],subset["objective_value"], label=model)

    plt.xlabel("Distanza media")
    plt.ylabel("Valore funzione obiettivo")
    plt.title("Confronto costo assegnazione medio / valore ottimo")

    plt.legend()
    plt.show()

"""
Genera grafico che mostra relazione tra costo fisso medio e numero facilities aperte

Parametri:
df : contiene i dati del file csv

"""
def avgFixedCostOpenFacilitiesGraphFLP(df):
    for model in ["UFLP", "CFLP"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["avg_fixedcosts"],subset["num_open_facilities"], label=model)

    plt.xlabel("Costo fisso medio")
    plt.ylabel("Numero di facilities aperte")
    plt.title("Confronto costo fisso medio / numero facilities aperte")

    plt.legend()
    plt.show()

"""
Genera grafico che mostra relazione tra nodi esplorati e runtime

Parametri:
df : contiene i dati del file csv

"""
def nodesExploredRuntimeGraphFLP(df):
    for model in ["UFLP", "CFLP"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["nodes_explored"], subset["runtime_s"], label=model)

    plt.xlabel("Numero nodi esplorati")
    plt.ylabel("Runtime(s)")

   
    # plot mezza parabola positiva 
    plt.ylim(-50,2000)
    x = np.linspace(-10, df["nodes_explored"].max(), 200)

    # parametri parabola
    a = 0.00035  
    b = 0        
    y = a * (x - x.min())**2 + b

    # plot parabola
    plt.plot(x, y, color="gray", linestyle="--", linewidth=1) 
    plt.title("Confronto nodi esplorati / runtime")

    plt.legend()
    plt.show()

"""
Genera grafico che mostra relazione tra facilities totali e tempo di runtime (Dispersion)

Parametri:
df : contiene i dati del file csv

"""
def totalFacilityRuntimeGraphDispersion(df):
    for model in ["Pdisp", "MaxS"]:
        subset = df[df["model"] == model]
        grouped = subset.groupby("i")["runtime_s"].mean().reset_index()
        x = grouped["i"]
        y = grouped["runtime_s"]
        plt.plot(x, y, "o-", label=f"{model}", alpha=0.7)

   

    a = 0.4                     
    x0 = x.min()           
    b = y.min() - 0.1 * y.min()     

    xParab = np.arange(x.min(), x.max() + 1)
    yParab = a * (xParab - x0)**2 + b
    plt.plot(xParab, yParab, '--', color="lightgray") 
    


    plt.xlabel("Numero facilities totali (i)")
    plt.ylabel("Runtime medio (s)")
    plt.xticks(np.arange(df["i"].min(), df["i"].max() + 1, 1))
    plt.title("Confronto facilities totali / runtime")

    plt.legend()
    plt.show()


"""
Genera grafico che mostra relazione tra num. facilities aperte e nodi esplorati (Dispersion)

Parametri:
df : contiene i dati del file csv

"""
def openFacilityNodesGraphDispersion(df):
    for model in ["Pdisp", "MaxS"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["p"], subset["nodes_explored"], label=model)

    plt.xlabel("Numero facilities aperte (p)")
    plt.ylabel("Nodi esplorati")
    plt.title("Confronto facilities aperte / ndoi esplorati")

    plt.legend()
    plt.show()

"""
Genera grafico che mostra relazione tra num. facilities aperte (p) e num.totale facilities (Dispersion)

Parametri:
df : contiene i dati del file csv

"""
def openFacilityTotalFacilitiesGraphDispersion(df):
    for model in ["Pdisp", "MaxS"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["p"], subset["i"], label=model)

    plt.xlabel("Numero facilities aperte (p)")
    plt.ylabel("Numero facilities totali")
    plt.legend()
    plt.title("Confronto facilities aperte / facilities totali")

    plt.show()


"""
Genera grafico che mostra relazione tra num. facilities aperte (p) e il runtime  (Dispersion)

Parametri:
df : contiene i dati del file csv

"""
def openFacilityRuntimeGraphDispersion(df):
    for model in ["Pdisp", "MaxS"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["p"], subset["runtime_s"], label=model)

    plt.xlabel("Numero facilities aperte (p)")
    plt.ylabel("Runtime (s)")
    plt.legend()
    plt.title("Confronto facilities aperte / runtime")

    plt.show()


"""
Genera grafico che mostra relazione tra num. totale facilities e memoria RAM usata

Parametri:
df : contiene i dati del file csv

"""
def totalFacilitiesMemGraphDispersion(df):
    for model in ["Pdisp", "MaxS"]:
        subset = df[df["model"] == model]
        grouped = subset.groupby("i")["mem_mb"].mean().reset_index()
        x = grouped["i"]
        y = grouped["mem_mb"]
        plt.scatter(x, y, label=f"{model} (dati)", alpha=0.7)
        coeffs = np.polyfit(x, y, deg=2) 
        xPlot = np.linspace(x.min(), x.max(), 200)
        yPlot = np.polyval(coeffs, xPlot)
        plt.plot(xPlot, yPlot, linestyle='--')


    plt.xlabel("Numero facilities totali (i)")
    plt.ylabel("Memoria utilizzata (MB)")
    plt.xticks(np.arange(df["i"].min(), df["i"].max() + 1, 1)) 
    plt.title("Confronto facilities totali / memoria")

    plt.legend()
    plt.show()


"""
Genera grafico che mostra relazione tra nodi esplorati e memoria RAM usata

Parametri:
df : contiene i dati del file csv

"""
def nodesExploredMemGraphDispersion(df):
    for model in ["Pdisp", "MaxS"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["nodes_explored"], subset["mem_mb"], label=model)

    plt.xlabel("Nodi esplorati")
    plt.ylabel("Memoria utilizzata (MB)")
    plt.xscale('log')



    plt.ylim(100,350)
    xMin = df["nodes_explored"].min()
    xMax = df["nodes_explored"].max()
    xParab = np.linspace(xMin, xMax, 100)

    # parametri parabola
    a = 0.00005 
    x0 = xMin   
    b = df["mem_mb"].min() 

    yParab = a * (xParab - x0)**2 + b
    plt.plot(xParab, yParab, color='gray', linestyle='--', linewidth=1) 
    plt.title("Confronto nodi esplorati / memoria")
    plt.legend()
    plt.show()

"""
Genera grafico che mostra relazione tra nodi esplorati e runtime (Dispersion)

Parametri:
df : contiene i dati del file csv

"""
def nodesExploredRuntimeGraphDispersion(df):
    for model in ["Pdisp", "MaxS"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["nodes_explored"], subset["runtime_s"], label=model)

    plt.xlabel("Nodi esplorati")
    plt.ylabel("Runtime (s)")


    plt.ylim(-10,500)
    xMin = df["nodes_explored"].min()
    xMax = df["nodes_explored"].max()
    xParab = np.linspace(xMin, xMax, 100)

    a = 0.000008  
    x0 = xMin  
    b = df["runtime_s"].min()  

    yParab = a * (xParab - x0)**2 + b
    plt.plot(xParab, yParab, color='gray', linestyle='--', linewidth=1) 

    plt.title("Confronto nodi esplorati / runtime")


    plt.legend()
    plt.show()

"""
Genera grafico che mostra relazione tra facilities totali (i) e nodi esplorati (Dispersion)

Parametri:
df : contiene i dati del file csv

"""
def totalFacilitiesNodesExploredGraphDispersion(df):
    for model in ["Pdisp", "MaxS"]:
        subset = df[df["model"] == model]
        plt.scatter(subset["i"], subset["nodes_explored"], label=model)

    plt.xlabel("Num. facilities totali (i)")
    plt.ylabel("Nodi esplorati")
    xMin = df["i"].min()
    xMax = df["i"].max()
    plt.xticks(np.arange(xMin, xMax + 1, 1))  

  
    xParab = np.linspace(xMin,xMax, 200)

    a = 15  
    x0 = xMin+2   
    b = df["nodes_explored"].min()  

    yParab = a * (xParab - x0)**2 + b

    plt.plot(xParab, yParab, color='gray', linestyle='--', linewidth=1) 
    plt.title("Confronto facilities totali / nodi esplorati")

    plt.legend()
    plt.show()



if __name__ == "__main__":

    # CARICAMENTO E ANALISI DATI FLP
    # Carica e normalizza entrambi i CSV (FLP)
    uflp = loadAndNormalize("results/FLP/uflp_results.csv")  # Carica dati UFLP
    cflp = loadAndNormalize("results/FLP/cflp_results.csv")  # Carica dati CFLP
    df = pd.concat([uflp, cflp], ignore_index=True)      # Combina i dataset FLP


    # CARICAMENTO E ANALISI DATI DISPERSION
    # Carica e normalizza entrambi i CSV (Dispersion)
    maxS = loadAndNormalize("results/P_dispersion/maxS_results.csv")   # Carica dati MaxS
    pDisp = loadAndNormalize("results/P_dispersion/pdisp_results.csv") # Carica dati P-dispersion
    dfDispersion = pd.concat([maxS, pDisp], ignore_index=True)         # Combina i dataset Dispersion

    # TABELLE RIASSUNTIVE
    createTableFLP(df)                                   # Tabella dati csv FLP
    createTableDispersion(dfDispersion)                  # Tabella dati csv Dispersion
    createTableDistanceDispersion(dfDispersion)          # Tabella statistiche sulle distanze per Dispersion 


    # GRAFICI ANALISI FLP (Runtime, Funzione Ob., Nodi esplorati )  

    clientsRuntimeGraphFLP(df)                              # Grafico clienti / runtime
    clientsOptimalValueGraphFLP(df)                         # Grafico clienti / valore obiettivo
    totalFacilitiesRuntimeGraphFLP(df)                      # Grafico facilities totali / runtime
    clientsOpenFacilitiesGraphFLP(df)                       # Grafico clienti / facilities aperte
    openFacilitiesOptimalValueGraphFLP(df)                  # Grafico facilities aperte / valore obiettivo
    nodesExploredRuntimeGraphFLP(df)                        # Grafico nodi esplorati / runtime

    # GRAFICI COSTI E DISTANZE FLP 
    avgFixedCostRuntimeGraphFLP(df)                         # Grafico costo fisso medio / runtime
    avgCostMatrixRuntimeGraphFLP(df)                        # Grafico distanza media / runtime
    avgFixedCostOptimalValueGraphFLP(df)                    # Grafico costo fisso medio / valore obiettivo
    avgCostMatrixOptimalValueGraphFLP(df)                   # Grafico distanza media / valore obiettivo
    avgFixedCostOpenFacilitiesGraphFLP(df)                  # Grafico costo fisso medio / facilities aperte
    avgCostMatrixNumOpenFacGraphFLP(df)                     # Grafico distanza media / facilities aperte

    # GRAFICI ANALISI DISPERSION (Runtime, nodi esplorati, memoria)
    totalFacilityRuntimeGraphDispersion(dfDispersion)              # Grafico facilities totali / runtime 
    openFacilityNodesGraphDispersion(dfDispersion)                 # Grafico facilities aperte / nodi esplorati
    openFacilityTotalFacilitiesGraphDispersion(dfDispersion)       # Grafico facilities aperte / facilities totali
    openFacilityRuntimeGraphDispersion(dfDispersion)               # Grafico facilities aperte / runtime
    totalFacilitiesMemGraphDispersion(dfDispersion)                # Grafico facilities totali / memoria
    nodesExploredMemGraphDispersion(dfDispersion)                  # Grafico nodi esplorati / memoria
    nodesExploredRuntimeGraphDispersion(dfDispersion)              # Grafico nodi esplorati / runtime (Dispersion)
    totalFacilitiesNodesExploredGraphDispersion(dfDispersion)      # Grafico facilities totali / nodi esplorati





