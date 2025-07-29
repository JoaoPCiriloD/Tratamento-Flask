# 🏢 Sistema de Banco de Dados com Dados Fictícios

Este projeto cria um banco de dados SQLite completo com dados fictícios de uma empresa, incluindo funcionários, produtos, clientes e vendas.

## 📁 Arquivos do Projeto

- `criar_banco_simples.py` - Script principal para criar o banco e inserir dados
- `criar_banco.py` - Versão com a biblioteca Faker (requer instalação)
- `visualizar_banco.py` - Interface para visualizar e explorar os dados
- `requirements.txt` - Dependências do projeto
- `empresa.db` - Arquivo do banco de dados (criado após execução)

## 🚀 Como Usar

### 1. Criar o Banco de Dados

Execute o script principal:

```bash
python criar_banco_simples.py
```

Este script irá:

- Criar o arquivo `empresa.db`
- Criar 4 tabelas: funcionarios, produtos, clientes, vendas
- Inserir dados fictícios nas tabelas
- Mostrar estatísticas dos dados inseridos

### 2. Visualizar os Dados

Execute o visualizador:

```bash
python visualizar_banco.py
```

O visualizador oferece várias opções:

- Ver todos os registros de cada tabela
- Buscar funcionários por nome
- Ver estatísticas gerais
- Analisar vendas por período
- Identificar produtos com estoque baixo

## 📊 Estrutura do Banco de Dados

### Tabela: funcionarios

- id (chave primária)
- nome, email, telefone, cpf
- data_nascimento, endereco, cidade, estado, cep
- salario, cargo, departamento
- data_contratacao, ativo

### Tabela: produtos

- id (chave primária)
- nome, categoria, preco, custo
- estoque, codigo_barras, fornecedor
- data_cadastro, ativo

### Tabela: clientes

- id (chave primária)
- nome, email, telefone, cpf
- data_nascimento, endereco, cidade, estado, cep
- data_cadastro, ativo

### Tabela: vendas

- id (chave primária)
- funcionario_id, produto_id (chaves estrangeiras)
- quantidade, preco_unitario, desconto, total
- data_venda, metodo_pagamento

## 📈 Dados Gerados

O banco será populado com:

- 50 funcionários fictícios
- 100 produtos de diversas categorias
- 200 clientes
- 500 vendas distribuídas ao longo do último ano

## 🛠️ Ferramentas Recomendadas

Para visualizar o banco de forma mais avançada:

- **DB Browser for SQLite** (gratuito)
- **SQLiteStudio** (gratuito)
- **DBeaver** (gratuito)

## 💡 Exemplos de Consultas SQL

```sql
-- Top 5 funcionários que mais venderam
SELECT f.nome, COUNT(v.id) as total_vendas, SUM(v.total) as receita
FROM vendas v
JOIN funcionarios f ON v.funcionario_id = f.id
GROUP BY f.id, f.nome
ORDER BY receita DESC
LIMIT 5;

-- Produtos mais vendidos por categoria
SELECT p.categoria, p.nome, SUM(v.quantidade) as total_vendido
FROM vendas v
JOIN produtos p ON v.produto_id = p.id
GROUP BY p.categoria, p.nome
ORDER BY p.categoria, total_vendido DESC;

-- Vendas por mês
SELECT strftime('%Y-%m', data_venda) as mes,
       COUNT(*) as total_vendas,
       SUM(total) as receita_mensal
FROM vendas
GROUP BY strftime('%Y-%m', data_venda)
ORDER BY mes;
```

## 🔧 Personalização

Você pode modificar os scripts para:

- Alterar a quantidade de registros gerados
- Adicionar novos campos às tabelas
- Incluir novas categorias de produtos
- Criar relacionamentos mais complexos
- Adicionar mais tabelas (ex: fornecedores, pedidos)

## ⚠️ Importante

- Os dados são completamente fictícios
- CPFs gerados seguem o algoritmo de validação brasileiro
- Emails e telefones são fictícios
- Use apenas para fins de desenvolvimento e testes
