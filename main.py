# Importações para o bote funcionar ( Não mexa nisso!! )

import asyncio, discord, config
from datetime import datetime
from discord.ext.commands.core import command
from discord import message
from discord.ext import commands
from colorama import Fore
from discord_components import DiscordComponents
from discord_components.component import Button, ButtonStyle

#Prefixo do bot para alterar mude aqui ↓ ( Não mexa nisso!! )                                    
intents = discord.Intents().all()
client = commands.Bot(command_prefix='.', intents = intents)

# Tirar o comando inicial do help ( Não mexa nisso!! )
client.remove_command('help')

@client.event
async def on_button_click(ctx):
    if (ctx.custom_id == "startStaffWork"):
       await baterPontoStaff(ctx)

async def baterPontoStaff(ctx):
    await ctx.respond(content="Iniciando...")
    InitialTime = datetime.now().replace(microsecond=0)
    hour = InitialTime.strftime("%H")
    minute = InitialTime.strftime("%M")
    second = InitialTime.strftime("%S")
    StartTime = f"{hour}:{minute}:{second} | {InitialTime.day}/{InitialTime.month}/{InitialTime.year}"
    embed = discord.Embed(description="```Serviço iniciado com sucesso!```", color=discord.Colour.orange())
    embed.set_author(name=f"{ctx.author.display_name}#{ctx.author.discriminator} - Ponto", icon_url=ctx.author.avatar_url)
    embed.add_field(name="Iniciado as:", value=f"> {StartTime}", inline=False)
    embed.add_field(name="Finalizado as:", value=f"> - x -", inline=False)
    Message = await ctx.channel.send(ctx.author.mention, embed=embed,  components=[[
    Button(style=ButtonStyle.green,
            label="🤖 Finalizar",
            custom_id='finalize_time'),
    ]])

    def check(reaction):
        return (reaction.author.id == ctx.author.id and reaction.message.id == Message.id)

    waitButon = await client.wait_for("button_click", timeout=86400, check=check)

    if (waitButon != None):
        if (waitButon.custom_id == 'finalize_time'):
            FinishTime = datetime.now().replace(microsecond=0)
            hour = FinishTime.strftime("%H")
            minute = FinishTime.strftime("%M")
            second = FinishTime.strftime("%S")
            Total_time = FinishTime - InitialTime

            await Message.delete()
            EndTime = f"{hour}:{minute}:{second} | {FinishTime.day}/{FinishTime.month}/{FinishTime.year}"
            channel = await client.fetch_channel(config.channels['resultadoBatePonto'])
            await ctx.respond(content="Iniciando...")
            embed = discord.Embed(description="```Serviço iniciado com sucesso!```", color=discord.Colour.blue())
            embed.set_author(name=f"{ctx.author.display_name}#{ctx.author.discriminator} - Ponto", icon_url=ctx.author.avatar_url)
            embed.add_field(name="Iniciado as:", value=f"> **{StartTime}**", inline=False)
            embed.add_field(name="Finalizado as:", value=f"> **{EndTime}**", inline=False)
            embed.add_field(name="Total:", value=f"> **{Total_time}**")
            Message = await channel.send(ctx.author.mention, embed=embed)

#Avisa quando o bot fica online.

@client.command()
@commands.guild_only()
async def send_batePontoMessage(ctx):
    if (ctx.author.id == 852759076353736705):
        await ctx.message.delete()
        embed = discord.Embed(description="```Deseja iniciar seu serviço? vamos lá!```", color=discord.Colour.purple())
        embed.set_author(name="Inicie seu trabalho agora mesmo!", icon_url=ctx.guild.icon_url)
        embed.set_footer(text="Versão em desenvolvimento, pode ocorrer erros!", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Aviso", value="> Em caso de problemas contate por Zeus.")
        await ctx.channel.send("||@everyone||", embed=embed,  components=[[
            Button(style=ButtonStyle.blue,
                label="🕙 Iniciar Serviço",
                custom_id='startStaffWork'),
        ]])


@client.event
async def on_ready():
    DiscordComponents(client)
    print(f"{Fore.WHITE}[{Fore.YELLOW} ============= CONEXÃO ============={Fore.WHITE} ]")
    print(f"{Fore.CYAN}> {Fore.WHITE}conectado como: {Fore.LIGHTGREEN_EX}{client.user.name}\n{Fore.CYAN}> {Fore.WHITE}Id: {Fore.LIGHTGREEN_EX}{client.user.id}")
    print(f"{Fore.WHITE}[{Fore.YELLOW} ============= CONEXÃO ============={Fore.WHITE} ]")
    #----------------------------------------------------------------------------------------------
    canal = client.get_channel(id=918595021945569321)
    embed=discord.Embed(title=f"**Sistema de log**\nAcabei de reiniciar novidades estão vindo hahaha!! 🥳", color=0x00e1ff)
    embed.set_author(name="Logs")
    await canal.send(embed=embed)
    
#Comandos do Bot

@client.command(aliases=["ajuda"])
async def help(ctx):
    embed=discord.Embed(description=f"{ctx.author.name}, Esse é o nosso painel de ajuda nele você pode ver e rever as categorias em que você tem duvida.\n\nO meu prefixo é .", color=0x7e1ad1)
    embed.set_author(name="Painel de ajuda", icon_url=ctx.author.avatar_url)
    embed.add_field(name="**Criação**", value="**Clique no botão abaixo para saber mais**", inline=True)
    embed.add_field(name="**Interações**", value="**Clique no botão abaixo para saber mais**", inline=True)
    embed.add_field(name="**Administração**", value="**Clique no botão abaixo para saber mais**", inline=True, )
    embed.set_footer(text="Lembrando o prefixo do bot é \".\" 👍 | 1 minuto para clicar no botão.")
    await ctx.send(embed=embed, components=[[
        Button(
            style=ButtonStyle.green,
            label="Ajuda Administração",
            custom_id="Administração",
        ),

        Button(
            style=ButtonStyle.green,
            label="Ajuda Interações",
            custom_id="Interações",
        ),

        Button(
            style=ButtonStyle.green,
            label="Criação da BOPE",
            custom_id="Criação",
        ),

    ]], delete_after=65.00,)
    await ctx.message.delete()
    

    def check(interaction):
        return interaction.author.id == ctx.author.id
    try:
        buttonEvent = await client.wait_for("button_click", timeout=60, check=check)
    except asyncio.TimeoutError:
        embed=discord.Embed(title="Nenhum botão não foi pressionado a tempo.", color=0xe10e0e)
        embed.set_author(name="Tempo expirado")
        await ctx.channel.send(embed=embed, delete_after=15.000)

    if (buttonEvent):
        if (buttonEvent.custom_id == 'Criação'):
            embed=discord.Embed(title=f"{ctx.author.name}, A bope foi criada no dia - 27/11/2021 pelo comandante geral /mica. ❤️", color=0x0ee143, delete_after=70.000)
            embed.set_author(name="Criação da BOPE", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url="https://c.tenor.com/4sEULzbSxlYAAAAC/bope.gif")
            await ctx.channel.send(embed=embed, delete_after=60.00)
            return

        if (buttonEvent.custom_id == 'Administração'):
            embed=discord.Embed(title="O yBot possui varios comandos com a finalidade de Administrar e deixar o servidor em segurança.\n\nComandos :\nClear\nSay\nHelp\nMute\nBan\nKick\nWarn", color=0x0ee143, delete_after=70.000)
            embed.set_author(name="Administração")
            embed.add_field(name="Clear", value="**O maximo de mensagens que podem ser apagadas de um chat usando o comando Clear é de 300.**")
            embed.add_field(name="Say", value="**O comando say é para fazer o bot falar algo tipo \".say blablabla\".**")
            embed.add_field(name="Mute", value="**O tempo maximo de Mute/Mutar é 1 semana.**")
            embed.add_field(name="Ban", value="**O ban pode ser apenas permanente por enquanto.**")
            embed.add_field(name="Kick", value="**O kick pode ser feito mutiplas vezes.**")
            embed.add_field(name="Warn", value= "*1/2 Warn = Nada! | 2/3 Warn = Nada! 4 Warn = Kick 5 Warn = Ban.**")
            await ctx.channel.send(embed=embed, delete_after=100.000)
            return

        else:
            embed=discord.Embed(title="O botão pressionado não foi indentificado porfavor contate o problema ao yMaycon#1309", color=0xe10e0e)
            embed.set_author(name="Erro x100000")
            await ctx.channel.send(embed=embed, delete_after=15.000)

@client.command(aliases=["limpar","apagar","delete","deletar"])
async def clear(ctx, amount=300):

    if(not ctx.author.guild_permissions.manage_messages):
        embed=discord.Embed(title=f"{ctx.author.name} Você não tem permissão para usar este comando 😡", color=0xff0000)
        embed.set_author(name="Sem permissão!")
        await ctx.send(embed=embed, delete_after=15.00)
        await ctx.message.delete()
        return

    if amount is None:
        embed=discord.Embed(title="**O formato de usar o Clear/Limpeza/Apagar deve ser :**\nclear(limpeza/apagar) 3/300(ou qualquer numero desejado.)\n o comando Clear é utilizado bastante na limpeza de chats e em servidores de comunidade.", color=0xc8ff00)
        embed.set_author(name="Limpeza de chat.")
        await ctx.send(embed=embed, delete_after=15.00)
        await ctx.message.delete()
        return
    
    if amount < 2:
        embed=discord.Embed(title=f"{ctx.author.name} O minimo de mensagens a serém excluidas deve ser acima de 2!", color=0xc8ff00)
        embed.set_author(name="Nada foi excluido!")
        await ctx.send(embed=embed, delete_after=15.00)
        await ctx.message.delete()
        return    

    if amount > 300:
        embed=discord.Embed(title=f"{ctx.author.name} O maximo de mensagens a serém excluidas devem ser abaixo de 300!", color=0xc8ff00)
        embed.set_author(name="Nada foi excluido!")
        await ctx.send(embed=embed, delete_after=15.00)
        await ctx.message.delete()
        return

    else:
        canal = client.get_channel(id=917846075606462464)
        await ctx.channel.purge(limit=amount)
        embed=discord.Embed(title=f"{amount} mensagens foram apagadas por {ctx.author.name}!!", color=0x00ff11)
        embed.set_author(name="Limpeza de chat")
        await ctx.send(embed=embed, delete_after=65.00)
        embed=discord.Embed(title=f"**Sistema de log**\n\nO administrador : {ctx.author.name}\nApagou {amount} mensagens\nNo chat : {ctx.channel.name}", color=0x00e1ff)
        embed.set_author(name="Logs")
        await canal.send(embed=embed)

@client.command(aliases=["falar","repetir"])
async def say(ctx, *, message=None):
    if (not ctx.author.guild_permissions.manage_messages):
        embed=discord.Embed(title="Você não tem permissão para usar este comando 😡", color=0xff0000)
        embed.set_author(name="Sem permissão")
        await ctx.send(embed=embed, delete_after=15.00)
        return

    if message == None:
        await ctx.send(f'{ctx.author.mention} Você tem que escrever algo!', delete_after=15.00) 
        ctx.message.delete()

    else:
        await ctx.send(f'{message}')
        await ctx.message.delete()

@client.command(aliases=["kickar","expulsar"])
async def kick(ctx, membro : discord.Member, *, motivo=None):
    if (not ctx.author.guild_permissions.kick_members):
        embed=discord.Embed(title="Você não tem permissão para usar este comando 😡", color=0xff0000)
        embed.set_author(name="Sem permissão")
        await ctx.send(embed=embed, delete_after=15.00)
        return

    if motivo == None:
        embed=discord.Embed(title=f"{ctx.author.name} Você tem que colocar um motivo para dar kick nesta pessoa!", color=0xff0000)
        embed.set_author(name="Sem permissão!")
        await ctx.send(embed=embed)

    if membro == (ctx.author):
        await ctx.send("Você não pode se auto expulsar.",color=0xc8ff00)
        return

    else:
        canal = client.get_channel(id=917846075606462464)
        await membro.kick()
        embed=discord.Embed(title=f"**Sistema de punição**\n\nO administrador {ctx.author.mention} expulsou {membro.mention}\n Motivo : {motivo}", color=0xff0000)
        embed.set_author(name="Logs de expulsão!")
        await canal.send(embed=embed)
        embed=discord.Embed(title=f"{ctx.author.name} O usuário foi expulso com sucesso!!", color=0x00ff08, delete_after=20.00)
        embed.set_author(name="Logs")
        await ctx.send(embed=embed)

@client.command(aliases=["banir","exonerar"])
async def ban(ctx, membro : discord.Member, *, motivo=None):
    if (not ctx.author.guild_permissions.ban_members):
        embed=discord.Embed(title="Você não tem permissão para usar este comando 😡", color=0xff0000)
        embed.set_author(name="Sem permissão")
        await ctx.send(embed=embed, delete_after=15.00)
        return

    if motivo == None:
        embed=discord.Embed(title=f"{ctx.author.name} Você tem que colocar um motivo para dar ban nesta pessoa!", color=0xff0000)
        embed.set_author(name="Sem permissão!")
        await ctx.send(embed=embed)

    if membro == (ctx.author):
        await ctx.send("Você não pode se auto banir.",color=0xc8ff00)
        return

    else:
        logsChannel = client.get_channel(id=config.channels['logsChannel'])
        await membro.ban()
        embed=discord.Embed(title=f"**Sistema de punição**\n\nO administrador {ctx.author.mention} baniu {membro.mention}\n Motivo : {motivo}", color=0xff0000)
        embed.set_author(name="Logs de banimentos!")
        await logsChannel.send(embed=embed)
        embed=discord.Embed(title=f"{ctx.author.name} O usuário foi banido com sucesso!!", color=0x00ff08, delete_after=20.00)
        embed.set_author(name="Logs")
        await ctx.send(embed=embed)

@commands.has_permissions(ban_members=True)
@client.command()
async def sendBatePontoMessage(ctx):
    embed=discord.Embed(description=">")

@client.command(aliases=["bateponto","ponto"])
async def bate(ctx, nome= str):
    embed=discord.Embed(title="Como fazer ? primeiro digite o seu nome, depois o horário em que você começou o patrulhamento, ex : 13:50\n\nApós isso digite o horário em que voce __TERMINOU__ o patrulhamento, ex : 15:30\n\nE após isso digite o tempo total em que você patrulhou.")
    embed.set_author(name="Bate Ponto")
    await ctx.send(embed=embed)
    embed=discord.Embed(title="Qual seu nome?")
    embed.set_author(name="Nome")
    await ctx.send(embed=embed)
    try:
        nome = await client.wait_for("message", timeout=10)
    except asyncio.TimeoutError:
        try:
            Message = await ctx.channel.send("Você demorou muito e a resposta foi anulada.")
            await asyncio.sleep(5)
            await Message.delete()
        except Exception as e:
            print("Erro encontrado na linha: ", e)
    await ctx.send(f"{message}")
            
            


#NÃO MEXA!!!    
client.run(config.bot['acessToken'])