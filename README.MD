# SUS Data Insights

Análise de dados de atendimentos do Sistema Único de Saúde (SUS) do Ceará integrados com informações demográficas municipais.

## Sobre o Projeto

Este projeto realiza a análise e visualização de dados de atendimentos do SUS no estado do Ceará, integrando-os com dados demográficos do IBGE para permitir análises proporcionais e identificação de padrões de distribuição dos atendimentos.

## Estrutura do Repositório

- `codigo/`: Scripts Python usados para processamento e análise
- `visualizacoes/`: Gráficos gerados pela análise
- `resultados/`: Relatórios e dados processados

## Arquivos de Dados Necessários (não incluídos no repositório)

**Importante:** Para executar esta análise, você precisará dos seguintes arquivos de dados que não estão incluídos neste repositório devido ao tamanho:

- `dados/DADOS.txt`: Arquivo de atendimentos do SUS (fictícios)
- `dados/mapa.csv`: Arquivo com dados demográficos dos municípios

Estes arquivos precisam ser adicionados manualmente à pasta `dados/` antes de executar os scripts.

## Como Usar

1. Clone o repositório
2. Crie uma pasta `dados/` na raiz do projeto
3. Adicione os arquivos de dados necessários à pasta `dados/`
4. Execute os scripts na sequência:
   ```bash
   python3 codigo/analisar_dados.py
   python3 codigo/gerar_relatorio.py


5. O relatório final será gerado em `resultados/relatorio_atendimentos_sus.html`

## Requisitos

- Python 3.6 ou superior
- Bibliotecas: pandas, numpy, matplotlib, seaborn
