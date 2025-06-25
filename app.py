from flask import Flask, request, make_response, render_template, jsonify,redirect,url_for, session, flash
from datetime import datetime, timedelta
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from database import session
from werkzeug.security import generate_password_hash, check_password_hash                    
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

@app.route('/comecar_qcbc', methods=['GET'])
def comecar_qcbc():
    fase_desbloqueada_qcbc = int(request.cookies.get('fase_desbloqueada_qcbc', 1))
    return redirect(url_for('Qcbc_jogo', fase=fase_desbloqueada_qcbc))


@app.route('/jogo_qcbc', methods=['POST', 'GET'])
def Qcbc_jogo():
    if request.method == 'GET':
        fase = request.args.get('fase')
        fase_desbloqueada_qcbc = int(request.cookies.get('fase_desbloqueada_qcbc', 1))

        if fase is None:
            return redirect(url_for('comecar_qcbc'))

        fase = int(fase)

        # Verifica se a fase está bloqueada
        fase_bloqueada = fase > fase_desbloqueada_qcbc

        response = make_response(render_template(
            'jogo_qcbc.html',
            valor=None,
            fase=fase,
            fase_desbloqueada_qcbc=fase_desbloqueada_qcbc,
            fase_bloqueada=fase_bloqueada,
        ))
        response.set_cookie('fase_atual_qcbc', str(fase))
        return response


     

@app.route('/questoes_qcbc', methods=['POST', 'GET'])
def Questoes_qcbc():
    fase = int(request.cookies.get('fase_atual_qcbc', 1))
    fase_desbloqueada_qcbc = int(request.cookies.get('fase_desbloqueada_qcbc', 1))

    if request.method == 'GET':
        if fase > fase_desbloqueada_qcbc:
            return render_template('jogo_qcbc.html', messagem=f"Fase {fase} bloqueada! Complete a fase {fase_desbloqueada_qcbc} antes.")

        questao = int(request.args.get('questao'))

    if request.method == 'GET':
        questao = int(request.args.get('questao'))
        if 'img' in fases_qcbc[fase-1][questao]:
            response = make_response(render_template(
            'questoes_qcbc.html',
            pergunta=fases_qcbc[fase - 1][questao]['pergunta'],
            img=fases_qcbc[fase-1][questao]['img'],
            opcoes=fases_qcbc[fase - 1][questao]['opcoes'],
            mensagem='',
            fase_desbloqueada_qcbc=fase_desbloqueada_qcbc))

        else:
            response = make_response(render_template(
                'questoes_qcbc.html',
                pergunta=fases_qcbc[fase - 1][questao]['pergunta'],
                opcoes=fases_qcbc[fase - 1][questao]['opcoes'],
                mensagem='',
                fase_desbloqueada_qcbc=fase_desbloqueada_qcbc))
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
                msg_resposta='Parabens! Resposta Correta!',
                fase_desbloqueada_qcbc=fase_desbloqueada_qcbc))

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
                    trofeu=trofeu,
                    fase_desbloqueada_qcbc=fase_desbloqueada_qcbc))
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
                    msg_resposta='Parabéns você passou de fase do Quebra-Cabeça!',
                    fase_desbloqueada_qcbc=fase_desbloqueada_qcbc))

            # Atualiza a fase desbloqueada
            response.set_cookie('fase_desbloqueada_qcbc', str(fase + 1), expires=expires)
            return response
                    
        else:  # se a resposta for incorreta
            response = make_response(render_template(
                'jogo_qcbc.html',
                questao_atual=questao,
                resposta=acertou,
                fase=fase, 
                msg_resposta='Ops! Resposta incorreta.. Tente novamente!',
                fase_desbloqueada_qcbc=fase_desbloqueada_qcbc))
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




@app.route('/fases_trilha', methods=['POST', 'GET'])
def Fases_trilha():
    if request.method == 'GET':
        trilha_concluida = str(request.cookies.get('trilha_concluida', False))
        fase_desbloqueada = int(request.cookies.get('trilha_desbloqueada', 1))
        return render_template('fases_trilha.html', fase=fase_desbloqueada, concluido=trilha_concluida)
    else:
        response = make_response(render_template('fases_trilha.html', fase=1, concluido=False))       
        response.set_cookie('trilha_concluida', str(False))
        response.set_cookie('trilha_desbloqueada', str(1))  # Atualiza o cookie
        return response



@app.route('/trilha_jogo')
def Trilha_jogo():
    return render_template('jogo_trilha.html')

# mostrar a questão da trilha e ver se estar correta
@app.route('/questoes_trilha', methods=['POST', 'GET'])
def Questoes_trilha():
    trilha_concluida = False
    fase_desbloqueada = int(request.cookies.get('trilha_desbloqueada', 1))
    trofeu_trilha = int(request.cookies.get('trofeu_trilha', 0))
    if request.method == 'GET':  # Mostrar a questão
        fase_get = request.args.get('fase')
    
        if fase_get is not None:  # Verifica se o parâmetro 'fase' existe
            fase = int(fase_get)
        else:
            return render_template('fases_trilha.html', fase=fase_desbloqueada)
        if fase <= fase_desbloqueada: 
            response = make_response(render_template('jogo_trilha.html', questao=fases_trilha[fase - 1]['pergunta'], mensagem=''))
            response.set_cookie('questao_atual_trilha', str(fase)) 
            return response
        else:
            mensagem = f'A fase {fase} não foi desbloqueada! Responda corretamente a fase {fase_desbloqueada}!'
            return render_template('fases_trilha.html', msg_resp=mensagem)
        
    else:  # Verificar se a resposta está correta ou não
        resposta = str(request.form.get('resp_trilha'))
        fase = int(request.cookies.get('questao_atual_trilha', 1))
        if resposta == fases_trilha[fase-1]['resposta']:

            mensagem = f"Parabéns você acertou a fase {fase}. Pode avançar de fase."
            if fase == 3:    
                trofeu = "/static/imgs/trofeus/trofeu1_trilha.svg"
                msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase}! Você tem {1+trofeu_trilha} trofeus do trilha!"
            elif fase == 6:
                trofeu = "/static/imgs/trofeu2.png"
                msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase}! Você tem {1+trofeu_trilha} trofeus do trilha!"
            elif fase == 9:
                trofeu = "/static/imgs/trofeu3.png"
                msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase}! Você tem {1+trofeu_trilha} trofeus do trilha!"
                trilha_concluida = True
            else:
                trofeu = ''
                msg_trofeu = f""

            if fase == fase_desbloqueada:  # Se a fase respondida for a fase desbloqueada
                if trofeu != '':
                    response = make_response(render_template('fases_trilha.html', msg_resp='Resposta correta! Parabéns você passou de fase!', fase=fase+1, msg_trofeu=msg_trofeu, trofeu=trofeu, concluido=trilha_concluida))
                    if trilha_concluida == True:
                        response.set_cookie('trilha_concluida', str(True))
                        response.set_cookie('trofeu_trilha', str(trofeu_trilha + 1))
                    else:
                        response.set_cookie('trilha_desbloqueada', str(fase_desbloqueada + 1))  # Atualiza o cookie
                        response.set_cookie('trofeu_trilha', str(trofeu_trilha + 1))
                    
                else:
                    response = make_response(render_template('fases_trilha.html', msg_resp='Resposta correta! Parabéns você passou de fase!', fase=fase+1, concluido=trilha_concluida))
                    response.set_cookie('trilha_desbloqueada', str(fase_desbloqueada + 1))  # Atualiza o cookie
                
            else:
                response = make_response(render_template('fases_trilha.html', msg_resp='Resposta correta!', fase=fase))
            return response

        else:
            # Mensagem de erro
            if fase == fase_desbloqueada:
                response = make_response(render_template('fases_trilha.html', msg_resp='Resposta errada! Tente novamente para passar de fase!', fase=fase))
            else:
                response = make_response(render_template('fases_trilha.html', msg_resp='Resposta errada!', fase=fase)) 
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

@app.route('/login', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = session.query(User).filter_by(email=email).first()
        
        # Verifica a senha usando a função correta
        if user and check_password_hash(user.senha, senha):
            # Atualiza o progresso do usuário com base nos cookies
            fase_quiz = int(request.cookies.get('fase_desbloqueada', 1))
            trofeu_quiz = int(request.cookies.get('trofeu_quiz', 0))
            fase_qcbc = int(request.cookies.get('fase_desbloqueada_qcbc', 1))
            trofeu_qcbc = int(request.cookies.get('trofeu_qcbc', 0))
            fase_trilha = int(request.cookies.get('trilha_desbloqueada', 1))
            trofeu_trilha = int(request.cookies.get('trofeu_trilha', 0))

            jogos_backup = request.cookies.get('jogos_backup', '{}')

            # guardar progresso de não logado
            jogos_backup = json.dumps({
                'fase_quiz': fase_quiz,
                'trofeu_quiz': trofeu_quiz,
                'fase_qcbc': fase_qcbc,
                'trofeu_qcbc': trofeu_qcbc,
                'fase_trilha': fase_trilha,
                'trofeu_trilha': trofeu_trilha
            })

            
            # Atualiza os dados do usuário se o progresso for maior
            user.fase_quiz = max(user.fase_quiz, fase_quiz)
            user.trofeu_quiz = max(user.trofeu_quiz, trofeu_quiz)
            user.fase_qcbc = max(user.fase_qcbc, fase_qcbc)
            user.trofeu_qcbc = max(user.trofeu_qcbc, trofeu_qcbc)
            user.fase_trilha = max(user.fase_trilha, fase_trilha)
            user.trofeu_trilha = max(user.trofeu_trilha, trofeu_trilha)
            session.commit()

            # Define os cookies com os dados do usuário
            response = make_response(redirect(url_for('index')))
            response.set_cookie('fase_desbloqueada', str(user.fase_quiz))
            response.set_cookie('trofeu_quiz', str(user.trofeu_quiz))
            response.set_cookie('fase_desbloqueada_qcbc', str(user.fase_qcbc))
            response.set_cookie('trofeu_qcbc', str(user.trofeu_qcbc))
            response.set_cookie('trilha_desbloqueada', str(user.fase_trilha))
            response.set_cookie('trofeu_trilha', str(user.trofeu_trilha))

            response.set_cookie('jogos_backup', jogos_backup)

            login_user(user)
            return response
        else:
            flash('Email ou senha incorretos')
            return redirect(url_for('Login'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('login.html')

@app.route('/cadastro', methods=['POST', 'GET'])
def Cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)

        # Verifica se o usuário já existe
        if session.query(User).filter_by(email=email).first():
            flash('Email já cadastrado')
            return redirect(url_for('Cadastro'))

        # Recupera valores de cookies
        fase_quiz = int(request.cookies.get('fase_desbloqueada', 1))
        trofeu_quiz = int(request.cookies.get('trofeu_quiz', 0))
        fase_qcbc = int(request.cookies.get('fase_desbloqueada_qcbc', 1))
        trofeu_qcbc = int(request.cookies.get('trofeu_qcbc', 0))
        fase_trilha = int(request.cookies.get('trilha_desbloqueada', 1))
        trofeu_trilha = int(request.cookies.get('trofeu_trilha', 0))

        user = User(
            nome=nome,
            email=email,
            senha=senha_hash,
            fase_quiz=fase_quiz,
            trofeu_quiz=trofeu_quiz,
            fase_qcbc=fase_qcbc,
            trofeu_qcbc=trofeu_qcbc,
            fase_trilha=fase_trilha,
            trofeu_trilha=trofeu_trilha
        )

        session.add(user)
        session.commit()
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('cadastro.html')

@app.route('/logout', methods=['POST'])
@login_required
def Logout():
    user_id = current_user.id
    user = session.query(User).filter(User.id == user_id).first()

    # Recupera o progresso atual antes de deslogar
    fase_quiz = int(request.cookies.get('fase_desbloqueada', 1))
    trofeu_quiz = int(request.cookies.get('trofeu_quiz', 0))
    fase_qcbc = int(request.cookies.get('fase_desbloqueada_qcbc', 1))
    trofeu_qcbc = int(request.cookies.get('trofeu_qcbc', 0))
    fase_trilha = int(request.cookies.get('trilha_desbloqueada', 1))
    trofeu_trilha = int(request.cookies.get('trofeu_trilha', 0))

    # Atualiza o progresso do usuário
    user.fase_quiz = max(user.fase_quiz, fase_quiz)
    user.trofeu_quiz = max(user.trofeu_quiz, trofeu_quiz)
    user.fase_qcbc = max(user.fase_qcbc, fase_qcbc)
    user.trofeu_qcbc = max(user.trofeu_qcbc, trofeu_qcbc)
    user.fase_trilha = max(user.fase_trilha, fase_trilha)
    user.trofeu_trilha = max(user.trofeu_trilha, trofeu_trilha)
    session.commit()

    user_choice = request.form.get('user_choice')
    response = make_response(redirect(url_for('index')))

    if user_choice != 'recuperar':
        response.set_cookie('jogos_backup', '', expires=0)

        response.set_cookie('fase_desbloqueada', str(1))
        response.set_cookie('trofeu_quiz', str(0))
        response.set_cookie('fase_desbloqueada_qcbc', str(1))
        response.set_cookie('trofeu_qcbc', str(0))
        response.set_cookie('trilha_desbloqueada', str(1))
        response.set_cookie('trofeu_trilha', str(0))

    else:
        jogos_backup = request.cookies.get('jogos_backup', '{}')
        dados = json.loads(jogos_backup)

        # Se o usuário quiser recuperar o progresso
        response.set_cookie('fase_desbloqueada', str(dados.get('fase_quiz',1)))
        response.set_cookie('trofeu_quiz', str(dados.get('trofeu_quiz',0)))
        response.set_cookie('fase_desbloqueada_qcbc', str(dados.get('fase_qcbc',1)))
        response.set_cookie('trofeu_qcbc', str(dados.get('trofeu_qcbc',0)))
        response.set_cookie('trilha_desbloqueada', str(dados.get('fase_trilha',1)))
        response.set_cookie('trofeu_trilha', str(dados.get('trofeu_trilha',0)))

    logout_user()
    return response