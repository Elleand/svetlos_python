import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Definuje prefix pro cestu ke slozce s daty pro import
IMPORT_CESTA_PROJEKTU = os.path.join(SCRIPT_DIR, './files/import/')

# Definuje prefix pro cestu ke slozce s daty pro import
EXPORT_CESTA_PROJEKTU = os.path.join(SCRIPT_DIR, './files/export/')

# Definuje název souboru dat pro export
NAZEC_SOUBORU_EXPORT = 'export'

# Definuje název souboru dat pro startovné
NAZEV_SOUBORU_STARTOVNE = 'startovne'

# Definuje název souboru pro import "data"
NAZEV_SOUBORU_IMPORT_DATA = 'data.xlsx'

# Definuje název souboru pro import "kluby"
NAZEV_SOUBORU_IMPORT_KLUBY = 'kluby.xlsx'

# Výše startovného v Kč
STARTOVNE = 200

# odsud neupravovat


# Cesta k vstupním datům Excel souboru (pokud to nic nenajde nakopírovat absolutní cestu, upravit formát)
file_path_data = IMPORT_CESTA_PROJEKTU + NAZEV_SOUBORU_IMPORT_DATA

# Cesta k seznamu názvu klubů a jejich zkratek
file_path_kluby = IMPORT_CESTA_PROJEKTU + NAZEV_SOUBORU_IMPORT_KLUBY

# Cesta a název souboru pro export csv.
file_path_export_csv = EXPORT_CESTA_PROJEKTU + NAZEC_SOUBORU_EXPORT + '.csv'

# Cesta a název souboru pro export excelu
file_path_export_excel = EXPORT_CESTA_PROJEKTU + NAZEC_SOUBORU_EXPORT + '.xlsx'

# Cesta a název souboru pro export csv.
file_path_startovne_csv = EXPORT_CESTA_PROJEKTU + NAZEV_SOUBORU_STARTOVNE + '.csv'

# Cesta a název souboru pro export excelu
file_path_startovne_excel = EXPORT_CESTA_PROJEKTU + NAZEV_SOUBORU_STARTOVNE + '.xlsx'

import pandas as pd
import numpy as np

# Načte soubor excelu
df = pd.read_excel(file_path_data)

# Vytvoří nový sloupec Pohlaví s hodnotou M pro muže a F pro ženu
if 'Věková kategorie' in df.columns:  # Kontroluje výskyt Věkové kategorie
    # Udělá sloupec pohlaví a přířadí hodnotu pokud má z čeho, jinan zapíše NaN-není hodnota
    df['Pohlaví'] = df['Věková kategorie'].apply(
        lambda x: 'F' if pd.notnull(x) and 'WU' in x else 'M' if pd.notnull(x) else np.nan)
else:
    df['Pohlaví'] = np.nan  # vypíše NaN do pohlaví

# Uspořádání sloupců - přesunutí sloupce 'Pohlaví' na šestou pozici
cols = df.columns.tolist()
cols.insert(5, cols.pop(cols.index('Pohlaví')))  # zde 5 protože python indexuje od 0 tudíž 6. sloupec
df = df[cols]

# Dopsání zkratek klubů
# Načtení seznamu zkratek
df_kluby = pd.read_excel(file_path_kluby)

if 'Klub' in df.columns and 'Klub' in df_kluby.columns and 'Zkratka klubu' in df_kluby.columns:  # Kontroluje výskyt Věkové kategorie
    # Udělá sloupec zkratek klubu a přířadí hodnotu pokud má z čeho, jinan zapíše NaN-není hodnota
    df = df.merge(df_kluby[['Klub', 'Zkratka klubu']], on='Klub', how='left')
else:
    df['Zkratka klubu'] = np.nan  # vypíše NaN do zkratky klubu

# Přidání sloupce s hmotností
df['Hmotnost'] = np.nan

# Uspořádání sloupců - přesunutí sloupce 'Hmotnost' na devatou pozici
cols = df.columns.tolist()
cols.insert(8, cols.pop(cols.index('Hmotnost')))  # zde 8 protože python indexuje od 0 tudíž 9. sloupec
df = df[cols]

# Počítání závodníků podle klubů a uložení do dataframu
count_by_oddil = pd.DataFrame(df['Klub'].value_counts()).reset_index()
count_by_oddil.columns = ['Klub', 'Počet závodníků']

# Výpočet startovného za danný klub
count_by_oddil['Startovné za klub'] = count_by_oddil['Počet závodníků'] * STARTOVNE

# check if folder export exists, if not, create it
if not os.path.exists(EXPORT_CESTA_PROJEKTU):
    # If not, create it
    os.makedirs(EXPORT_CESTA_PROJEKTU)
# Ukládání dat do csv
df.to_csv(file_path_export_csv, sep=';')

# Ukládání dat do excelu
df.to_excel(file_path_export_excel)

# Ukládání dat do csv
count_by_oddil.to_csv(file_path_startovne_csv, sep=';')

# Ukládání dat do excelu
count_by_oddil.to_excel(file_path_startovne_excel)
