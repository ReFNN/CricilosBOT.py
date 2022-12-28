import discord
from discord.ext import commands
import responses


# EVITA LOOP AO ENVIAR MSG
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


TOKEN = 'TOKEN APAGADO PRA EVITAR ACESSO NÃO AUTORIZADO'
bot = commands.Bot(command_prefix="", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'{bot.user} ta online!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Bot em desenvolvimento"))
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizado {len(synced)} comando(s)")
    except Exception as e:
        print(f"Erro em sincronizar comandos: ", e)


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

    # Se a mensagem do usuário contiver um '?' na frente do texto,
    # torna-se uma mensagem privada
    if user_message[0] == '?':
        user_message = user_message[1:]  # [1:] Remove o '?'
        await send_message(message, user_message, is_private=True)
    else:
        await send_message(message, user_message, is_private=False)


###################################################
########### VISUALIZAR COMANDOS DO BOT ############
###################################################
@bot.tree.command(name="help", description="Visualizar comandos do bot")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f"`{interaction.user.mention}, esse comando não está pronto ainda.` :face_with_peeking_eye:")


###################################################
############## ABRIR TICKET NO SUPORTE ############
###################################################
@bot.tree.command(name="suporte", description="Abre um ticket no suporte")
async def suporte(interaction: discord.Interaction):
    await interaction.response.send_message(f"`{interaction.user.mention}, esse comando não está pronto ainda.` :face_with_peeking_eye:")


###################################################
############### DESATIVAR O BOT ###################
###################################################
@bot.tree.command(name="desligar", description="Desliga o bot")
async def desativar(interaction: discord.Interaction):
    await interaction.response.send_message(f"O bot foi desligado por {interaction.user.mention}! fdp")
    quit()


###################################################
##### FERRAMENTA VERIFICADOR DE LATÊNCIA/PING #####
###################################################
@bot.tree.command(name="ping", description="Verifica o tempo de resposta do bot")
async def ping(interaction: discord.Interaction):
    pingEmbed = discord.Embed(title="VERIFICAR LATÊNCIA DO CRICILOS BOT",
                              description="Use para verificar a latência do bot.", color=0xeb0000)
    pingEmbed.set_author(name="by ReFN#0847", url='https://github.com/erickkdev',
                         icon_url='https://cdn.discordapp.com/attachments/1053125437125042267/1053127644352352347/criciloscircle.png')
    pingEmbed.add_field(name="Latência(Ping)",
                        value=f"{round(bot.latency * 1000)}ms", inline=False)
    pingEmbed.set_footer(text="@erickkdev",
                         icon_url='https://cdn.discordapp.com/attachments/1053125437125042267/1053126406470631434/25231.png')
    await interaction.response.send_message(embed=pingEmbed)


###################################################
##### FERRAMENTA VERIFICADOR DE LATÊNCIA/PING #####
###################################################
@bot.tree.command(name="clear", description="Verifica o tempo de resposta do bot")
async def clear(interaction: discord.Interaction, quantidade: int):
    try:
        deletado = await interaction.channel.purge(limit=quantidade+1)
    except Exception as e:
        print(
            f"Infelizmente ocorreu um erro ao deletar as mensagens :( . Informe esse erro: {e}.")
    if len(deletado) == 1:
        await interaction.response.send_message(f"Foram apagadas {len(deletado)} mensagens! Por {interaction.user.mention}")
    elif quantidade == 0:
        await interaction.response.send_message(f"Escolha uma quantidade acima de 0 para deletar", ephemeral=True)
    else:
        await interaction.response.send_message(f"Foi apagado {len(deletado)} mensagem! Por {interaction.user.mention}")


###################################################
########### EXPULSAR E BANIR MEMBRO ###############
###################################################
@bot.tree.command(name="kick", description="Expulsa um membro")
async def kick(interaction: discord.Interaction, membro: discord.Member, *, motivo: str):
    await membro.kick(reason=motivo)
    if motivo == str:
        await interaction.response.send_message(f"{membro} foi expulso por {interaction.user.mention} sem motivo específico.")
    else:
        await interaction.response.send_message(f"{membro} foi expulso por {interaction.user.mention}. Motivo: {motivo}")


@bot.tree.command(name="ban", description="Bane um mebro")
async def ban(interaction: discord.Interaction, membro: discord.Member, *, motivo: str):
    await membro.ban(reason=motivo)
    if motivo == str:
        await interaction.response.send_message(f"{membro} foi banido por {interaction.user.mention} sem motivo específico.")
    else:
        await interaction.response.send_message(f"{membro} foi banido por {interaction.user.mention}. Motivo: {motivo}")


# Rodando o bot
if __name__ == '__main__':
    bot.run(TOKEN)
