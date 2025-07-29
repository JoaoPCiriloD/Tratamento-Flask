import sqlite3
import random
from datetime import datetime, timedelta

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

def gerar_cpf():
    """Gera um CPF fictício válido"""
    def calcular_digito(cpf, peso):
        soma = sum(int(cpf[i]) * peso[i] for i in range(len(peso)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    
    # Gera os 9 primeiros dígitos
    cpf = [random.randint(0, 9) for _ in range(9)]
    
    # Calcula o primeiro dígito verificador
    peso1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    cpf.append(calcular_digito(cpf, peso1))
    
    # Calcula o segundo dígito verificador
    peso2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    cpf.append(calcular_digito(cpf, peso2))
    
    return ''.join(map(str, cpf))

def gerar_email(nome):
    """Gera um email baseado no nome"""
    dominios = ['gmail.com', 'hotmail.com', 'yahoo.com.br', 'uol.com.br', 'outlook.com']
    nome_limpo = nome.lower().replace(' ', '.').replace('ç', 'c').replace('ã', 'a').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    return f"{nome_limpo}@{random.choice(dominios)}"

def gerar_telefone():
    """Gera um número de telefone brasileiro"""
    ddd = random.choice(['11', '21', '31', '41', '51', '61', '71', '81', '85', '11'])
    numero = f"9{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
    return f"({ddd}) {numero[:5]}-{numero[5:]}"

def gerar_cep():
    """Gera um CEP fictício"""
    return f"{random.randint(10000, 99999)}-{random.randint(100, 999)}"

def inserir_funcionarios(quantidade=50):
    """Insere funcionários fictícios no banco"""
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    nomes = [
        'João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa', 'Carlos Pereira',
        'Juliana Lima', 'Roberto Alves', 'Fernanda Rocha', 'Marcos Ferreira', 'Luciana Martins',
        'Rafael Souza', 'Camila Rodrigues', 'Diego Barbosa', 'Patrícia Gomes', 'Bruno Cardoso',
        'Vanessa Dias', 'Thiago Nascimento', 'Priscila Moreira', 'Gabriel Teixeira', 'Amanda Ribeiro',
        'Leonardo Castro', 'Renata Araújo', 'Gustavo Monteiro', 'Sabrina Cavalcanti', 'Rodrigo Melo',
        'Tatiane Freitas', 'Vinicius Correia', 'Cristina Vieira', 'Eduardo Mendes', 'Carla Batista',
        'Daniel Ramos', 'Mônica Torres', 'Felipe Duarte', 'Simone Cunha', 'André Lopes',
        'Elaine Barros', 'Maurício Franco', 'Rosângela Moura', 'Alexandre Nunes', 'Denise Campos',
        'Ricardo Farias', 'Silvia Machado', 'Lucas Nogueira', 'Adriana Pinto', 'Fábio Godoy',
        'Mariana Leite', 'Paulo Rezende', 'Viviane Sales', 'Henrique Azevedo', 'Larissa Porto'
    ]
    
    cargos = ['Analista', 'Desenvolvedor', 'Gerente', 'Coordenador', 'Assistente', 
              'Diretor', 'Supervisor', 'Especialista', 'Consultor', 'Técnico']
    
    departamentos = ['TI', 'Vendas', 'Marketing', 'RH', 'Financeiro', 
                     'Operações', 'Jurídico', 'Suporte', 'Logística']
    
    cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Brasília',
               'Fortaleza', 'Curitiba', 'Recife', 'Porto Alegre', 'Goiânia']
    
    estados = ['SP', 'RJ', 'MG', 'BA', 'DF', 'CE', 'PR', 'PE', 'RS', 'GO']
    
    enderecos = [
        'Rua das Flores, 123', 'Av. Paulista, 456', 'Rua do Comércio, 789',
        'Av. Brasil, 321', 'Rua da Paz, 654', 'Av. Central, 987',
        'Rua dos Jardins, 147', 'Av. Principal, 258', 'Rua das Pedras, 369',
        'Av. das Nações, 741'
    ]
    
    cpfs_usados = set()
    emails_usados = set()
    
    for i in range(min(quantidade, len(nomes))):
        nome = nomes[i]
        
        # Gerar CPF único
        cpf = gerar_cpf()
        while cpf in cpfs_usados:
            cpf = gerar_cpf()
        cpfs_usados.add(cpf)
        
        # Gerar email único
        email = gerar_email(nome)
        counter = 1
        base_email = email
        while email in emails_usados:
            email = base_email.replace('@', f'{counter}@')
            counter += 1
        emails_usados.add(email)
        
        telefone = gerar_telefone()
        data_nascimento = f"{random.randint(1970, 2000)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        endereco = random.choice(enderecos)
        cidade = random.choice(cidades)
        estado = random.choice(estados)
        cep = gerar_cep()
        salario = round(random.uniform(2000, 15000), 2)
        cargo = random.choice(cargos)
        departamento = random.choice(departamentos)
        data_contratacao = f"{random.randint(2020, 2024)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        ativo = random.choice([1, 1, 1, 0])  # 75% ativo
        
        cursor.execute('''
            INSERT INTO funcionarios (nome, email, telefone, cpf, data_nascimento,
                                    endereco, cidade, estado, cep, salario, cargo,
                                    departamento, data_contratacao, ativo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, email, telefone, cpf, data_nascimento, endereco, cidade,
              estado, cep, salario, cargo, departamento, data_contratacao, ativo))
    
    conn.commit()
    conn.close()
    print(f"✅ {min(quantidade, len(nomes))} funcionários inseridos!")

def inserir_produtos(quantidade=100):
    """Insere produtos fictícios no banco"""
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    produtos_base = [
        'Smartphone Samsung Galaxy', 'iPhone Apple', 'Notebook Dell', 'Mouse Logitech',
        'Teclado Mecânico', 'Monitor LG', 'Headset Gamer', 'Câmera Canon',
        'Tablet Samsung', 'Impressora HP', 'Roteador TP-Link', 'SSD Kingston',
        'Camiseta Polo', 'Calça Jeans', 'Tênis Nike', 'Jaqueta de Couro',
        'Relógio Casio', 'Óculos Ray-Ban', 'Mochila Adidas', 'Carteira Couro',
        'Mesa de Escritório', 'Cadeira Ergonômica', 'Luminária LED', 'Vaso Decorativo',
        'Tapete Persa', 'Espelho Grande', 'Quadro Moderno', 'Almofada Decorativa',
        'Bicicleta Mountain Bike', 'Patins Inline', 'Bola de Futebol', 'Raquete de Tênis',
        'Halter 5kg', 'Esteira Elétrica', 'Bola de Basquete', 'Luvas de Boxe',
        'Livro Python Programming', 'Romance Best Seller', 'Revista Tecnologia', 'Dicionário Inglês',
        'Enciclopédia Britannica', 'Livro de Receitas', 'Manual de JavaScript', 'Biografia Steve Jobs',
        'Shampoo Pantene', 'Condicionador Loreal', 'Creme Facial Nivea', 'Perfume Natura',
        'Batom Ruby Rose', 'Base Maybelline', 'Máscara para Cílios', 'Esmalte Colorama',
        'Café Especial 500g', 'Chocolate Lindt', 'Biscoito Bauducco', 'Refrigerante Coca-Cola',
        'Água Mineral Crystal', 'Suco Natural Del Valle', 'Cereal Matinal', 'Iogurte Danone'
    ]
    
    categorias = ['Eletrônicos', 'Roupas', 'Casa e Jardim', 'Esportes', 'Livros',
                  'Beleza', 'Alimentação', 'Automóveis', 'Brinquedos', 'Ferramentas']
    
    fornecedores = ['Fornecedor A Ltda', 'B&B Distribuidora', 'Mega Suprimentos',
                    'Central de Produtos', 'Distribuidora Sul', 'Norte Atacado']
    
    codigos_usados = set()
    
    for i in range(min(quantidade, len(produtos_base) * 2)):
        if i < len(produtos_base):
            nome = produtos_base[i]
        else:
            nome = f"{random.choice(produtos_base)} Pro"
            
        categoria = random.choice(categorias)
        custo = round(random.uniform(10, 500), 2)
        preco = round(custo * random.uniform(1.2, 3.0), 2)  # Margem de 20% a 200%
        estoque = random.randint(0, 1000)
        
        # Gerar código de barras único
        codigo_barras = f"{random.randint(1000000000000, 9999999999999)}"
        while codigo_barras in codigos_usados:
            codigo_barras = f"{random.randint(1000000000000, 9999999999999)}"
        codigos_usados.add(codigo_barras)
        
        fornecedor = random.choice(fornecedores)
        data_cadastro = f"{random.randint(2022, 2024)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        ativo = random.choice([1, 1, 1, 0])  # 75% ativo
        
        cursor.execute('''
            INSERT INTO produtos (nome, categoria, preco, custo, estoque,
                                codigo_barras, fornecedor, data_cadastro, ativo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, categoria, preco, custo, estoque, codigo_barras,
              fornecedor, data_cadastro, ativo))
    
    conn.commit()
    conn.close()
    print(f"✅ {min(quantidade, len(produtos_base) * 2)} produtos inseridos!")

def inserir_clientes(quantidade=200):
    """Insere clientes fictícios no banco"""
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    nomes_clientes = [
        'Alice Fernandes', 'Bruno Carvalho', 'Carla Mendes', 'Daniel Rosa', 'Elisa Moura',
        'Felipe Torres', 'Gabriela Dias', 'Hugo Barbosa', 'Isabela Cruz', 'Jorge Pinto',
        'Kelly Ramos', 'Luis Monteiro', 'Monica Vidal', 'Nuno Silveira', 'Olga Machado',
        'Paulo Caldeira', 'Quintino Faria', 'Rita Gonçalves', 'Samuel Braga', 'Tânia Coelho',
        'Ulisses Vargas', 'Vera Nunes', 'Wagner Freire', 'Ximena Correa', 'Yara Bastos',
        'Zeca Tavares', 'Abel Fonseca', 'Bianca Leal', 'César Amaral', 'Débora Campos'
    ]
    
    # Expandir lista de nomes
    prefixos = ['Dr.', 'Dra.', 'Prof.', '']
    sufixos = ['Jr.', 'Filho', 'Neto', '']
    
    nomes_expandidos = []
    for nome in nomes_clientes:
        nomes_expandidos.append(nome)
        nomes_expandidos.append(f"{random.choice(prefixos)} {nome} {random.choice(sufixos)}".strip())
    
    cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Brasília',
               'Fortaleza', 'Curitiba', 'Recife', 'Porto Alegre', 'Goiânia']
    
    estados = ['SP', 'RJ', 'MG', 'BA', 'DF', 'CE', 'PR', 'PE', 'RS', 'GO']
    
    enderecos = [
        'Rua das Flores, 123', 'Av. Paulista, 456', 'Rua do Comércio, 789',
        'Av. Brasil, 321', 'Rua da Paz, 654', 'Av. Central, 987',
        'Rua dos Jardins, 147', 'Av. Principal, 258', 'Rua das Pedras, 369',
        'Av. das Nações, 741', 'Rua XV de Novembro, 852', 'Av. Getúlio Vargas, 963'
    ]
    
    cpfs_usados = set()
    emails_usados = set()
    
    for i in range(quantidade):
        if i < len(nomes_expandidos):
            nome = nomes_expandidos[i]
        else:
            nome = f"{random.choice(nomes_clientes)} {random.randint(1, 999)}"
        
        # Email pode ser None para alguns clientes
        email = None
        if random.random() > 0.1:  # 90% tem email
            email = gerar_email(nome)
            counter = 1
            base_email = email
            while email in emails_usados:
                email = base_email.replace('@', f'{counter}@')
                counter += 1
            emails_usados.add(email)
        
        # Telefone pode ser None para alguns clientes
        telefone = gerar_telefone() if random.random() > 0.05 else None  # 95% tem telefone
        
        # CPF pode ser None para alguns clientes
        cpf = None
        if random.random() > 0.02:  # 98% tem CPF
            cpf = gerar_cpf()
            while cpf in cpfs_usados:
                cpf = gerar_cpf()
            cpfs_usados.add(cpf)
        
        data_nascimento = f"{random.randint(1960, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        endereco = random.choice(enderecos)
        cidade = random.choice(cidades)
        estado = random.choice(estados)
        cep = gerar_cep()
        data_cadastro = f"{random.randint(2021, 2024)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        ativo = random.choice([1, 1, 1, 1, 0])  # 80% ativo
        
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
    print(f"✅ Clientes inseridos!")

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
        
        # Gerar data e hora de venda no último ano
        dias_atras = random.randint(0, 365)
        data_venda = datetime.now() - timedelta(days=dias_atras)
        data_venda = data_venda.strftime('%Y-%m-%d %H:%M:%S')
        
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
