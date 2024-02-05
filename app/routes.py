from flask import request, jsonify
from app import app, db, ma
from app.models import Base
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from .scraping import scrape_prsim
from marshmallow import post_dump

# Schema Base
class BaseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nome', 'nM', 'valor', 'valor_por_nM', 'data_consulta', 'link_compra', 'status_preco', 'categoria', 'status')

    @post_dump
    def reorder(self, data, **kwargs):
        order = ["id", "data_consulta", "link_compra", "nome", "nM", "categoria", "valor", "valor_por_nM", "status_preco", "status"]
        return {k: data[k] for k in order}

base_schema = BaseSchema()
bases_schema = BaseSchema(many=True)

# Endpoint para criar um novo produto
@app.route('/base', methods=['POST'])
def add_base():
    link_compra = request.json['link_compra']
    categoria = request.json['categoria']

    # Faz uma solicitação GET para a página do produto
    response = requests.get(link_compra)

    # Analisa a página da web com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Determina qual função de scraping usar com base no URL do produto
    if 'loja.prsim.com.br' in link_compra:
        nome, nM, valor = scrape_prsim(soup)
    else:
        return jsonify({'error': 'Site não suportado'}), 400

    # Buscar o produto existente
    produto_existente = Base.query.filter_by(link_compra=link_compra).first()

    valor_por_nM = valor / float(nM)
    data_consulta = datetime.now()

    if produto_existente:
        # Atualizar o produto existente
        produto_existente.valor = valor
        produto_existente.data_consulta = data_consulta
        produto_existente.valor_por_nM = valor_por_nM
        produto_existente.categoria = categoria
        produto_existente.status = 'ativo'

        # Calcular o status_preco
        if valor > produto_existente.valor:
            produto_existente.status_preco = 'subiu'
        elif valor < produto_existente.valor:
            produto_existente.status_preco = 'desceu'
        else:
            produto_existente.status_preco = 'manteve'
    else:
        # Inserir um novo produto
        novo_base = Base(nome, nM, valor, valor_por_nM, data_consulta, link_compra, categoria, status='ativo')
        db.session.add(novo_base)

    # Commit das alterações
    db.session.commit()

    produto_final = produto_existente if produto_existente else novo_base
    print(produto_final.categoria)  # Imprime a categoria do produto final

    return base_schema.jsonify(produto_final)

# Endpoint para atualizar todos os produtos
@app.route('/update', methods=['POST'])
def update_products():
    # Get all products from the database
    products = Base.query.all()

    # Loop through each product
    for product in products:
        # Faz uma solicitação GET para a página do produto
        response = requests.get(product.link_compra)

        # Analisa a página da web com BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Determina qual função de scraping usar com base no URL do produto
        if 'loja.prsim.com.br' in product.link_compra:
            nome, nM, valor = scrape_prsim(soup)
        else:
            continue  # Skip this product if the site is not supported

        # Update the product's information
        product.nome = nome
        product.nM = nM
        product.valor = valor
        product.valor_por_nM = valor / float(nM)
        product.data_consulta = datetime.now()

        # Calcular o status_preco
        if valor > product.valor:
            product.status_preco = 'subiu'
        elif valor < product.valor:
            product.status_preco = 'desceu'
        else:
            product.status_preco = 'manteve'

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': 'Products updated successfully'}), 200

# Endpoint para listar todos os produtos
@app.route('/bases', methods=['GET'])
def get_bases():
    all_bases = Base.query.all()
    result = bases_schema.dump(all_bases)
    return jsonify(result)