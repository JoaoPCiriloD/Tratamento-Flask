from flask import Flask, render_template, jsonify, request, send_file
import sqlite3
import json
import os
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    """Conecta ao banco de dados SQLite"""
    conn = sqlite3.connect('empresa.db')
    conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
    return conn

def dict_from_row(row):
    """Converte uma linha do SQLite em dicionário"""
    return dict(zip(row.keys(), row))

@app.route('/')
def index():
    """Página inicial - serve o arquivo HTML da pasta raiz"""
    try:
        # Verifica se o arquivo index.html existe na pasta raiz
        if os.path.exists('index.html'):
            return send_file('index.html')
        else:
            # Se não existir, redireciona para a API de estatísticas
            return jsonify({
                "message": "Página inicial não encontrada",
                "endpoints_disponiveis": {
                    "estatisticas": "/api/stats",
                    "funcionarios": "/api/funcionarios", 
                    "produtos": "/api/produtos",
                    "clientes": "/api/clientes",
                    "vendas": "/api/vendas",
                    "export_completo": "/api/export/json"
                }
            })
    except Exception as e:
        return jsonify({"error": f"Erro ao carregar página: {str(e)}"}), 500

@app.route('/api/stats')
def api_stats():
    """Retorna estatísticas em formato JSON"""
    try:
        conn = get_db_connection()
        
        # Estatísticas gerais
        stats = {}
        
        # Contagem de registros
        stats['funcionarios'] = conn.execute('SELECT COUNT(*) FROM funcionarios').fetchone()[0]
        stats['produtos'] = conn.execute('SELECT COUNT(*) FROM produtos').fetchone()[0]
        stats['clientes'] = conn.execute('SELECT COUNT(*) FROM clientes').fetchone()[0]
        stats['vendas'] = conn.execute('SELECT COUNT(*) FROM vendas').fetchone()[0]
        
        # Receita total
        receita = conn.execute('SELECT SUM(total) FROM vendas').fetchone()[0]
        stats['receita_total'] = f"R$ {receita:,.2f}" if receita else "R$ 0,00"
        
        # Top vendedor
        top_vendedor = conn.execute('''
            SELECT f.nome, SUM(v.total) as receita
            FROM vendas v
            JOIN funcionarios f ON v.funcionario_id = f.id
            GROUP BY f.id, f.nome
            ORDER BY receita DESC
            LIMIT 1
        ''').fetchone()
        
        if top_vendedor:
            stats['top_vendedor'] = f"{top_vendedor[0]} - R$ {top_vendedor[1]:,.2f}"
        else:
            stats['top_vendedor'] = "Nenhum"
        
        conn.close()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({"error": f"Erro ao obter estatísticas: {str(e)}"}), 500

@app.route('/api/funcionarios')
def api_funcionarios():
    """API para listar funcionários"""
    try:
        conn = get_db_connection()
        funcionarios = conn.execute('''
            SELECT id, nome, email, departamento, cargo, salario, ativo
            FROM funcionarios
            ORDER BY nome
        ''').fetchall()
        conn.close()
        
        return jsonify([dict_from_row(f) for f in funcionarios])
    except Exception as e:
        return jsonify({"error": f"Erro ao obter funcionários: {str(e)}"}), 500

@app.route('/api/produtos')
def api_produtos():
    """API para listar produtos"""
    try:
        conn = get_db_connection()
        produtos = conn.execute('''
            SELECT id, nome, categoria, preco, estoque, ativo
            FROM produtos
            ORDER BY nome
        ''').fetchall()
        conn.close()
        
        return jsonify([dict_from_row(p) for p in produtos])
    except Exception as e:
        return jsonify({"error": f"Erro ao obter produtos: {str(e)}"}), 500

@app.route('/api/clientes')
def api_clientes():
    """API para listar clientes"""
    try:
        conn = get_db_connection()
        clientes = conn.execute('''
            SELECT id, nome, email, telefone, cidade, ativo
            FROM clientes
            ORDER BY nome
        ''').fetchall()
        conn.close()
        
        return jsonify([dict_from_row(c) for c in clientes])
    except Exception as e:
        return jsonify({"error": f"Erro ao obter clientes: {str(e)}"}), 500

@app.route('/api/vendas')
def api_vendas():
    """API para listar vendas"""
    try:
        limit = request.args.get('limit', 50, type=int)
        
        conn = get_db_connection()
        vendas = conn.execute('''
            SELECT v.id, f.nome as funcionario, p.nome as produto,
                   v.quantidade, v.total, v.data_venda, v.metodo_pagamento
            FROM vendas v
            JOIN funcionarios f ON v.funcionario_id = f.id
            JOIN produtos p ON v.produto_id = p.id
            ORDER BY v.data_venda DESC
            LIMIT ?
        ''', (limit,)).fetchall()
        conn.close()
        
        return jsonify([dict_from_row(v) for v in vendas])
    except Exception as e:
        return jsonify({"error": f"Erro ao obter vendas: {str(e)}"}), 500

@app.route('/api/estatisticas')
def api_estatisticas():
    """API para estatísticas avançadas"""
    try:
        conn = get_db_connection()
        
        # Vendas por departamento
        vendas_dept = conn.execute('''
            SELECT f.departamento, COUNT(v.id) as total_vendas, 
                   ROUND(SUM(v.total), 2) as receita_total
            FROM vendas v
            JOIN funcionarios f ON v.funcionario_id = f.id
            GROUP BY f.departamento
            ORDER BY receita_total DESC
        ''').fetchall()
        
        # Vendas por mês
        vendas_mes = conn.execute('''
            SELECT strftime('%Y-%m', data_venda) as mes,
                   COUNT(*) as total_vendas,
                   ROUND(SUM(total), 2) as receita
            FROM vendas
            GROUP BY strftime('%Y-%m', data_venda)
            ORDER BY mes DESC
            LIMIT 6
        ''').fetchall()
        
        # Top produtos
        top_produtos = conn.execute('''
            SELECT p.nome, SUM(v.quantidade) as quantidade_total,
                   ROUND(SUM(v.total), 2) as receita_total
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id
            GROUP BY p.id, p.nome
            ORDER BY quantidade_total DESC
            LIMIT 5
        ''').fetchall()
        
        conn.close()
        
        return jsonify({
            'vendas_por_departamento': [dict_from_row(r) for r in vendas_dept],
            'vendas_por_mes': [dict_from_row(r) for r in vendas_mes],
            'top_produtos': [dict_from_row(r) for r in top_produtos]
        })
    except Exception as e:
        return jsonify({"error": f"Erro ao obter estatísticas: {str(e)}"}), 500

@app.route('/funcionarios')
def funcionarios():
    """Página de funcionários"""
    try:
        return render_template('funcionarios.html')
    except:
        return jsonify({"message": "Use /api/funcionarios para acessar os dados"}), 200

@app.route('/produtos')
def produtos():
    """Página de produtos"""
    try:
        return render_template('produtos.html')
    except:
        return jsonify({"message": "Use /api/produtos para acessar os dados"}), 200

@app.route('/clientes')
def clientes():
    """Página de clientes"""
    try:
        return render_template('clientes.html')
    except:
        return jsonify({"message": "Use /api/clientes para acessar os dados"}), 200

@app.route('/vendas')
def vendas():
    """Página de vendas"""
    try:
        return render_template('vendas.html')
    except:
        return jsonify({"message": "Use /api/vendas para acessar os dados"}), 200

@app.route('/estatisticas')
def estatisticas():
    """Página de estatísticas"""
    try:
        return render_template('estatisticas.html')
    except:
        return jsonify({"message": "Use /api/estatisticas para acessar os dados"}), 200

@app.route('/api/export/json')
def export_json():
    """Exporta todos os dados em JSON"""
    try:
        conn = get_db_connection()
        
        # Exportar todas as tabelas
        data = {}
        
        # Funcionários
        funcionarios = conn.execute('SELECT * FROM funcionarios').fetchall()
        data['funcionarios'] = [dict_from_row(f) for f in funcionarios]
        
        # Produtos
        produtos = conn.execute('SELECT * FROM produtos').fetchall()
        data['produtos'] = [dict_from_row(p) for p in produtos]
        
        # Clientes
        clientes = conn.execute('SELECT * FROM clientes').fetchall()
        data['clientes'] = [dict_from_row(c) for c in clientes]
        
        # Vendas
        vendas = conn.execute('SELECT * FROM vendas').fetchall()
        data['vendas'] = [dict_from_row(v) for v in vendas]
        
        # Metadata
        data['metadata'] = {
            'exported_at': datetime.now().isoformat(),
            'total_records': {
                'funcionarios': len(data['funcionarios']),
                'produtos': len(data['produtos']),
                'clientes': len(data['clientes']),
                'vendas': len(data['vendas'])
            }
        }
        
        conn.close()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Erro ao exportar dados: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor web...")
    print("📱 Acesse: http://localhost:5000")
    print("📊 API JSON: http://localhost:5000/api/export/json")
    app.run(debug=True, host='0.0.0.0', port=5000)
