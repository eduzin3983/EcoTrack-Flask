# 🌍 EcoTrack - Sistema de Monitoramento de Sustentabilidade Pessoal

O **EcoTrack** é uma plataforma web desenvolvida com **Flask** que permite aos usuários monitorar seu impacto ambiental diário. O sistema oferece ferramentas para registrar dados de consumo, visualizar indicadores, acompanhar históricos e receber sugestões personalizadas para hábitos mais sustentáveis.

---

## 🌱 Funcionalidades

### 🔢 Registro Diário
- Permite que o usuário insira dados diários de consumo:
  - **Água** (litros)
  - **Energia** (kWh)
  - **Resíduos** (kg)
  - **Transporte** (meio utilizado)
- A data é definida automaticamente pelo sistema.

### 📊 Dashboard
- Exibe:
  - **Classificação Geral**: Calculada com base nos registros do usuário.
  - **Indicadores Recentes**: Consumo de água, energia, resíduos e transporte.
  - **Gráficos Interativos**: Médias dos últimos 7 registros (usando Chart.js).
  - **Alertas e Notificações**: Baseados em regras de comparação (ex.: consumo acima da média, redução no consumo, etc.).

### 📋 Histórico
- Lista os registros diários do usuário.
- Oferece filtros por:
  - **Data Inicial e Final**
  - **Ordenação**: Data, consumo de água, energia, resíduos, transporte ou classificação.

### 💡 Sugestões Personalizadas
- Exibe dicas baseadas nos registros dos últimos 7 dias.
- Sugestões categorizadas por:
  - **Tópico**: Água, energia, resíduos e transporte.
  - **Nível de Impacto**: Baixo, Médio ou Alto.

### 🔐 Autenticação
- Gerenciamento de usuários com **Flask-Login**:
  - **Usuários Logados**: Acesso ao Dashboard, Registro, Histórico e Sugestões.
  - **Visitantes**: Acesso às páginas públicas (Home, Sobre, Como Funciona, Login e Cadastro).

---

## 🚀 Tecnologias Utilizadas

- **Back-End**:
  - Flask (Framework Web)
  - Flask-SQLAlchemy (ORM para integração com MySQL)
  - Flask-Login (Gerenciamento de autenticação)
- **Front-End**:
  - HTML5, CSS3 e JavaScript
  - Chart.js (Gráficos interativos)
- **Banco de Dados**:
  - MySQL
- **Outras Ferramentas**:
  - Python 3.10+
  - PyMySQL (Driver para MySQL)

---

## 📂 Estrutura do Projeto

```plaintext
EcoTrack/
├── app/
│   ├── routes/             # Módulo que contém as rotas (blueprints)
│   │   ├── auth.py         # Rotas de autenticação (login, logout, cadastro)
│   │   ├── dashboard.py    # Rotas do dashboard, histórico, registro
│   │   ├── public.py       # Rotas públicas (home, sobre, como-funciona)
│   │   └── sugestoes.py    # Rotas relacionadas às sugestões personalizadas
│   ├── services/           # Lógica adicional (ex.: cálculos, algoritmos)
│   │   └── algoritmos.py   # Funções de cálculo de score e classificação
│   ├── __init__.py         # Inicialização da aplicação Flask
│   ├── errors.py           # Handlers de erros (404, 500, etc.)
│   ├── models.py           # Modelos do SQLAlchemy (Usuários, Registros, Sugestoes)
│   └── utils.py            # Funções utilitárias (ex.: custom_encrypt)
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   ├── img/
│   └── js/
├── templates/              # Templates HTML (páginas do sistema)
│   ├── cadastro.html
│   ├── como-funciona.html
│   ├── dashboard.html
│   ├── erro.html
│   ├── historico.html
│   ├── index.html
│   ├── login.html
│   ├── registro.html
│   ├── sobre.html
│   └── sugestoes.html
├── .gitignore              # Arquivos/pastas ignorados pelo Git
├── config.py               # Configurações da aplicação
├── README.md               # Documentação do projeto
├── requirements.txt        # Dependências do projeto
└── run.py                  # Ponto de entrada para executar a aplicação
```

## 🛠️ Instalação e Execução

### 1. Clonar o Repositório  
```bash
git clone https://github.com/seu_usuario/EcoTrack.git }
```

### 2. Criar e Ativar o Ambiente Virtual  
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate # Linux/macOS
```

```bash
.venv\Scripts\activate # Windows
```

### 3. Instalar as Dependências  
```bash
pip install -r requirements.txt
```

Caso precise instalar as dependências individualmente, use:  
```bash
pip install Flask Flask-SQLAlchemy Flask-Login PyMySQL
```

### 4. Configurar o Banco de Dados  
Crie um banco de dados MySQL chamado `ecotrack` (ou o nome que desejar) usando o MySQL Workbench ou linha de comando.  
Verifique se o usuário e a senha estão configurados corretamente no `app.config['SQLALCHEMY_DATABASE_URI']` no `app.py`.

### 5. Inicializar o Banco de Dados  
```bash
flask init-db
```

Esse comando criará as tabelas (`usuarios`, `registros_diarios`, `sugestoes`) conforme os modelos definidos.

### 6. Popular a Tabela de Sugestões
Para inserir todas as sugestões iniciais (conforme o comando `@app.cli.command("populate-suggestions")` no `app/__init__.py`), execute:
```bash
flask populate-suggestions
```

Cuidado, isso limpará a tabela sugestoes e inserirá novamente todos os registros de dicas.

### 6. Executar o Servidor  
```bash
flask run
```

O servidor será iniciado em `http://127.0.0.1:5000/`.

## 🌐 Uso

- **Home**: Página inicial com informações do EcoTrack.  
- **Sobre / Como Funciona**: Documentação e explicação do funcionamento do sistema.  
- **Cadastro / Login**: Permite criar uma nova conta ou autenticar um usuário.  
- **Dashboard**: Após o login, exibe indicadores, gráficos, notificações e a classificação geral dos dados.  
- **Registrar**: Página para inserir os dados diários (consumo de água, energia, resíduos e transporte).  
- **Histórico**: Exibe os registros cadastrados, com filtros de data e ordenação por diversos parâmetros.  
- **Sugestões**: Exibe dicas personalizadas baseadas nos registros dos últimos 7 dias.

## 💡 Considerações Finais

### Personalização das Sugestões  
As sugestões são selecionadas aleatoriamente a partir de uma tabela de sugestões no banco de dados, de acordo com a classificação (Baixo, Médio, Alto) de cada variável nos últimos 7 registros.

## 🚧 Futuras Melhorias
- **Criação de Algoritmo de Criptografia**: Desenvolver um algoritmo de criptografia baseado em álgebra linear para garantir maior segurança dos dados.
- **Aprimoramento da Interface**: Melhorar a experiência do usuário com ajustes visuais e usabilidade.
- **Refatoração de Código**: Revisar e otimizar o código para maior eficiência e legibilidade.
- **Implementação de Testes Unitários**: Adicionar testes automatizados para validar as funções críticas do sistema.
- **Otimizações Gerais**: Realizar ajustes de desempenho e correções de bugs identificados durante o uso.
  
## 🤝 Contribuição  
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorar o projeto.

## 📄 Licença  
Este projeto é open source.
