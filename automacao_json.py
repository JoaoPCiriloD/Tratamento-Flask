import sqlite3
import json
import os
import time
import threading
from datetime import datetime

class SimpleJsonAutoExporter:
    """Sistema simples de automação para exportar dados para JSON"""
    
    def __init__(self, db_path='empresa.db', json_dir='dados_json_auto', check_interval=5):
        self.db_path = db_path
        self.json_dir = json_dir
        self.check_interval = check_interval  # segundos
        self.is_running = False
        self.table_counts = {}
        
        self.ensure_json_directory()
        self.initialize_counts()
    
    def ensure_json_directory(self):
        """Cria o diretório JSON se não existir"""
        if not os.path.exists(self.json_dir):
            os.makedirs(self.json_dir)
            print(f"📁 Diretório '{self.json_dir}' criado")
    
    def initialize_counts(self):
        """Inicializa contadores das tabelas"""
        if os.path.exists(self.db_path):
            self.table_counts = self.get_current_counts()
            print(f"📊 Contadores inicializados: {self.table_counts}")
    
    def get_current_counts(self):
        """Obtém contagem atual de registros"""
        counts = {}
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Obter tabelas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                counts[table_name] = cursor.fetchone()[0]
            
            conn.close()
        except sqlite3.Error as e:
            print(f"❌ Erro ao verificar contagens: {e}")
        
        return counts
    
    def export_table_data(self, table_name):
        """Exporta dados de uma tabela para JSON"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Converter para lista de dicionários
            data = []
            for row in rows:
                row_dict = {}
                for key in row.keys():
                    row_dict[key] = row[key]
                data.append(row_dict)
            
            # Salvar arquivo principal
            main_file = os.path.join(self.json_dir, f"{table_name}.json")
            with open(main_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            # Salvar com timestamp (histórico)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            history_file = os.path.join(self.json_dir, f"{table_name}_history_{timestamp}.json")
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "table": table_name,
                    "total_records": len(data),
                    "data": data
                }, f, indent=2, ensure_ascii=False, default=str)
            
            conn.close()
            return len(data)
            
        except Exception as e:
            print(f"❌ Erro ao exportar {table_name}: {e}")
            return 0
    
    def check_and_export_changes(self):
        """Verifica mudanças e exporta se necessário"""
        if not os.path.exists(self.db_path):
            return
        
        current_counts = self.get_current_counts()
        changes_detected = False
        
        for table_name, current_count in current_counts.items():
            previous_count = self.table_counts.get(table_name, 0)
            
            if current_count != previous_count:
                changes_detected = True
                difference = current_count - previous_count
                
                print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] Mudança em '{table_name}': {previous_count} → {current_count} ({difference:+d})")
                
                # Exportar tabela
                exported_count = self.export_table_data(table_name)
                print(f"✅ {table_name}: {exported_count} registros exportados para JSON")
        
        if changes_detected:
            self.table_counts = current_counts
            self.create_summary_report()
        
        return changes_detected
    
    def create_summary_report(self):
        """Cria relatório resumo da automação"""
        report = {
            "last_check": datetime.now().isoformat(),
            "database_file": self.db_path,
            "json_directory": self.json_dir,
            "table_counts": self.table_counts,
            "total_records": sum(self.table_counts.values())
        }
        
        report_file = os.path.join(self.json_dir, "_automation_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    
    def start_monitoring(self):
        """Inicia monitoramento automático"""
        if not os.path.exists(self.db_path):
            print(f"❌ Banco de dados '{self.db_path}' não encontrado!")
            return False
        
        self.is_running = True
        print(f"🤖 Automação iniciada!")
        print(f"📁 Banco: {self.db_path}")
        print(f"📂 JSON: {self.json_dir}")
        print(f"⏱️ Intervalo: {self.check_interval} segundos")
        print("🛑 Pressione Ctrl+C para parar\n")
        
        # Exportação inicial
        print("🔄 Executando exportação inicial...")
        self.check_and_export_changes()
        
        try:
            while self.is_running:
                time.sleep(self.check_interval)
                self.check_and_export_changes()
                
        except KeyboardInterrupt:
            print("\n🛑 Parando automação...")
            self.is_running = False
        
        return True
    
    def stop_monitoring(self):
        """Para o monitoramento"""
        self.is_running = False
        print("⏹️ Automação parada")
    
    def export_all_now(self):
        """Força exportação de todas as tabelas"""
        print("🔄 Forçando exportação completa...")
        
        if not os.path.exists(self.db_path):
            print(f"❌ Banco '{self.db_path}' não encontrado!")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            conn.close()
            
            for table in tables:
                table_name = table[0]
                count = self.export_table_data(table_name)
                print(f"✅ {table_name}: {count} registros exportados")
            
            self.table_counts = self.get_current_counts()
            self.create_summary_report()
            print("✅ Exportação completa finalizada!")
            
        except Exception as e:
            print(f"❌ Erro na exportação: {e}")

def insert_test_data():
    """Insere dados de teste para demonstrar a automação"""
    try:
        conn = sqlite3.connect('empresa.db')
        cursor = conn.cursor()
        
        # Cliente teste
        cursor.execute('''
            INSERT INTO clientes (nome, email, telefone, cidade, data_cadastro, ativo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            f'Cliente Auto {datetime.now().strftime("%H:%M:%S")}',
            f'auto{int(time.time())}@teste.com',
            '(11) 99999-0000',
            'São Paulo',
            datetime.now().strftime('%Y-%m-%d'),
            1
        ))
        
        # Produto teste
        cursor.execute('''
            INSERT INTO produtos (nome, categoria, preco, custo, estoque, 
                                codigo_barras, fornecedor, data_cadastro, ativo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            f'Produto Auto {datetime.now().strftime("%H:%M:%S")}',
            'Automação',
            99.99,
            50.00,
            50,
            str(int(time.time())),
            'Fornecedor Auto',
            datetime.now().strftime('%Y-%m-%d'),
            1
        ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Dados de teste inseridos às {datetime.now().strftime('%H:%M:%S')}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inserir dados de teste: {e}")
        return False

def main():
    """Função principal com menu"""
    print("🤖 AUTOMAÇÃO BANCO → JSON")
    print("=" * 40)
    
    exporter = SimpleJsonAutoExporter()
    
    while True:
        print("\nEscolha uma opção:")
        print("1. Iniciar monitoramento automático")
        print("2. Exportar tudo agora (manual)")
        print("3. Inserir dados de teste")
        print("4. Ver arquivos JSON criados")
        print("5. Configurar intervalo de verificação")
        print("0. Sair")
        
        opcao = input("\nDigite a opção: ")
        
        if opcao == "1":
            exporter.start_monitoring()
        
        elif opcao == "2":
            exporter.export_all_now()
        
        elif opcao == "3":
            insert_test_data()
        
        elif opcao == "4":
            if os.path.exists(exporter.json_dir):
                files = os.listdir(exporter.json_dir)
                if files:
                    print(f"\n📁 Arquivos em '{exporter.json_dir}':")
                    for file in sorted(files):
                        if file.endswith('.json'):
                            file_path = os.path.join(exporter.json_dir, file)
                            size = os.path.getsize(file_path)
                            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                            print(f"  📄 {file} ({size:,} bytes) - {mod_time.strftime('%d/%m/%Y %H:%M:%S')}")
                else:
                    print(f"📁 Diretório vazio")
            else:
                print(f"📁 Diretório não existe")
        
        elif opcao == "5":
            try:
                novo_intervalo = int(input(f"Intervalo atual: {exporter.check_interval}s. Novo intervalo (segundos): "))
                if novo_intervalo > 0:
                    exporter.check_interval = novo_intervalo
                    print(f"✅ Intervalo alterado para {novo_intervalo} segundos")
                else:
                    print("❌ Intervalo deve ser maior que 0")
            except ValueError:
                print("❌ Digite um número válido")
        
        elif opcao == "0":
            exporter.stop_monitoring()
            print("👋 Saindo...")
            break
        
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()
