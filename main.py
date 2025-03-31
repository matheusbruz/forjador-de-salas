import discord
from discord.ext import commands, tasks
import os
import json
import datetime
from pathlib import Path
import asyncio
from config import Config
from channels_manager import ChannelsManager

# Configuração de intents para o bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

# Inicialização do bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Configurações do bot
config = Config('config.json')

# Gerenciador de canais
channels_manager = ChannelsManager(bot, config)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    check_inactive_channels.start()

@bot.command(name="setjoinchannel")
@commands.has_permissions(administrator=True)
async def set_join_channel(ctx, channel: discord.VoiceChannel = None):
    """Define o canal 'join to create'"""
    if channel is None:
        channel = ctx.author.voice.channel if ctx.author.voice else None
        if channel is None:
            await ctx.send("Por favor, mencione um canal de voz ou esteja em um canal de voz.")
            return

    config.set_join_channel(ctx.guild.id, channel.id)
    await ctx.send(f"Canal 'join to create' definido como: {channel.name}")

@bot.event
async def on_voice_state_update(member, before, after):
    """Monitora mudanças de estado de voz dos usuários"""
    await channels_manager.handle_voice_state_update(member, before, after)

@bot.event
async def on_message(message):
    """Monitora mensagens para atualizar atividade nos canais temporários"""
    if message.author.bot:
        return

    # Atualiza o timestamp de atividade se a mensagem for em um canal temporário
    await channels_manager.update_text_activity(message)
    
    # Processa comandos
    await bot.process_commands(message)

@tasks.loop(hours=6)
async def check_inactive_channels():
    """Verifica canais inativos periodicamente"""
    await channels_manager.check_and_delete_inactive_channels()

@check_inactive_channels.before_loop
async def before_check_inactive_channels():
    """Aguarda o bot estar pronto antes de iniciar o loop de verificação"""
    await bot.wait_until_ready()

# Carrega o token do arquivo .env ou diretamente da variável
def load_token():
    token = None
    
    # Tenta carregar do .env primeiro
    try:
        from dotenv import load_dotenv
        load_dotenv()
        token = os.getenv('DISCORD_TOKEN')
        if token:
            print("Token carregado do arquivo .env")
            return token
    except ImportError:
        print("Módulo python-dotenv não encontrado, tentando outras opções...")
    
    # Tenta carregar do config.json
    token = config.get_token()
    if token:
        print("Token carregado do arquivo config.json")
        return token
    
    # Se tudo falhar, tenta carregar de um arquivo token.txt simples
    try:
        if os.path.exists('token.txt'):
            with open('token.txt', 'r') as f:
                token = f.read().strip()
                if token:
                    print("Token carregado do arquivo token.txt")
                    return token
    except Exception as e:
        print(f"Erro ao ler token.txt: {e}")
    
    return None

# Executa o bot
if __name__ == "__main__":
    token = load_token()
    if not token:
        print("Token não encontrado. Configure o token de uma das seguintes formas:")
        print("1. No arquivo config.json como {'token': 'SEU_TOKEN_AQUI'}")
        print("2. No arquivo .env como DISCORD_TOKEN=SEU_TOKEN_AQUI")
        print("3. Em um arquivo token.txt contendo apenas o token")
    else:
        bot.run(token)