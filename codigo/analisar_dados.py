# Script para analisar os dados de atendimentos SUS do Ceará

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import unicodedata

# Configurações para os gráficos
plt.style.use('seaborn-v0_8')
sns.set(font_scale=1.1)
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.family'] = 'sans-serif'

# Função para padronizar nomes de municípios
def padronizar_municipio(nome):
    if pd.isna(nome):
        return None
    nome = str(nome).upper()
    nome = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore').decode('ascii')
    nome = ' '.join(nome.split())
    return nome

print("Iniciando análise dos atendimentos SUS do Ceará...")

try:
    # Processar arquivo de atendimentos
    arquivo_atendimentos = '../dados/DADOS.txt'
    
    # Ler o arquivo bruto
    with open(arquivo_atendimentos, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Verificar o conteúdo das primeiras linhas
    print(f"Primeiras 5 linhas do arquivo de atendimentos:")
    for i in range(min(5, len(linhas))):
        print(linhas[i].strip())
    
    # Processar manualmente o arquivo
    atendimentos_dados = []
    cabecalho = True
    
    for linha in linhas:
        if cabecalho:
            # Pular a linha de cabeçalho
            cabecalho = False
            continue
        
        # Dividir a linha em ID, MUNICÍPIO e PRIMEIRO_NOME
        partes = linha.strip().split(',')
        if len(partes) >= 2:
            id_atendimento = partes[0].strip()
            
            # O município pode ter vindo com o ID junto
            if id_atendimento.isdigit():
                municipio = partes[1].strip()
            else:
                # Extrair o ID do início
                partes_id = id_atendimento.split(' ', 1)
                if len(partes_id) > 1 and partes_id[0].isdigit():
                    id_atendimento = partes_id[0]
                    municipio = partes_id[1]
                else:
                    municipio = id_atendimento
                    id_atendimento = "0"  # ID padrão se não conseguir extrair
            
            # O primeiro nome pode estar na terceira parte ou não existir
            primeiro_nome = partes[2].strip() if len(partes) > 2 else ""
            
            atendimentos_dados.append({
                'id_atendimento': id_atendimento,
                'nome_municipio': municipio,
                'primeiro_nome_atendido': primeiro_nome
            })
    
    # Criar DataFrame
    atendimentos = pd.DataFrame(atendimentos_dados)
    print(f"\nProcessado arquivo de atendimentos: {len(atendimentos)} registros")
    print("Primeiras 5 linhas processadas:")
    print(atendimentos.head())
    
    # Processar arquivo do IBGE
    arquivo_ibge = '../dados/mapa.csv'
    
    # Tentar ler o arquivo bruto
    with open(arquivo_ibge, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Verificar o conteúdo das primeiras linhas
    print(f"\nPrimeiras 5 linhas do arquivo do IBGE:")
    for i in range(min(5, len(linhas))):
        print(linhas[i].strip())
    
    # Processar manualmente o arquivo
    ibge_dados = []
    cabecalho = True
    
    for linha in linhas:
        if cabecalho:
            # Pular a linha de cabeçalho
            cabecalho = False
            continue
        
        # Dividir a linha
        partes = linha.strip().split(',')
        if len(partes) >= 2:
            municipio = partes[0].strip()
            
            # Remover aspas se presentes
            municipio = municipio.replace('"', '').strip()
            
            # População pode ter aspas
            populacao_str = partes[1].strip().replace('"', '')
            
            # Converter para número
            try:
                populacao = int(populacao_str)
            except ValueError:
                try:
                    # Tentar novamente removendo espaços
                    populacao = int(populacao_str.replace(' ', ''))
                except ValueError:
                    # Se ainda falhar, usar um valor padrão
                    populacao = 0
            
            ibge_dados.append({
                'codigo_municipio': len(ibge_dados) + 1,  # Gerar código sequencial
                'nome_municipio': municipio,
                'populacao_estimada': populacao,
                'regiao': 'Nordeste',  # Todos são do Ceará, que é Nordeste
                'uf': 'CE'  # Código do Ceará
            })
    
    # Criar DataFrame
    ibge_df = pd.DataFrame(ibge_dados)
    print(f"\nProcessado arquivo do IBGE: {len(ibge_df)} municípios")
    print("Primeiras 5 linhas processadas:")
    print(ibge_df.head())
    
    # Padronizar nomes de municípios para facilitar a integração
    atendimentos['nome_municipio_padronizado'] = atendimentos['nome_municipio'].apply(padronizar_municipio)
    ibge_df['nome_municipio_padronizado'] = ibge_df['nome_municipio'].apply(padronizar_municipio)
    
    # Contar atendimentos por município
    contagem_atendimentos = atendimentos.groupby('nome_municipio_padronizado').size().reset_index(name='total_atendimentos')
    print(f"\nContagem de atendimentos por município: {len(contagem_atendimentos)} municípios")
    print("Primeiros 5 municípios por número de atendimentos:")
    print(contagem_atendimentos.sort_values('total_atendimentos', ascending=False).head())
    
    # Realizar a junção (merge) das bases
    dados_integrados = pd.merge(
        contagem_atendimentos,
        ibge_df,
        how='left',
        on='nome_municipio_padronizado'
    )
    
    # Verificar municípios não encontrados
    nao_encontrados = dados_integrados[dados_integrados['codigo_municipio'].isnull()]
    if len(nao_encontrados) > 0:
        print(f"\nAtenção: {len(nao_encontrados)} municípios não foram encontrados na base do IBGE")
        print("Municípios não encontrados:")
        print(nao_encontrados['nome_municipio_padronizado'].tolist())
        
    # Calcular proporções
    dados_analise = dados_integrados.dropna(subset=['codigo_municipio', 'populacao_estimada'])
    dados_analise['atendimentos_por_habitante'] = dados_analise['total_atendimentos'] / dados_analise['populacao_estimada']
    dados_analise['atendimentos_por_100mil'] = dados_analise['atendimentos_por_habitante'] * 100000
    
    # Identificar municípios com mais atendimentos que habitantes
    inconsistentes = dados_analise[dados_analise['atendimentos_por_habitante'] > 1]
    if len(inconsistentes) > 0:
        print(f"\nAtenção: {len(inconsistentes)} municípios têm mais atendimentos que habitantes")
        print(inconsistentes[['nome_municipio_padronizado', 'total_atendimentos', 
                             'populacao_estimada', 'atendimentos_por_habitante']].head())
        inconsistentes.to_csv('../resultados/municipios_inconsistentes.csv', index=False)
    
    # Criar rankings
    ranking_maior = dados_analise.sort_values(by='atendimentos_por_100mil', ascending=False).head(10)
    ranking_menor = dados_analise.sort_values(by='atendimentos_por_100mil', ascending=True).head(10)
    
    # Salvar todos os arquivos processados
    atendimentos.to_csv('../resultados/atendimentos_processados.csv', index=False)
    ibge_df.to_csv('../resultados/ibge_processados.csv', index=False)
    contagem_atendimentos.to_csv('../resultados/contagem_atendimentos.csv', index=False)
    dados_integrados.to_csv('../resultados/dados_integrados.csv', index=False)
    dados_analise.to_csv('../resultados/dados_analise.csv', index=False)
    ranking_maior.to_csv('../resultados/ranking_maior.csv', index=False)
    ranking_menor.to_csv('../resultados/ranking_menor.csv', index=False)
    
    print("\nDados processados e salvos com sucesso!")
    print("\nArquivos gerados:")
    print("- ../resultados/atendimentos_processados.csv")
    print("- ../resultados/ibge_processados.csv")
    print("- ../resultados/contagem_atendimentos.csv")
    print("- ../resultados/dados_integrados.csv")
    print("- ../resultados/dados_analise.csv")
    print("- ../resultados/ranking_maior.csv")
    print("- ../resultados/ranking_menor.csv")
    if len(inconsistentes) > 0:
        print("- ../resultados/municipios_inconsistentes.csv")
    
    # Criar visualizações
    print("\nCriando visualizações...")
    
    # 1. Visualização: Volume de atendimentos por município (top 15)
    top_atendimentos = dados_analise.sort_values(by='total_atendimentos', ascending=False).head(15)
    
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(y='nome_municipio_padronizado', x='total_atendimentos', data=top_atendimentos)
    plt.title('Top 15 Municípios do Ceará com Maior Volume de Atendimentos SUS')
    plt.xlabel('Total de Atendimentos')
    plt.ylabel('Município')
    
    # Adicionar os valores nas barras
    for i, v in enumerate(top_atendimentos['total_atendimentos']):
        ax.text(v + 0.1, i, f"{v:,.0f}", va='center')
    
    plt.tight_layout()
    plt.savefig('../visualizacoes/01_volume_atendimentos_municipio.png', dpi=300)
    plt.close()
    
    # 2. Visualização: Proporção de atendimentos por 100 mil habitantes (top 10)
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(y='nome_municipio_padronizado', x='atendimentos_por_100mil', data=ranking_maior)
    plt.title('Top 10 Municípios do Ceará com Maior Proporção de Atendimentos por 100 mil Habitantes')
    plt.xlabel('Atendimentos por 100 mil Habitantes')
    plt.ylabel('Município')
    
    # Adicionar os valores nas barras
    for i, v in enumerate(ranking_maior['atendimentos_por_100mil']):
        ax.text(v + 0.1, i, f"{v:,.0f}", va='center')
    
    plt.tight_layout()
    plt.savefig('../visualizacoes/02_proporcao_maior.png', dpi=300)
    plt.close()
    
    # 3. Visualização: Municípios com menor proporção de atendimentos
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(y='nome_municipio_padronizado', x='atendimentos_por_100mil', data=ranking_menor)
    plt.title('Top 10 Municípios do Ceará com Menor Proporção de Atendimentos por 100 mil Habitantes')
    plt.xlabel('Atendimentos por 100 mil Habitantes')
    plt.ylabel('Município')
    
    # Adicionar os valores nas barras
    for i, v in enumerate(ranking_menor['atendimentos_por_100mil']):
        ax.text(v + 0.1, i, f"{v:,.0f}", va='center')
    
    plt.tight_layout()
    plt.savefig('../visualizacoes/03_proporcao_menor.png', dpi=300)
    plt.close()
    
    print("\nVisualizações criadas com sucesso!")
    print("Arquivos gerados:")
    print("- ../visualizacoes/01_volume_atendimentos_municipio.png")
    print("- ../visualizacoes/02_proporcao_maior.png")
    print("- ../visualizacoes/03_proporcao_menor.png")
    
except Exception as e:
    print(f"Erro ao analisar os dados: {e}")