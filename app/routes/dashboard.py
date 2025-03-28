# app/routes/dashboard.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, timezone
from app.models import RegistrosDiarios
from app import db
from app.services.algoritmos import (calcular_score_registro, classificar_score, classificar_variavel_agua, 
                            classificar_variavel_energia, classificar_variavel_residuos, classificar_variavel_transporte, score_transporte)

dashboard_bp = Blueprint('dashboard', __name__)

# Mapeamento para exibição dos nomes dos transportes
TRANSPORTE_MAP = {
    "transporte_publico": "Transporte Público",
    "bicicleta": "Bicicleta",
    "caminhada": "Caminhada",
    "carro": "Carro",
    "carro_eletrico": "Carro Elétrico",
    "carona_compartilhada": "Carona Compartilhada"
}

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    registros = RegistrosDiarios.query.filter_by(user_id=current_user.id).all()
    notifications = []
    if registros:
        total_score = sum(calcular_score_registro(reg.agua, reg.energia, reg.residuos, reg.transporte) for reg in registros)
        score_medio = total_score / len(registros)
        classificacao_geral = classificar_score(score_medio)
    else:
        score_medio = 0
        classificacao_geral = "Sem Dados Registrados."

    records = RegistrosDiarios.query.filter_by(user_id=current_user.id).order_by(RegistrosDiarios.id.desc()).limit(7).all()

    if records:
        water_values = [r.agua for r in records]
        energy_values = [r.energia for r in records]
        residuos_values = [r.residuos for r in records]

        avg_water = sum(water_values) / len(water_values)
        avg_energy = sum(energy_values) / len(energy_values)
        avg_residuos = sum(residuos_values) / len(residuos_values)

        last_record = records[0]
        agua_recente = last_record.agua
        energia_recente = last_record.energia
        residuos_recente = last_record.residuos
        transporte_bruto = last_record.transporte
        transporte_recente = TRANSPORTE_MAP.get(transporte_bruto, "Desconhecido")

        penultimo_record = records[1] if len(records) > 1 else None

        if agua_recente > avg_water * 1.2:
            notifications.append("Seu consumo de água hoje está 20% acima da média.")

        if penultimo_record and energia_recente < penultimo_record.energia * 0.9:
            notifications.append("O consumo de energia apresentou uma redução de 10% em relação ao dia anterior.")

        if score_medio > 0.6:
            notifications.append("Verifique as sugestões para melhorar seu índice de sustentabilidade.")

        if agua_recente < avg_water * 0.8:
            notifications.append("Ótimo! Seu consumo de água está 20% abaixo da sua média. Continue assim!")

        if energia_recente > 8:
            notifications.append("Atenção! Seu consumo de energia ultrapassou 8 kWh. Tente reduzir aparelhos em stand-by.")

        if residuos_recente > 2:
            notifications.append("Você gerou mais de 2 kg de resíduos hoje. Busque separar materiais recicláveis e reutilizar embalagens.")

        if penultimo_record and penultimo_record.transporte == "carro" and last_record.transporte in ["bicicleta", "caminhada", "transporte_publico"]:
            notifications.append("Parabéns! Você optou por um meio de transporte mais sustentável hoje.")

        carro_count = sum(1 for r in records if r.transporte == "carro")
        if carro_count > (len(records) / 2):
            notifications.append("Você tem usado muito o carro nos últimos dias. Considere opções como carona, bicicleta ou transporte público.")
    else:
        avg_water = avg_energy = avg_residuos = 0
        agua_recente = energia_recente = residuos_recente = 0
        transporte_recente = "N/A"

    data_chart = {
        "agua": avg_water,
        "energia": avg_energy,
        "residuos": avg_residuos,
    }

    return render_template(
        'dashboard.html',
        data_chart=data_chart,
        agua_recente=agua_recente,
        energia_recente=energia_recente,
        residuos_recente=residuos_recente,
        transporte_recente=transporte_recente,
        classificacao_geral=classificacao_geral,
        notifications=notifications
    )

@dashboard_bp.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar():
    if request.method == 'POST':
        record_date = datetime.now(timezone.utc).date()
        agua = request.form.get('agua')
        energia = request.form.get('energia')
        residuos = request.form.get('residuos')
        transporte = request.form.get('transporte')

        try:
            agua = float(agua)
            energia = float(energia)
            residuos = float(residuos)
        except Exception:
            flash("Erro na conversão dos dados. Verifique os valores informados.", "danger")
            return render_template('registro.html')

        new_record = RegistrosDiarios(
            user_id=current_user.id,
            data_registro=record_date,
            agua=agua,
            energia=energia,
            residuos=residuos,
            transporte=transporte
        )
        db.session.add(new_record)
        db.session.commit()
        
        flash("Dados registrados com sucesso!", "success")
        return redirect(url_for('dashboard.registrar'))
    else:
        return render_template('registro.html')

@dashboard_bp.route('/historico', methods=['GET'])
@login_required
def historico():
    data_inicio_str = request.args.get('dataInicio', '')
    data_fim_str = request.args.get('dataFim', '')
    ordenar = request.args.get('ordenar', 'data_desc')

    query = RegistrosDiarios.query.filter_by(user_id=current_user.id)
    if data_inicio_str:
        try:
            from datetime import datetime
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
            query = query.filter(RegistrosDiarios.data_registro >= data_inicio)
        except ValueError:
            flash("Formato de data inicial inválido (use YYYY-MM-DD).", "danger")
    if data_fim_str:
        try:
            from datetime import datetime
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
            query = query.filter(RegistrosDiarios.data_registro <= data_fim)
        except ValueError:
            flash("Formato de data final inválido (use YYYY-MM-DD).", "danger")

    if ordenar == 'data_desc':
        query = query.order_by(RegistrosDiarios.created_at.desc())
    elif ordenar == 'data_asc':
        query = query.order_by(RegistrosDiarios.created_at.asc())
    elif ordenar == 'agua':
        query = query.order_by(RegistrosDiarios.agua.desc())
    elif ordenar == 'energia':
        query = query.order_by(RegistrosDiarios.energia.desc())
    elif ordenar == 'residuos':
        query = query.order_by(RegistrosDiarios.residuos.desc())

    registros = query.all()

    dados_registros = []
    for reg in registros:
        score = calcular_score_registro(reg.agua, reg.energia, reg.residuos, reg.transporte)
        classificacao = classificar_score(score)
        transporte_amigavel = TRANSPORTE_MAP.get(reg.transporte, reg.transporte)
        dados_registros.append({
            "data_registro": reg.data_registro,
            "agua": reg.agua,
            "energia": reg.energia,
            "residuos": reg.residuos,
            "transporte": transporte_amigavel,
            "classificacao": classificacao,
            "score": score,
        })

    if ordenar == 'classificacao':
        dados_registros.sort(key=lambda x: x["score"])
    elif ordenar == 'transporte':
        dados_registros.sort(key=lambda x: x.get("transporte"))

    return render_template('historico.html', dados_registros=dados_registros)
