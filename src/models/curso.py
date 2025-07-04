from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Importar db do app principal
from src.extensions import db


class Curso(db.Model):
    """Modelo que representa um curso no sistema"""
    
    # Nome da tabela no banco
    __tablename__ = 'cursos'
    
    # Colunas da tabela
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    area = db.Column(db.String(100), nullable=True)
    metodologia = db.Column(db.String(50), nullable=False)
    faixa = db.Column(db.String(50), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    def __init__(self, nome, area, metodologia, faixa):
        """Construtor da classe"""
        self.nome = nome
        self.area = area
        self.metodologia = metodologia
        self.faixa = faixa
    
    def to_dict(self):
        """Converte o objeto para dicionário (útil para JSON)"""
        return {
            'id': self.id,
            'nome': self.nome,
            'area': self.area,
            'metodologia': self.metodologia,
            'faixa': self.faixa,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'ativo': self.ativo
        }
    
    def __repr__(self):
        """Representação string do objeto"""
        return f'<Curso {self.nome}>'