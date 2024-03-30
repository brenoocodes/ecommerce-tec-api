import sys
from pathlib import Path
file = Path(__file__).resolve()
parent = file.parent.parent.parent
sys.path.append(str(parent))

from sqlalchemy import Boolean, Column, Integer, Float, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, backref
from src.configure import Base, engine
from datetime import datetime, timezone
import random
import string


def id_generator():
    caracteres = string.ascii_letters + string.digits
    tamanho_combinacao = 36
    return ''.join(random.choices(caracteres, k=tamanho_combinacao))

class Funcionarios(Base):
    __tablename__ = 'funcionarios'
    matricula = Column(String(36), primary_key=True, nullable=False)
    nome = Column(String(200), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)
    administrador = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, nullable=False)
    data_atualizacao = Column(DateTime, nullable=False)

    entradas = relationship('Entradas', backref='funcionario', lazy=True, foreign_keys='Entradas.funcionario_responsavel_matricula')

    def __init__(self, nome, email, senha, administrador=False, ativo=True, data_atualizacao= datetime.now(timezone.utc)):
        self.matricula = id_generator()
        self.nome = nome
        self.email = email
        self.senha = senha
        self.administrador = administrador
        self.ativo = ativo
        self.data_criacao = datetime.now(timezone.utc)
        self.data_atualizacao = data_atualizacao

class Clientes(Base):
    __tablename__ = 'clientes'
    id = Column(String(36), primary_key=True, nullable=False)
    cpf = Column(String(20), unique=True, nullable=False)
    data_de_nascimento = Column(String(20))
    nome = Column(String(120), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)
    email_confirmado = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, nullable=False)
    data_atualizacao = Column(DateTime, nullable=False)

    email_token = relationship('EmailToken', backref='cliente', lazy=True, foreign_keys='EmailToken.cliente_id')
    enderecos = relationship('Enderecos', backref='cliente', lazy=True, foreign_keys='Enderecos.cliente_id')
    compras = relationship('Vendas', backref='cliente', lazy=True, foreign_keys='Vendas.cliente_id')

    def __init__(self, cpf, data_de_nascimento, nome, email, senha, data_atualizacao= datetime.now(timezone.utc)):
        self.id = id_generator()
        self.cpf = cpf
        self.data_de_nascimento = data_de_nascimento
        self.nome = nome
        self.email = email
        self.senha = senha
        self.data_criacao = datetime.now(timezone.utc)
        self.data_atualizacao = data_atualizacao

class Enderecos(Base):
    __tablename__ = 'enderecos'
    id = Column(String(36), primary_key=True, nullable=False)
    cliente_id = Column(String(36), ForeignKey('clientes.id'), nullable=False)
    cep = Column(String(10), nullable=False)
    cidade = Column(String(200), nullable=False)
    estado = Column(String(100), nullable=False)
    logradouro = Column(String(250), nullable=False)
    bairro = Column(String(250), nullable=False)
    numero = Column(String(20), nullable=True)
    referencia = Column(String(150), nullable=True)
    observacao = Column(String(200), nullable=True)
    data_criacao = Column(DateTime, nullable=False)
    data_atualizacao = Column(DateTime, nullable=False)

    vendas = relationship('Vendas', backref='endereco', lazy=True, foreign_keys='Vendas.endereco_id')

    def __init__(self, cliente_id, cep, cidade, estado, logradouro, bairro, numero=' ', referencia=' ', observacao=' ', data_atualizacao= datetime.now(timezone.utc)):
        self.id = id_generator()
        self.cliente_id = cliente_id
        self.cep = cep
        self.cidade = cidade
        self.estado = estado
        self.logradouro = logradouro
        self.bairro = bairro
        self.numero = numero
        self.referencia = referencia
        self.observacao = observacao
        self.data_criacao = datetime.now(timezone.utc)
        self.data_atualizacao = data_atualizacao

class Categorias(Base):
    __tablename__ = 'categorias'
    id = Column(String(36), primary_key=True, nullable=False)
    nome = Column(String(50), unique=True, nullable=False)
    data_criacao = Column(DateTime, nullable=False)
    data_atualizacao = Column(DateTime, nullable=False)
    produtos = relationship('Produtos', backref='categoria', lazy=True, foreign_keys='Produtos.categoria_id')

    def __init__(self, nome , data_atualizacao= datetime.now(timezone.utc)):
        self.id = id_generator()
        self.nome = nome
        self.data_criacao = datetime.now(timezone.utc)
        self.data_atualizacao = data_atualizacao

class Fornecedores(Base):
    __tablename__ = 'fornecedores'
    id = Column(String(36), primary_key=True, nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    telefone = Column(String(14), nullable=False)
    data_criacao = Column(DateTime, nullable=False)
    data_atualizacao = Column(DateTime, nullable=False)

    entradas = relationship('Entradas', backref='fornecedor', lazy=True, foreign_keys='Entradas.fornecedor_id')

    def __init__(self, cnpj, razao_social, nome_fantasia, email, telefone, data_atualizacao= datetime.now(timezone.utc)):
        self.id = id_generator()
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.nome_fantasia = nome_fantasia
        self.email = email
        self.telefone = telefone
        self.data_criacao = datetime.now(timezone.utc)
        self.data_atualizacao = data_atualizacao

class Produtos(Base):
    __tablename__ = 'produtos'
    id = Column(String(36), primary_key=True, nullable=False)
    categoria_id = Column(String(36), ForeignKey('categorias.id'), nullable=False)
    nome = Column(String(120), nullable=False)
    nome_estoque = Column(String(120), nullable=False)
    descricao = Column(JSON, nullable=True, default={})
    data_criacao = Column(DateTime, nullable=False)
    data_atualizacao = Column(DateTime, nullable=False)

    itens_estoque = relationship('ItensEstoque', backref='produto', lazy=True, foreign_keys='ItensEstoque.produto_id')
    entradas = relationship('Entradas', backref='produto', lazy=True, primaryjoin='Produtos.id == Entradas.produto_id', foreign_keys='Entradas.produto_id')

    def __init__(self, categoria_id, nome, nome_estoque, descricao={''}, data_atualizacao= datetime.now(timezone.utc)):
        self.id = id_generator()
        self.categoria_id = categoria_id
        self.nome = nome
        self.nome_estoque = nome_estoque
        self.descricao = descricao
        self.data_criacao = datetime.now(timezone.utc)
        self.data_atualizacao = data_atualizacao

class ItensEstoque(Base):
    __tablename__ = 'itensestoque'
    id = Column(String(36), primary_key=True, nullable=False)
    produto_id = Column(String(36), ForeignKey('produtos.id'), nullable=False) 
    preco = Column(Float, default=0, nullable=False)
    cor = Column(String(50), nullable=False)
    quantidade = Column(Integer, default=0)
    imagens = Column(JSON, nullable=True, default={})
    itenscarrinho = relationship('ItensCarrinhos', backref='itemestoque', lazy=True, foreign_keys='ItensCarrinhos.itemestoque_id')
    itemvendas = relationship('ItensVendas', backref='itemestoque', lazy=True, foreign_keys='ItensVendas.itemestoque_id')

    def __init__(self, produto_id, preco, cor, quantidade, imagens={''}, data_atualizacao= datetime.now(timezone.utc)):
        self.id = id_generator()
        self.produto_id = produto_id
        self.preco = preco
        self.cor = cor
        self.quantidade = quantidade
        self.imagens = imagens
        self.data_criacao = datetime.now(timezone.utc)
        self.data_atualizacao = data_atualizacao

class ProdutosFornecedores(Base):
    __tablename__ = 'produtos_fornecedores'
    produto_id = Column(String(36), ForeignKey('produtos.id'), primary_key=True)
    fornecedor_id = Column(String(36), ForeignKey('fornecedores.id'), primary_key=True)

    def __init__(self, produto_id, fornecedor_id):
        self.produto_id = produto_id
        self.fornecedor_id = fornecedor_id

class Entradas(Base):
    __tablename__ = 'entradaestoque'
    id = Column(String(36), primary_key=True, nullable=False)
    nota = Column(String(50), nullable=False)
    produto_id = Column(String(36), ForeignKey('itensestoque.id'), nullable=False)
    fornecedor_id = Column(String(36), ForeignKey('fornecedores.id'), nullable=False)
    data_criacao = Column(DateTime, nullable=False)
    data_atualizacao = Column(DateTime, nullable=False)
    quantidade = Column(Integer, nullable=False)
    funcionario_responsavel_matricula = Column(String(36), ForeignKey('funcionarios.matricula'), nullable=False)

    def __init__(self, nota, produto_id, fornecedor_id, quantidade, funcionario_responsavel_matricula, data_atualizacao= datetime.now(timezone.utc)):
        self.id = id_generator()
        self.nota = nota
        self.produto_id = produto_id
        self.fornecedor_id = fornecedor_id
        self.quantidade = quantidade
        self.funcionario_responsavel_matricula = funcionario_responsavel_matricula
        self.data_criacao = datetime.now(timezone.utc)
        self.data_atualizacao = data_atualizacao

class Carrinhos(Base):
    __tablename__ = 'carrinhos'
    id = Column(String(36), primary_key=True, nullable=False)
    nome = Column(String(150), nullable=False)
    descricao = Column(String(250), nullable=True)
    quantidade_itens = Column(Integer, nullable=True)
    valor_total = Column(Float, nullable=True)
    data_criacao = Column(DateTime, nullable=False)
    data_atualizacao = Column(DateTime, nullable=False)
    itens = relationship('ItensCarrinhos', backref='carrinho', lazy=True, foreign_keys='ItensCarrinhos.carrinho_id')
    vendas = relationship('Vendas', backref='carrinho', lazy=True, foreign_keys='Vendas.carrinho_id')

    def __init__(self, nome, descricao=' ', data_atualizacao= datetime.now(timezone.utc)):
        self.id = id_generator()
        self.nome = nome
        self.descricao = descricao
        self.data_criacao = datetime.now(timezone.utc)
        self.data_atualizacao = data_atualizacao

class ItensCarrinhos(Base):
    __tablename__ = 'itenscarrinhos'
    id = Column(String(36), primary_key=True, nullable=False)
    carrinho_id = Column(String(36), ForeignKey('carrinhos.id'), nullable=False)
    itemestoque_id = Column(String(36), ForeignKey('itensestoque.id'), nullable=False)
    valor_unitario = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)

    def __init__(self, carrinho_id, itemestoque_id, valor_unitario, quantidade):
        self.id = id_generator()
        self.carrinho_id = carrinho_id
        self.itemestoque_id = itemestoque_id
        self.valor_unitario = valor_unitario
        self.quantidade = quantidade

class Vendas(Base):
    __tablename__ = 'vendas'
    id = Column(String(36), primary_key=True, nullable=False)
    cliente_id = Column(String(36), ForeignKey('clientes.id'), nullable=False) 
    endereco_id = Column(String(36), ForeignKey('enderecos.id'), nullable=True)
    carrinho_id = Column(String(36), ForeignKey('carrinhos.id'), nullable=True)
    status = Column(String(50), nullable=False)
    link_pagamento = Column(String(200), nullable=True)
    pagamento_confirmado = Column(Boolean, default=False)
    data_criacao = Column(DateTime, nullable=False)
    data_atualizacao = Column(DateTime, nullable=False)
    itensvendas = relationship('ItensVendas', backref='venda', lazy=True, foreign_keys='ItensVendas.venda_id')

    def __init__(self, cliente_id, status, endereco_id=' ', carrinho_id=' ', link_pagamento=' ', data_atualizacao= datetime.now(timezone.utc)):
        self.id = id_generator()
        self.cliente_id = cliente_id
        self.endereco_id = endereco_id
        self.carrinho_id = carrinho_id
        self.status = status
        self.link_pagamento = link_pagamento
        self.data_criacao = datetime.now(timezone.utc)
        self.data_atualizacao = data_atualizacao

class ItensVendas(Base):
    __tablename__ = 'itensvendas'
    id = Column(String(36), primary_key=True, nullable=False)
    venda_id = Column(String(36), ForeignKey('vendas.id'), nullable=False)
    itemestoque_id = Column(String(36), ForeignKey('itensestoque.id'), nullable=False)
    valor_unitario = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)

    def __init__(self, venda_id, itemestoque_id, valor_unitario, quantidade):
        self.id = id_generator()
        self.venda_id = venda_id
        self.itemestoque_id = itemestoque_id
        self.valor_unitario = valor_unitario
        self.quantidade = quantidade

class EmailToken(Base):
    __tablename__ = 'emailtoken'
    id = Column(String(36), primary_key=True, nullable=False)
    cliente_id = Column(String(36), ForeignKey('clientes.id'), nullable=False)
    email = Column(String(50), nullable=False)
    token = Column(String(200), nullable=False)
    finalidade = Column(String(30), default='login')
    data_criacao = Column(DateTime, nullable=False)

    def __init__(self, cliente_id, email, token, finalidade='login', data_criacao=datetime.now(timezone.utc)):
        self.id = id_generator()
        self.cliente_id = cliente_id
        self.email = email
        self.token = token
        self.finalidade = finalidade
        self.data_criacao = data_criacao




# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)