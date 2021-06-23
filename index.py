import discord
from discord.ext import commands
import pandas as pd
import asyncio
import numpy as np
import matplotlib.pyplot as plt

intents = discord.Intents.default()
intents.members = True

pd.set_option("display.max_rows", None, "display.max_columns", None)
bot = commands.Bot(command_prefix=['E!', 'e!'], intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    print("bot online")

@bot.event
@commands.guild_only()
async def on_message(ctx):
    if ctx.author.bot == True:
        return
    try:
        arquivo = pd.read_csv(f'arquivo/{ctx.guild.id}.csv')
    except:
        dado_inserir = pd.DataFrame(columns=['ChatID', 'ChatName', 'CountMessage'])
        dado_inserir.set_index("ChatID", inplace=True)
        dado_inserir.to_csv(f'arquivo/{ctx.guild.id}.csv')
        arquivo = pd.read_csv(f'arquivo/{ctx.guild.id}.csv')
        try:
            arquivo.columns.drop('Unnamed: 0')
        except:
            pass

    arquivo.set_index("ChatID", inplace=True)


    # SE JÁ ESTÁ SALVO O CHAT

    try:
        count = arquivo.loc[ctx.channel.id]['CountMessage']
        arquivo.loc[ctx.channel.id] = [str(ctx.channel.name), count + 1]


    # SE O CHAT N ESTÁ SALVO

    except:
        colunas = arquivo.columns.values.tolist()
        tamanho = arquivo.shape[0]
        arquivo.loc[tamanho] = {
            colunas[0]: ctx.channel.name,
            colunas[1]: 1
        }

        arquivo.rename(index={tamanho: str(ctx.channel.id)}, inplace=True)
    arquivo.to_csv(f'arquivo/{ctx.guild.id}.csv')
    await bot.process_commands(ctx)


@bot.command(aliases=['dado', 'dads', 'estatistica', 'estatistics'])
@commands.guild_only()
async def dados(ctx):
    arquivo = pd.read_csv(f'arquivo/{ctx.guild.id}.csv')
    arquivo.set_index("ChatID", inplace=True)
    fig = arquivo.plot.bar(x='ChatName', y='CountMessage', rot=0).get_figure()
    fig.savefig(f'graphics/{ctx.author.id}.png')
    picture = discord.File(f'graphics/{ctx.author.id}.png')
    if ctx.guild.owner == ctx.author:
        var = "\nVocê, **owner do servidor**, pode utilizar o comando `e!deletar_dados`"
    else:
        var = ''
    await ctx.send(content=f'{ctx.author.mention}, Aqui está o gráfico, cujo demonstra a intensidade de uso dos chats! {var}', file=picture)

@bot.event
@commands.guild_only()
async def on_guild_channel_delete(channel):
    arquivo = pd.read_csv(f'arquivo/{channel.guild.id}.csv')
    arquivo.set_index("ChatID", inplace=True)
    arquivo.drop(channel.id, axis=0, inplace=True)
    arquivo.to_csv(f'arquivo/{channel.guild.id}.csv')

@bot.command(aliases=['drop_data', 'deletar_dados', 'deletar_dado'])
@commands.guild_only()
async def drop_dados(ctx):
    if ctx.author == ctx.guild.owner:
        pass
    else:
        return await ctx.send(f'**Esse comando é exclusivo para o `{ctx.guild.owner}`')

    arquivo = pd.read_csv(f'arquivo/{ctx.guild.id}.csv')
    arquivo.set_index("ChatID", inplace=True)
    arquivo.drop(arquivo.index, inplace=True)
    arquivo.to_csv(f'arquivo/{ctx.guild.id}.csv')
    await ctx.send('Você apagou todos os dados do comando `e!dados`')

bot.run('')
