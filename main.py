import pandas as pd
import json

def classificar_estrela_com_nome(row):
    """
    Classifica a estrela com base no raio e retorna um dicionário com nome, tipo e raio.
    """
    

  

    
# --- Configurações ---


# Colunas esperadas no seu arquivo CSV/DataFrame


# --- Processamento ---
try:
    # Carrega os dados. Ajuste o separador se o seu CSV usar ponto e vírgula (;)
   

    # Verifica se as colunas necessárias existem
   

    # Converte a coluna 'st_rad' para numérico, tratando erros
    
    # Remove linhas onde o raio não pôde ser convertido ou é nulo
   

    # Aplica a função para classificar e extrair informações
    # Usamos .apply() para iterar sobre as linhas e criar os dicionários
   

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
