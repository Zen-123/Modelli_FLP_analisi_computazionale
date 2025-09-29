# Modelli FLP - Analisi Computazionale

Questo repository contiene il codice Python sviluppato per l'analisi computazionale di diversi modelli di Facility Location Problem (FLP) e problemi di dispersione trattati nella tesi di laurea.

## Descrizione del Progetto

Il progetto implementa i seguenti quattro problemi FLP descritti in maniera estesa nella tesi:

**Problemi di Facility Location:**
- **UFLP**: problema di localizzazione senza vincoli di capacità (Cap. 2, par. 2.3)
- **CFLP**: problema di localizzazione con capacità limitate (Cap 2, par. 2.4)
  
**Problemi di Dispersione:**
- **p-Dispersion**: problema di massimizzazione della distanza minima tra p facilities selezionate (Cap.2, par. 2.5.1)
- **Maxisum**: problema di massimizzazione della somma delle distanze tra p facilities selezionate (Cap.2, par. 2.5.2)

## Struttura del Repository

```
Modelli_FLP_analisi_computazionale/
│
├── generateInstance.py
├── generateTable.py         
├── FLP_code/
│   ├── CFLP.py
│   └── UFLP.py
│
├── Dispersion_code/
│   ├── pdispersion.py
│   └── Maxisum.py
│
├── benchmark_instances/
│   └── [istanze di test utilizzate nella tesi]
│
└── results/
    └── [file .csv con i risultati delle analisi]
```
### Descrizione delle Directory

**FLP_code**: contiene i programmi per la risoluzione dei problemi CFLP e UFLP

**Dispersion_code**: contiene i programmi per la risoluzione dei problemi di dispersione

**benchmark_instances**: raccoglie tutte le istanze di test utilizzate negli esperimenti della tesi, organizzate per categoria dimensionale.

**results**: contiene i file in formato CSV con i risultati degli esperimenti computazionali, utilizzati successivamente per generare tabelle e grafici attraverso il file `generateTable.py`.

## Requisiti di Sistema

### Prerequisiti

- Python 3.12
- pip 
- virtualenv (venv)

### Dipendenze

Il progetto è stato sviluppato all'interno di un ambiente virtuale Python con le seguenti librerie principali:

- pyscipopt (per la risoluzione dei modelli di ottimizzazione)
- numpy (per operazioni numeriche)
- pandas (per la gestione dei dati csv)
- matplotlib (per la generazione di grafici)
- psutil (statistiche sulla memoria usata)

## Installazione

### 1. Clonare il Repository

```bash
git clone https://github.com/Zen-123/Modelli_FLP_analisi_computazionale.git
cd Modelli_FLP_analisi_computazionale
```

### 2. Creare e Attivare l'Ambiente Virtuale

#### Su Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### Su macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installare le Dipendenze

```bash
pip install -r requirements.txt
```

## Utilizzo

### Generazione delle Istanze

Prima di eseguire i problemi, è possibile generare nuove istanze di test utilizzando il file `generateInstance.py` presente in ciascuna cartella.

```bash
python generateInstance.py
```
Di default vengono generate 10 istanze per ogni categoria dimensionale, per cambiare il numero di istanze generate è sufficiente modificare il parametro instanceRange presente nel main.

All'interno del file `generateInstance.py` è possibile configurare:

- Numero di istanze da generare per categoria dimensionale
- Dimensioni delle istanze (numero di facilities, numero di clienti) tramite INSTANCE_GROUPS
- Range dei valori per costi fissi, costi variabili e capacità

### Esecuzione dei Modelli

#### Problemi di Facility Location

**CFLP:**
```bash
python FLP_code/CFLP.py
```

**UFLP:**
```bash
python FLP_code/UFLP.py
```

#### Problemi di Dispersione

**p-Dispersion:**
```bash
python Dispersion_code/pdispersion.py
```

**Maxisum:**
```bash
python Dispersion_code/Maxisum.py
```

### Generazione di Tabelle e Grafici

Dopo aver eseguito i programmi dei modelli per risolvere i corrispettivi problemi, i risultati vengono salvati nella cartella `results/` in formato CSV. Per generare tabelle e grafici riepilogativi:

```bash
python generateTable.py
```

Questo script legge i file CSV presenti nella cartella `results/` e produce i grafici dei dati sperimentali.

## Output

I programmi producono diversi tipi di output:

**Output su console**: durante l'esecuzione vengono stampate informazioni sul progresso della risoluzione, tempo impiegato, valore della funzione obiettivo, memoria usata, gap di ottimalità.

**File CSV**: i risultati dettagliati vengono salvati nella cartella `results/` con informazioni su ogni istanza risolta, per un elenco dettagliato delle colonne salvate fare riferimento alla tesi (Cap.3, par. 3.1.1 o cap.4 par. 4.2 ).



### Ambiente virtuale non attivo

Prima di eseguire qualsiasi script, verificare che l'ambiente virtuale sia attivo. Si dovrebbe vedere `(venv)` all'inizio della riga di comando. In caso contrario, attivare l'ambiente come descritto nella sezione Installazione.

### Istanze non trovate

Se i programmi non trovano le istanze, verificate che:

- Le istanze siano presenti nella cartella corretta (`benchmark_instances/`)
- I path nei file Python corrispondano alla struttura delle directory
- I nomi dei file delle istanze siano corretti

## Estensioni e Personalizzazioni

Il codice è strutturato per facilitare estensioni e personalizzazioni:

**Aggiunta di nuove formulazioni**: è possibile implementare varianti dei modelli modificando le funzioni di creazione del modello nei file principali.

**Analisi di sensibilità**: modificando i parametri di generazione delle istanze è possibile studiare l'impatto di diversi fattori sulla difficoltà computazionale.

**Nuove metriche di performance**: la struttura modulare consente di aggiungere facilmente nuove metriche di valutazione nei file di output.


## Licenze delle dipendenze

Questo progetto utilizza la libreria [PySCIPOpt](https://github.com/SCIP-Interfaces/PySCIPOpt), rilasciata sotto licenza Apache 2.0.  
Per maggiori dettagli, consulta il file [LICENSE-APACHE](https://www.apache.org/licenses/LICENSE-2.0).


## Riferimenti

Per una descrizione dettagliata dei modelli matematici, delle formulazioni e dei risultati sperimentali, si rimanda alla tesi di laurea associata a questo progetto.

---

**Nota**: Prima di eseguire qualsiasi script, assicurarsi sempre che l'ambiente virtuale sia attivo per garantire che tutte le dipendenze siano correttamente caricate.
