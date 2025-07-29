# 🌐 Sistema Web - Banco de Dados Empresa

Sistema web completo para visualizar e acessar o banco de dados da empresa através de uma interface web moderna e APIs JSON.

## 🚀 Como Executar o Sistema Web

### 1. Instalar Dependências

```bash
pip install Flask
```

### 2. Executar o Servidor

```bash
python app.py
```

### 3. Acessar o Sistema

- **Interface Web**: http://localhost:5000
- **API JSON Completa**: http://localhost:5000/api/export/json
- **API Funcionários**: http://localhost:5000/api/funcionarios
- **API Produtos**: http://localhost:5000/api/produtos
- **API Clientes**: http://localhost:5000/api/clientes
- **API Vendas**: http://localhost:5000/api/vendas
- **API Estatísticas**: http://localhost:5000/api/estatisticas

## 📱 Recursos da Interface Web

### 🏠 Dashboard Principal

- Estatísticas gerais do banco de dados
- Cartões com totais de registros
- Informações de receita e top vendedor
- Links para exportação em JSON

### 👥 Funcionários

- Lista completa de funcionários
- Filtros e busca avançada
- Indicadores de status (ativo/inativo)
- Destaque para salários altos

### 📦 Produtos

- Catálogo completo de produtos
- Indicadores de estoque (alto/médio/baixo/zerado)
- Organização por categoria
- Status de ativo/inativo

### 👤 Clientes

- Base completa de clientes
- Informações de contato
- Localização por cidade
- Status de ativo/inativo

### 💰 Vendas

- Histórico de vendas em tempo real
- Informações de funcionário e produto
- Métodos de pagamento categorizados
- Valores destacados por faixa

### 📊 Estatísticas e Relatórios

- Gráfico de vendas por departamento
- Evolução de vendas por mês
- Top 5 produtos mais vendidos
- Resumo executivo com indicadores chave

## 🔌 APIs JSON Disponíveis

### Endpoints Principais

- `GET /api/funcionarios` - Lista todos os funcionários
- `GET /api/produtos` - Lista todos os produtos
- `GET /api/clientes` - Lista todos os clientes
- `GET /api/vendas?limit=N` - Lista vendas (limite opcional)
- `GET /api/estatisticas` - Estatísticas avançadas
- `GET /api/export/json` - Exportação completa em JSON

### Exemplo de Uso das APIs

```javascript
// Buscar todos os funcionários
fetch("/api/funcionarios")
  .then((response) => response.json())
  .then((data) => console.log(data));

// Buscar estatísticas
fetch("/api/estatisticas")
  .then((response) => response.json())
  .then((stats) => {
    console.log("Vendas por departamento:", stats.vendas_por_departamento);
    console.log("Vendas por mês:", stats.vendas_por_mes);
    console.log("Top produtos:", stats.top_produtos);
  });
```

## 🎨 Tecnologias Utilizadas

### Backend

- **Flask**: Framework web Python
- **SQLite**: Banco de dados
- **Python**: Linguagem principal

### Frontend

- **Bootstrap 5**: Framework CSS responsivo
- **Font Awesome**: Ícones
- **DataTables**: Tabelas interativas
- **Chart.js**: Gráficos e visualizações
- **jQuery**: Manipulação DOM e AJAX

## 📊 Funcionalidades de Dados

### Transformação Automática para JSON

- Todos os dados são automaticamente convertidos para JSON
- APIs RESTful para cada tabela
- Metadados incluídos nas exportações
- Timestamps de exportação

### Recursos de Visualização

- Tabelas ordenáveis e filtráveis
- Gráficos interativos
- Indicadores visuais de status
- Responsividade para mobile

### Exportação de Dados

- JSON completo de todas as tabelas
- APIs individuais por entidade
- Formato padronizado para integração
- Metadados e timestamps incluídos

## 🔧 Personalização

### Modificar Porta do Servidor

Edite o arquivo `app.py`, linha final:

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Altere a porta aqui
```

### Adicionar Novos Endpoints

```python
@app.route('/api/nova_funcionalidade')
def nova_funcionalidade():
    # Sua lógica aqui
    return jsonify(dados)
```

### Customizar Interface

- Templates estão em `/templates/`
- Use Bootstrap para manter consistência
- Ícones Font Awesome disponíveis

## 🌐 Deploy para Produção

### Usando Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Configurações Recomendadas

- Use HTTPS em produção
- Configure proxy reverso (Nginx)
- Implemente autenticação se necessário
- Monitore logs e performance

## 📱 Acesso Mobile

O sistema é totalmente responsivo e funciona perfeitamente em:

- Smartphones
- Tablets
- Desktops
- Diferentes navegadores

## 🔒 Segurança

- Dados locais (SQLite)
- Sem exposição externa por padrão
- APIs somente leitura
- Validação de dados no backend
