import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from db import SessionLocal, Trivia, Question

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

# Slash command de ejemplo para administradores
@bot.slash_command(description="Saca una trivia solo para administradores")
@commands.has_permissions(administrator=True)
async def admin_trivia(ctx):
    embed = discord.Embed(
        title="Admin Trivia Time!",
        description="Let's play a special admin trivia game!",
        color=discord.Color.red()
    )
    await ctx.respond(embed=embed)

# Slash command de ejemplo para moderadores
@bot.slash_command(description="Saca una trivia solo para moderadores")
@commands.has_permissions(manage_guild=True)
async def mod_trivia(ctx):
    embed = discord.Embed(
        title="Mod Trivia Time!",
        description="Let's play a special mod trivia game!",
        color=discord.Color.orange()
    )
    await ctx.respond(embed=embed)

# Slash command para crear trivias
@bot.slash_command(description="Crea una nueva trivia")
async def crearTrivia(ctx, nombre: str):
    embed = discord.Embed(
        title=f"Creado Trivia '{nombre}'",
        description="Ahora puedes añadir preguntas a esta trivia.",
        color=discord.Color.green()
    )
    
    # Guardar la trivia en la base de datos
    session = SessionLocal()
    new_trivia = Trivia(title=nombre, description="Trivia creada por el usuario")
    session.add(new_trivia)
    session.commit()
    
    await ctx.respond(embed=embed)

# Ejecutar el bot con el token proporcionado
bot.run(TOKEN)