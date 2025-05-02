# Script para gerar relatório em HTML da análise de atendimentos SUS do Ceará

import pandas as pd
import os
from datetime import datetime

print("Gerando relatório da análise...")

try:
    # Verificar se os arquivos necessários existem
    arquivos_necessarios = [
        '../resultados/dados_analise.csv',
        '../resultados/ranking_maior.csv',
        '../resultados/ranking_menor.csv',
        '../visualizacoes/01_volume_atendimentos_municipio.png',
        '../visualizacoes/02_proporcao_maior.png',
        '../visualizacoes/03_proporcao_menor.png',
        '../visualizacoes/04_relacao_populacao_atendimentos.png',
        '../visualizacoes/05_distribuicao_atendimentos.png'
    ]
    
    arquivos_faltantes = [f for f in arquivos_necessarios if not os.path.exists(f)]
    if arquivos_faltantes:
        print(f"AVISO: Alguns arquivos necessários não foram encontrados: {arquivos_faltantes}")
        print("Execute primeiro os scripts anteriores.")
        exit()
    
    # Carregar dados
    dados_analise = pd.read_csv('../resultados/dados_analise.csv')
    ranking_maior = pd.read_csv('../resultados/ranking_maior.csv')
    ranking_menor = pd.read_csv('../resultados/ranking_menor.csv')
    
    # Verificar se há municípios inconsistentes
    inconsistentes_file = '../resultados/municipios_inconsistentes.csv'
    tem_inconsistentes = os.path.exists(inconsistentes_file)
    if tem_inconsistentes:
        inconsistentes = pd.read_csv(inconsistentes_file)
    
    # Estatísticas para o relatório
    total_municipios = len(dados_analise)
    total_atendimentos = dados_analise['total_atendimentos'].sum()
    media_atendimentos = dados_analise['total_atendimentos'].mean()
    media_por_100mil = dados_analise['atendimentos_por_100mil'].mean()
    municipio_maior_volume = dados_analise.sort_values('total_atendimentos', ascending=False).iloc[0]
    municipio_maior_proporcao = dados_analise.sort_values('atendimentos_por_100mil', ascending=False).iloc[0]
    
    # Data do relatório
    data_relatorio = datetime.now().strftime("%d/%m/%Y")
    
    # Construir HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Relatório de Análise de Atendimentos SUS no Ceará</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 1200px; margin: 0 auto; }}
            h1, h2, h3 {{ color: #2c3e50; }}
            .section {{ margin-bottom: 20px; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .chart-container {{ margin: 20px 0; text-align: center; }}
            .chart {{ max-width: 100%; height: auto; border: 1px solid #ddd; }}
            .info-box {{ background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; margin-bottom: 20px; }}
            .warning-box {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h1>Relatório de Análise de Atendimentos SUS no Ceará</h1>
        <p><strong>Data de geração:</strong> {data_relatorio}</p>
        
        <div class="section">
            <h2>1. Introdução</h2>
            <p>Este relatório apresenta uma análise dos atendimentos do Sistema Único de Saúde (SUS) nos municípios do Ceará, integrados com dados demográficos municipais do IBGE. O objetivo é demonstrar a distribuição e volume de atendimentos, identificando padrões e possíveis inconsistências.</p>
            
            <div class="info-box">
                <h3>Principais Estatísticas:</h3>
                <ul>
                    <li><strong>Total de municípios analisados:</strong> {total_municipios}</li>
                    <li><strong>Total de atendimentos registrados:</strong> {total_atendimentos:,}</li>
                    <li><strong>Média de atendimentos por município:</strong> {media_atendimentos:.2f}</li>
                    <li><strong>Média de atendimentos por 100 mil habitantes:</strong> {media_por_100mil:.2f}</li>
                    <li><strong>Município com maior volume de atendimentos:</strong> {municipio_maior_volume['nome_municipio_padronizado']} ({municipio_maior_volume['total_atendimentos']:,} atendimentos)</li>
                    <li><strong>Município com maior proporção de atendimentos:</strong> {municipio_maior_proporcao['nome_municipio_padronizado']} ({municipio_maior_proporcao['atendimentos_por_100mil']:.2f} por 100 mil hab.)</li>
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h2>2. Metodologia</h2>
            <p>Para esta análise, foram utilizadas duas bases de dados principais:</p>
            <ul>
                <li><strong>Base de Atendimentos SUS:</strong> Contendo registros de atendimentos com identificação do município.</li>
                <li><strong>Base de Dados Municipais (IBGE):</strong> Contendo informações demográficas dos municípios do Ceará.</li>
            </ul>
            
            <p>O processo de análise seguiu as seguintes etapas:</p>
            <ol>
                <li>Padronização dos nomes de municípios para garantir a correta integração das bases.</li>
                <li>Contagem dos atendimentos por município.</li>
                <li>Integração (merge) das bases de atendimentos e dados municipais.</li>
                <li>Cálculo da proporção de atendimentos por habitante e por 100 mil habitantes.</li>
                <li>Identificação de municípios com dados inconsistentes (mais atendimentos que habitantes).</li>
                <li>Criação de rankings e visualizações para apoiar a análise.</li>
            </ol>
        </div>
    """

    if tem_inconsistentes and len(inconsistentes) > 0:
        html += f"""
        <div class="section">
            <h2>3. Análise de Coerência dos Dados</h2>
            
            <div class="warning-box">
                <h3>Municípios com mais atendimentos que habitantes:</h3>
                <p>Foram identificados {len(inconsistentes)} municípios com proporção de atendimentos por habitante maior que 1, o que indica mais atendimentos que habitantes.</p>
            </div>
            
            <p>Possíveis explicações para esse fenômeno:</p>
            <ul>
                <li>Municípios que são polos regionais de saúde, atendendo pacientes de municípios vizinhos.</li>
                <li>Erros na codificação dos municípios de residência dos pacientes.</li>
                <li>Possível duplicação de registros de atendimentos.</li>
                <li>Desatualização dos dados populacionais em municípios com crescimento rápido.</li>
            </ul>
            
            <h3>Municípios com proporção atendimentos/habitantes maior que 1:</h3>
            <table>
                <tr>
                    <th>Município</th>
                    <th>Total de Atendimentos</th>
                    <th>População</th>
                    <th>Atendimentos/Habitante</th>
                </tr>
        """
        
        # Adicionar até 10 municípios inconsistentes à tabela
        for _, row in inconsistentes.sort_values('atendimentos_por_habitante', ascending=False).head(10).iterrows():
            html += f"""
                <tr>
                    <td>{row['nome_municipio_padronizado']}</td>
                    <td>{row['total_atendimentos']:,}</td>
                    <td>{row['populacao_estimada']:,}</td>
                    <td>{row['atendimentos_por_habitante']:.2f}</td>
                </tr>
            """
        
        html += """
            </table>
        </div>
        """

    # Ajuste o número do próximo item (4 ou 5 dependendo se tem inconsistências)
    next_section = 4 if tem_inconsistentes and len(inconsistentes) > 0 else 3

    html += f"""
        <div class="section">
            <h2>{next_section}. Volume de Atendimentos por Município</h2>
            
            <p>A análise do volume absoluto de atendimentos revela grandes diferenças entre os municípios, com alguns apresentando números significativamente maiores:</p>
            
            <div class="chart-container">
                <img class="chart" src="../visualizacoes/01_volume_atendimentos_municipio.png" alt="Volume de Atendimentos por Município">
            </div>
            
            <p>Os municípios com maior volume de atendimentos geralmente correspondem às cidades mais populosas ou aos polos regionais de saúde que atendem pacientes de municípios vizinhos.</p>
        </div>
        
        <div class="section">
            <h2>{next_section + 1}. Municípios com Maior Proporção de Atendimentos</h2>
            
            <p>Ao analisar a proporção de atendimentos por 100 mil habitantes, podemos identificar municípios que têm um volume de atendimentos desproporcional à sua população:</p>
            
            <div class="chart-container">
                <img class="chart" src="../visualizacoes/02_proporcao_maior.png" alt="Municípios com Maior Proporção de Atendimentos">
            </div>
            
            <p>Estes municípios podem representar polos regionais de saúde, centros de referência para tratamentos específicos, ou podem indicar inconsistências nos dados.</p>
            
            <h3>Tabela: Municípios com Maior Proporção de Atendimentos</h3>
            <table>
                <tr>
                    <th>Município</th>
                    <th>Total de Atendimentos</th>
                    <th>População</th>
                    <th>Atendimentos por 100 mil hab.</th>
                </tr>
    """

    # Adicionar municípios do ranking à tabela
    for _, row in ranking_maior.iterrows():
        html += f"""
                <tr>
                    <td>{row['nome_municipio_padronizado']}</td>
                    <td>{row['total_atendimentos']:,}</td>
                    <td>{row['populacao_estimada']:,}</td>
                    <td>{row['atendimentos_por_100mil']:.2f}</td>
                </tr>
        """

    html += f"""
            </table>
        </div>
        
        <div class="section">
            <h2>{next_section + 2}. Municípios com Menor Proporção de Atendimentos</h2>
            
            <p>Por outro lado, alguns municípios apresentam uma proporção de atendimentos significativamente menor:</p>
            
            <div class="chart-container">
                <img class="chart" src="../visualizacoes/03_proporcao_menor.png" alt="Municípios com Menor Proporção de Atendimentos">
            </div>
            
            <p>Estes municípios podem indicar áreas com menor acesso a serviços de saúde, ou podem representar municípios cujos habitantes recorrem a serviços em cidades vizinhas.</p>
            
            <h3>Tabela: Municípios com Menor Proporção de Atendimentos</h3>
            <table>
                <tr>
                    <th>Município</th>
                    <th>Total de Atendimentos</th>
                    <th>População</th>
                    <th>Atendimentos por 100 mil hab.</th>
                </tr>
    """

    # Adicionar municípios do ranking à tabela
    for _, row in ranking_menor.iterrows():
        html += f"""
                <tr>
                    <td>{row['nome_municipio_padronizado']}</td>
                    <td>{row['total_atendimentos']:,}</td>
                    <td>{row['populacao_estimada']:,}</td>
                    <td>{row['atendimentos_por_100mil']:.2f}</td>
                </tr>
        """

    html += f"""
            </table>
        </div>
        
        <div class="section">
            <h2>{next_section + 3}. Conclusões e Recomendações</h2>
            
            <h3>Principais Conclusões:</h3>
            <ul>
                <li>Há disparidades significativas na distribuição de atendimentos do SUS entre os municípios do Ceará.</li>
                <li>Municípios que são polos regionais de saúde tendem a apresentar proporções mais elevadas de atendimentos.</li>
                <li>Alguns municípios apresentam proporções de atendimentos que excedem sua população, o que pode indicar seu papel como centros de referência ou inconsistências nos dados.</li>
                <li>Municípios menores frequentemente apresentam proporções mais baixas de atendimentos, sugerindo que seus habitantes podem buscar atendimento em centros maiores.</li>
            </ul>
            
            <h3>Recomendações:</h3>
            <ul>
                <li>Investigar mais detalhadamente os municípios com valores extremos (muito altos ou muito baixos) para identificar possíveis causas.</li>
                <li>Considerar fatores como IDH e acessibilidade geográfica na análise da distribuição de atendimentos.</li>
                <li>Realizar uma análise dos tipos de atendimentos para identificar padrões específicos por município ou região.</li>
                <li>Desenvolver políticas para equilibrar a oferta de serviços de saúde, considerando as necessidades específicas de cada região.</li>
                <li>Implementar sistemas de monitoramento contínuo para acompanhar a evolução dos atendimentos ao longo do tempo.</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>{next_section + 4}. Considerações Metodológicas</h2>
            
            <p>Esta análise apresenta algumas limitações que devem ser consideradas:</p>
            <ul>
                <li>Os dados de atendimentos podem incluir registros duplicados ou imprecisos.</li>
                <li>A padronização dos nomes de municípios pode não ter sido perfeita, resultando em algumas inconsistências na integração das bases.</li>
                <li>Os dados populacionais utilizados podem não refletir com precisão a população atual de cada município.</li>
                <li>A análise não considera fatores como perfil epidemiológico, estrutura etária da população ou presença de unidades de saúde especializadas.</li>
            </ul>
            
            <p>Para análises futuras mais aprofundadas, recomenda-se incorporar dados adicionais como:
            perfil socioeconômico dos municípios, capacidade instalada de serviços de saúde, 
            perfil epidemiológico da população e informações sobre fluxos intermunicipais de pacientes.</p>
        </div>
        
        <div class="section">
            <p><strong>Relatório gerado automaticamente por script Python.</strong></p>
            <p><em>Análise Enriquecida de Atendimentos SUS com Informações Municipais</em></p>
        </div>
    </body>
    </html>
    """
    
    # Salvar o HTML
    with open('../resultados/relatorio_atendimentos_sus.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Relatório gerado com sucesso: '../resultados/relatorio_atendimentos_sus.html'")
    
except Exception as e:
    print(f"Erro durante a geração do relatório: {e}")
    import traceback
    traceback.print_exc()  # Mostrar detalhes do erro