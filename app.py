from flask import Flask, request, make_response, render_template, jsonify,redirect,url_for, session, flash
from datetime import datetime, timedelta
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from database import session
from werkzeug.security import generate_password_hash
from models.user import User

from quiz import fases, obter_resposta_usuario,fase_inicial,exibir_fase,resposta_none,resposta_correta,resposta_incorreta, tempo_esgotado, verificar_resultado
from trilha import fases_trilha
from qcbc import fases_qcbc

import json

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
    trofeu_quiz = request.cookies.get('trofeu_quiz',0)
    trofeu_trilha = request.cookies.get('trofeu_trilha',0)
    trofeu_qcbc = request.cookies.get('trofeu_qcbc',0)

    
    trofeu_quiz = int(trofeu_quiz)
    trofeu_trilha = int(trofeu_trilha)
    trofeu_qcbc = int(trofeu_qcbc)
    return render_template('perfil.html', trofeu_quiz=trofeu_quiz, trofeu_qcbc=trofeu_qcbc, trofeu_trilha=trofeu_trilha)

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


@app.route('/jogo_qcbc', methods=['POST', 'GET'])
def Qcbc_jogo():
    if request.method == 'GET':
        fase = request.args.get('fase')
        fase_desbloqueada_qcbc = int(request.cookies.get('fase_desbloqueada_qcbc', 1))

        if fase is None:
            return redirect(url_for('Fases_qcbc'))
        else:
            if int(fase) > int(fase_desbloqueada_qcbc):
                return render_template('fases_qcbc.html', messagem=f'Fase Bloqueada! Complete o {fase_desbloqueada_qcbc}° Quebra Cabeça!')
            else:
                response = make_response(render_template('jogo_qcbc.html', valor=None, fase=fase, fase_desbloqueada_qcbc=fase_desbloqueada_qcbc))
                response.set_cookie('fase_atual_qcbc', str(fase))
                return response
     

@app.route('/questoes_qcbc', methods=['POST', 'GET'])
def Questoes_qcbc():
    fase = int(request.cookies.get('fase_atual_qcbc', 1))
    fase_desbloqueada_qcbc = int(request.cookies.get('fase_desbloqueada_qcbc', 1))

    if request.method == 'GET':
        questao = int(request.args.get('questao'))
        if 'img' in fases_qcbc[fase-1][questao]:
            response = make_response(render_template(
            'questoes_qcbc.html',
            pergunta=fases_qcbc[fase - 1][questao]['pergunta'],
            img=fases_qcbc[fase-1][questao]['img'],
            opcoes=fases_qcbc[fase - 1][questao]['opcoes'],
            mensagem=''))

        else:
            response = make_response(render_template(
                'questoes_qcbc.html',
                pergunta=fases_qcbc[fase - 1][questao]['pergunta'],
                opcoes=fases_qcbc[fase - 1][questao]['opcoes'],
                mensagem=''))
        # Define cookies com expiração de 30 dias
        expires = datetime.now() + timedelta(days=30)
        response.set_cookie('questao_atual_qcbc', str(questao), expires=expires)
        return response

    else:
        trofeu_qcbc = int(request.cookies.get('trofeu_qcbc', 0))
        resposta = request.form.get('resposta')
        questao = int(request.cookies.get('questao_atual_qcbc', 0))
        acertou = resposta == fases_qcbc[fase - 1][questao]['resposta']

        # Se a resposta estiver correta
        if acertou:
            # Atualiza questao_atual_qcbc imediatamente após resposta correta
            expires = datetime.now() + timedelta(days=30)
            response = make_response(render_template(
                'jogo_qcbc.html',
                questao_atual=questao,
                resposta=acertou,
                fase=fase,
                msg_resposta='Resposta Correta!'))

            response.set_cookie('questao_atual_qcbc', str(questao), expires=expires)

            # Lógica para verificação de troféu
            cookie_tabuleiro = request.cookies.get('tabuleiro-' + str(fase))
            qcbc_completo = False
            concluido = 0
            cont = 0
            q = 0
            
            tabuleiro = json.loads(cookie_tabuleiro)
            for peca in range(9):
                if tabuleiro[peca]['bloqueado']:
                    concluido += 1
                    q = cont
                cont += 1
            
            if concluido == 1 and q == questao:
                qcbc_completo = True

            if not qcbc_completo:
                return response
            
            # Se o quebra-cabeça foi completado, atribui o troféu
            msg_resposta = f"Parabéns você completou a fase {fase} do quebra-cabeça. Pode avançar de fase."
            trofeu, msg_trofeu = '', ''
            if fase == 1:    
                trofeu = "/static/imgs/trofeu1.png"
                msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase}! "
            elif fase == 5:
                trofeu = "/static/imgs/trofeu2.png"
                msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase}! "
            elif fase == 9:
                trofeu = "/static/imgs/trofeu3.png"
                msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase}! "

            if trofeu:
                response = make_response(render_template(
                    'jogo_qcbc.html',
                    questao_atual=questao,
                    resposta=acertou,
                    fase=fase,
                    msg_trofeu=msg_trofeu,
                    msg_resposta=msg_resposta,
                    trofeu=trofeu))
                response.set_cookie('trofeu_qcbc', str(trofeu_qcbc + 1), expires=expires)

                # Atualiza a fase desbloqueada
                response.set_cookie('fase_desbloqueada_qcbc', str(fase + 1), expires=expires)

                return response
            else:
                response = make_response(render_template(
                    'jogo_qcbc.html',
                    questao_atual=questao,
                    resposta=acertou,
                    fase=fase, 
                    msg_resposta='Parabéns você passou de fase do Quebra-Cabeça!'))

            # Atualiza a fase desbloqueada
            response.set_cookie('fase_desbloqueada_qcbc', str(fase + 1), expires=expires)
            return response
                    
        else:  # se a resposta for incorreta
            response = make_response(render_template(
                'jogo_qcbc.html',
                questao_atual=questao,
                resposta=acertou,
                fase=fase, 
                msg_resposta='Resposta incorreta!'))
            expires = datetime.now() + timedelta(days=30)
            response.set_cookie('questao_atual_qcbc', str(questao), expires=expires)
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

@app.route('/fases_trilha')
def Fases_trilha():
    return render_template('fases_trilha.html')

@app.route('/trilha_jogo')
def Trilha_jogo():
    return render_template('jogo_trilha.html')

# mostrar a questão da trilha e ver se estar correta
@app.route('/questoes_trilha', methods=['POST', 'GET'])
def Questoes_trilha():
    fase_desbloqueada = int(request.cookies.get('trilha_desbloqueada', 1))
    trofeu_trilha = int(request.cookies.get('trofeu_trilha', 0))
    if request.method == 'GET':  # Mostrar a questão
        fase = int(request.args.get('fase'))
        if fase <= fase_desbloqueada: 
            response = make_response(render_template('jogo_trilha.html', questao=fases_trilha[fase - 1]['pergunta'], mensagem=''))
            response.set_cookie('questao_atual_trilha', str(fase)) 
            return response
        else:
            mensagem = f'A fase {fase} não foi desbloqueada! Responda corretamente a fase {fase_desbloqueada}!'
            return render_template('fases_trilha.html', mensagem=mensagem)
        
    else:  # Verificar se a resposta está correta ou não
        resposta = str(request.form.get('resp_trilha'))
        fase = int(request.cookies.get('questao_atual_trilha', 1))
        if resposta == fases_trilha[fase - 1]['resposta']:

            mensagem = f"Parabéns você acertou a fase {fase}. Pode avançar de fase."
            if fase == 3:    
                trofeu = "/static/imgs/trofeu1.png"
                msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase}! Você tem {1+trofeu_trilha} trofeus do trilha!"
            elif fase == 6:
                trofeu = "/static/imgs/trofeu2.png"
                msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase}! Você tem {1+trofeu_trilha} trofeus do trilha!"
            elif fase == 9:
                trofeu = "/static/imgs/trofeu3.png"
                msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase}! Você tem {1+trofeu_trilha} trofeus do trilha!"
            else:
                trofeu = ''
                msg_trofeu = f""

            if fase == fase_desbloqueada:  # Se a fase respondida for a fase desbloqueada
                if trofeu != '':
                    response = make_response(render_template('fases_trilha.html', resposta='Resposta correta! Parabéns você passou de fase!', fase=fase, msg=msg_trofeu, trofeu=trofeu))
                    response.set_cookie('trilha_desbloqueada', str(fase_desbloqueada + 1))  # Atualiza o cookie
                    response.set_cookie('trofeu_trilha', str(trofeu_trilha + 1))
                else:
                    response = make_response(render_template('fases_trilha.html', resposta='Resposta correta! Parabéns você passou de fase!', fase=fase))
                    response.set_cookie('trilha_desbloqueada', str(fase_desbloqueada + 1))  # Atualiza o cookie
                
            else:
                response = make_response(render_template('fases_trilha.html', resposta='Resposta correta!', fase=fase))
            return response

        else:
            # Mensagem de erro
            if fase == fase_desbloqueada:
                response = make_response(render_template('fases_trilha.html', resposta='Resposta errada! Tente novamente para passar de fase!', fase=fase))
            else:
                response = make_response(render_template('fases_trilha.html', resposta='Resposta errada!', fase=fase)) 
            response.set_cookie('trilha_desbloqueada', str(fase_desbloqueada))  # Mantém o cookie
            return response
    

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

