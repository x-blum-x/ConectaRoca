# 🌾 ConectaRoça+ API

**ConectaRoça+** é uma API RESTful voltada à gestão integrada para pequenas propriedades rurais. Ela oferece ferramentas acessíveis para controle financeiro, planejamento agrícola, controle de estoque, relatórios gerenciais e acompanhamento da produtividade agrícola. Foi pensada para operar mesmo em áreas com conectividade limitada, com suporte a execução em containers Docker com persistência em banco de dados local (SQLite).

---

## 📦 Módulos da API

### 🔑 1. Autenticação e Usuários

Gerencia perfis e acesso ao sistema com autenticação baseada em JWT. Os dados são armazenados com hash seguro de senha e validação de email.

- `POST /auth/login` — Autenticação usando nome ou email + senha.
- `POST /auth/register` — Cadastro de usuário com nome, email e senha.
- `GET /users/me` — Retorna dados do usuário autenticado.
- `PUT /users/{id}` — Permite atualização de nome e email.

---

### 💰 2. Controle Financeiro

Permite o registro de receitas e despesas, visualização de transações e geração de relatórios financeiros básicos por usuário.

- `POST /finance/transactions` — Cadastra uma transação financeira (receita ou despesa).
- `GET /finance/transactions` — Lista todas as transações filtradas por `user_id`.
- `GET /finance/summary` — Exibe o saldo atual, receita total e despesas acumuladas.
- `GET /finance/cashflow` — Retorna fluxo de uma faixa de tempo determinada.
- `GET /finance/categories` — Lista de categorias típicas para organizar os lançamentos.

---

### 🏪 3. Gestão de Estoque (Inventário)

Gerencia insumos e produtos colhidos, com controle de entrada, saída, localização, peso, valor unitário e total por movimentação.

- `POST /inventory/items` — Cria um novo item de estoque com unidade, categoria e descrição opcional.
- `POST /inventory/movements` — Registra movimentações com cálculo automático de peso e valor total.
- `GET /inventory/balance` — Mostra o saldo atual e valor estimado de cada item por usuário.
- `GET /inventory/history` — Histórico completo das movimentações de um item (entrada e saída).

Campos opcionais disponíveis: `unit_weight`, `unit_price`, `location`, `responsible`, `note`.

---

### 🌱 4. Planejamento de Safra e Atividades

Gerencia o planejamento agrícola, incluindo definição de culturas, etapas de plantio, manejo e colheita com atribuição de tarefas.

- `POST /cropplans` — Criar novo plano de safra.
- `GET /cropplans` — Listar planos existentes.
- `POST /cropplans/{id}/tasks` — Adicionar tarefas agrícolas.
- `PUT /tasks/{id}/status` — Atualizar o status da atividade.
- `GET /tasks/timeline` — Visualizar atividades em formato cronológico.

---

### 📊 5. Relatórios Visuais e Acessíveis *(em construção)*

- `GET /reports/dashboard` — Painel geral da propriedade.
- `GET /reports/finance` — Gráficos de fluxo de caixa e receitas/despesas.
- `GET /reports/productivity` — Produtividade por cultura e área.
- `GET /reports/tasks` — Relatórios de execução de atividades.

---

### 🌾 6. Produtividade por Cultura e Área *(em construção)*

Permite registrar e acompanhar o rendimento por tipo de cultivo e por área específica da propriedade.

- `POST /productivity/records` — Registrar produtividade por área.
- `GET /productivity/by-area` — Comparativo por talhão ou lote.
- `GET /productivity/by-crop` — Históricos por tipo de cultivo.
- `GET /productivity/summary` — Visão geral da produtividade por período.

---

## ✅ Testes Funcionais

### Estrutura básica dos testes

Os testes são implementados com `pytest` + `Flask test client`, com cobertura das principais rotas ativas até o momento:

#### 🔐 Auth

- Verificação de erro com campos ausentes
- Cadastro de novo usuário com email único
- Login com nome ou email + senha
- Geração e verificação de JWT

#### 👤 Users

- Acesso ao perfil usando token JWT
- Atualização de dados com validação

#### 💰 Finanças

- Criação de transações (validação de campos obrigatórios e tipo)
- Listagem filtrada por usuário
- Resumo financeiro com saldo e totais
- Fluxo de caixa agrupado por mês

#### 🏪 Inventário

- Cadastro de novo item com campos opcionais
- Registro de movimentações com cálculo automático
- Cálculo de saldo e valor atual de estoque
- Histórico detalhado e ordenado de movimentações

> Os testes garantem que os dados sejam persistidos corretamente no banco SQLite e que os endpoints respondam conforme esperado em casos válidos e inválidos.

---

## 🔧 Tecnologias Utilizadas

- **Python 3.11 + Flask** (API REST)
- **SQLite 3** (banco de dados local)
- **JWT (PyJWT)** (autenticação segura)
- **Docker + Docker Compose** (ambiente de execução)
- **pytest** (testes automatizados)
- **SQL script loaders** (migrations simples via `models/schema.sql`)

---

## 🚀 Tutorial de Execução

### 🔹 Usando Ambiente Virtual (modo desenvolvimento)

1. Crie e ative o ambiente virtual:

    ```
    python3 -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

2. Instale as dependências:

    ```
    pip install -r requirements.txt
    ```

3. Execute a aplicação:

    ```
    flask run
    ```

    A aplicação estará disponível em: http://localhost:5000

---

### 🔹 Usando Docker Compose (modo produção)

1. Certifique-se de ter **Docker** e **Docker Compose** instalados.

2. Inicie os containers:

    ```
    docker-compose up --build
    ```

    A aplicação estará disponível em: http://localhost:5000

## 📚 Documentação da API

Acesse a documentação interativa das rotas e testes via Postman:

👉 [https://documenter.getpostman.com/view/38182127/2sB2j98UnU](https://documenter.getpostman.com/view/38182127/2sB2j98UnU)