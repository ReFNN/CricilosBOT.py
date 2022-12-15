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
    bot = commands.Bot(command_prefix="m!", intents=discord.Intents.all())
    TOKEN = 'MTA1MTU2NzIyNTQ2ODg4NzIwMQ.G3r7E9.k0fT27wPU5EO3AMluiPCUpLb1cK1hXXmlquzXk'
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} ta rodando o fino!')
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Bot em desenvolvimento"))
        try:
            synced = await bot.tree.sync()
            print(f"Sincronizado {len(synced)} comando(s)")
        except Exception as e:
            print(f"deu erro no sincronismo", e)

    @client.event
    async def on_message(message):
        # Certificando de que o bot não fique preso em um loop infinito
        if message.author == client.user:
            return

        # Obter dados sobre o usuário
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")

        # Se a mensagem do usuário contiver um '?' na frente do texto, torna-se uma mensagem privada
        if user_message[0] == '?':
            user_message = user_message[1:]  # [1:] Remove o '?'
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    # Rodando o bot
    client.run(TOKEN)
    bot.run(TOKEN)
