from src.curso import Curso
from src.extensions import db


def criar_cursos_iniciais():
    """Cria cursos iniciais se o banco estiver vazio"""
    
    # Verificar se já existem cursos
    if Curso.query.count() > 0:
        print("Banco já possui cursos, pulando criação inicial")
        return
    
    # Lista de cursos iniciais
    cursos_iniciais = [
        {
            'nome': 'Direito Tributário (A).TEST',
            'area': 'Direito',
            'metodologia': 'CV100',
            'faixa': 'FAIXA 2'
        },
    ]
    
    # Criar e salvar cada curso
    for curso_data in cursos_iniciais:
        curso = Curso(
            nome=curso_data['nome'],
            area=curso_data['area'],
            metodologia=curso_data['metodologia'],
            faixa=curso_data['faixa']
        )
        db.session.add(curso)
    
    # Salvar no banco
    db.session.commit()
    print(f"Criados {len(cursos_iniciais)} cursos iniciais")

if __name__ == '__main__':
    from app import app
    with app.app_context():
        criar_cursos_iniciais()