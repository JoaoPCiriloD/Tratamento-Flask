import sqlite3
import faker
import random
from datetime import datetime, timedelta

# Configurar o gerador de dados falsos
fake = faker.Faker('pt_BR')  # Usando localização brasileira

def create_database():
    """Cria o banco de dados e as tabelas"""
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    # Criar tabela de funcionários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefone TEXT,
            cpf TEXT UNIQUE NOT NULL,
            data_nascimento DATE,
            endereco TEXT,
            cidade TEXT,
            estado TEXT,
            cep TEXT,
            salario REAL,
            cargo TEXT,
            departamento TEXT,
            data_contratacao DATE,
            ativo BOOLEAN DEFAULT 1
        )
    ''')
    
    # Criar tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT,
            preco REAL NOT NULL,
            custo REAL NOT NULL,
            estoque INTEGER DEFAULT 0,
            codigo_barras TEXT UNIQUE,
            fornecedor TEXT,
            data_cadastro DATE,
            ativo BOOLEAN DEFAULT 1
        )
    ''')
    
    # Criar tabela de vendas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario_id INTEGER,
            produto_id INTEGER,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            desconto REAL DEFAULT 0,
            total REAL NOT NULL,
            data_venda DATETIME,
            metodo_pagamento TEXT,
            FOREIGN KEY (funcionario_id) REFERENCES funcionarios (id),
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')
    
    # Criar tabela de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE,
            telefone TEXT,
            cpf TEXT UNIQUE,
            data_nascimento DATE,
            endereco TEXT,
            cidade TEXT,
            estado TEXT,
            cep TEXT,
            data_cadastro DATE,
            ativo BOOLEAN DEFAULT 1
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Banco de dados criado com sucesso!")

def inserir_funcionarios(quantidade=50):
    """Insere funcionários fictícios no banco"""
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    cargos = ['Analista', 'Desenvolvedor', 'Gerente', 'Coordenador', 'Assistente', 
              'Diretor', 'Supervisor', 'Especialista', 'Consultor', 'Técnico']
    
    departamentos = ['TI', 'Vendas', 'Marketing', 'RH', 'Financeiro', 
                     'Operações', 'Jurídico', 'Suporte', 'Logística']
    
    for _ in range(quantidade):
        nome = fake.name()
        email = fake.email()
        telefone = fake.phone_number()
        cpf = fake.cpf()
        data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=65)
        endereco = fake.address().replace('\n', ', ')
        cidade = fake.city()
        estado = fake.state()
        cep = fake.postcode()
        salario = round(random.uniform(2000, 15000), 2)
        cargo = random.choice(cargos)
        departamento = random.choice(departamentos)
        data_contratacao = fake.date_between(start_date='-5y', end_date='today')
        ativo = random.choice([True, True, True, False])  # 75% ativo
        
        try:
            cursor.execute('''
                INSERT INTO funcionarios (nome, email, telefone, cpf, data_nascimento,
                                        endereco, cidade, estado, cep, salario, cargo,
                                        departamento, data_contratacao, ativo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome, email, telefone, cpf, data_nascimento, endereco, cidade,
                  estado, cep, salario, cargo, departamento, data_contratacao, ativo))
        except sqlite3.IntegrityError:
            # Ignora se email ou CPF já existir
            pass
    
    conn.commit()
    conn.close()
    print(f"✅ {quantidade} funcionários inseridos!")

def inserir_produtos(quantidade=100):
    """Insere produtos fictícios no banco"""
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    categorias = ['Eletrônicos', 'Roupas', 'Casa e Jardim', 'Esportes', 'Livros',
                  'Beleza', 'Alimentação', 'Automóveis', 'Brinquedos', 'Ferramentas']
    
    fornecedores = ['Fornecedor A Ltda', 'B&B Distribuidora', 'Mega Suprimentos',
                    'Central de Produtos', 'Distribuidora Sul', 'Norte Atacado']
    
    for _ in range(quantidade):
        nome = fake.catch_phrase()
        categoria = random.choice(categorias)
        custo = round(random.uniform(10, 500), 2)
        preco = round(custo * random.uniform(1.2, 3.0), 2)  # Margem de 20% a 200%
        estoque = random.randint(0, 1000)
        codigo_barras = fake.ean13()
        fornecedor = random.choice(fornecedores)
        data_cadastro = fake.date_between(start_date='-2y', end_date='today')
        ativo = random.choice([True, True, True, False])  # 75% ativo
        
        try:
            cursor.execute('''
                INSERT INTO produtos (nome, categoria, preco, custo, estoque,
                                    codigo_barras, fornecedor, data_cadastro, ativo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome, categoria, preco, custo, estoque, codigo_barras,
                  fornecedor, data_cadastro, ativo))
        except sqlite3.IntegrityError:
            # Ignora se código de barras já existir
            pass
    
    conn.commit()
    conn.close()
    print(f"✅ {quantidade} produtos inseridos!")

def inserir_clientes(quantidade=200):
    """Insere clientes fictícios no banco"""
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    for _ in range(quantidade):
        nome = fake.name()
        email = fake.email() if random.random() > 0.1 else None  # 90% tem email
        telefone = fake.phone_number() if random.random() > 0.05 else None  # 95% tem telefone
        cpf = fake.cpf() if random.random() > 0.02 else None  # 98% tem CPF
        data_nascimento = fake.date_of_birth(minimum_age=16, maximum_age=80)
        endereco = fake.address().replace('\n', ', ')
        cidade = fake.city()
        estado = fake.state()
        cep = fake.postcode()
        data_cadastro = fake.date_between(start_date='-3y', end_date='today')
        ativo = random.choice([True, True, True, True, False])  # 80% ativo
        
        try:
            cursor.execute('''
                INSERT INTO clientes (nome, email, telefone, cpf, data_nascimento,
                                    endereco, cidade, estado, cep, data_cadastro, ativo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome, email, telefone, cpf, data_nascimento, endereco,
                  cidade, estado, cep, data_cadastro, ativo))
        except sqlite3.IntegrityError:
            # Ignora se email ou CPF já existir
            pass
    
    conn.commit()
    conn.close()
    print(f"✅ {quantidade} clientes inseridos!")

def inserir_vendas(quantidade=500):
    """Insere vendas fictícias no banco"""
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    # Buscar IDs dos funcionários e produtos ativos
    cursor.execute("SELECT id FROM funcionarios WHERE ativo = 1")
    funcionarios_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id, preco FROM produtos WHERE ativo = 1")
    produtos = [(row[0], row[1]) for row in cursor.fetchall()]
    
    metodos_pagamento = ['Cartão de Crédito', 'Cartão de Débito', 'Dinheiro', 
                         'PIX', 'Boleto', 'Transferência']
    
    for _ in range(quantidade):
        if not funcionarios_ids or not produtos:
            break
            
        funcionario_id = random.choice(funcionarios_ids)
        produto_id, preco_produto = random.choice(produtos)
        quantidade_vendida = random.randint(1, 10)
        preco_unitario = preco_produto
        desconto = round(random.uniform(0, 0.2), 2) if random.random() > 0.7 else 0  # 30% chance de desconto
        total = round(quantidade_vendida * preco_unitario * (1 - desconto), 2)
        data_venda = fake.date_time_between(start_date='-1y', end_date='now')
        metodo_pagamento = random.choice(metodos_pagamento)
        
        cursor.execute('''
            INSERT INTO vendas (funcionario_id, produto_id, quantidade, preco_unitario,
                              desconto, total, data_venda, metodo_pagamento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (funcionario_id, produto_id, quantidade_vendida, preco_unitario,
              desconto, total, data_venda, metodo_pagamento))
    
    conn.commit()
    conn.close()
    print(f"✅ {quantidade} vendas inseridas!")

def mostrar_estatisticas():
    """Mostra estatísticas do banco de dados"""
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    print("\n📊 ESTATÍSTICAS DO BANCO DE DADOS:")
    print("=" * 40)
    
    # Contagem de registros por tabela
    tabelas = ['funcionarios', 'produtos', 'clientes', 'vendas']
    for tabela in tabelas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
        count = cursor.fetchone()[0]
        print(f"{tabela.capitalize()}: {count} registros")
    
    # Vendas por departamento
    print("\n💰 VENDAS POR DEPARTAMENTO:")
    cursor.execute('''
        SELECT f.departamento, COUNT(v.id) as total_vendas, 
               ROUND(SUM(v.total), 2) as receita_total
        FROM vendas v
        JOIN funcionarios f ON v.funcionario_id = f.id
        GROUP BY f.departamento
        ORDER BY receita_total DESC
    ''')
    
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]} vendas - R$ {row[2]}")
    
    # Top 5 produtos mais vendidos
    print("\n🏆 TOP 5 PRODUTOS MAIS VENDIDOS:")
    cursor.execute('''
        SELECT p.nome, SUM(v.quantidade) as quantidade_total,
               ROUND(SUM(v.total), 2) as receita_total
        FROM vendas v
        JOIN produtos p ON v.produto_id = p.id
        GROUP BY p.id, p.nome
        ORDER BY quantidade_total DESC
        LIMIT 5
    ''')
    
    for i, row in enumerate(cursor.fetchall(), 1):
        print(f"{i}. {row[0]} - {row[1]} unidades - R$ {row[2]}")
    
    conn.close()

if __name__ == "__main__":
    print("🚀 Criando banco de dados com dados fictícios...")
    print("=" * 50)
    
    # Criar banco e tabelas
    create_database()
    
    # Inserir dados fictícios
    inserir_funcionarios(50)
    inserir_produtos(100)
    inserir_clientes(200)
    inserir_vendas(500)
    
    # Mostrar estatísticas
    mostrar_estatisticas()
    
    print("\n✅ Banco de dados criado com sucesso!")
    print("📁 Arquivo: empresa.db")
    print("🔧 Você pode usar ferramentas como DB Browser for SQLite para visualizar os dados.")
