from flask import Flask, request, make_response, render_template, jsonify,redirect,url_for, session, flash
from datetime import datetime
from quiz import obter_resposta_usuario,fase_inicial,exibir_fase,resposta_none,resposta_correta,resposta_incorreta, tempo_esgotado, verificar_resultado ,fases
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from database import session
from werkzeug.security import generate_password_hash
from models.user import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Supersenha'
app.config['tempo_de_expiracao_quiz'] = 60 # 1 minuto
app.config['pergunta_atual'] = 0
app.config['pontuacao'] = 0
app.config['trofeu_quiz'] = 0

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perfil')
def Perfil():
    trofeu_quiz = request.cookies.get('trofeu_quiz')
    if trofeu_quiz is None:
        return render_template('perfil.html', trofeu_quiz=None)
    else:
        trofeu_quiz = int(trofeu_quiz)
        return render_template('perfil.html', trofeu_quiz=trofeu_quiz)

@app.route('/quiz', methods=['POST', 'GET'])
def Quiz():
    pergunta_atual = app.config.get('pergunta_atual', 0)
    pontuacao = app.config.get('pontuacao', 0)
    trofeu_quiz = app.config.get('trofeu_quiz', 0)
    if request.method == 'POST':
        fase_desbloqueada = int(request.cookies.get('fase_desbloqueada',1))
        fase_atual = int(request.cookies.get('fase_atual', 1))
        trofeu_quiz = int(request.cookies.get('trofeu_quiz', 0))
        resposta_user = obter_resposta_usuario()
        if resposta_user is None:
            return resposta_none(fase_atual,pergunta_atual)
        else:
            # se a resposta está correta
            if resposta_user == fases[fase_atual-1][pergunta_atual]['resposta']:
                pontuacao += 1
                app.config['pontuacao'] = pontuacao
                pergunta_atual += 1
                app.config['pergunta_atual'] = pergunta_atual
                if pergunta_atual < len(fases[fase_atual-1]):
                    return resposta_correta(fase_atual,pergunta_atual)
                else:
                    return verificar_resultado(pontuacao,fase_atual,fase_desbloqueada,trofeu_quiz,app)
            # se a resposta está incorreta
            else:
                pergunta_atual += 1
                app.config['pergunta_atual'] = pergunta_atual
                if pergunta_atual < len(fases[fase_atual-1]):
                    return resposta_incorreta(fase_atual,pergunta_atual)
                else:
                    return verificar_resultado(pontuacao,fase_atual,fase_desbloqueada,trofeu_quiz,app)
    else:
        fase_atual = request.args.get('fase')
        if fase_atual is None:
            fase_atual = int(request.cookies.get('fase_atual',1))
            fase_desbloqueada = int(request.cookies.get('fase_desbloqueada',1))
            tempo_de_inicio = request.cookies.get('tempo_de_inicio_quiz',str(datetime.now()))
            if tempo_de_inicio is not None:
                tempo_de_inicio = datetime.strptime(tempo_de_inicio, '%Y-%m-%d %H:%M:%S.%f')
                tempo_restante = int(app.config['tempo_de_expiracao_quiz'] - (datetime.now() - tempo_de_inicio).total_seconds())
                # se o tempo acabar
                if tempo_restante <= 0:
                    pergunta_atual += 1
                    app.config['pergunta_atual'] = pergunta_atual
                    if pergunta_atual < len(fases[fase_atual-1]):
                        return tempo_esgotado(fase_atual, pergunta_atual)
                    else:
                        return verificar_resultado(pontuacao,fase_atual,fase_desbloqueada,trofeu_quiz,app)
        else:
            app.config['pontuacao'] = 0
            fase_atual = int(request.args.get('fase',1))
            if fase_atual == 1:
                return fase_inicial(app,fase_atual)
            else:
                return exibir_fase(fase_atual,app)

@app.route('/quebra-cabeca')
def Quebra_cabeca():
    return render_template('inicial_qcbc.html')

@app.route('/fases_qcbc')
def Fases_qcbc():
    return render_template('fases_qcbc.html')

@app.route('/jogo_qcbc',methods=['POST', 'GET'])
def Jogo_qcbc():
    if request.method == 'GET':
        fase = request.args.get('fase')
        if fase is None:
            return redirect(url_for('Fases_qcbc'))
        else:
            response = make_response(render_template('jogo_qcbc.html',valor=None,fase=fase))
            response.set_cookie('fase_atual_qcbc',str(fase))
            return response
    
@app.route('/questoes_qcbc',methods=['POST', 'GET'])
def Questoes_qcbc():
    fase = int(request.cookies.get('fase_atual',1))
    if request.method == 'GET':
        questao = int(request.args.get('questao'))
        response = make_response(render_template('questoes_qcbc.html',pergunta=fases[fase-1][questao-1]['pergunta'],opcoes=fases[fase-1][questao-1]['opcoes'],mensagem=''))
        response.set_cookie('questao_atual', str(questao))
        return response
        
    else:
        resposta = request.form.get('resposta')
        questao = int(request.cookies.get('questao_atual',1))
        if resposta == fases[fase-1][questao-1]['resposta']:
            correct = True
            response = make_response(render_template('jogo_qcbc.html',valor=questao,resposta=correct,fase=fase))
            response.set_cookie('questao_atual',str(questao))
            return response
        else:
            false = False
            response = make_response(render_template('jogo_qcbc.html',valor=questao,resposta=false,fase=fase))
            response.set_cookie('questao_atual',str(questao))
            return response

        
@app.route('/inicial_quiz')
def Inicial_quiz():
    return render_template('inicial_quiz.html')

@app.route('/fases_quiz')
def Fases_quiz():
    app.config['pergunta_atual'] = 0
    response = make_response(render_template('fases_quiz.html'))
    response.set_cookie('tempo_de_inicio_quiz', str(datetime.now()))
    return response

@app.route('/tempo_restante')
def Tempo_restante():
    tempo_de_inicio = request.cookies.get('tempo_de_inicio_quiz')
    if tempo_de_inicio is not None:
        tempo_de_inicio = datetime.strptime(tempo_de_inicio, '%Y-%m-%d %H:%M:%S.%f')
        tempo_restante = app.config['tempo_de_expiracao_quiz'] - (datetime.now() - tempo_de_inicio).total_seconds()
        if tempo_restante <= 0:
            tempo_restante = 0
        return jsonify({'tempo_restante_em_segundos': int(tempo_restante)})
    else:
        return jsonify({'tempo_restante_em_segundos': app.config['tempo_de_expiracao_quiz']})

@app.route('/trilha')
def Trilha():
    return render_template ('inicial_trilha.html')

@app.route('/ajuda')
def Ajuda():
    return render_template ('ajuda.html')

@app.route('/sobre')
def Sobre():
    return render_template ('sobre.html')

@app.route('/jogos')
def Jogos():
    return render_template ('jogos.html')

@app.route('/login', methods = ['POST','GET'])
def Login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = session.query(User).filter_by(email=email).first()
        senha_hash = session.query(User).filter_by(senha=generate_password_hash(senha))
        if user and senha_hash:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('email ou senha incorreto')
            return redirect(url_for('Login'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('login.html')

@app.route('/cadastro', methods = ['POST', 'GET'])
def Cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)
        user = User(nome=nome,email=email,senha=senha_hash)
        usuario_existente = session.query(User).filter_by(email=email).first()
        if usuario_existente:
            flash('email já cadastrado')
            return redirect(url_for('Cadastro'))
        session.add(user)
        session.commit()
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        else:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('cadastro.html')


@app.route('/logout', methods = ['POST'])
@login_required
def Logout():
    logout_user()
    return redirect(url_for('index'))

