# Sets
set MODULI;                                  # Stesso del master

# Parametri
param L;                                     # Lunghezza totale dell'asse
param l{MODULI};                             # Lunghezza del singolo modulo
param u{MODULI} >= 0;                        # Variabili duali (prezzi ombra)

# Var
var alpha{MODULI} >= 0 integer;              # Variabili del pricing (num pezzi di i nel nuovo pattern)

# F.O.
maximize W:
    sum{i in MODULI} u[i] * alpha[i];        # Massimizzare val tot pattern con i prezzi ombra

# Vincoli
subject to Capacita:
    sum{i in MODULI} l[i] * alpha[i] <= L;   # Somma prezzi tagliati deve essere minore o uguale alla lunghezza dell'asse