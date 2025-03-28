# app/errors.py
from flask import render_template

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return render_template('erro.html',
                               error_code=400,
                               error_name="Bad Request",
                               error_description="A requisição não pôde ser processada."), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('erro.html',
                               error_code=401,
                               error_name="Unauthorized",
                               error_description="Você não está autorizado a acessar este recurso."), 401

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('erro.html',
                               error_code=403,
                               error_name="Forbidden",
                               error_description="Acesso proibido."), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template('erro.html',
                               error_code=404,
                               error_name="Página Não Encontrada",
                               error_description="A página que você procura não foi encontrada."), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('erro.html',
                               error_code=500,
                               error_name="Erro Interno do Servidor",
                               error_description="Ocorreu um erro interno. Tente novamente mais tarde."), 500
