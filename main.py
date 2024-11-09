from flask import Flask, request, make_response, render_template, jsonify,redirect,url_for, session, flash
from datetime import datetime
from models.quiz import obter_resposta_usuario,resposta_none,resposta_correta,resposta_incorreta, fases
from models.codigo import codigo_quiz

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Supersenha'
app.config['tempo_de_expiracao_quiz'] = 62 # 1 minuto
app.config['pergunta_atual'] = 0
app.config['pontuacao'] = 0
app.config['trofeu_quiz'] = 0


@app.route('/')
def Index():
    return render_template('inicial.html')

@app.route('/perfil')
def Perfil():
    return render_template('perfil.html')

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
            if resposta_user == fases[fase_atual-1][pergunta_atual]['resposta']:
                pontuacao += 1
                app.config['pontuacao'] = pontuacao
                pergunta_atual += 1
                app.config['pergunta_atual'] = pergunta_atual
                if pergunta_atual < len(fases[fase_atual-1]):
                    return resposta_correta(fase_atual,pergunta_atual)
                else:
                    return codigo_quiz(pontuacao,fase_atual,fase_desbloqueada,trofeu_quiz,app)
            else:
                pergunta_atual += 1
                app.config['pergunta_atual'] = pergunta_atual
                if pergunta_atual < len(fases[fase_atual-1]):
                    return resposta_incorreta(fase_atual,pergunta_atual)
                else:
                    return codigo_quiz(pontuacao,fase_atual,fase_desbloqueada,trofeu_quiz,app)
    else:
        fase_atual = request.args.get('fase')
        if fase_atual is None:
            fase_atual = int(request.cookies.get('fase_atual',1))
            fase_desbloqueada = int(request.cookies.get('fase_desbloqueada',1))
            tempo_de_inicio = request.cookies.get('tempo_de_inicio_quiz',str(datetime.now()))
            if tempo_de_inicio is not None:
                tempo_de_inicio = datetime.strptime(tempo_de_inicio, '%Y-%m-%d %H:%M:%S.%f')
                tempo_restante = int(app.config['tempo_de_expiracao_quiz'] - (datetime.now() - tempo_de_inicio).total_seconds())
                if tempo_restante <= 0:
                    pergunta_atual += 1
                    app.config['pergunta_atual'] = pergunta_atual
                    if pergunta_atual < len(fases[fase_atual-1]):
                        mensagem = 'TEMPO ESGOTADO!!!'
                        response = make_response(render_template('jogo_quiz.html',pergunta=fases[fase_atual-1][pergunta_atual]['pergunta'],opcoes=fases[fase_atual-1][pergunta_atual]['opcoes'],mensagem=mensagem))
                        response.set_cookie('fase_atual', str(fase_atual))
                        response.set_cookie('tempo_de_inicio_quiz', str(datetime.now()))
                        return response
                    else:
                        if pontuacao >= 7:
                            if fase_atual < fase_desbloqueada:
                                message = f"Parabéns sua pontuação foi {pontuacao}/{len(fases[fase_atual-1])}"                            
                                pontuacao = 0
                                app.config['pontuacao'] = pontuacao
                                pergunta_atual = 0
                                app.config['pergunta_atual'] = pergunta_atual
                                response = make_response(render_template('tela_final.html', mensagem=message))
                                response.set_cookie('fase_atual', str(fase_atual))
                                response.set_cookie('fase_desbloqueada', str(fase_desbloqueada))
                                return response
                            else:
                                if (fase_atual) in (1,2,3):  # ganhou um trófeu

                                    message = f"Parabéns sua pontuação foi {pontuacao}/{len(fases[fase_atual-1])}. Pode avançar de fase."
                                        
                                    if fase_atual == 1:    
                                        trofeu = "/static/imgs/trofeu1.png"
                                        msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase_atual}! Você tem {1+trofeu_quiz} trofeus do quiz!"
                                    elif fase_atual == 2:
                                        trofeu = "/static/imgs/trofeu2.png"
                                        msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase_atual}! Você tem {1+trofeu_quiz} trofeus do quiz!"
                                    else:
                                        trofeu = "/static/imgs/trofeu3.png"
                                        msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase_atual}! Você tem {1+trofeu_quiz} trofeus do quiz!"
                                    pontuacao = 0
                                    app.config['pontuacao'] = pontuacao
                                    pergunta_atual = 0
                                    app.config['pergunta_atual'] = pergunta_atual
                                    response = make_response(render_template('tela_final.html', mensagem=message, msg_trofeu = msg_trofeu, trofeu = trofeu))
                                    response.set_cookie('fase_atual', str(fase_atual))
                                    response.set_cookie('fase_desbloqueada', str(fase_desbloqueada + 1))
                                    response.set_cookie('trofeu_quiz', str(trofeu_quiz + 1))
                                    return response
                                
                                else:
                                    message = f"Parabéns sua pontuação foi {pontuacao}/{len(fases[fase_atual-1])}. Pode avançar de fase."
                                    pontuacao = 0
                                    app.config['pontuacao'] = pontuacao
                                    pergunta_atual = 0
                                    app.config['pergunta_atual'] = pergunta_atual
                                    response = make_response(render_template('tela_final.html', mensagem=message))
                                    response.set_cookie('fase_atual', str(fase_atual))
                                    response.set_cookie('fase_desbloqueada', str(fase_desbloqueada + 1))
                                    return response
                        else:
                            if fase_atual < fase_desbloqueada:
                                message = f"Sua pontuação foi {pontuacao}/{len(fases[fase_atual-1])}"                            
                                pontuacao = 0
                                app.config['pontuacao'] = pontuacao
                                pergunta_atual = 0
                                app.config['pergunta_atual'] = pergunta_atual
                                response = make_response(render_template('tela_final.html', mensagem=message))
                                response.set_cookie('fase_atual', str(fase_atual))
                                response.set_cookie('fase_desbloqueada', str(fase_desbloqueada))
                                return response
                            else:
                                message = f"Sua pontuação foi {pontuacao}/{len(fases[fase_atual-1])}. Tente fazer melhor para avançar de fase."
                                pontuacao = 0
                                app.config['pontuacao'] = pontuacao
                                pergunta_atual = 0
                                app.config['pergunta_atual'] = pergunta_atual
                                response = make_response(render_template('tela_final.html', mensagem=message))
                                response.set_cookie('fase_atual', str(fase_atual))
                                response.set_cookie('fase_desbloqueada', str(fase_desbloqueada))
                                return response
                else:
                    if fase_atual <= fase_desbloqueada:
                        tempo_restante = int(app.config['tempo_de_expiracao_quiz'] - (datetime.now() - tempo_de_inicio).total_seconds())
                        response = make_response(render_template('jogo_quiz.html',pergunta=fases[fase_atual-1][pergunta_atual]['pergunta'],opcoes=fases[fase_atual-1][pergunta_atual]['opcoes'],mensagem=''))
                        response.set_cookie('fase_atual', str(fase_atual))
                        return response
        else:
            pontuacao = 0
            app.config['pontuacao'] = pontuacao
            fase_atual = int(request.args.get('fase',1))
            #define o cookie fase_desbloqueada
            if fase_atual == 1:
                if request.cookies.get('fase_desbloqueada',1) is None:
                    pergunta_atual = 0
                    app.config['pergunta_atual'] = pergunta_atual
                    fase_desbloqueada = 1
                    response = make_response(render_template('jogo_quiz.html',pergunta=fases[fase_atual-1][pergunta_atual]['pergunta'],opcoes=fases[fase_atual-1][pergunta_atual]['opcoes'],mensagem=''))
                    response.set_cookie('fase_desbloqueada', str(fase_desbloqueada))
                    response.set_cookie('tempo_de_inicio_quiz', str(datetime.now()))
                    response.set_cookie('fase_atual', str(fase_atual))
                    return response
                else:
                    pergunta_atual = 0
                    app.config['pergunta_atual'] = pergunta_atual
                    tempo_de_inicio = request.cookies.get('tempo_de_inicio_quiz')
                    if tempo_de_inicio is not None:
                        tempo_de_inicio = datetime.strptime(tempo_de_inicio, '%Y-%m-%d %H:%M:%S.%f')
                        tempo_restante = int(app.config['tempo_de_expiracao_quiz'] - (datetime.now() - tempo_de_inicio).total_seconds())
                        if tempo_restante > 0:
                            response = make_response(render_template('jogo_quiz.html',pergunta=fases[fase_atual-1][pergunta_atual]['pergunta'],opcoes=fases[fase_atual-1][pergunta_atual]['opcoes'],mensagem=''))
                            response.set_cookie('fase_atual', str(fase_atual))
                            return response
            #se já tiver criado, pega o valor
            else:
                fase_desbloqueada = int(request.cookies.get('fase_desbloqueada', 1))
                if fase_atual <= fase_desbloqueada:
                    pergunta_atual = 0
                    app.config['pergunta_atual'] = pergunta_atual
                    response = make_response(render_template('jogo_quiz.html',pergunta=fases[fase_atual-1][pergunta_atual]['pergunta'],opcoes=fases[fase_atual-1][pergunta_atual]['opcoes'],mensagem=''))
                    response.set_cookie('fase_atual', str(fase_atual))
                    response.set_cookie('tempo_de_inicio_quiz', str(datetime.now()))
                    return response
                else:
                    return redirect(url_for('Fases_quiz'))
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
    pergunta_atual = 0
    app.config['pergunta_atual'] = pergunta_atual
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
