import math
from amplpy import AMPL

MASTER_MOD_FILE = "./models/master.mod"
PRICING_MOD_FILE = "./models/pricing.mod"

def risolvi_istanza(moduli, domanda, lunghezze, lunghezza_asse):
    # Master
    master = AMPL()
    master.read(MASTER_MOD_FILE)
    
    # Pricing (Slave)
    pricing = AMPL()
    pricing.read(PRICING_MOD_FILE)
    
    # Soluzione euristica (1 pattern per ogni modulo, che taglia esattamente 1 pezzo di quel modulo)
    patterns_iniziali = [f"P{i}" for i in range(1, len(moduli) + 1)]
    
    master.set["MODULI"] = moduli
    master.set["R"] = patterns_iniziali
    master.param["d"] = domanda
    
    # Matrice A[i, j]: identità (1 solo se il pattern P_i taglia il modulo M_i)
    matrice_A = { (moduli[i], patterns_iniziali[i]): 1 for i in range(len(moduli)) }
    master.param["A"] = matrice_A

    master.option["solver"] = "gurobi" 
    pricing.option["solver"] = "gurobi"
    master.option["solver_msg"] = 0
    pricing.option["solver_msg"] = 0

    # =========================================================
    # SOLUZIONE 1: Euristica Predeterminata 
    # =========================================================
    sol1_euristica = sum(domanda.values())
    print(f"1. Soluzione Euristica predeterminata: {sol1_euristica} assi")

    # =========================================================
    # SOLUZIONE 2: Problema Intero
    # =========================================================
    master.solve()
    sol2_intera = master.get_objective("Obj_Master").value()
    print(f"2. Soluzione Problema Intero: {sol2_intera} assi")

    # =========================================================
    # SOLUZIONE 3: Arrotondata per Eccesso
    # =========================================================
    # Rilassiamo del master
    master.eval("let {j in R} x[j].relax := 1;") 
    master.solve()
    
    sol3_arrotondata = 0
    for j in master.get_variable("x").get_values().to_dict():
        valore_continuo = master.get_variable("x")[j].value()
        sol3_arrotondata += math.ceil(valore_continuo)
    print(f"3. Soluzione Arrotondata per eccesso: {sol3_arrotondata} assi")

    # =========================================================
    # CICLO DI PRICING (COLUMN GENERATION)
    # =========================================================
    pricing.set["MODULI"] = moduli
    pricing.param["L"] = lunghezza_asse
    pricing.param["l"] = lunghezze

    iterazione = 0
    pattern_count = len(patterns_iniziali)

    while True:
        iterazione += 1
        
        master.solve()

        duali = master.get_constraint("Vincolo_Domanda").get_values().to_dict() # Prezzi ombra
        pricing.param["u"] = duali
        pricing.solve()
        valore_pricing = pricing.get_objective("W").value()
        
        # Termina se non ho più pattern con costo ridotto (valore_pricing <= 1)
        if valore_pricing <= 1.00001:
            break
            
        nuovo_pattern_nome = f"P_new_{pattern_count}"
        pattern_count += 1
        nuovi_tagli = pricing.get_variable("alpha").get_values().to_dict()
        
        # Aggiungo il nuovo pattern
        master.eval(f'let R := R union {{"{nuovo_pattern_nome}"}};')
        master.eval(f'let x["{nuovo_pattern_nome}"].relax := 1;')
        for m in moduli:
            if nuovi_tagli[m] > 0:
                master.eval(f'let A["{m}", "{nuovo_pattern_nome}"] := {nuovi_tagli[m]};')

    # =========================================================
    # SOLUZIONE 4: Ottima Rilassata 
    # =========================================================
    sol4_ottima_rilassata = master.get_objective("Obj_Master").value()
    print(f"4. Soluzione Ottima Rilassata: {sol4_ottima_rilassata:.2f} assi")
    print(f"   (Iterazioni di pricing effettuate: {iterazione})")

    # =========================================================
    # SOLUZIONE 5: Intera Arrotondando (dall'ottima rilassata) 
    # =========================================================
    sol5_intera_arrotondando = 0
    for j in master.get_variable("x").get_values().to_dict():
        valore_continuo = master.get_variable("x")[j].value()
        sol5_intera_arrotondando += math.ceil(valore_continuo)
    print(f"5. Soluzione Intera Arrotondando: {sol5_intera_arrotondando} assi")

    return sol1_euristica, sol2_intera, sol3_arrotondata, round(sol4_ottima_rilassata, 2), sol5_intera_arrotondando, iterazione