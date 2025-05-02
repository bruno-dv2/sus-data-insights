import os
import subprocess
import shutil

# Verificar se quer manter backup
resposta = input("Deseja manter backup dos arquivos anteriores? (s/n): ")
if resposta.lower() == 's':
    # Criar pastas de backup se não existirem
    os.makedirs('../backup/resultados', exist_ok=True)
    os.makedirs('../backup/visualizacoes', exist_ok=True)
    
    # Copiar arquivos para backup
    for arquivo in os.listdir('../resultados'):
        if arquivo.endswith('.csv') or arquivo.endswith('.html'):
            shutil.copy2(f'../resultados/{arquivo}', f'../backup/resultados/{arquivo}')
    
    for arquivo in os.listdir('../visualizacoes'):
        if arquivo.endswith('.png'):
            shutil.copy2(f'../visualizacoes/{arquivo}', f'../backup/visualizacoes/{arquivo}')
    
    print("Backup concluído com sucesso!")

# Limpar arquivos anteriores
for arquivo in os.listdir('../resultados'):
    if arquivo.endswith('.csv') or arquivo.endswith('.html'):
        os.remove(f'../resultados/{arquivo}')

for arquivo in os.listdir('../visualizacoes'):
    if arquivo.endswith('.png'):
        os.remove(f'../visualizacoes/{arquivo}')

print("Arquivos anteriores removidos!")

# Executar scripts
print("Executando análise...")
subprocess.run(['python3', 'analisar_dados.py'])

print("\nGerando relatório...")
subprocess.run(['python3', 'gerar_relatorio.py'])

print("\nProcesso concluído! Novos arquivos gerados.")