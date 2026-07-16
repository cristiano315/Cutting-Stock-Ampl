# Sets
set MODULI;
set R;                                      # Insieme dei pattern (colonne)

# Parametri
param d{MODULI};                            # Domanda (pezzi per ogni modulo)
param A{MODULI, R} >= 0 default 0;          # Matrice dei coefficienti (pezzi di i nel pattern j)

# Var
var x{R} >= 0 integer;                      # Volte in cui uso un pattern. Intera, si rilassa a continua da python.

# F.O.
minimize Obj_Master:                        # Minimizzare num tot assi
    sum{j in R} x[j];

# Vincoli
subject to Vincolo_Domanda {i in MODULI}:   # Ogni modulo deve soddisfare la domanda minima richiesta
    sum{j in R} A[i,j] * x[j] >= d[i];