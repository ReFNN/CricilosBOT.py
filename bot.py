import discord
from discord.ext import commands
import responses


# Send messages
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTA1MTU2NzIyNTQ2ODg4NzIwMQ.GZMM9k.YVqfk4gmAGe4oURXFO7S3-T7dgj5x-Nz_A-bWI'
    bot = commands.Bot(command_prefix="", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f'{bot.user} ta rodando o fino!')
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Bot em desenvolvimento"))
        try:
            synced = await bot.tree.sync()
            print(f"Sincronizado {len(synced)} comando(s)")
        except Exception as e:
            print(f"deu erro no sincronismo", e)

    @bot.event
    async def on_message(message):
        # Certificando de que o bot não fique preso em um loop infinito
        if message.author == bot.user:
            return

        # Obter dados sobre o usuário
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Debug printing
        print(f"{username} disse: '{user_message}' ({channel})")

        # Se a mensagem do usuário contiver um '?' na frente do texto, torna-se uma mensagem privada
        if user_message[0] == '?':
            user_message = user_message[1:]  # [1:] Remove o '?'
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    @bot.tree.command(name="help", description="Visualizar comandos do bot")
    async def help(interaction: discord.Interaction):
        await interaction.response.send_message(f"`{interaction.user.mention}, esse comando não está pronto ainda.` :face_with_peeking_eye:")

    @bot.tree.command(name="help", description="Visualizar comandos do bot")
    async def help(interaction: discord.Interaction):
        await interaction.response.send_message(f"`{interaction.user.mention}, esse comando não está pronto ainda.` :face_with_peeking_eye:")

    @bot.tree.command(name="desligar", description="Desliga o bot")
    async def desativar(interaction: discord.Interaction):
        await interaction.response.send_message(f"O bot foi desligado por {interaction.user.mention}! fdp")
        quit()

    # Rodando o bot
    bot.run(TOKEN)
