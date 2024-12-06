import csv
import random
from datetime import datetime, timedelta

# Função para gerar uma data aleatória entre duas datas
def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

# Definir o intervalo de datas
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

# Ler o arquivo CSV
with open('carros.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

# Atualizar as datas de cadastro
header = rows[0]
header[-1] = 'data_cadastro'  # Atualizar o nome da coluna
for row in rows[1:]:
    row[-1] = random_date(start_date, end_date).strftime('%Y-%m-%d')

# Escrever o arquivo CSV atualizado
with open('carros_atualizado.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print("Arquivo CSV atualizado com sucesso!")