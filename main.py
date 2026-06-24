import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener el token del bot de las variables de entorno
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Intents necesarios para el bot
intents = discord.Intents.default()
intents.message_content = True

# Configurar el bot con slash commands y intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    await bot.change_presence(activity=discord.Game(name="Playing Trivia"))

# Slash command de ejemplo
@bot.slash_command(description="Saca una trivia")
async def trivia(ctx):
    embed = discord.Embed(
        title="Trivia Time!",
        description="Let's play a trivia game!",
        color=discord.Color.blue()
    )
    await ctx.respond(embed=embed)

# Ejecutar el bot con el token proporcionado
bot.run(TOKEN)