import random
import re

def genera_dati(dim_grande, domanda_alta, asse_lungo):
    """
    Genera i dati dell'istanza in base ai 3 parametri booleani.
    """
    # 1) Dimensioni del problema 
    # Tra 5 e 10 moduli, oppure intorno ai 50 
    num_moduli = random.randint(45, 55) if dim_grande else random.randint(5, 10)
    
    moduli = [f"M{i}" for i in range(1, num_moduli + 1)]
    
    # 2) Entità della domanda 
    # Da 1 a 10 unità, oppure tra 50 e 100 
    domanda = {}
    for m in moduli:
        if domanda_alta:
            domanda[m] = random.randint(50, 100)
        else:
            domanda[m] = random.randint(1, 10)
            
    # 3) Lunghezze e Asse 
    lunghezze = {m: random.randint(10, 50) for m in moduli}
    
    # Asse molto lungo rispetto ai moduli o abbastanza corto 
    max_lunghezza_modulo = max(lunghezze.values())
    if asse_lungo:
        lunghezza_asse = max_lunghezza_modulo * random.randint(10, 20) # Ricavo molti pezzi
    else:
        lunghezza_asse = max_lunghezza_modulo * random.randint(2, 4)   # Ricavo pochi pezzi
        
    return moduli, domanda, lunghezze, lunghezza_asse

def esporta_in_dat(istanza_dict, nome_file):
    """Genera un file .dat compatibile con AMPL a partire dal dizionario dell'istanza."""
    with open(nome_file, "w") as f:
        # Lunghezza asse
        f.write(f"param L := {istanza_dict['Lunghezza_Asse_Principale']};\n\n")
        
        # Insieme moduli
        f.write("set MODULI := ")
        for m in istanza_dict['Moduli_Generati']:
            f.write(f"{m} ")
        f.write(";\n\n")
        
        # Parametro domanda
        f.write("param d :=\n")
        for m, dom in istanza_dict['Domanda_Per_Modulo'].items():
            f.write(f"  {m} {dom}\n")
        f.write(";\n\n")
        
        # Parametro lunghezze
        f.write("param l :=\n")
        for m, lung in istanza_dict['Lunghezza_Per_Modulo'].items():
            f.write(f"  {m} {lung}\n")
        f.write(";\n")

def leggi_da_dat(nome_file):
    """Legge un file .dat e ricostruisce i parametri per la risoluzione."""
    with open(nome_file, 'r') as f:
        content = f.read()

    match_L = re.search(r'param L := (\d+);', content)
    lunghezza_asse = int(match_L.group(1))

    match_M = re.search(r'set MODULI := (.*?);', content, re.DOTALL)
    moduli = match_M.group(1).strip().split()

    match_d = re.search(r'param d :=\n(.*?);', content, re.DOTALL)
    domanda = {}
    for line in match_d.group(1).strip().split('\n'):
        parts = line.strip().split()
        if len(parts) == 2:
            domanda[parts[0]] = int(parts[1])

    match_l = re.search(r'param l :=\n(.*?);', content, re.DOTALL)
    lunghezze = {}
    for line in match_l.group(1).strip().split('\n'):
        parts = line.strip().split()
        if len(parts) == 2:
            lunghezze[parts[0]] = int(parts[1])

    return moduli, domanda, lunghezze, lunghezza_asse