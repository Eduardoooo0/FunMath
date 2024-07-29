from flask import Flask, request, make_response, render_template

app = Flask(__name__)

perguntas = ['Quando Felipe tinha 5 anos, o pai dele tinha 36 anos. Agora Felipe tem a metade da idade do pai. Quantos anos Felipe tem?',
             'Observando a sequência, o número que substitui a interrogação é? 1, 7, 6, – 1, – 7, – 6, 1, 7, 6, ?',
             'Qual é o sucessor do sucessor de 199?']

opcoes = [['18 anos', '24 anos', '31 anos', '36 anos'], ['1', '-7', '6', '-1'], ['199', '200', '201', '202']]

respostas = ['31 anos', '-1', '201']

@app.route('/')
def Index():
    return render_template('inicial.html')

@app.route('/login')
def Login():
    return render_template('login.html')

@app.route('/quiz', methods=['POST', 'GET'])
def Quiz():
    mensagem = ''
    pergunta_atual = 0
    if request.method == 'POST':
        # Obter a resposta do usuário
        resposta_user = request.form['resposta']

        # Verificar se a resposta está correta
        if resposta_user == respostas[pergunta_atual]:
            # Passar para a próxima questão
            pergunta_atual += 1
            if pergunta_atual == len(perguntas):
                return render_template('tela_final.html')
            else:
                mensagem = "Parabéns! Sua resposta está correta."
                return render_template('jogo_quiz.html', pergunta=perguntas[pergunta_atual], opcoes=opcoes[pergunta_atual], mensagem=mensagem)
        else:
            mensagem = f"Desculpe, a resposta correta é {respostas[pergunta_atual]}."
            return render_template('jogo_quiz.html', pergunta=perguntas[pergunta_atual], opcoes=opcoes[pergunta_atual], mensagem=mensagem)
    else:
        # Iniciar o quiz com a primeira questão
        pergunta_atual = 0
        return render_template('jogo_quiz.html', pergunta=perguntas[pergunta_atual], opcoes=opcoes[pergunta_atual], mensagem='')