import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("Caricamento dati dal CSV...")
df = pd.read_csv('./results/risultati_esperimenti.csv', sep=';')

# Calcolo metriche
df['Gap_Iniziale_%'] = ((df['3_Arrotondata_Iniziale'] - df['2_Intera']) / df['2_Intera']) * 100
df['Gap_Ottimo_%'] = ((df['5_Intera_Arrotondando'] - df['4_Ottima_Rilassata']) / df['4_Ottima_Rilassata']) * 100
df['Risparmio_Assi_%'] = ((df['1_Euristica'] - df['5_Intera_Arrotondando']) / df['1_Euristica']) * 100

# Etichette leggibili
df['Domanda_Etichetta'] = df['Domanda_Alta'].map({False: 'Domanda Bassa (1-10)', True: 'Domanda Alta (50-100)'})
df['Dim_Etichetta'] = df['Dim_Grande'].map({False: 'Pochi Moduli (5-10)', True: 'Molti Moduli (~50)'})

# ==========================================
# GRAFICO 1: Impatto della Domanda sul Gap
# ==========================================
plt.figure(figsize=(8, 6))
gap_per_domanda = df.groupby('Domanda_Etichetta')['Gap_Ottimo_%'].mean()
bars = plt.bar(gap_per_domanda.index, gap_per_domanda.values, color=['#FF9999', '#66B2FF'])
plt.title('Scarto % tra Ottima Rilassata e Intera Arrotondata', fontsize=14)
plt.ylabel('Scarto Medio (%)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f"{yval:.2f}%", ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig('./results/grafico_1_gap_domanda.png', dpi=300)
plt.close()

# ==========================================
# GRAFICO 2: Tempi di Calcolo
# ==========================================
plt.figure(figsize=(8, 6))
tempi_per_dim = df.groupby('Dim_Etichetta')['Tempo_Esecuzione(s)'].mean()
bars2 = plt.bar(tempi_per_dim.index, tempi_per_dim.values, color=['#99FF99', '#FFCC99'])
plt.title('Impatto del Numero di Moduli sui Tempi di Calcolo', fontsize=14)
plt.ylabel('Tempo Medio (Secondi)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars2:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + (max(tempi_per_dim.values)*0.02), f"{yval:.2f} s", ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig('./results/grafico_2_tempi_dimensioni.png', dpi=300)
plt.close()

# ==========================================
# GRAFICO 3: Memoria Occupata
# ==========================================
plt.figure(figsize=(8, 6))
mem_per_dim = df.groupby('Dim_Etichetta')['Memoria_Picco(MB)'].mean()
bars3 = plt.bar(mem_per_dim.index, mem_per_dim.values, color=['#DDA0DD', '#E6E6FA'])
plt.title('Impatto del Numero di Moduli sulla Memoria Occupata', fontsize=14)
plt.ylabel('Memoria di Picco Media (MB)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars3:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + (max(mem_per_dim.values)*0.02), f"{yval:.2f} MB", ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig('./results/grafico_3_memoria.png', dpi=300)
plt.close()

# ==========================================
# GRAFICO 4: Efficienza dell'Algoritmo
# ==========================================
plt.figure(figsize=(8, 6))
media_euristica = df['1_Euristica'].mean()
media_ottima = df['5_Intera_Arrotondando'].mean()
bars4 = plt.bar(['Euristica Iniziale', 'Ottima con Pricing'], [media_euristica, media_ottima], color=['#FF6666', '#99CC99'], width=0.5)
plt.title('Consumo Medio di Assi: Euristica vs Ottima', fontsize=14)
plt.ylabel('Numero Medio di Assi Utilizzati', fontsize=12)
for bar in bars4:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + (max([media_euristica, media_ottima])*0.02), f"{int(yval)}", ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig('./results/grafico_4_risparmio_assi.png', dpi=300)
plt.close()

# ==========================================
# STAMPA SUMMARY IN CONSOLE
# ==========================================
print("\n" + "="*50)
print("ANALISI COMPLETATA CON SUCCESSO")
print("="*50)
print(f"Risparmio medio di assi: {df['Risparmio_Assi_%'].mean():.2f}%")
print(f"Tempo esecuzione medio totale: {df['Tempo_Esecuzione(s)'].mean():.2f} secondi")
print(f"Memoria di picco media: {df['Memoria_Picco(MB)'].mean():.2f} MB")
print(f"Media iterazioni pricing: {df['Iterazioni_Pricing'].mean():.1f} cicli")
print("\nSono stati generati 4 file PNG nella cartella pronti per la presentazione.")