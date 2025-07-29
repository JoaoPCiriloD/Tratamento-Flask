import sqlite3
import json
import os
import time
import threading
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DatabaseMonitor(FileSystemEventHandler):
    """Monitor que detecta mudanças no banco de dados"""
    
    def __init__(self, db_path='empresa.db', json_dir='dados_json_auto'):
        self.db_path = db_path
        self.json_dir = json_dir
        self.last_check = datetime.now()
        self.ensure_json_directory()
        
        # Armazenar contadores de registros para detectar mudanças
        self.table_counts = self.get_table_counts()
        
    def ensure_json_directory(self):
        """Cria o diretório JSON se não existir"""
        if not os.path.exists(self.json_dir):
            os.makedirs(self.json_dir)
            print(f"📁 Diretório de monitoramento '{self.json_dir}' criado")
    
    def get_table_counts(self):
        """Obtém contagem atual de registros em cada tabela"""
        if not os.path.exists(self.db_path):
            return {}
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        counts = {}
        
        try:
            # Obter lista de tabelas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                counts[table_name] = cursor.fetchone()[0]
                
        except sqlite3.Error as e:
            print(f"❌ Erro ao verificar contagens: {e}")
        finally:
            conn.close()
            
        return counts
    
    def on_modified(self, event):
        """Executado quando o arquivo do banco é modificado"""
        if event.src_path.endswith('empresa.db') and not event.is_directory:
            print(f"🔔 Mudança detectada no banco: {datetime.now().strftime('%H:%M:%S')}")
            self.check_for_changes()
    
    def check_for_changes(self):
        """Verifica se houve mudanças nos dados e exporta para JSON"""
        new_counts = self.get_table_counts()
        changes_detected = False
        
        for table_name, new_count in new_counts.items():
            old_count = self.table_counts.get(table_name, 0)
            
            if new_count != old_count:
                changes_detected = True
                difference = new_count - old_count
                
                if difference > 0:
                    print(f"➕ {table_name}: +{difference} registros (total: {new_count})")
                else:
                    print(f"➖ {table_name}: {difference} registros (total: {new_count})")
                
                # Exportar tabela alterada para JSON
                self.export_table_to_json(table_name)
        
        if changes_detected:
            self.table_counts = new_counts
            self.create_change_log()
            print("✅ Dados automaticamente convertidos para JSON")
        
    def export_table_to_json(self, table_name):
        """Exporta uma tabela específica para JSON"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Converter para lista de dicionários
            data = [dict(row) for row in rows]
            
            # Salvar em arquivo JSON
            filename = os.path.join(self.json_dir, f"{table_name}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            # Salvar com timestamp
            timestamp_filename = os.path.join(
                self.json_dir, 
                f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            with open(timestamp_filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
        except sqlite3.Error as e:
            print(f"❌ Erro ao exportar {table_name}: {e}")
        finally:
            conn.close()
    
    def create_change_log(self):
        """Cria log das mudanças detectadas"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "table_counts": self.table_counts,
            "changes_detected": True
        }
        
        log_file = os.path.join(self.json_dir, "change_log.json")
        
        # Ler log existente ou criar novo
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        else:
            log_data = {"changes": []}
        
        log_data["changes"].append(log_entry)
        
        # Manter apenas os últimos 100 registros
        if len(log_data["changes"]) > 100:
            log_data["changes"] = log_data["changes"][-100:]
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False, default=str)

class AutoJsonExporter:
    """Sistema de exportação automática para JSON"""
    
    def __init__(self, db_path='empresa.db'):
        self.db_path = db_path
        self.monitor = DatabaseMonitor(db_path)
        self.observer = Observer()
        self.is_monitoring = False
        
    def start_monitoring(self):
        """Inicia o monitoramento do banco de dados"""
        if not os.path.exists(self.db_path):
            print(f"❌ Arquivo {self.db_path} não encontrado!")
            return False
        
        # Configurar observer para monitorar o diretório do banco
        db_dir = os.path.dirname(os.path.abspath(self.db_path))
        self.observer.schedule(self.monitor, db_dir, recursive=False)
        
        # Iniciar monitoramento
        self.observer.start()
        self.is_monitoring = True
        
        print(f"👁️ Monitoramento iniciado para: {self.db_path}")
        print("🔄 Os dados serão automaticamente convertidos para JSON quando houver mudanças")
        print("⏹️ Pressione Ctrl+C para parar o monitoramento")
        
        return True
    
    def stop_monitoring(self):
        """Para o monitoramento"""
        if self.is_monitoring:
            self.observer.stop()
            self.observer.join()
            self.is_monitoring = False
            print("⏹️ Monitoramento parado")
    
    def manual_export(self):
        """Executa exportação manual de todos os dados"""
        print("🔄 Executando exportação manual...")
        self.monitor.check_for_changes()

def start_auto_monitor():
    """Inicia o sistema de monitoramento automático"""
    print("🤖 SISTEMA DE AUTOMAÇÃO JSON")
    print("=" * 40)
    
    exporter = AutoJsonExporter()
    
    if not exporter.start_monitoring():
        return
    
    try:
        # Executar exportação inicial
        exporter.manual_export()
        
        # Manter o programa rodando
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Interrupção detectada...")
        exporter.stop_monitoring()

def test_automation():
    """Testa a automação inserindo dados fictícios"""
    print("🧪 TESTE DE AUTOMAÇÃO")
    print("=" * 30)
    
    # Inserir alguns dados de teste
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    try:
        # Inserir cliente teste
        cursor.execute('''
            INSERT INTO clientes (nome, email, telefone, cidade, data_cadastro, ativo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            'Cliente Teste Automação',
            'teste@automacao.com',
            '(11) 99999-9999',
            'São Paulo',
            datetime.now().strftime('%Y-%m-%d'),
            1
        ))
        
        # Inserir produto teste
        cursor.execute('''
            INSERT INTO produtos (nome, categoria, preco, custo, estoque, 
                                codigo_barras, fornecedor, data_cadastro, ativo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Produto Teste Automação',
            'Teste',
            99.99,
            50.00,
            100,
            '1234567890123',
            'Fornecedor Teste',
            datetime.now().strftime('%Y-%m-%d'),
            1
        ))
        
        conn.commit()
        print("✅ Dados de teste inseridos no banco")
        print("🔍 Verifique se os arquivos JSON foram atualizados automaticamente")
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao inserir dados de teste: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test_automation()
    else:
        start_auto_monitor()
