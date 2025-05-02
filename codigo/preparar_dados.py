# Script para preparar os dados de atendimentos SUS do Ceará

import pandas as pd
import os
import unicodedata

# Criar pastas necessárias
os.makedirs('../resultados', exist_ok=True)
os.makedirs('../visualizacoes', exist_ok=True)

# Função para padronizar nomes de municípios
def padronizar_municipio(nome):
    if pd.isna(nome):
        return None
    nome = str(nome).upper()
    nome = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore').decode('ascii')
    nome = ' '.join(nome.split())
    return nome

print("Preparando dados do Ceará...")

# Encontrar o arquivo TXT na pasta dados
arquivos_txt = [f for f in os.listdir('../dados') if f.endswith('.txt')]
if not arquivos_txt:
    print("ERRO: Arquivo TXT não encontrado na pasta 'dados/'")
    print("Por favor, coloque o arquivo TXT do professor na pasta 'dados/'")
    exit()

arquivo_txt = os.path.join('../dados', arquivos_txt[0])
print(f"Encontrado arquivo de atendimentos SUS: {arquivo_txt}")

# Encontrar o arquivo CSV do IBGE
arquivos_csv = [f for f in os.listdir('../dados') if f.endswith('.csv')]
if not arquivos_csv:
    print("ERRO: Arquivo CSV não encontrado na pasta 'dados/'")
    print("Por favor, coloque o arquivo CSV do IBGE na pasta 'dados/'")
    exit()

arquivo_csv = os.path.join('../dados', arquivos_csv[0])
print(f"Encontrado arquivo do IBGE: {arquivo_csv}")

# Tentar carregar o arquivo TXT com diferentes configurações
try:
    # Tentar vários separadores e encodings
    separadores = ['\t', ',', ';', '|']
    encodings = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']
    
    atendimentos = None
    sep_usado = None
    encoding_usado = None
    
    for sep in separadores:
        for enc in encodings:
            try:
                # Tentar ler as primeiras linhas
                df_teste = pd.read_csv(arquivo_txt, sep=sep, encoding=enc, nrows=5)
                # Se chegou aqui, funcionou
                atendimentos = pd.read_csv(arquivo_txt, sep=sep, encoding=enc)
                sep_usado = sep
                encoding_usado = enc
                break
            except Exception as e:
                continue
        
        if atendimentos is not None:
            break
    
    if atendimentos is None:
        raise Exception("Não foi possível ler o arquivo TXT com nenhuma combinação de separador/encoding")
    
    print(f"Arquivo de atendimentos carregado com sucesso usando separador '{sep_usado}' e encoding '{encoding_usado}'")
    print(f"Total de registros de atendimentos: {len(atendimentos)}")
    print("\nPrimeiras 5 linhas dos atendimentos:")
    print(atendimentos.head())
    
    # Verificar as colunas do arquivo de atendimentos
    print("\nColunas no arquivo de atendimentos:")
    for i, coluna in enumerate(atendimentos.columns):
        print(f"{i+1}. {coluna}")
    
    # Carregar o arquivo CSV do IBGE
    # Tentar vários separadores e encodings
    ibge_dados = None
    
    for sep in separadores:
        for enc in encodings:
            try:
                # Tentar ler as primeiras linhas
                df_teste = pd.read_csv(arquivo_csv, sep=sep, encoding=enc, nrows=5)
                # Se chegou aqui, funcionou
                ibge_dados = pd.read_csv(arquivo_csv, sep=sep, encoding=enc)
                sep_usado = sep
                encoding_usado = enc
                break
            except Exception as e:
                continue
        
        if ibge_dados is not None:
            break
    
    if ibge_dados is None:
        raise Exception("Não foi possível ler o arquivo CSV do IBGE com nenhuma combinação de separador/encoding")
    
    print(f"\nArquivo do IBGE carregado com sucesso usando separador '{sep_usado}' e encoding '{encoding_usado}'")
    print(f"Total de municípios no IBGE: {len(ibge_dados)}")
    print("\nPrimeiras 5 linhas do IBGE:")
    print(ibge_dados.head())
    
    # Verificar as colunas do arquivo do IBGE
    print("\nColunas no arquivo do IBGE:")
    for i, coluna in enumerate(ibge_dados.columns):
        print(f"{i+1}. {coluna}")
    
    # Verificar se as colunas necessárias existem nos atendimentos
    # Normalmente precisamos de id_atendimento, nome_municipio e talvez primeiro_nome_atendido
    colunas_necessarias_atendimentos = ['id_atendimento', 'nome_municipio']
    
    # Verificar se o arquivo tem essas colunas ou nomes similares
    colunas_atendimentos = []
    for coluna in colunas_necessarias_atendimentos:
        if coluna in atendimentos.columns:
            colunas_atendimentos.append(coluna)
        else:
            # Procurar colunas com nomes similares
            colunas_similares = [c for c in atendimentos.columns if coluna.lower() in c.lower()]
            if colunas_similares:
                print(f"Coluna '{coluna}' não encontrada, mas encontrada coluna similar: {colunas_similares[0]}")
                # Renomear para o nome padrão
                atendimentos = atendimentos.rename(columns={colunas_similares[0]: coluna})
                colunas_atendimentos.append(coluna)
            else:
                print(f"ATENÇÃO: Coluna '{coluna}' não encontrada e nenhuma coluna similar")
    
    # Verificar se as colunas necessárias existem no IBGE
    # Normalmente precisamos de codigo_municipio, nome_municipio, populacao_estimada
    colunas_necessarias_ibge = ['codigo_municipio', 'nome_municipio', 'populacao_estimada']
    
    # Verificar se o arquivo tem essas colunas ou nomes similares
    colunas_ibge = []
    for coluna in colunas_necessarias_ibge:
        if coluna in ibge_dados.columns:
            colunas_ibge.append(coluna)
        else:
            # Procurar colunas com nomes similares
            colunas_similares = [c for c in ibge_dados.columns if coluna.lower() in c.lower()]
            if colunas_similares:
                print(f"Coluna '{coluna}' não encontrada no IBGE, mas encontrada coluna similar: {colunas_similares[0]}")
                # Renomear para o nome padrão
                ibge_dados = ibge_dados.rename(columns={colunas_similares[0]: coluna})
                colunas_ibge.append(coluna)
            else:
                print(f"ATENÇÃO: Coluna '{coluna}' não encontrada no IBGE e nenhuma coluna similar")
    
    # Padronizar nomes de municípios
    print("\nPadronizando nomes de municípios...")
    if 'nome_municipio' in atendimentos.columns:
        atendimentos['nome_municipio_padronizado'] = atendimentos['nome_municipio'].apply(padronizar_municipio)
    
    if 'nome_municipio' in ibge_dados.columns:
        ibge_dados['nome_municipio_padronizado'] = ibge_dados['nome_municipio'].apply(padronizar_municipio)
    
    # Salvando os dados processados
    atendimentos.to_csv('../resultados/atendimentos_processados.csv', index=False)
    ibge_dados.to_csv('../resultados/ibge_processados.csv', index=False)
    
    print("\nDados processados e salvos com sucesso!")
    print("Arquivos gerados:")
    print("- ../resultados/atendimentos_processados.csv")
    print("- ../resultados/ibge_processados.csv")

except Exception as e:
    print(f"Erro ao processar os dados: {e}")