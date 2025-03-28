from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from app.models import Usuarios  # Importação local para evitar importação circular
    return Usuarios.query.get(int(user_id))

def create_app():
    # Criação da aplicação com as pastas de templates e estáticos configuradas
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Registro dos blueprints
    from app.routes.public import public_bp
    app.register_blueprint(public_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.sugestoes import sugestoes_bp
    app.register_blueprint(sugestoes_bp)

    # Registro dos handlers de erro
    from app.errors import register_error_handlers
    register_error_handlers(app)

    # Função de comando CLI
    register_cli_commands(app)

    return app

def register_cli_commands(app):
    # Cria Tabelas do Banco
    @app.cli.command("init-db")
    def init_db():
        """Cria todas as tabelas no banco de dados."""
        from app import db
        db.create_all()
        print("Banco de dados criado com sucesso!")

    # Popula Tabela Sugestões
    @app.cli.command("populate-suggestions")
    def populate_suggestions():

        from app.models import Sugestoes

        Sugestoes.query.delete()

        data = [
            # AGUA - BAIXO
            {"topico": "agua", "impacto": "Baixo", "texto_sugestao": "Parabéns! Seu consumo de água está em um nível exemplar. Continue assim para manter a sustentabilidade."},
            {"topico": "agua", "impacto": "Baixo", "texto_sugestao": "Seu consumo de água está dentro do ideal. Mantenha os hábitos de economia que já pratica."},
            {"topico": "agua", "impacto": "Baixo", "texto_sugestao": "Continue verificando vazamentos e consertando-os rapidamente para manter seu baixo consumo de água."},
            {"topico": "agua", "impacto": "Baixo", "texto_sugestao": "Você está economizando água de forma exemplar! Incentive amigos e familiares a seguirem seu exemplo."},
            {"topico": "agua", "impacto": "Baixo", "texto_sugestao": "Seu banho rápido e consciente faz diferença. Mantenha essa prática para preservar recursos hídricos."},
            {"topico": "agua", "impacto": "Baixo", "texto_sugestao": "Com seu nível de consumo, você contribui ativamente para a preservação de rios e mananciais."},
            {"topico": "agua", "impacto": "Baixo", "texto_sugestao": "Parabéns por usar baldes para reutilizar água da máquina de lavar ou do banho!"},
            {"topico": "agua", "impacto": "Baixo", "texto_sugestao": "Você já atingiu um consumo baixo de água. Continue monitorando para manter esse excelente resultado."},
            {"topico": "agua", "impacto": "Baixo", "texto_sugestao": "Seu cuidado ao escovar os dentes e lavar a louça com a torneira fechada está ajudando muito."},
            {"topico": "agua", "impacto": "Baixo", "texto_sugestao": "Ótimo trabalho! Ao lavar o carro ou quintal, mantenha o uso de baldes em vez de mangueira para continuar nesse patamar."},

            # AGUA - MÉDIO
            {"topico": "agua", "impacto": "Médio", "texto_sugestao": "Seu consumo de água é moderado, mas ainda há espaço para redução. Experimente reduzir alguns minutos do banho."},
            {"topico": "agua", "impacto": "Médio", "texto_sugestao": "Verifique se existem pequenos vazamentos em torneiras ou descargas para diminuir ainda mais o consumo."},
            {"topico": "agua", "impacto": "Médio", "texto_sugestao": "Procure reutilizar água da máquina de lavar para limpeza de pisos ou irrigação de plantas."},
            {"topico": "agua", "impacto": "Médio", "texto_sugestao": "Seu nível de consumo de água está na média. Que tal usar redutores de vazão em chuveiros e torneiras?"},
            {"topico": "agua", "impacto": "Médio", "texto_sugestao": "Mantenha um balde no chuveiro para coletar água enquanto ela esquenta, reaproveitando-a em outras tarefas."},
            {"topico": "agua", "impacto": "Médio", "texto_sugestao": "Você pode reduzir o consumo usando regadores em vez de mangueira para regar as plantas."},
            {"topico": "agua", "impacto": "Médio", "texto_sugestao": "Sempre que possível, opte por louças sanitárias econômicas e duchas de baixo fluxo."},
            {"topico": "agua", "impacto": "Médio", "texto_sugestao": "Para continuar progredindo, tente reduzir 1 minuto do seu banho diário e veja a diferença no fim do mês."},
            {"topico": "agua", "impacto": "Médio", "texto_sugestao": "Faça um teste de vazamentos no hidrômetro antes de viajar ou ficar fora de casa por muito tempo."},
            {"topico": "agua", "impacto": "Médio", "texto_sugestao": "Você está no caminho certo. Pequenos ajustes diários podem levar seu consumo de água ao nível ideal."},

            # AGUA - ALTO
            {"topico": "agua", "impacto": "Alto", "texto_sugestao": "Seu consumo de água está acima do recomendado. Considere banhos mais curtos para reduzir o gasto."},
            {"topico": "agua", "impacto": "Alto", "texto_sugestao": "Evite lavar calçadas com mangueira. Use balde e vassoura para economizar litros preciosos."},
            {"topico": "agua", "impacto": "Alto", "texto_sugestao": "Verifique vazamentos imediatamente. Um simples gotejamento pode elevar muito seu consumo."},
            {"topico": "agua", "impacto": "Alto", "texto_sugestao": "Repense o uso de máquinas de lavar roupas e louças: procure sempre usar a capacidade máxima."},
            {"topico": "agua", "impacto": "Alto", "texto_sugestao": "Se possível, instale arejadores de torneira e chuveiros de baixo fluxo para reduzir drasticamente o consumo."},
            {"topico": "agua", "impacto": "Alto", "texto_sugestao": "Mantenha um copo de água na geladeira em vez de deixar a torneira aberta esperando esfriar."},
            {"topico": "agua", "impacto": "Alto", "texto_sugestao": "Fique atento ao hidrômetro. Leituras muito altas podem indicar vazamentos ou uso excessivo."},
            {"topico": "agua", "impacto": "Alto", "texto_sugestao": "Use bacias para lavar frutas e verduras em vez de água corrente por muito tempo."},
            {"topico": "agua", "impacto": "Alto", "texto_sugestao": "Evite mangueiras pressurizadas ao limpar o carro; prefira baldes e panos para controlar melhor o uso de água."},
            {"topico": "agua", "impacto": "Alto", "texto_sugestao": "Seu consumo está alto, mas com mudanças simples é possível economizar litros todos os dias. Tente reduzir alguns minutos de cada banho e verifique vazamentos."},

            # ENERGIA - BAIXO
            {"topico": "energia", "impacto": "Baixo", "texto_sugestao": "Parabéns! Seu consumo de energia está excelente. Continue apagando as luzes ao sair de cada ambiente."},
            {"topico": "energia", "impacto": "Baixo", "texto_sugestao": "Mantenha seus equipamentos em modo de economia de energia quando possível."},
            {"topico": "energia", "impacto": "Baixo", "texto_sugestao": "Seu uso consciente de aparelhos eletrônicos contribui para a redução das emissões de CO2."},
            {"topico": "energia", "impacto": "Baixo", "texto_sugestao": "Continue aproveitando a luz natural e evitando lâmpadas acesas desnecessariamente."},
            {"topico": "energia", "impacto": "Baixo", "texto_sugestao": "Seu hábito de desligar equipamentos em stand-by é ótimo para manter o baixo consumo de energia."},
            {"topico": "energia", "impacto": "Baixo", "texto_sugestao": "Incentive outros a seguirem seu exemplo: cada aparelho desligado faz diferença na conta de luz."},
            {"topico": "energia", "impacto": "Baixo", "texto_sugestao": "Seu consumo está abaixo da média. Isso ajuda a diminuir o uso de termelétricas e poluição."},
            {"topico": "energia", "impacto": "Baixo", "texto_sugestao": "Você está fazendo um excelente trabalho em relação à eficiência energética!"},
            {"topico": "energia", "impacto": "Baixo", "texto_sugestao": "Troque lâmpadas incandescentes por LEDs para manter e até melhorar seu baixo consumo."},
            {"topico": "energia", "impacto": "Baixo", "texto_sugestao": "Seu nível de consumo de energia é exemplar. Continue assim e compartilhe dicas com amigos."},

            # ENERGIA - MÉDIO
            {"topico": "energia", "impacto": "Médio", "texto_sugestao": "Você está em um nível moderado de consumo de energia. Considere trocar lâmpadas comuns por LEDs."},
            {"topico": "energia", "impacto": "Médio", "texto_sugestao": "Desligue os aparelhos da tomada quando não estiverem em uso para reduzir o consumo stand-by."},
            {"topico": "energia", "impacto": "Médio", "texto_sugestao": "Aproveite mais a luz natural, abrindo cortinas e janelas ao longo do dia."},
            {"topico": "energia", "impacto": "Médio", "texto_sugestao": "Mantenha a manutenção de ar-condicionado em dia, limpando filtros para melhorar a eficiência."},
            {"topico": "energia", "impacto": "Médio", "texto_sugestao": "Use régua de tomadas para desligar vários aparelhos simultaneamente ao sair."},
            {"topico": "energia", "impacto": "Médio", "texto_sugestao": "Escolha eletrodomésticos com selo Procel de eficiência energética para reduzir ainda mais o consumo."},
            {"topico": "energia", "impacto": "Médio", "texto_sugestao": "Procure usar ferro de passar roupas e máquina de lavar em horários de menor demanda."},
            {"topico": "energia", "impacto": "Médio", "texto_sugestao": "Seu consumo de energia é razoável, mas pequenas ações diárias podem torná-lo ainda melhor."},
            {"topico": "energia", "impacto": "Médio", "texto_sugestao": "Verifique se suas lâmpadas são compatíveis com a potência ideal para cada ambiente."},
            {"topico": "energia", "impacto": "Médio", "texto_sugestao": "Faça um checklist semanal de aparelhos que podem ficar desligados quando não estiverem em uso."},

            # ENERGIA - ALTO
            {"topico": "energia", "impacto": "Alto", "texto_sugestao": "Seu consumo de energia está acima do recomendado. Evite deixar aparelhos em stand-by."},
            {"topico": "energia", "impacto": "Alto", "texto_sugestao": "Desligue o ar-condicionado quando não houver ninguém no ambiente e mantenha portas e janelas fechadas."},
            {"topico": "energia", "impacto": "Alto", "texto_sugestao": "Invista em lâmpadas LED para substituir incandescentes e halógenas, reduzindo até 80% do consumo."},
            {"topico": "energia", "impacto": "Alto", "texto_sugestao": "Revise a borracha de vedação da geladeira e evite abrir a porta com frequência."},
            {"topico": "energia", "impacto": "Alto", "texto_sugestao": "Procure secar roupas ao sol em vez de usar a secadora, economizando muita energia."},
            {"topico": "energia", "impacto": "Alto", "texto_sugestao": "Desligue a TV e outros eletrônicos se não estiver assistindo ou usando ativamente."},
            {"topico": "energia", "impacto": "Alto", "texto_sugestao": "Evite banhos muito longos com chuveiro elétrico. Ele é um dos maiores vilões da conta de luz."},
            {"topico": "energia", "impacto": "Alto", "texto_sugestao": "Instale um medidor de energia individual para identificar onde está o maior consumo."},
            {"topico": "energia", "impacto": "Alto", "texto_sugestao": "Tente concentrar o uso de aparelhos de alta potência em horários alternados para não sobrecarregar o sistema."},
            {"topico": "energia", "impacto": "Alto", "texto_sugestao": "Considere a instalação de painéis solares se possível, diminuindo seu consumo da rede elétrica."},

            # RESIDUOS - BAIXO
            {"topico": "residuos", "impacto": "Baixo", "texto_sugestao": "Parabéns! Você gera poucos resíduos e isso ajuda a reduzir a poluição e a demanda por aterros."},
            {"topico": "residuos", "impacto": "Baixo", "texto_sugestao": "Continue separando adequadamente seu lixo para reciclagem, mantendo esse baixo volume."},
            {"topico": "residuos", "impacto": "Baixo", "texto_sugestao": "Seu nível de resíduos é exemplar. Considere compartilhar dicas de redução de lixo com amigos."},
            {"topico": "residuos", "impacto": "Baixo", "texto_sugestao": "Você está contribuindo para a sustentabilidade ao evitar produtos descartáveis em excesso."},
            {"topico": "residuos", "impacto": "Baixo", "texto_sugestao": "Parabéns por usar recipientes reutilizáveis em vez de sacolas plásticas."},
            {"topico": "residuos", "impacto": "Baixo", "texto_sugestao": "Se possível, faça compostagem dos resíduos orgânicos para fechar o ciclo de maneira sustentável."},
            {"topico": "residuos", "impacto": "Baixo", "texto_sugestao": "Seu consumo consciente de embalagens mantém a geração de resíduos em um nível muito bom."},
            {"topico": "residuos", "impacto": "Baixo", "texto_sugestao": "Continue comprando a granel e evitando embalagens desnecessárias para manter esse ótimo resultado."},
            {"topico": "residuos", "impacto": "Baixo", "texto_sugestao": "Seu esforço em reutilizar e reciclar está fazendo diferença na diminuição do lixo geral."},
            {"topico": "residuos", "impacto": "Baixo", "texto_sugestao": "Inspire outras pessoas a adotarem práticas de redução de resíduos como você faz."},

            # RESIDUOS - MÉDIO
            {"topico": "residuos", "impacto": "Médio", "texto_sugestao": "Você gera uma quantidade moderada de resíduos. Tente substituir produtos descartáveis por reutilizáveis."},
            {"topico": "residuos", "impacto": "Médio", "texto_sugestao": "Separe e recicle o lixo para reduzir o que vai para aterros. Isso pode baixar ainda mais seu volume de resíduos."},
            {"topico": "residuos", "impacto": "Médio", "texto_sugestao": "Reutilize potes e recipientes para armazenamento em vez de jogá-los fora."},
            {"topico": "residuos", "impacto": "Médio", "texto_sugestao": "Avalie seu consumo de embalagens plásticas e tente optar por produtos com menos plástico."},
            {"topico": "residuos", "impacto": "Médio", "texto_sugestao": "Evite desperdício de alimentos, planejando as refeições e armazenando-os corretamente."},
            {"topico": "residuos", "impacto": "Médio", "texto_sugestao": "Procure levar sua própria sacola reutilizável ao fazer compras."},
            {"topico": "residuos", "impacto": "Médio", "texto_sugestao": "Antes de descartar, verifique se algo pode ser consertado ou doado, prolongando sua vida útil."},
            {"topico": "residuos", "impacto": "Médio", "texto_sugestao": "Para reduzir o lixo, evite impressões desnecessárias e opte por documentos digitais."},
            {"topico": "residuos", "impacto": "Médio", "texto_sugestao": "Invista em garrafas de água e canecas reutilizáveis para o dia a dia."},
            {"topico": "residuos", "impacto": "Médio", "texto_sugestao": "Seu nível de resíduos pode melhorar. Identifique o que mais gera lixo e busque alternativas sustentáveis."},

            # RESIDUOS - ALTO
            {"topico": "residuos", "impacto": "Alto", "texto_sugestao": "Você está gerando muitos resíduos. Tente reduzir embalagens e opte por produtos a granel."},
            {"topico": "residuos", "impacto": "Alto", "texto_sugestao": "Evite produtos descartáveis, como copos e talheres de plástico. Use versões reutilizáveis."},
            {"topico": "residuos", "impacto": "Alto", "texto_sugestao": "Verifique se está separando corretamente o lixo reciclável. Isso reduz muito o volume final."},
            {"topico": "residuos", "impacto": "Alto", "texto_sugestao": "Planeje suas compras para evitar desperdício de alimentos e produtos."},
            {"topico": "residuos", "impacto": "Alto", "texto_sugestao": "Busque comprar em embalagens retornáveis ou grandes, diminuindo o lixo gerado."},
            {"topico": "residuos", "impacto": "Alto", "texto_sugestao": "Considere iniciar uma composteira doméstica para resíduos orgânicos, reduzindo o lixo comum."},
            {"topico": "residuos", "impacto": "Alto", "texto_sugestao": "Doe roupas e objetos que não usa mais, em vez de descartá-los diretamente."},
            {"topico": "residuos", "impacto": "Alto", "texto_sugestao": "Seu lixo está alto. Procure soluções de reciclagem e reuso em sua cidade ou condomínio."},
            {"topico": "residuos", "impacto": "Alto", "texto_sugestao": "Evite impressões desnecessárias e priorize arquivos digitais para reduzir papel descartado."},
            {"topico": "residuos", "impacto": "Alto", "texto_sugestao": "Reduza o consumo de produtos supérfluos. Cada compra consciente ajuda a diminuir o lixo gerado."},

            # TRANSPORTE - BAIXO
            {"topico": "transporte", "impacto": "Baixo", "texto_sugestao": "Excelente! Seu uso de meios de transporte sustentáveis está ajudando a reduzir emissões."},
            {"topico": "transporte", "impacto": "Baixo", "texto_sugestao": "Continue optando por caminhada ou bicicleta sempre que possível."},
            {"topico": "transporte", "impacto": "Baixo", "texto_sugestao": "Você está contribuindo para menos congestionamentos e menor poluição do ar."},
            {"topico": "transporte", "impacto": "Baixo", "texto_sugestao": "Incentive amigos a se unirem a você em caronas ou uso de transporte público."},
            {"topico": "transporte", "impacto": "Baixo", "texto_sugestao": "Seu hábito de usar bicicleta ou caminhar melhora a saúde e o meio ambiente."},
            {"topico": "transporte", "impacto": "Baixo", "texto_sugestao": "Parabéns por priorizar alternativas limpas de locomoção. Mantenha-se motivado!"},
            {"topico": "transporte", "impacto": "Baixo", "texto_sugestao": "Se possível, organize um grupo de carona compartilhada em seu trabalho ou faculdade."},
            {"topico": "transporte", "impacto": "Baixo", "texto_sugestao": "Seu baixo impacto em transporte reflete um estilo de vida mais saudável e consciente."},
            {"topico": "transporte", "impacto": "Baixo", "texto_sugestao": "Avalie a possibilidade de usar transporte público em outras rotas para manter esse padrão."},
            {"topico": "transporte", "impacto": "Baixo", "texto_sugestao": "Continue pesquisando rotas de ciclovias e faixas de pedestre para expandir ainda mais sua mobilidade sustentável."},

            # TRANSPORTE - MÉDIO
            {"topico": "transporte", "impacto": "Médio", "texto_sugestao": "Você utiliza meios de transporte moderadamente sustentáveis. Que tal reduzir o uso do carro em pequenas distâncias?"},
            {"topico": "transporte", "impacto": "Médio", "texto_sugestao": "Avalie substituir parte dos trajetos por bicicleta ou caminhada para melhorar ainda mais seu impacto."},
            {"topico": "transporte", "impacto": "Médio", "texto_sugestao": "Opte por transporte público em alguns dias da semana para reduzir emissões."},
            {"topico": "transporte", "impacto": "Médio", "texto_sugestao": "Compartilhar caronas é uma forma de diminuir custos e poluição ao mesmo tempo."},
            {"topico": "transporte", "impacto": "Médio", "texto_sugestao": "Procure planejar rotas e horários para evitar congestionamentos e reduzir o tempo de deslocamento."},
            {"topico": "transporte", "impacto": "Médio", "texto_sugestao": "Mantenha a manutenção do carro ou moto em dia, pois isso melhora a eficiência de combustível."},
            {"topico": "transporte", "impacto": "Médio", "texto_sugestao": "Se possível, estacione em um ponto estratégico e complete o restante do percurso a pé ou de bicicleta."},
            {"topico": "transporte", "impacto": "Médio", "texto_sugestao": "Experimente revezar a direção com colegas de trabalho para diminuir o número de veículos nas ruas."},
            {"topico": "transporte", "impacto": "Médio", "texto_sugestao": "Seu impacto é moderado. Com alguns ajustes, pode chegar a um nível ainda mais sustentável."},
            {"topico": "transporte", "impacto": "Médio", "texto_sugestao": "Verifique se há aplicativos de carona compartilhada que possam ser úteis em sua rotina."},

            # TRANSPORTE - ALTO
            {"topico": "transporte", "impacto": "Alto", "texto_sugestao": "Seu uso de transporte gera alto impacto. Tente trocar o carro por transporte público ou bicicleta em algumas viagens."},
            {"topico": "transporte", "impacto": "Alto", "texto_sugestao": "Considere combinar caronas com colegas, diminuindo o número de carros na rua."},
            {"topico": "transporte", "impacto": "Alto", "texto_sugestao": "Verifique se existe uma estação de metrô ou trem próxima para viagens mais longas."},
            {"topico": "transporte", "impacto": "Alto", "texto_sugestao": "Avalie a possibilidade de adquirir um carro elétrico ou híbrido, caso seja viável."},
            {"topico": "transporte", "impacto": "Alto", "texto_sugestao": "Evite usar o carro para pequenas distâncias. Caminhar ou pedalar é mais saudável e menos poluente."},
            {"topico": "transporte", "impacto": "Alto", "texto_sugestao": "Pesquise linhas de ônibus que atendam suas rotas frequentes e verifique os horários para melhor planejamento."},
            {"topico": "transporte", "impacto": "Alto", "texto_sugestao": "Caso more perto do trabalho, tente caminhar ou pedalar pelo menos uma vez na semana."},
            {"topico": "transporte", "impacto": "Alto", "texto_sugestao": "Faça manutenção regular do veículo para melhorar a eficiência de combustível e reduzir emissões."},
            {"topico": "transporte", "impacto": "Alto", "texto_sugestao": "Considere aplicativos de carona ou táxi compartilhado para evitar usar o carro sozinho."},
            {"topico": "transporte", "impacto": "Alto", "texto_sugestao": "Seu impacto em transporte é alto, mas pequenas mudanças diárias podem fazer diferença na redução de CO2."}
        ]

        # Inserir os registros
        for item in data:
            nova_sugestao = Sugestoes(
                topico=item["topico"],
                impacto=item["impacto"],
                texto_sugestao=item["texto_sugestao"]
            )
            db.session.add(nova_sugestao)

            db.session.commit()
            print("Sugestões inseridas com sucesso!")