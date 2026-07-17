from solve import risolvi_istanza
import csv
import json
import time
from utils.generate_data import genera_dati, esporta_in_dat, leggi_da_dat
import tracemalloc 

MODALITA_CARICAMENTO = True #Parametro per decidere se caricare i dati da file .dat o generarli ex-novo

cartella_dat = "data"

if MODALITA_CARICAMENTO:
    print(f"Lettura file .dat dalla cartella '{cartella_dat}'...\n")
else:
    print(f"Creazione nuovi dati e salvataggio in '{cartella_dat}'...\n")

risultati = []
tutte_le_istanze = []

intestazione = [
    "Dim_Grande", "Domanda_Alta", "Asse_Lungo", "Istanza_Num", 
    "Tempo_Esecuzione(s)", "Memoria_Picco(MB)", "Iterazioni_Pricing", 
    "1_Euristica", "2_Intera", "3_Arrotondata_Iniziale", 
    "4_Ottima_Rilassata", "5_Intera_Arrotondando"
]
risultati.append(intestazione)

conteggio_run = 1

for dim_grande in [False, True]: # Primo parametro: una istanza con tanti moduli, una con pochi moduli
    for domanda_alta in [False, True]: # Secondo parametro: una istanza con un numero basso di pezzi per modulo, una con un numero alto di pezzi per modulo
        for asse_lungo in [False, True]: # Terzo parametro: una istanza con asse corto rispetto a moduli, una con asse lungo rispetto a moduli
            for i in range(1, 11):
                print(f"Esecuzione {conteggio_run}/80 | Classe: Dim={dim_grande}, Dom={domanda_alta}, Asse={asse_lungo} | Istanza={i}")
                
                nome_file_dat = f"{cartella_dat}/istanza_{conteggio_run}_dim{dim_grande}_dom{domanda_alta}_asse{asse_lungo}_num{i}.dat"
                
                if MODALITA_CARICAMENTO:
                    # Lettura da file dat
                    m, dom, lung, asse = leggi_da_dat(nome_file_dat)
                else:
                    # Generazione dati casuali
                    m, dom, lung, asse = genera_dati(dim_grande, domanda_alta, asse_lungo)
                    
                    istanza_corrente = {
                        "ID_Run": conteggio_run,
                        "Classe": f"Dim_Grande={dim_grande}, Domanda_Alta={domanda_alta}, Asse_Lungo={asse_lungo}",
                        "Istanza_Num": i,
                        "Lunghezza_Asse_Principale": asse,
                        "Moduli_Generati": m,
                        "Domanda_Per_Modulo": dom,
                        "Lunghezza_Per_Modulo": lung
                    }
                    tutte_le_istanze.append(istanza_corrente)
                    
                    # Salvataggio istanza
                    esporta_in_dat(istanza_corrente, nome_file_dat)
                
                # Tracciamento per statistiche
                tracemalloc.start()
                inizio = time.time()
                
                # Esecuzione solver
                s1, s2, s3, s4, s5, iters = risolvi_istanza(m, dom, lung, asse)
                
                # Fine tracciamento
                fine = time.time()
                corrente, picco = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                tempo_esec = round(fine - inizio, 2)
                memoria_mb = round(picco / (1024 * 1024), 3) 
                
                riga = [dim_grande, domanda_alta, asse_lungo, i, tempo_esec, memoria_mb, iters, s1, s2, s3, s4, s5]
                risultati.append(riga)
                
                conteggio_run += 1

# Scrittura dati in CSV
nome_file_csv = "./results/risultati_esperimenti.csv"
with open(nome_file_csv, "w", newline="", encoding="utf-8") as file_csv:
    writer = csv.writer(file_csv, delimiter=";") 
    writer.writerows(risultati)
    
# Scrittura JSON dati input generati
if not MODALITA_CARICAMENTO:
    nome_file_json = "./results/dati_istanze_2.json"
    with open(nome_file_json, "w", encoding="utf-8") as file_json:
        json.dump(tutte_le_istanze, file_json, indent=4)

print(f"\nOperazione completata!")
print(f"Risultati esportati con successo.")