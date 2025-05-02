# Script principal para executar toda a análise de atendimentos SUS do Ceará

import os
import time
import subprocess

def executar_script(nome_script, descricao):
    print(f"\n{'=' * 80}")
    print(f"Executando: {descricao}")
    print(f"{'=' * 80}")
    
    resultado = subprocess.run(['python3', nome_script])
    
    if resultado.returncode == 0:
        print(f"\n✅ {descricao} concluído com sucesso!")
        return True
    else:
        print(f"\n❌ Erro ao executar {nome_script}")
        return False

def main():
    # Criar pastas necessárias se não existirem
    for pasta in ['../dados', '../resultados', '../visualizacoes']:
        os.makedirs(pasta, exist_ok=True)
    
    print("=" * 80)
    print("ANÁLISE DE ATENDIMENTOS SUS DO CEARÁ")
    print("=" * 80)
    print("\nEste script executará toda a análise, do tratamento dos dados até a geração do relatório final.")
    print("\nCertifique-se de que os arquivos de dados estão na pasta '../dados/':")
    print("  - Arquivo TXT de atendimentos do SUS")
    print("  - Arquivo CSV do IBGE com dados dos municípios")
    
    input("\nPressione ENTER para iniciar a análise...")
    
    # Verificar se os arquivos existem
    arquivos_txt = [f for f in os.listdir('../dados') if f.endswith('.txt')]
    arquivos_csv = [f for f in os.listdir('../dados') if f.endswith('.csv')]
    
    if not arquivos_txt:
        print("\n❌ ERRO: Arquivo TXT não encontrado na pasta '../dados/'")
        print("Por favor, coloque o arquivo TXT do professor na pasta '../dados/'")
        return
    
    if not arquivos_csv:
        print("\n❌ ERRO: Arquivo CSV não encontrado na pasta '../dados/'")
        print("Por favor, coloque o arquivo CSV do IBGE na pasta '../dados/'")
        return
    
    print("\nArquivos encontrados:")
    print(f"  - Atendimentos SUS: {arquivos_txt[0]}")
    print(f"  - Dados IBGE: {arquivos_csv[0]}")
    
    # Etapa 1: Preparar os dados
    if not executar_script('preparar_dados.py', "Preparação dos dados"):
        print("\n❌ Erro na preparação dos dados. Verifique os arquivos e tente novamente.")
        return
    
    # Etapa 2: Analisar os dados
    if not executar_script('analisar_dados.py', "Análise dos dados"):
        print("\n❌ Erro na análise dos dados. Verifique os logs e tente novamente.")
        return
    
    # Etapa 3: Criar visualizações
    if not executar_script('criar_visualizacoes.py', "Criação de visualizações"):
        print("\n❌ Erro na criação de visualizações. Verifique os logs e tente novamente.")
        return
    
    # Etapa 4: Gerar relatório
    if not executar_script('gerar_relatorio.py', "Geração do relatório final"):
        print("\n❌ Erro na geração do relatório. Verifique os logs e tente novamente.")
        return
    
    print("\n" + "=" * 80)
    print("🎉 ANÁLISE CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    
    print("\nArquivos gerados:")
    print("  - Dados processados: ../resultados/")
    print("  - Visualizações: ../visualizacoes/")
    print("  - Relatório HTML: ../resultados/relatorio_atendimentos_sus.html")
    
    print("\nPara visualizar o relatório, abra o arquivo HTML em um navegador web.")
    
    # Tentar abrir o relatório automaticamente
    try:
        import webbrowser
        relatorio_path = os.path.abspath('../resultados/relatorio_atendimentos_sus.html')
        print(f"\nAbrindo o relatório no navegador: {relatorio_path}")
        webbrowser.open('file://' + relatorio_path)
    except:
        print("Não foi possível abrir o relatório automaticamente. Por favor, abra manualmente.")

if __name__ == "__main__":
    main()