from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import RegistrosDiarios, Sugestoes
from app.services.algoritmos import (classificar_variavel_agua, classificar_variavel_energia, 
                            classificar_variavel_residuos, classificar_variavel_transporte, score_transporte)
import random

sugestoes_bp = Blueprint('sugestoes', __name__)

def get_random_sugestao(topico, impacto):
    sugestoes = Sugestoes.query.filter_by(topico=topico, impacto=impacto).all()
    if not sugestoes:
        return "Nenhuma sugestão encontrada para este tópico/impacto."
    return random.choice(sugestoes).texto_sugestao

@sugestoes_bp.route('/sugestoes')
@login_required
def sugestoes():
    registros = RegistrosDiarios.query.filter_by(user_id=current_user.id)\
                    .order_by(RegistrosDiarios.id.desc())\
                    .limit(7).all()

    if not registros:
        msg_sem_dados = "Você ainda não registrou nenhum dado. Registre seus dados diários para receber sugestões personalizadas."
        return render_template('sugestoes.html', dicas={}, msg_sem_dados=msg_sem_dados)

    avg_agua = sum(r.agua for r in registros) / len(registros)
    avg_energia = sum(r.energia for r in registros) / len(registros)
    avg_residuos = sum(r.residuos for r in registros) / len(registros)
    
    transport_scores = [score_transporte(r.transporte) for r in registros]
    avg_transport_score = sum(transport_scores) / len(transport_scores)

    impacto_agua = classificar_variavel_agua(avg_agua)
    impacto_energia = classificar_variavel_energia(avg_energia)
    impacto_residuos = classificar_variavel_residuos(avg_residuos)
    impacto_transporte = classificar_variavel_transporte(avg_transport_score)

    sugestao_agua = get_random_sugestao('agua', impacto_agua)
    sugestao_energia = get_random_sugestao('energia', impacto_energia)
    sugestao_residuos = get_random_sugestao('residuos', impacto_residuos)
    sugestao_transporte = get_random_sugestao('transporte', impacto_transporte)

    dicas = {
        'agua': sugestao_agua,
        'energia': sugestao_energia,
        'residuos': sugestao_residuos,
        'transporte': sugestao_transporte
    }

    return render_template('sugestoes.html', dicas=dicas)
