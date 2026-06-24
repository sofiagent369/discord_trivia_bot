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

# Slash command para jugar trivias
@bot.slash_command(description="Jugar a una trivia")
async def jugarTrivia(ctx):
    # Obtener todas las trivias de la base de datos
    session = SessionLocal()
    trivias = session.query(Trivia).all()
    
    if not trivias:
        embed = discord.Embed(
            title="No hay trivias disponibles",
            description="Por favor, crea una trivia primero.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
        return
    
    # Crear un menú interactivo para seleccionar la trivia
    options = [discord.SelectOption(label=trivia.title, value=str(trivia.id)) for trivia in trivias]
    
    async def select_callback(interaction):
        selected_trivia_id = int(interaction.data['values'][0])
        selected_trivia = session.query(Trivia).filter(Trivia.id == selected_trivia_id).first()
        
        if not selected_trivia:
            embed = discord.Embed(
                title="Error",
                description="Trivia seleccionada no encontrada.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Comenzar el juego
        questions = session.query(Question).filter(Question.trivia_id == selected_trivia.id).all()
        score = 0
        
        for question in questions:
            embed = discord.Embed(
                title=question.question_text,
                description=f"Opciones: {', '.join(question.options.split(', '))}",
                color=discord.Color.blue()
            )
            
            await interaction.followup.send(embed=embed)
            
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            
            try:
                response = await bot.wait_for('message', check=check, timeout=30.0)
                
                if response.content.lower() == question.correct_option.lower():
                    score += 1
                    embed = discord.Embed(
                        title="Correcto",
                        description=f"Respuesta correcta: {question.correct_option}",
                        color=discord.Color.green()
                    )
                else:
                    embed = discord.Embed(
                        title="Incorrecto",
                        description=f"Respuesta incorrecta. La respuesta correcta era: {question.correct_option}",
                        color=discord.Color.red()
                    )
                
                await response.delete()
                await interaction.followup.send(embed=embed)
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title="Tiempo agotado",
                    description=f"No respondiste a tiempo. La respuesta correcta era: {question.correct_option}",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
        
        # Mostrar puntuación final
        embed = discord.Embed(
            title="Trivia Finalizada",
            description=f"Puntuación final: {score}/{len(questions)}",
            color=discord.Color.gold()
        )
        await interaction.followup.send(embed=embed)
    
    select_view = discord.ui.View()
    select_menu = discord.ui.Select(options=options, callback=select_callback)
    select_view.add_item(select_menu)
    await ctx.respond("Selecciona una trivia:", view=select_view)

# Ejecutar el bot con el token proporcionado
bot.run(TOKEN)