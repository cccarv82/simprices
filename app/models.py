from app import db

# Classe Base
class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True)
    nM = db.Column(db.String(50))
    valor = db.Column(db.Float)
    valor_por_nM = db.Column(db.Float)
    data_consulta = db.Column(db.DateTime)
    link_compra = db.Column(db.String(200))
    categoria = db.Column(db.String(50))
    status_preco = db.Column(db.String(50))

    def __init__(self, nome, nM, valor, valor_por_nM, data_consulta, link_compra, categoria, status_preco=None):
        self.nome = nome
        self.nM = nM
        self.valor = valor
        self.valor_por_nM = valor_por_nM
        self.data_consulta = data_consulta
        self.link_compra = link_compra
        self.categoria = categoria
        self.status_preco = status_preco