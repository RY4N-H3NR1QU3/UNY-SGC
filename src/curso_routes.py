from flask import Blueprint, request, jsonify, current_app
from src.curso import Curso, db
import os


# Criar blueprint para organizar as rotas
curso_bp = Blueprint('cursos', __name__)

@curso_bp.route('/cursos', methods=['GET'])
def listar_cursos():
    """Lista todos os cursos com filtros opcionais"""
    try:
        # Pegar parâmetros de filtro da URL
        area = request.args.get('area')
        metodologia = request.args.get('metodologia')
        faixa = request.args.get('faixa')
        busca = request.args.get('busca')
        tipo_busca = request.args.get('tipo_busca', 'curso')
        
        # Começar com todos os cursos ativos
        query = Curso.query.filter_by(ativo=True)
        
        # Aplicar filtros se fornecidos
        if area:
            query = query.filter(Curso.area == area)
        
        if metodologia:
            query = query.filter(Curso.metodologia == metodologia)
            
        if faixa:
            query = query.filter(Curso.faixa == faixa)
        
        # Aplicar busca por texto
        if busca:
            busca = f"%{busca}%"  # Adicionar wildcards para LIKE
            
            if tipo_busca == 'curso':
                query = query.filter(Curso.nome.like(busca))
            elif tipo_busca == 'area':
                query = query.filter(Curso.area.like(busca))
            elif tipo_busca == 'metodologia':
                query = query.filter(Curso.metodologia.like(busca))
            elif tipo_busca == 'faixa':
                query = query.filter(Curso.faixa.like(busca))
        
        # Executar query e converter para lista de dicionários
        cursos = query.all()
        cursos_dict = [curso.to_dict() for curso in cursos]
        
        return jsonify({
            'success': True,
            'cursos': cursos_dict,
            'total': len(cursos_dict)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500





@curso_bp.route('/cursos', methods=['POST'])
def criar_curso():
    """Cria um novo curso"""
    try:
        # Pegar dados do JSON enviado pelo frontend
        data = request.get_json()
        
        # Validar campos obrigatórios
        if not data.get('nome'):
            return jsonify({
                'success': False,
                'error': 'Nome do curso é obrigatório'
            }), 400
            
        if not data.get('metodologia'):
            return jsonify({
                'success': False,
                'error': 'Metodologia é obrigatória'
            }), 400
            
        if not data.get('faixa'):
            return jsonify({
                'success': False,
                'error': 'Faixa é obrigatória'
            }), 400
        
        # Criar novo curso
        novo_curso = Curso(
            nome=data['nome'],
            area=data.get('area', ''),  # Área pode ser vazia
            metodologia=data['metodologia'],
            faixa=data['faixa']
        )
        
        # Salvar no banco
        db.session.add(novo_curso)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'curso': novo_curso.to_dict(),
            'message': 'Curso criado com sucesso'
        }), 201
        
    except Exception as e:
        db.session.rollback()  # Desfazer mudanças em caso de erro
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500





@curso_bp.route('/cursos/<int:curso_id>', methods=['PUT'])
def atualizar_curso(curso_id):
    """Atualiza um curso existente"""
    try:
        # Buscar curso no banco
        curso = Curso.query.get(curso_id)
        if not curso:
            return jsonify({
                'success': False,
                'error': 'Curso não encontrado'
            }), 404
        
        # Pegar dados do JSON
        data = request.get_json()
        
        # Atualizar campos se fornecidos
        if 'nome' in data:
            curso.nome = data['nome']
        if 'area' in data:
            curso.area = data['area']
        if 'metodologia' in data:
            curso.metodologia = data['metodologia']
        if 'faixa' in data:
            curso.faixa = data['faixa']
        
        # Salvar mudanças
        db.session.commit()
        
        return jsonify({
            'success': True,
            'curso': curso.to_dict(),
            'message': 'Curso atualizado com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500





@curso_bp.route('/cursos/<int:curso_id>', methods=['DELETE'])
def excluir_curso(curso_id):
    """Exclui um curso do banco de dados permanentemente"""
    try:
        curso = Curso.query.get(curso_id)
        if not curso:
            return jsonify({
                'success': False,
                'error': 'Curso não encontrado'
            }), 404

        db.session.delete(curso)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Curso removido permanentemente'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500






@curso_bp.route('/cursos/opcoes', methods=['GET'])
def obter_opcoes():
    """Retorna opções disponíveis para filtros"""
    try:
        # Buscar valores únicos para cada campo
        areas = db.session.query(Curso.area).filter(
            Curso.ativo == True,
            Curso.area.isnot(None),
            Curso.area != ''
        ).distinct().all()
        
        metodologias = db.session.query(Curso.metodologia).filter(
            Curso.ativo == True
        ).distinct().all()
        
        faixas = db.session.query(Curso.faixa).filter(
            Curso.ativo == True
        ).distinct().all()
        
        return jsonify({
            'success': True,
            'opcoes': {
                'areas': [area[0] for area in areas],
                'metodologias': [met[0] for met in metodologias],
                'faixas': [faixa[0] for faixa in faixas]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    





from werkzeug.utils import secure_filename
import openpyxl
from flask import current_app

# Adicionar ao final do arquivo curso_routes.py

@curso_bp.route('/cursos/upload', methods=['POST'])
def upload_planilha():
    """Faz upload de planilha Excel com cursos"""
    try:
        # Verificar se arquivo foi enviado
        if 'arquivo' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo foi enviado'
            }), 400
        
        arquivo = request.files['arquivo']
        
        # Verificar se arquivo foi selecionado
        if arquivo.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo foi selecionado'
            }), 400
        
        # Verificar extensão do arquivo
        extensoes_permitidas = {'.xlsx', '.xls'}
        nome_arquivo = secure_filename(arquivo.filename)
        extensao = os.path.splitext(nome_arquivo)[1].lower()
        
        if extensao not in extensoes_permitidas:
            return jsonify({
                'success': False,
                'error': 'Apenas arquivos Excel (.xlsx, .xls) são permitidos'
            }), 400
        
        # Salvar arquivo temporariamente
        caminho_arquivo = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_arquivo)
        arquivo.save(caminho_arquivo)
        
        # Processar planilha
        resultado = processar_planilha_excel(caminho_arquivo)
        
        # Remover arquivo temporário
        os.remove(caminho_arquivo)
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao processar planilha: {str(e)}'
        }), 500


def processar_planilha_excel(caminho_arquivo):
    """Processa planilha Excel e adiciona cursos ao banco"""
    try:
        # Abrir planilha
        workbook = openpyxl.load_workbook(caminho_arquivo)
        sheet = workbook.active
        
        cursos_adicionados = []
        erros = []
        linha_atual = 1
        
        # Verificar se a primeira linha contém cabeçalhos
        primeira_linha = [cell.value for cell in sheet[1]]
        tem_cabecalho = any(str(cell).lower() in ['nome', 'curso', 'área', 'metodologia', 'faixa'] 
                           for cell in primeira_linha if cell)
        
        # Definir linha inicial (pular cabeçalho se existir)
        linha_inicial = 2 if tem_cabecalho else 1
        
        # Processar cada linha
        for linha in sheet.iter_rows(min_row=linha_inicial, values_only=True):
            linha_atual += 1
            
            # Pular linhas vazias
            if not any(linha):
                continue
            
            try:
                # Extrair dados da linha (assumindo ordem: Nome, Área, Metodologia, Faixa)
                nome = str(linha[0]).strip() if linha[0] else ''
                area = str(linha[1]).strip() if linha[1] else ''
                metodologia = str(linha[2]).strip() if linha[2] else ''
                faixa = str(linha[3]).strip() if linha[3] else ''
                
                # Validar campos obrigatórios
                if not nome:
                    erros.append(f'Linha {linha_atual}: Nome do curso é obrigatório')
                    continue
                
                if not metodologia:
                    erros.append(f'Linha {linha_atual}: Metodologia é obrigatória')
                    continue
                
                if not faixa:
                    erros.append(f'Linha {linha_atual}: Faixa é obrigatória')
                    continue
                
                # Verificar se curso já existe
                curso_existente = Curso.query.filter_by(nome=nome, ativo=True).first()
                if curso_existente:
                    erros.append(f'Linha {linha_atual}: Curso "{nome}" já existe')
                    continue
                
                # Criar novo curso
                novo_curso = Curso(
                    nome=nome,
                    area=area,
                    metodologia=metodologia,
                    faixa=faixa
                )
                
                db.session.add(novo_curso)
                cursos_adicionados.append({
                    'nome': nome,
                    'area': area,
                    'metodologia': metodologia,
                    'faixa': faixa
                })
                
                
            except Exception as e:
                erros.append(f'Linha {linha_atual}: Erro ao processar - {str(e)}')
        
        # Salvar todos os cursos de uma vez
        if cursos_adicionados:
            db.session.commit()
        
        return {
            'success': True,
            'cursos_adicionados': len(cursos_adicionados),
            'erros': erros,
            'detalhes': cursos_adicionados
        }
        
        
    except Exception as e:
        db.session.rollback()
        raise e



from flask import send_file, request, jsonify
from src.pdf_generator import criar_pdf_design1, criar_pdf_design2  # certifique-se que está certo

@curso_bp.route('/cursos/export/pdf', methods=['POST'])
def exportar_pdf():
    dados = request.get_json()
    curso_ids = dados.get('curso_ids', [])
    design = dados.get('design', 'design1')
    titulo = dados.get('titulo', 'Relatório de Cursos')

    if not curso_ids:
        return jsonify({'success': False, 'error': 'Nenhum curso selecionado'}), 400

    cursos = Curso.query.filter(Curso.id.in_(curso_ids)).all()
    cursos_dict = [curso.to_dict() for curso in cursos]

    if design == 'design1':
        buffer = criar_pdf_design1(cursos_dict, titulo)
    elif design == 'design2':
        buffer = criar_pdf_design2(cursos_dict, titulo)
    else:
        return jsonify({'success': False, 'error': 'Design inválido'}), 400

    return send_file(buffer, mimetype='application/pdf',
                     as_attachment=True, download_name='relatorio_cursos.pdf')


