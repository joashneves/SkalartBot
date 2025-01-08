# Comando para baixar as dependências e iniciar o bot

### Ao clonar o repositório com Python já instalado

1. O primeiro comando para instalar as dependências:
   ```bash
   pip install -e .
   ```

2. O segundo comando para iniciar o bot:
   ```bash
   discord-bot
   ```

---

# Pré-commit Hook

Para garantir que o código esteja formatado corretamente e sem erros de estilo, é recomendado usar o **pre-commit**. Isso ajuda a automatizar o processo de formatação e linting.

### Passos para configurar o pre-commit:

1. Instalar o `pre-commit`:
   ```bash
   pip install pre-commit
   ```

2. Instalar os hooks configurados no projeto:
   ```bash
   pre-commit install
   ```

3. Para atualizar os hooks:
   ```bash
   pre-commit autoupdate
   ```

Isso instalará o hook do `black` para formatação de código e o `pylint` para análise estática, garantindo que o código esteja limpo antes de cada commit.

---

# As Issues

As issues são as tarefas a serem feitas e estão organizadas dentro de milestones. Você pode conferir as tarefas [aqui](https://github.com/joashneves/SkalartBot/issues).

---

# O objetivo

O objetivo deste projeto é desenvolver um bot de Discord em conjunto, enquanto se aprimora o uso do GitHub para colaboração e controle de versões.
