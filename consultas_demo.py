import sqlite3

def executar_consultas_demo():
    """Executa consultas demonstrativas no banco de dados"""
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    print("🔍 DEMONSTRAÇÃO DE CONSULTAS SQL")
    print("=" * 50)
    
    # 1. Funcionários por departamento
    print("\n👥 FUNCIONÁRIOS POR DEPARTAMENTO:")
    cursor.execute('''
        SELECT departamento, COUNT(*) as total, 
               ROUND(AVG(salario), 2) as salario_medio
        FROM funcionarios 
        WHERE ativo = 1
        GROUP BY departamento
        ORDER BY total DESC
    ''')
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]} funcionários | Salário médio: R$ {row[2]}")
    
    # 2. Produtos mais caros por categoria
    print("\n💰 PRODUTO MAIS CARO POR CATEGORIA:")
    cursor.execute('''
        SELECT categoria, nome, ROUND(preco, 2) as preco_max
        FROM produtos p1
        WHERE preco = (
            SELECT MAX(preco) 
            FROM produtos p2 
            WHERE p2.categoria = p1.categoria AND p2.ativo = 1
        ) AND ativo = 1
        ORDER BY preco_max DESC
    ''')
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]} - R$ {row[2]}")
    
    # 3. Vendas por método de pagamento
    print("\n💳 VENDAS POR MÉTODO DE PAGAMENTO:")
    cursor.execute('''
        SELECT metodo_pagamento, COUNT(*) as quantidade,
               ROUND(SUM(total), 2) as valor_total,
               ROUND(AVG(total), 2) as ticket_medio
        FROM vendas
        GROUP BY metodo_pagamento
        ORDER BY valor_total DESC
    ''')
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]} vendas | Total: R$ {row[2]} | Ticket médio: R$ {row[3]}")
    
    # 4. Top 5 clientes por cidade
    print("\n🏙️ CLIENTES POR CIDADE (TOP 5):")
    cursor.execute('''
        SELECT cidade, COUNT(*) as total_clientes
        FROM clientes
        WHERE ativo = 1
        GROUP BY cidade
        ORDER BY total_clientes DESC
        LIMIT 5
    ''')
    for i, row in enumerate(cursor.fetchall(), 1):
        print(f"{i}. {row[0]}: {row[1]} clientes")
    
    # 5. Performance de vendas por mês
    print("\n📈 VENDAS POR MÊS (ÚLTIMOS 6 MESES):")
    cursor.execute('''
        SELECT strftime('%Y-%m', data_venda) as mes,
               COUNT(*) as total_vendas,
               ROUND(SUM(total), 2) as receita,
               ROUND(AVG(total), 2) as ticket_medio
        FROM vendas
        WHERE data_venda >= date('now', '-6 months')
        GROUP BY strftime('%Y-%m', data_venda)
        ORDER BY mes DESC
    ''')
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]} vendas | R$ {row[2]} | Ticket médio: R$ {row[3]}")
    
    # 6. Produtos com maior margem de lucro
    print("\n📊 TOP 5 PRODUTOS COM MAIOR MARGEM:")
    cursor.execute('''
        SELECT nome, categoria,
               ROUND(custo, 2) as custo,
               ROUND(preco, 2) as preco,
               ROUND(((preco - custo) / custo) * 100, 1) as margem_pct
        FROM produtos
        WHERE ativo = 1 AND custo > 0
        ORDER BY margem_pct DESC
        LIMIT 5
    ''')
    for i, row in enumerate(cursor.fetchall(), 1):
        print(f"{i}. {row[0]} ({row[1]}) | Custo: R$ {row[2]} | Preço: R$ {row[3]} | Margem: {row[4]}%")
    
    # 7. Funcionários com melhor performance
    print("\n🏆 TOP 5 VENDEDORES (ÚLTIMA PERFORMANCE):")
    cursor.execute('''
        SELECT f.nome, f.departamento,
               COUNT(v.id) as total_vendas,
               ROUND(SUM(v.total), 2) as receita_total,
               ROUND(AVG(v.total), 2) as ticket_medio
        FROM funcionarios f
        JOIN vendas v ON f.id = v.funcionario_id
        WHERE f.ativo = 1
        GROUP BY f.id, f.nome, f.departamento
        ORDER BY receita_total DESC
        LIMIT 5
    ''')
    for i, row in enumerate(cursor.fetchall(), 1):
        print(f"{i}. {row[0]} ({row[1]}) | {row[2]} vendas | R$ {row[3]} | Ticket: R$ {row[4]}")
    
    # 8. Análise de estoque
    print("\n📦 ANÁLISE DE ESTOQUE:")
    cursor.execute('''
        SELECT 
            COUNT(*) as total_produtos,
            SUM(CASE WHEN estoque = 0 THEN 1 ELSE 0 END) as sem_estoque,
            SUM(CASE WHEN estoque BETWEEN 1 AND 10 THEN 1 ELSE 0 END) as estoque_baixo,
            SUM(CASE WHEN estoque BETWEEN 11 AND 50 THEN 1 ELSE 0 END) as estoque_medio,
            SUM(CASE WHEN estoque > 50 THEN 1 ELSE 0 END) as estoque_alto
        FROM produtos
        WHERE ativo = 1
    ''')
    row = cursor.fetchone()
    print(f"Total de produtos ativos: {row[0]}")
    print(f"Sem estoque: {row[1]} produtos")
    print(f"Estoque baixo (1-10): {row[2]} produtos")
    print(f"Estoque médio (11-50): {row[3]} produtos")
    print(f"Estoque alto (50+): {row[4]} produtos")
    
    # 9. Sazonalidade de vendas
    print("\n🗓️ VENDAS POR DIA DA SEMANA:")
    cursor.execute('''
        SELECT 
            CASE strftime('%w', data_venda)
                WHEN '0' THEN 'Domingo'
                WHEN '1' THEN 'Segunda'
                WHEN '2' THEN 'Terça'
                WHEN '3' THEN 'Quarta'
                WHEN '4' THEN 'Quinta'
                WHEN '5' THEN 'Sexta'
                WHEN '6' THEN 'Sábado'
            END as dia_semana,
            COUNT(*) as total_vendas,
            ROUND(AVG(total), 2) as ticket_medio
        FROM vendas
        GROUP BY strftime('%w', data_venda)
        ORDER BY total_vendas DESC
    ''')
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]} vendas | Ticket médio: R$ {row[2]}")
    
    conn.close()
    print(f"\n✅ Consultas executadas com sucesso!")

if __name__ == "__main__":
    try:
        executar_consultas_demo()
    except sqlite3.OperationalError as e:
        print("❌ Erro: Banco de dados não encontrado!")
        print("Execute primeiro o script 'criar_banco_simples.py' para criar o banco.")
