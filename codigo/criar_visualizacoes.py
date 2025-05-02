# Script para criar visualizações dos dados de atendimentos SUS do Ceará

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Configurações para os gráficos
plt.style.use('seaborn-v0_8')
sns.set(font_scale=1.1)
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.family'] = 'sans-serif'

print("Criando visualizações dos atendimentos SUS do Ceará...")

try:
    # Carregar dados de análise
    dados_analise = pd.read_csv('../resultados/dados_analise.csv')
    ranking_maior = pd.read_csv('../resultados/ranking_maior.csv')
    ranking_menor = pd.read_csv('../resultados/ranking_menor.csv')
    
    print(f"Dados carregados: {len(dados_analise)} municípios para análise")
    
    # 1. Visualização: Volume de atendimentos por município (top 15)
    print("Criando visualização 1: Volume de atendimentos por município...")
    
    # Ordenar por total de atendimentos e pegar os 15 maiores
    top_atendimentos = dados_analise.sort_values(by='total_atendimentos', ascending=False).head(15)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(y='nome_municipio_padronizado', x='total_atendimentos', data=top_atendimentos)
    plt.title('Top 15 Municípios do Ceará com Maior Volume de Atendimentos SUS')
    plt.xlabel('Total de Atendimentos')
    plt.ylabel('Município')
    plt.tight_layout()
    plt.savefig('../visualizacoes/01_volume_atendimentos_municipio.png', dpi=300)
    plt.close()
    
    # 2. Visualização: Proporção de atendimentos por 100 mil habitantes (top 15)
    print("Criando visualização 2: Proporção de atendimentos por 100 mil habitantes...")
    
    plt.figure(figsize=(12, 8))
    sns.barplot(y='nome_municipio_padronizado', x='atendimentos_por_100mil', data=ranking_maior)
    plt.title('Top 10 Municípios do Ceará com Maior Proporção de Atendimentos por 100 mil Habitantes')
    plt.xlabel('Atendimentos por 100 mil Habitantes')
    plt.ylabel('Município')
    plt.tight_layout()
    plt.savefig('../visualizacoes/02_proporcao_maior.png', dpi=300)
    plt.close()
    
    # 3. Visualização: Municípios com menor proporção de atendimentos
    print("Criando visualização 3: Municípios com menor proporção de atendimentos...")
    
    plt.figure(figsize=(12, 8))
    sns.barplot(y='nome_municipio_padronizado', x='atendimentos_por_100mil', data=ranking_menor)
    plt.title('Top 10 Municípios do Ceará com Menor Proporção de Atendimentos por 100 mil Habitantes')
    plt.xlabel('Atendimentos por 100 mil Habitantes')
    plt.ylabel('Município')
    plt.tight_layout()
    plt.savefig('../visualizacoes/03_proporcao_menor.png', dpi=300)
    plt.close()
    
    # 4. Visualização: Relação entre população e atendimentos
    print("Criando visualização 4: Relação entre população e atendimentos...")
    
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='populacao_estimada', y='total_atendimentos', 
                    data=dados_analise, alpha=0.7)
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Relação entre População e Atendimentos SUS nos Municípios do Ceará (escala log)')
    plt.xlabel('População Estimada')
    plt.ylabel('Total de Atendimentos')
    plt.tight_layout()
    plt.savefig('../visualizacoes/04_relacao_populacao_atendimentos.png', dpi=300)
    plt.close()
    
    # 5. Visualização: Distribuição dos atendimentos por 100 mil habitantes
    print("Criando visualização 5: Distribuição dos atendimentos por 100 mil habitantes...")
    
    plt.figure(figsize=(10, 6))
    sns.histplot(data=dados_analise, x='atendimentos_por_100mil', bins=20, kde=True)
    plt.title('Distribuição dos Atendimentos por 100 mil Habitantes nos Municípios do Ceará')
    plt.xlabel('Atendimentos por 100 mil Habitantes')
    plt.ylabel('Número de Municípios')
    plt.tight_layout()
    plt.savefig('../visualizacoes/05_distribuicao_atendimentos.png', dpi=300)
    plt.close()
    
    print("\nVisualizações criadas com sucesso!")
    print("Arquivos gerados:")
    print("- ../visualizacoes/01_volume_atendimentos_municipio.png")
    print("- ../visualizacoes/02_proporcao_maior.png")
    print("- ../visualizacoes/03_proporcao_menor.png")
    print("- ../visualizacoes/04_relacao_populacao_atendimentos.png")
    print("- ../visualizacoes/05_distribuicao_atendimentos.png")

except Exception as e:
    print(f"Erro ao criar visualizações: {e}")