import sqlite3
import json
import os
import time
from datetime import datetime

def demonstrar_automacao():
    """Demonstra o sistema de automação JSON"""
    print("🎯 DEMONSTRAÇÃO DA AUTOMAÇÃO JSON")
    print("=" * 50)
    
    # Verificar se o banco existe
    if not os.path.exists('empresa.db'):
        print("❌ Banco 'empresa.db' não encontrado!")
        print("Execute primeiro: python criar_banco_simples.py")
        return
    
    print("1️⃣ Executando exportação inicial...")
    from automacao_json import SimpleJsonAutoExporter
    
    exporter = SimpleJsonAutoExporter(check_interval=2)  # Verificar a cada 2 segundos
    
    # Exportação inicial
    exporter.export_all_now()
    
    print("\n2️⃣ Iniciando monitoramento automático...")
    print("🔄 Vou inserir alguns dados de teste para demonstrar a automação")
    print("⏰ Aguarde alguns segundos...")
    
    # Iniciar monitoramento em thread separada
    import threading
    
    def monitor_thread():
        for i in range(10):  # Monitorar por 20 segundos
            time.sleep(2)
            if exporter.check_and_export_changes():
                print(f"📤 Exportação automática #{i+1} concluída!")
    
    # Iniciar thread de monitoramento
    monitor = threading.Thread(target=monitor_thread)
    monitor.daemon = True
    monitor.start()
    
    # Inserir dados de teste para demonstrar automação
    print("\n3️⃣ Inserindo dados de teste...")
    
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    try:
        for i in range(5):
            print(f"\n📝 Inserindo lote {i+1}/5...")
            
            # Inserir cliente
            cursor.execute('''
                INSERT INTO clientes (nome, email, telefone, cidade, data_cadastro, ativo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                f'Cliente Demo {i+1} - {datetime.now().strftime("%H:%M:%S")}',
                f'demo{i+1}_{int(time.time())}@teste.com',
                f'(11) 9999{i:04d}',
                ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Brasília'][i],
                datetime.now().strftime('%Y-%m-%d'),
                1
            ))
            
            # Inserir produto
            cursor.execute('''
                INSERT INTO produtos (nome, categoria, preco, custo, estoque, 
                                    codigo_barras, fornecedor, data_cadastro, ativo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                f'Produto Demo {i+1} - {datetime.now().strftime("%H:%M:%S")}',
                'Demonstração',
                round(50 + (i * 25.50), 2),
                round(25 + (i * 12.75), 2),
                100 + (i * 10),
                f'DEMO{i+1}{int(time.time())}',
                'Fornecedor Demo',
                datetime.now().strftime('%Y-%m-%d'),
                1
            ))
            
            conn.commit()
            print(f"✅ Lote {i+1} inserido - aguardando detecção automática...")
            time.sleep(3)  # Aguardar para ver a automação funcionando
    
    except Exception as e:
        print(f"❌ Erro ao inserir dados: {e}")
    finally:
        conn.close()
    
    # Aguardar thread de monitoramento finalizar
    monitor.join()
    
    print("\n4️⃣ Verificando arquivos JSON gerados...")
    
    json_dir = 'dados_json_auto'
    if os.path.exists(json_dir):
        files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
        
        print(f"\n📁 Arquivos JSON em '{json_dir}':")
        for file in sorted(files):
            file_path = os.path.join(json_dir, file)
            size = os.path.getsize(file_path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"  📄 {file}")
            print(f"      💾 Tamanho: {size:,} bytes")
            print(f"      🕐 Modificado: {mod_time.strftime('%d/%m/%Y %H:%M:%S')}")
            
            # Mostrar preview do conteúdo
            if not file.startswith('_') and 'history' not in file:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        print(f"      📊 Registros: {len(data) if isinstance(data, list) else 'N/A'}")
                except:
                    pass
            print()
    
    print("5️⃣ Demonstração de consulta nos dados JSON...")
    
    # Ler dados JSON e fazer algumas análises
    try:
        clientes_file = os.path.join(json_dir, 'clientes.json')
        produtos_file = os.path.join(json_dir, 'produtos.json')
        
        if os.path.exists(clientes_file):
            with open(clientes_file, 'r', encoding='utf-8') as f:
                clientes = json.load(f)
            
            clientes_demo = [c for c in clientes if 'Demo' in c.get('nome', '')]
            print(f"👥 Clientes de demonstração encontrados: {len(clientes_demo)}")
            
            for cliente in clientes_demo[-3:]:  # Últimos 3
                print(f"   • {cliente['nome']} ({cliente['cidade']})")
        
        if os.path.exists(produtos_file):
            with open(produtos_file, 'r', encoding='utf-8') as f:
                produtos = json.load(f)
            
            produtos_demo = [p for p in produtos if 'Demo' in p.get('nome', '')]
            print(f"\n📦 Produtos de demonstração encontrados: {len(produtos_demo)}")
            
            for produto in produtos_demo[-3:]:  # Últimos 3
                print(f"   • {produto['nome']} - R$ {produto['preco']}")
    
    except Exception as e:
        print(f"❌ Erro ao analisar JSON: {e}")
    
    print("\n✅ DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 50)
    print("🔧 Para usar a automação:")
    print("   python automacao_json.py")
    print("\n📊 Para converter dados existentes:")
    print("   python db_to_json.py")
    print("\n🎯 Os dados agora são automaticamente convertidos para JSON!")

if __name__ == "__main__":
    demonstrar_automacao()
