# Project Overview

Questo progetto è stato sviluppato all’interno di un **ambiente virtuale (venv)** in cui sono state installate tutte le librerie necessarie per l’esecuzione dei programmi Python.
Prima di eseguire i codici è neessario assicurarsi di avere attivo venv.

## Struttura del progetto

- **`Dispersion_code/`** → contiene i programmi per risolvere i due problemi di dispersione (`Maxisum` e `Pdispersion`).
- **`FLP_code/`** → contiene i programmi per risolvere i problemi **FLP** (`CFLP` e `UFLP`).
- **`benchmark_instances/`** → raccoglie tutte le istanze studiate nella tesi.
- **`results/`** → contiene le tabelle in formato `.csv` utilizzate per generare tabelle e grafici tramite `generateTable.py`.

## Generazione delle istanze di test

Per generare le istanze di test si utilizza il file `generateInstance.py`, presente sia nella cartella **`Dispersion_code`** che in **`FLP_code`**.  
Di default, vengono generate **10 istanze per ogni categoria dimensionale**.

Esempio di utilizzo:

```bash
python Dispersion_code/[pdispersion or Maxisum].py

python FLP_code/[UFLP or CFLP].py

