# Funcionamento do bot

## Inicialização

A incialização do bot pelo `main.py` aonde ele vai chamar todos os comandos, inicialização do bot tambem
A inicialização do bot parte por esse ponto

```python
async def carregar_comandos():
    for arquivo in os.listdir("comandos"):
        if arquivo.endswith(".py"):
            await bot.load_extension(f"comandos.{arquivo[:-3]}")

@bot.event
async def on_ready():
    print("Inciand...")
    """Atribui cargos automaticamente a todos os membros ao iniciar o bot."""
    for guild in bot.guilds:
        print(f"Processando guild: {guild.name} (ID: {guild.id})")
        for member in guild.members:
            if not member.bot:  # Ignorar bots
                print(f"Atribuindo cargos para {member.name}")
                await atribuir_cargos(member)
    await carregar_comandos()
    try:
        synced = await bot.tree.sync()  # Sincroniza os comandos de barra
        print(f"Comandos de barra sincronizados: {len(synced)} comandos")
    except Exception as e:
        print(f"Erro ao sincronizar comandos de barra: {e}")
    print(f"Bot {bot.user.name} está online!")

    await bot.change_presence(
        activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="Por todo tempo e espaço"))

    return "Bot Online"
```

## Atribui cargo
Quando a pessoa entrar ela vai atribuir o cargo
```python
async def atribuir_cargos(member: discord.Member):
    id_guild = str(member.guild.id)
    cargos_ids = Obter_cargo.Manipular_Cargo.obter_Cargo(id_guild)
    print(f"Verificando cargos para o guild_id: {id_guild}")
    # Verifica se o membro já possui algum dos cargos
    cargos_do_membro = [
        cargo for cargo in member.roles if cargo.id in map(int, cargos_ids)
    ]
    if cargos_do_membro:
        print(f"{member.name} já tem um dos cargos, ignorando atribuição.")
        return  # Ignora se o membro já tem um dos cargos
    # Escolher um cargo aleatório da lista de cargos
    if cargos_ids:
        cargo_id = random.choice(cargos_ids)  # Escolher um cargo aleatoriamente
        cargo = discord.utils.get(member.guild.roles, id=int(cargo_id))
        if cargo and cargo not in member.roles:
            await member.add_roles(cargo)
            print(f"Cargo {cargo.name} atribuído a {member.name}.")

# Evento quando um membro entra no servidor
@bot.event
async def on_member_join(member: discord.Member):
    """Atribui cargos automaticamente quando um membro entra no servidor."""
    await atribuir_cargos(member)
```

# Inicilização do banco de dados
Usando o `sqlalchemy` chamamos o banco de dados no `/models/db.py`assim :
```python
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///dados.db")
Base = declarative_base()
_Sessao = sessionmaker(engine)
```

# Estrutura

- Models
- Comandos
