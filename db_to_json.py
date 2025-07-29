import sqlite3
import json
import os
from datetime import datetime

class DatabaseToJsonConverter:
    """Conversor de banco de dados SQLite para JSON"""
    
    def __init__(self, db_path='empresa.db', json_dir='dados_json'):
        self.db_path = db_path
        self.json_dir = json_dir
        self.ensure_json_directory()
    
    def ensure_json_directory(self):
        """Cria o diretório JSON se não existir"""
        if not os.path.exists(self.json_dir):
            os.makedirs(self.json_dir)
            print(f"📁 Diretório '{self.json_dir}' criado")
    
    def get_table_data(self, table_name):
        """Extrai dados de uma tabela específica"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Converter Row objects para dicionários
            data = []
            for row in rows:
                data.append(dict(row))
            
            return data
        except sqlite3.Error as e:
            print(f"❌ Erro ao acessar tabela {table_name}: {e}")
            return []
        finally:
            conn.close()
    
    def save_table_to_json(self, table_name):
        """Salva uma tabela específica em JSON"""
        data = self.get_table_data(table_name)
        
        if data:
            filename = os.path.join(self.json_dir, f"{table_name}.json")
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"✅ {table_name}: {len(data)} registros salvos em {filename}")
            return True
        else:
            print(f"⚠️ Nenhum dado encontrado para a tabela {table_name}")
            return False
    
    def export_all_tables(self):
        """Exporta todas as tabelas para JSON"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Obter lista de tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        
        print("🚀 INICIANDO EXPORTAÇÃO PARA JSON")
        print("=" * 40)
        
        exported_tables = []
        for table in tables:
            table_name = table[0]
            if self.save_table_to_json(table_name):
                exported_tables.append(table_name)
        
        # Criar arquivo de resumo
        self.create_summary_file(exported_tables)
        
        print(f"\n✅ Exportação concluída! {len(exported_tables)} tabelas exportadas")
        return exported_tables
    
    def create_summary_file(self, exported_tables):
        """Cria arquivo de resumo da exportação"""
        summary = {
            "exportacao": {
                "data_hora": datetime.now().isoformat(),
                "banco_origem": self.db_path,
                "total_tabelas": len(exported_tables),
                "tabelas_exportadas": exported_tables
            },
            "estatisticas": {}
        }
        
        # Adicionar estatísticas de cada tabela
        for table in exported_tables:
            data = self.get_table_data(table)
            summary["estatisticas"][table] = {
                "total_registros": len(data),
                "arquivo_json": f"{table}.json"
            }
        
        summary_file = os.path.join(self.json_dir, "_resumo_exportacao.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📊 Resumo salvo em {summary_file}")
    
    def create_unified_json(self):
        """Cria um arquivo JSON unificado com todas as tabelas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Obter lista de tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        
        unified_data = {
            "metadados": {
                "data_exportacao": datetime.now().isoformat(),
                "banco_origem": self.db_path,
                "total_tabelas": len(tables)
            },
            "dados": {}
        }
        
        for table in tables:
            table_name = table[0]
            unified_data["dados"][table_name] = self.get_table_data(table_name)
        
        unified_file = os.path.join(self.json_dir, "banco_completo.json")
        with open(unified_file, 'w', encoding='utf-8') as f:
            json.dump(unified_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"🗂️ Arquivo unificado salvo em {unified_file}")
    
    def export_with_relationships(self):
        """Exporta dados com relacionamentos preservados"""
        # Funcionários com suas vendas
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        funcionarios_vendas = []
        
        cursor.execute("SELECT * FROM funcionarios WHERE ativo = 1")
        funcionarios = cursor.fetchall()
        
        for funcionario in funcionarios:
            func_dict = dict(funcionario)
            
            # Buscar vendas do funcionário
            cursor.execute("""
                SELECT v.*, p.nome as produto_nome, p.categoria
                FROM vendas v
                JOIN produtos p ON v.produto_id = p.id
                WHERE v.funcionario_id = ?
                ORDER BY v.data_venda DESC
            """, (funcionario['id'],))
            
            vendas = cursor.fetchall()
            func_dict['vendas'] = [dict(venda) for venda in vendas]
            func_dict['total_vendas'] = len(vendas)
            func_dict['receita_total'] = sum(venda['total'] for venda in vendas)
            
            funcionarios_vendas.append(func_dict)
        
        conn.close()
        
        # Salvar dados com relacionamentos
        rel_file = os.path.join(self.json_dir, "funcionarios_com_vendas.json")
        with open(rel_file, 'w', encoding='utf-8') as f:
            json.dump(funcionarios_vendas, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"🔗 Dados com relacionamentos salvos em {rel_file}")

def main():
    """Função principal para executar a conversão"""
    print("🔄 CONVERSOR DE BANCO PARA JSON")
    print("=" * 50)
    
    # Verificar se o banco existe
    if not os.path.exists('empresa.db'):
        print("❌ Arquivo 'empresa.db' não encontrado!")
        print("Execute primeiro o script 'criar_banco_simples.py'")
        return
    
    converter = DatabaseToJsonConverter()
    
    # Menu de opções
    while True:
        print("\nEscolha uma opção:")
        print("1. Exportar todas as tabelas (arquivos separados)")
        print("2. Criar arquivo JSON unificado")
        print("3. Exportar com relacionamentos")
        print("4. Exportar tudo (opções 1, 2 e 3)")
        print("5. Ver arquivos JSON criados")
        print("0. Sair")
        
        opcao = input("\nDigite a opção: ")
        
        if opcao == "1":
            converter.export_all_tables()
        
        elif opcao == "2":
            converter.create_unified_json()
        
        elif opcao == "3":
            converter.export_with_relationships()
        
        elif opcao == "4":
            print("\n🚀 EXPORTAÇÃO COMPLETA")
            print("-" * 30)
            converter.export_all_tables()
            print("\n" + "-" * 30)
            converter.create_unified_json()
            print("\n" + "-" * 30)
            converter.export_with_relationships()
            print("\n✅ Exportação completa finalizada!")
        
        elif opcao == "5":
            json_dir = "dados_json"
            if os.path.exists(json_dir):
                files = os.listdir(json_dir)
                if files:
                    print(f"\n📁 Arquivos JSON em '{json_dir}':")
                    for file in sorted(files):
                        file_path = os.path.join(json_dir, file)
                        size = os.path.getsize(file_path)
                        print(f"  📄 {file} ({size:,} bytes)")
                else:
                    print(f"📁 Diretório '{json_dir}' está vazio")
            else:
                print(f"📁 Diretório '{json_dir}' não existe")
        
        elif opcao == "0":
            print("👋 Saindo...")
            break
        
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()
