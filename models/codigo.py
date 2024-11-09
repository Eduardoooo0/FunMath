from models.quiz import finalizar_fase_repetida,finalizar_fase_concluida,finalizar_fase_fracassada

def codigo_quiz(pontuacao,fase_atual,fase_desbloqueada,trofeu_quiz,app):
    if pontuacao >= 7:
        if fase_atual < fase_desbloqueada:
            finalizar = finalizar_fase_repetida(fase_atual,fase_desbloqueada,pontuacao)                       
            app.config['pontuacao'] = 0
            app.config['pergunta_atual'] = 0
            return finalizar
        else:
            if (fase_atual) in (1,2,3):  # ganhou um trófeu
                finalizar = finalizar_fase_concluida(fase_atual,pontuacao,fase_desbloqueada,trofeu_quiz)
                app.config['pontuacao'] = 0
                app.config['pergunta_atual'] = 0
                return finalizar
            else:
                finalizar = finalizar_fase_concluida(fase_atual,pontuacao,fase_desbloqueada,trofeu_quiz)
                app.config['pontuacao'] = 0
                app.config['pergunta_atual'] = 0
                return finalizar
            
    else:
        if fase_atual < fase_desbloqueada:      
            finalizar = finalizar_fase_repetida(fase_atual,fase_desbloqueada,pontuacao)
            app.config['pontuacao'] = 0
            app.config['pergunta_atual'] = 0
            return finalizar
        else:
            finalizar = finalizar_fase_fracassada(fase_atual,pontuacao,fase_desbloqueada)
            app.config['pontuacao'] = 0
            app.config['pergunta_atual'] = 0
            return finalizar