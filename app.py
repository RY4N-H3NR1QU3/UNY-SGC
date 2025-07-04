from flask import Flask, request, jsonify, send_from_directory
from src.extensions import db
from flask_cors import CORS
import os

# Criar a aplicação Flask
app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = 'unyleya-gestao-cursos-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

# Inicializar extensões
db.init_app(app)
CORS(app, origins="*")  # Permite acesso de qualquer origem

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Importar modelos (deve vir depois da criação do db)
with app.app_context():
    from src.models.curso import Curso
    from src.routes.curso_routes import curso_bp
    
    # Registrar blueprints
    app.register_blueprint(curso_bp, url_prefix='/api')
    
    # Criar tabelas
    db.create_all()
    
    # Popular com dados iniciais
    from src.utils.populate_db import criar_cursos_iniciais
    criar_cursos_iniciais()

# Rota para servir o frontend
@app.route('/')
def index():
    """Serve a página principal"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve arquivos estáticos do frontend"""
    try:
        return send_from_directory('../frontend', path)
    except:
        # Se arquivo não encontrado, retornar 404
        return "Arquivo não encontrado", 404

# Rota de status para verificar se API está funcionando
@app.route('/api/status')
def status():
    """Verifica status da API"""
    return jsonify({
        'status': 'online',
        'message': 'API do Sistema de Gestão de Cursos está funcionando',
        'version': '1.0'
    })




# Adicione este código para debug no app.py
@app.route('/api/debug/cursos')
def debug_cursos():
    cursos = Curso.query.all()
    return jsonify([curso.to_dict() for curso in cursos])


# Tratamento de erros
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

# Adicione este código ao app.py para mostrar o IP automaticamente
import socket

def obter_ip_local():
    try:
        # Conectar a um endereço externo para descobrir IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

# Usar na função main:
if __name__ == '__main__':
    ip_local = obter_ip_local()
    print("🚀 Iniciando Sistema de Gestão de Cursos - Unyleya")
    print(f"📍 Acesso local: http://localhost:5000")
    print(f"🌐 Acesso na rede: http://{ip_local}:5000")
    print(f"📊 API Status: http://{ip_local}:5000/api/status")
    print("⏹️  Para parar: Ctrl+C")
    print("-" * 50)
    
    app.run(
        debug=True,           # Modo desenvolvimento
        host='0.0.0.0',      # Permite acesso de outros dispositivos
        port=5000,           # Porta padrão
        threaded=True        # Suporte a múltiplas requisições
    )



