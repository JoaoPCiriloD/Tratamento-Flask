import sqlite3

def visualizar_dados():
    """Script para visualizar os dados do banco criado"""
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    print("🔍 VISUALIZADOR DO BANCO DE DADOS")
    print("=" * 50)
    
    # Menu de opções
    while True:
        print("\nEscolha uma opção:")
        print("1. Ver todos os funcionários")
        print("2. Ver todos os produtos")
        print("3. Ver todos os clientes")
        print("4. Ver todas as vendas")
        print("5. Ver estatísticas gerais")
        print("6. Buscar funcionário por nome")
        print("7. Ver vendas de um período")
        print("8. Ver produtos em estoque baixo")
        print("0. Sair")
        
        opcao = input("\nDigite a opção: ")
        
        if opcao == "1":
            print("\n👥 FUNCIONÁRIOS:")
            cursor.execute('''
                SELECT id, nome, email, departamento, cargo, salario, ativo 
                FROM funcionarios 
                ORDER BY nome
            ''')
            for row in cursor.fetchall():
                status = "✅ Ativo" if row[6] else "❌ Inativo"
                print(f"ID: {row[0]} | {row[1]} | {row[2]} | {row[3]} - {row[4]} | R$ {row[5]} | {status}")
        
        elif opcao == "2":
            print("\n📦 PRODUTOS:")
            cursor.execute('''
                SELECT id, nome, categoria, preco, estoque, ativo 
                FROM produtos 
                ORDER BY nome
            ''')
            for row in cursor.fetchall():
                status = "✅ Ativo" if row[5] else "❌ Inativo"
                print(f"ID: {row[0]} | {row[1]} | {row[2]} | R$ {row[3]} | Estoque: {row[4]} | {status}")
        
        elif opcao == "3":
            print("\n👤 CLIENTES:")
            cursor.execute('''
                SELECT id, nome, email, telefone, cidade, ativo 
                FROM clientes 
                ORDER BY nome
            ''')
            for row in cursor.fetchall():
                status = "✅ Ativo" if row[5] else "❌ Inativo"
                email = row[2] if row[2] else "Sem email"
                telefone = row[3] if row[3] else "Sem telefone"
                print(f"ID: {row[0]} | {row[1]} | {email} | {telefone} | {row[4]} | {status}")
        
        elif opcao == "4":
            print("\n💰 VENDAS:")
            cursor.execute('''
                SELECT v.id, f.nome as funcionario, p.nome as produto, 
                       v.quantidade, v.total, v.data_venda, v.metodo_pagamento
                FROM vendas v
                JOIN funcionarios f ON v.funcionario_id = f.id
                JOIN produtos p ON v.produto_id = p.id
                ORDER BY v.data_venda DESC
                LIMIT 20
            ''')
            for row in cursor.fetchall():
                print(f"ID: {row[0]} | Funcionário: {row[1]} | Produto: {row[2]} | Qtd: {row[3]} | Total: R$ {row[4]} | Data: {row[5]} | Pagamento: {row[6]}")
        
        elif opcao == "5":
            print("\n📊 ESTATÍSTICAS GERAIS:")
            
            # Total de vendas
            cursor.execute("SELECT COUNT(*), SUM(total) FROM vendas")
            vendas_count, vendas_total = cursor.fetchone()
            print(f"Total de vendas: {vendas_count} | Receita total: R$ {vendas_total:.2f}")
            
            # Funcionário que mais vendeu
            cursor.execute('''
                SELECT f.nome, COUNT(v.id) as total_vendas, SUM(v.total) as receita
                FROM vendas v
                JOIN funcionarios f ON v.funcionario_id = f.id
                GROUP BY f.id, f.nome
                ORDER BY receita DESC
                LIMIT 1
            ''')
            top_funcionario = cursor.fetchone()
            if top_funcionario:
                print(f"Top vendedor: {top_funcionario[0]} | {top_funcionario[1]} vendas | R$ {top_funcionario[2]:.2f}")
            
            # Produto mais vendido
            cursor.execute('''
                SELECT p.nome, SUM(v.quantidade) as total_vendido
                FROM vendas v
                JOIN produtos p ON v.produto_id = p.id
                GROUP BY p.id, p.nome
                ORDER BY total_vendido DESC
                LIMIT 1
            ''')
            top_produto = cursor.fetchone()
            if top_produto:
                print(f"Produto mais vendido: {top_produto[0]} | {top_produto[1]} unidades")
        
        elif opcao == "6":
            nome_busca = input("Digite o nome do funcionário: ")
            cursor.execute('''
                SELECT id, nome, email, departamento, cargo, salario
                FROM funcionarios 
                WHERE nome LIKE ?
            ''', (f"%{nome_busca}%",))
            resultados = cursor.fetchall()
            if resultados:
                print(f"\n🔍 Resultados para '{nome_busca}':")
                for row in resultados:
                    print(f"ID: {row[0]} | {row[1]} | {row[2]} | {row[3]} - {row[4]} | R$ {row[5]}")
            else:
                print("Nenhum funcionário encontrado.")
        
        elif opcao == "7":
            print("\n📅 VENDAS POR PERÍODO:")
            cursor.execute('''
                SELECT DATE(data_venda) as data, COUNT(*) as vendas, SUM(total) as receita
                FROM vendas
                GROUP BY DATE(data_venda)
                ORDER BY data DESC
                LIMIT 10
            ''')
            for row in cursor.fetchall():
                print(f"Data: {row[0]} | Vendas: {row[1]} | Receita: R$ {row[2]:.2f}")
        
        elif opcao == "8":
            print("\n⚠️ PRODUTOS COM ESTOQUE BAIXO (menos de 50 unidades):")
            cursor.execute('''
                SELECT nome, categoria, estoque, preco
                FROM produtos 
                WHERE estoque < 50 AND ativo = 1
                ORDER BY estoque ASC
            ''')
            for row in cursor.fetchall():
                print(f"Produto: {row[0]} | Categoria: {row[1]} | Estoque: {row[2]} | Preço: R$ {row[3]}")
        
        elif opcao == "0":
            print("👋 Saindo...")
            break
        
        else:
            print("❌ Opção inválida!")
    
    conn.close()

if __name__ == "__main__":
    try:
        visualizar_dados()
    except sqlite3.OperationalError as e:
        print("❌ Erro: Banco de dados não encontrado!")
        print("Execute primeiro o script 'criar_banco_simples.py' para criar o banco.")
