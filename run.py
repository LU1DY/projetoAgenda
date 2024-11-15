# importa o app, que é o nosso projeto e a função init_app é a função que inicia o projeto do painel administrativo
from app import app
from app.appAdmin import init_app

# função que executa o projeto do painel administrativo
init_app(app)

# essa estrutura é usada para executar o nosso projeto
if __name__ == '__main__':
    app.run(debug=True)
