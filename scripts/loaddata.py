
import pandas as pd
import json
import os
from tqdm import tqdm

from django_scian.models import SCIAN

# Leer excel con pandas

path = './scripts/'
files = os.listdir(path)
files_xlsx = [f for f in files if f[-4:] == 'xlsx']

print(files_xlsx)

# Main

df = pd.read_excel(path+files_xlsx[0], sheet_name='SCIAN 2023', header=1)

# Drop rows with NaN values in Código column

newdf = df.dropna(subset=['Código'])
# Column Código is a string, so we need to convert it to a string withouth the decimal point

newdf['Código'] = newdf['Código'].astype(str).str[:-2]
orderdf = newdf.sort_values(by='Código')

# Replace Nan values with ''

orderdf = orderdf.fillna('')

# Create tree structure with the data

def create_json_tree(df):

    # 1. The first level of the tree is the first two digits of the code (the sector code)
    # 2. The second level of the tree is the third digit of the code (the subsector code)
    # 3. The third level of the tree is the fourth digit of the code (the branch code)
    # 4. The fourth level of the tree is the fifth digit of the code (the subbranch code)

    tree = {
        'Sectores': {}
    }

    # Example - 11 should be the first level of the tree and 111 or 112 should be the second level of the tree

    for index, row in tqdm(df.iterrows()):
        code = str(row['Código'])

        titulo  = row['Título'].replace('T ', '')

        if len(code) == 2:
            tree['Sectores'][code] = {
                'Título': titulo,
                'Descripción': row['Descripción'],
                'Incluye': row['Incluye'],
                'Excluye': row['Excluye'],
                'Índice de bienes y servicios': row['Índice de bienes y servicios comprendidos en las categorías del SCIAN México 2023'],
                'Subsectores': {}
            }
            SCIAN.objects.create(
                id=code,
                titulo=titulo,
                nivel='sector',
                descripcion=row['Descripción'],
                incluye=row['Incluye'],
                excluye=row['Excluye'],
                indice=row['Índice de bienes y servicios comprendidos en las categorías del SCIAN México 2023']
            )
        elif len(code) == 3:
            tree['Sectores'][code[:2]]['Subsectores'][code] = {
                'Título': titulo,
                'Descripción': row['Descripción'],
                'Incluye': row['Incluye'],
                'Excluye': row['Excluye'],
                'Índice de bienes y servicios': row['Índice de bienes y servicios comprendidos en las categorías del SCIAN México 2023'],
                'Ramas': {}
            }
            SCIAN.objects.create(
                id=code,
                tn_parent_id=code[:2],
                nivel='subsector',
                titulo=titulo,
                descripcion=row['Descripción'],
                incluye=row['Incluye'],
                excluye=row['Excluye'],
                indice=row['Índice de bienes y servicios comprendidos en las categorías del SCIAN México 2023']
            )
        elif len(code) == 4:
            tree['Sectores'][code[:2]]['Subsectores'][code[:3]]['Ramas'][code] = {
                'Título': titulo,
                'Descripción': row['Descripción'],
                'Incluye': row['Incluye'],
                'Excluye': row['Excluye'],
                'Índice de bienes y servicios': row['Índice de bienes y servicios comprendidos en las categorías del SCIAN México 2023'],
                'Subramas': {}
            }
            SCIAN.objects.create(
                id=code,
                tn_parent_id=code[:3],
                nivel='rama',
                titulo=titulo,
                descripcion=row['Descripción'],
                incluye=row['Incluye'],
                excluye=row['Excluye'],
                indice=row['Índice de bienes y servicios comprendidos en las categorías del SCIAN México 2023']
            )
        elif len(code) == 5:
            tree['Sectores'][code[:2]]['Subsectores'][code[:3]]['Ramas'][code[:4]]['Subramas'][code] = {
                'Título': titulo,
                'Descripción': row['Descripción'],
                'Incluye': row['Incluye'],
                'Excluye': row['Excluye'],
                'Índice de bienes y servicios': row['Índice de bienes y servicios comprendidos en las categorías del SCIAN México 2023'],              
                'Clases': {}
            }
            SCIAN.objects.create(
                id=code,
                tn_parent_id=code[:4],
                nivel='subrama',
                titulo=titulo,
                descripcion=row['Descripción'],
                indice=row['Índice de bienes y servicios comprendidos en las categorías del SCIAN México 2023'],
                incluye=row['Incluye'],
                excluye=row['Excluye']
            )
        elif len(code) == 6:
            tree['Sectores'][code[:2]]['Subsectores'][code[:3]]['Ramas'][code[:4]]['Subramas'][code[:5]]['Clases'][code] = {
                'Título': titulo,
                'Descripción': row['Descripción'],
                'Incluye': row['Incluye'],
                'Excluye': row['Excluye'],
                'Índice de bienes y servicios': row['Índice de bienes y servicios comprendidos en las categorías del SCIAN México 2023']
            }
            SCIAN.objects.create(
                id=code,
                tn_parent_id=code[:5],
                nivel='clase',
                titulo=titulo,
                descripcion=row['Descripción'],
                incluye=row['Incluye'],
                excluye=row['Excluye'],
                indice=row['Índice de bienes y servicios comprendidos en las categorías del SCIAN México 2023']
            )
    return tree

tree = create_json_tree(orderdf)

# Save tree to json file in utf-8 format

with open('SCIAN.json', 'w', encoding='utf-8') as f:
    json.dump(tree, f, ensure_ascii=False, indent=4)
