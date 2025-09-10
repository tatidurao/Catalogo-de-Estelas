import pandas as pd
import json

def classificar_estrela_com_nome(row):
    """
    Classifica a estrela com base no raio e retorna um dicionário com nome, tipo e raio.
    """
    raio = row["st_rad"]
    nome = row["hostname"] # ou a coluna que contém o nome da estrela

    if pd.isna(raio) or pd.isna(nome):
        return None # Ignora linhas com dados faltantes

    if raio < 0.8:
        classe = "Anã"
        img_type = "dwarf-star.png" # Nome do arquivo de imagem para Anã
    elif raio < 10:
        classe = "Gigante"
        img_type = "giant-star.png" # Nome do arquivo de imagem para Gigante
    else:
        classe = "Supergigante"
        img_type = "supergiant-star.png" # Nome do arquivo de imagem para Supergigante

    return {
        "name": nome,
        "st_teff": row.get("st_teff", "N/A"), # Assumindo que você tem essa coluna
        "sy_kmag": row.get("sy_kmag", "N/A"), # Assumindo que você tem essa coluna
        "type": classe,
        "img_type": img_type, # Adicionamos o tipo de imagem aqui
        "st_mass": row.get("st_mass", "N/A"), # Exemplo de outra informação
        "st_rad": f"{raio:.2f} R☉" # Formata o raio com 2 casas decimais e 'R☉' (Raio Solar)
    }

# --- Configurações ---
# Substitua 'seu_arquivo_de_estrelas.csv' pelo nome do seu arquivo de dados.
# Se você já tem um DataFrame no Python, pode pular a leitura do CSV.
ARQUIVO_CSV_ESTRELAS = 'STELLARHOSTS.csv'
ARQUIVO_SAIDA_JS = 'stars.js'

# Colunas esperadas no seu arquivo CSV/DataFrame
COLUNAS_NECESSARIAS = ['hostname', 'st_rad'] # Adicione outras colunas como 'distance_ly', 'absolute_magnitude', 'spectral_class' se elas existirem e você quiser exibi-las no modal.

# --- Processamento ---
try:
    # Carrega os dados. Ajuste o separador se o seu CSV usar ponto e vírgula (;)
    df = pd.read_csv(ARQUIVO_CSV_ESTRELAS, sep=',')

    # Verifica se as colunas necessárias existem
    for col in COLUNAS_NECESSARIAS:
        if col not in df.columns:
            print(f"Erro: A coluna '{col}' não foi encontrada no arquivo '{ARQUIVO_CSV_ESTRELAS}'.")
            print("Por favor, verifique o nome das colunas ou adicione-as ao seu arquivo.")
            exit()

    # Converte a coluna 'st_rad' para numérico, tratando erros
    df['st_rad'] = pd.to_numeric(df['st_rad'], errors='coerce')

    # Remove linhas onde o raio não pôde ser convertido ou é nulo
    df.dropna(subset=['st_rad', 'hostname'], inplace=True)

    # Aplica a função para classificar e extrair informações
    # Usamos .apply() para iterar sobre as linhas e criar os dicionários
    star_data_list = df.apply(classificar_estrela_com_nome, axis=1).dropna().tolist()

    # --- Criação do arquivo stars.js ---
    # Formato do arquivo JS: const stars = [ { ... }, { ... } ];
    js_content = f"const stars = {json.dumps(star_data_list, indent=4)};\n"

    # Adiciona a função getImageForType (você pode colocar essa função separadamente ou aqui)
    # Para simplificar, vamos adicionar um trecho que possa ser copiado para o seu HTML JS.
    # Na sua página HTML, você precisará ter a função `getImageForType` que mapeia `img_type` para o caminho correto.
    # Ex: "dwarf-star.png" -> "assets/dwarf-star.png"

    with open(ARQUIVO_SAIDA_JS, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"Arquivo '{ARQUIVO_SAIDA_JS}' gerado com sucesso!")
    print(f"Ele contém dados para {len(star_data_list)} estrelas.")
    print("\nLembre-se de adicionar a pasta 'assets' com as imagens das estrelas:")
    print("  - dwarf-star.png")
    print("  - giant-star.png")
    print("  - supergiant-star.png")

except FileNotFoundError:
    print(f"Erro: O arquivo '{ARQUIVO_CSV_ESTRELAS}' não foi encontrado.")
    print("Certifique-se de que o arquivo está no mesmo diretório do script ou forneça o caminho completo.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")