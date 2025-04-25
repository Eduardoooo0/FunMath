from flask import render_template, request, make_response,redirect,url_for
from datetime import datetime


PONTUACAO_MINIMA = 2

fases = [

            # fase1:

            [
                {
                    "pergunta": "Quando Felipe tinha 5 anos, o pai dele tinha 36 anos. Agora Felipe tem a metade da idade do pai. Quantos anos Felipe tem?",
                    "opcoes": ["18 anos", "24 anos", "31 anos", "36 anos"],
                    "resposta": "31 anos"
                },
                {
                    "pergunta": "Observando a sequência, o número que substitui a interrogação é? 1, 7, 6, – 1, – 7, – 6, 1, 7, 6, ?",
                    "opcoes": ["1", "-7", "6", "-1"],
                    "resposta": "-1"
                },
                {
                    "pergunta": "Qual é o sucessor do sucessor de 199?",
                    "opcoes": ["199", "200", "201", "202"],
                    "resposta": "201"
                },
                {
                    "pergunta": "Qual é o antecessor do sucessor de 45?",
                    "opcoes": ["44", "45", "46", "47"],
                    "resposta": "45"
                },
                {
                    "pergunta": "O valor da expressão (100 - 40) : 3 é:",
                    "opcoes": ["10", "15", "20", "24"],
                    "resposta": "20"
                },
                {
                    "pergunta": "Em um anfiteatro, as cadeiras estão dispostas em 20 linhas e 15 colunas. Qual é o número total de cadeiras?",
                    "opcoes": ["35", "150", "200", "300"],
                    "resposta": "300"
                },
                {
                    "pergunta": "Carlos guardou sua coleção de latas de refrigerante em casa. Em cada caixa couberam 28 latas. Ele usou 7 caixas e sobraram 6 latas de refrigerante. Quantas latas tem a coleção de Carlos?",
                    "opcoes": ["194", "196", "202", "238"],
                    "resposta": "202"
                },
                {
                    "pergunta": "Arrumando 512 cadernos em 12 pacotes de mesma quantidade, sobraram ainda 8 cadernos. Quantos cadernos foram colocados em cada pacote?",
                    "opcoes": ["28", "36", "42", "48"],
                    "resposta": "42"
                },
                {
                    "pergunta": "Um granjeiro tem 3 333 ovos para vender. Se colocar 33 ovos em cada caixa, quantas caixas completas vão formar?",
                    "opcoes": ["100", "101", "110", "111"],
                    "resposta": "101"
                },
                {
                    "pergunta": "Alvimar pagou uma compra de R$ 3,50 com uma nota de R$ 5,00 e recebeu o troco em moedas de R$ 0,25. Quantas moedas ele recebeu?",
                    "opcoes": ["4", "5", "6", "7"],
                    "resposta": "6"
                }
            ],

            # fase2:

            [
                {
                    "pergunta": "O número em que o algarismo 8 vale 8 centésimos é:",
                    "opcoes": ["0,0008 ", " 0,008", "0,08", " 0,8"],
                    "resposta": "0,08"
                },
                {
                    "pergunta": "O quadrado da metade de (− 6) é:",
                    "opcoes": ["36", "9", "27", "3"],
                    "resposta": "9"
                },
                {
                    "pergunta": "Na multiplicação de potências de mesma base, o produto é obtido mantendo-se a base e _______ os expoentes.",
                    "opcoes": ["adicionando-se", "subtraindo-se", "multiplicando-se", "dividindo-se"],
                    "resposta": "adicionando-se"
                },
                {
                    "pergunta": "Na divisão de potências de mesma base não nula, o quociente é obtido mantendo-se a base e _______ os expoentes.",
                    "opcoes": ["adicionando-se", "subtraindo-se", "multiplicando-se", "dividindo-se"],
                    "resposta": "subtraindo-se"
                },
                {
                    "pergunta": "1+5?",
                    "opcoes": ["1", "6", "2", "5"],
                    "resposta": "6"
                },
                {
                    "pergunta": "1+6?",
                    "opcoes": ["7", "3", "2", "5"],
                    "resposta": "7"
                },
                {
                    "pergunta": "1+7?",
                    "opcoes": ["1", "8", "2", "5"],
                    "resposta": "8"
                },
                {
                    "pergunta": "1+8?",
                    "opcoes": ["1", "3", "2", "9"],
                    "resposta": "9"
                },
                {
                    "pergunta": "1+9?",
                    "opcoes": ["1", "3", "10", "5"],
                    "resposta": "10"
                },
                {
                    "pergunta": "1+10?",
                    "opcoes": ["11", "3", "2", "5"],
                    "resposta": "11"
                }
            ],

            # fase3:

            [
                {
                    "pergunta": "1+1?",
                    "opcoes": ["1", "2", "3", "4"],
                    "resposta": "2"
                },
                {
                    "pergunta": "1+2?",
                    "opcoes": ["1", "3", "2", "5"],
                    "resposta": "3"
                },
                {
                    "pergunta": "1+3?",
                    "opcoes": ["1", "3", "4", "5"],
                    "resposta": "4"
                },
                {
                    "pergunta": "1+4?",
                    "opcoes": ["1", "3", "2", "5"],
                    "resposta": "5"
                },
                {
                    "pergunta": "1+5?",
                    "opcoes": ["1", "6", "2", "5"],
                    "resposta": "6"
                },
                {
                    "pergunta": "1+6?",
                    "opcoes": ["7", "3", "2", "5"],
                    "resposta": "7"
                },
                {
                    "pergunta": "1+7?",
                    "opcoes": ["1", "8", "2", "5"],
                    "resposta": "8"
                },
                {
                    "pergunta": "1+8?",
                    "opcoes": ["1", "3", "2", "9"],
                    "resposta": "9"
                },
                {
                    "pergunta": "1+9?",
                    "opcoes": ["1", "3", "10", "5"],
                    "resposta": "10"
                },
                {
                    "pergunta": "1+10?",
                    "opcoes": ["11", "3", "2", "5"],
                    "resposta": "11"
                }
            ],
            
        ]

# pega a resposta do user
def obter_resposta_usuario():
    resposta_user = request.form.get('resposta')
    return resposta_user

# retorna se a resposta for None (não será necessário)
def resposta_none(fase_atual,pergunta_atual):
    mensagem = "Por favor, selecione uma resposta."
    response = make_response(render_template('jogo_quiz.html', pergunta=fases[fase_atual-1][pergunta_atual]['pergunta'],    opcoes=fases[fase_atual-1][pergunta_atual]['opcoes'],    mensagem=mensagem))
    response.set_cookie('fase_atual', str(fase_atual))
    response.set_cookie('tempo_de_inicio_quiz', str(datetime.now()))
    return response

# retorna se o user acertar a questão
def resposta_correta(fase_atual,pergunta_atual):
    mensagem = "Parabéns! Sua resposta está correta."
    response = make_response(render_template('jogo_quiz.html',pergunta=fases[fase_atual-1][pergunta_atual]['pergunta'],opcoes=fases[fase_atual-1][pergunta_atual]['opcoes'],mensagem=mensagem))
    response.set_cookie('fase_atual', str(fase_atual))
    response.set_cookie('tempo_de_inicio_quiz', str(datetime.now()))
    return response

# retorna se o user errar a questão
def resposta_incorreta(fase_atual, pergunta_atual):
    mensagem = f"Desculpe, a resposta correta era {fases[fase_atual-1][pergunta_atual - 1]['resposta']}."
    response = make_response(render_template('jogo_quiz.html',pergunta=fases[fase_atual-1][pergunta_atual]['pergunta'],opcoes=fases[fase_atual-1][pergunta_atual]['opcoes'],mensagem=mensagem))
    response.set_cookie('fase_atual', str(fase_atual))
    response.set_cookie('tempo_de_inicio_quiz', str(datetime.now()))
    return response

# retorna se o user concluir uma fase que já foi concluída anteriormente
def finalizar_fase_repetida(fase_atual,fase_desbloqueada,pontuacao):
    if pontuacao > 7:
        message = f"Parabéns sua pontuação foi {pontuacao}/{len(fases[fase_atual-1])}"
    else:
        message = f"Sua pontuação foi {pontuacao}/{len(fases[fase_atual-1])}"             
    response = make_response(render_template('tela_final.html', mensagem=message))
    response.set_cookie('fase_atual', str(fase_atual))
    response.set_cookie('fase_desbloqueada', str(fase_desbloqueada))
    return response
    
# retorna quando o user conclui uma fase e desbloqueia outra
def finalizar_fase_concluida(fase_atual,pontuacao, fase_desbloqueada, trofeu_quiz):
    message = f"Parabéns sua pontuação foi {pontuacao}/{len(fases[fase_atual-1])}. Pode avançar de fase."
    if fase_atual == 1:    
        trofeu = "/static/imgs/trofeu1.png"
        msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase_atual}! Você tem {1+trofeu_quiz} trofeus do quiz!"
    elif fase_atual == 2:
        trofeu = "/static/imgs/trofeu2.png"
        msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase_atual}! Você tem {1+trofeu_quiz} trofeus do quiz!"
    elif fase_atual == 3:
        trofeu = "/static/imgs/trofeu3.png"
        msg_trofeu = f" Você ganhou um trófeu por completar a fase {fase_atual}! Você tem {1+trofeu_quiz} trofeus do quiz!"
    else:
        trofeu = ''
        msg_trofeu = f""
    response = make_response(render_template('tela_final.html', mensagem=message, msg_trofeu = msg_trofeu, trofeu = trofeu))
    response.set_cookie('fase_atual', str(fase_atual + 1))
    response.set_cookie('fase_desbloqueada', str(fase_desbloqueada + 1))
    response.set_cookie('trofeu_quiz', str(trofeu_quiz + 1))
    return response

# retorna quando um user não atinge a pontuação para avançar de fase
def finalizar_fase_fracassada(fase_atual,pontuacao,fase_desbloqueada):
    message = f"Sua pontuação foi {pontuacao}/{len(fases[fase_atual-1])}. Tente fazer melhor para avançar de fase."
    response = make_response(render_template('tela_final.html', mensagem=message))
    response.set_cookie('fase_atual', str(fase_atual))
    response.set_cookie('fase_desbloqueada', str(fase_desbloqueada))
    return response

# retorna quando o tempo acaba
def tempo_esgotado(fase_atual,pergunta_atual):
    mensagem = 'TEMPO ESGOTADO!!!'
    response = make_response(render_template('jogo_quiz.html',pergunta=fases[fase_atual-1][pergunta_atual]['pergunta'],opcoes=fases[fase_atual-1][pergunta_atual]['opcoes'],mensagem=mensagem))
    response.set_cookie('fase_atual', str(fase_atual))
    response.set_cookie('tempo_de_inicio_quiz', str(datetime.now()))
    return response

# retorna quando for a primeira fase
def fase_inicial(app,fase_atual):
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

# exibe a primeira pergunta de cada fase
def exibir_fase(fase_atual,app):
    fase_desbloqueada = int(request.cookies.get('fase_desbloqueada', 1))
    if fase_atual <= fase_desbloqueada:
        pergunta_atual = 0
        app.config['pergunta_atual'] = pergunta_atual
        response = make_response(render_template('jogo_quiz.html',pergunta=fases[fase_atual-1][pergunta_atual]['pergunta'],opcoes=fases[fase_atual-1][pergunta_atual]['opcoes'],mensagem=''))
        response.set_cookie('fase_atual', str(fase_atual))
        response.set_cookie('tempo_de_inicio_quiz', str(datetime.now()))
        return response
    else:
        app.config['pergunta_atual'] = 0
        response = make_response(render_template('fases_quiz.html', messagem=f'Fase Bloqueada! Complete a {fase_desbloqueada}° fase do Quiz!'))
        response.set_cookie('tempo_de_inicio_quiz', str(datetime.now()))
        return response
    
# reune códigos parecidos, quando a fase é fracassada e quando é concluída
def verificar_resultado(pontuacao: int, fase_atual: int, fase_desbloqueada: int, trofeu_quiz: int, app):
    if fase_atual < fase_desbloqueada:
        finalizar = finalizar_fase_repetida(fase_atual, fase_desbloqueada, pontuacao)
    else:
        if pontuacao >= PONTUACAO_MINIMA:
            finalizar = finalizar_fase_concluida(fase_atual, pontuacao, fase_desbloqueada, trofeu_quiz)
        else:
            finalizar = finalizar_fase_fracassada(fase_atual, pontuacao, fase_desbloqueada)
    app.config['pontuacao'] = 0
    app.config['pergunta_atual'] = 0
    return finalizar