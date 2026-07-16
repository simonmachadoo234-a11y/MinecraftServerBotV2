import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer
import os
import random
from dotenv import load_dotenv

load_dotenv()

# ================== CONFIG ==================
TOKEN = os.getenv("DISCORD_TOKEN")
MINECRAFT_IP = "Krypt_server.aternos.me"          # ← Cambia esto
MINECRAFT_PORT = 43787

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

server = JavaServer.lookup(f"{MINECRAFT_IP}:{MINECRAFT_PORT}")

# ================== COMANDOS DIVERTIDOS ==================
@bot.event
async def on_ready():
    print(f"✅ {bot.user} está conectado!")
    status_loop.start()

@tasks.loop(seconds=40)
async def status_loop():
    try:
        status = server.status()
        players = status.players.online
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{players} mineros online"
            )
        )
    except:
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Minecraft | OFFLINE 💀"
            )
        )

# Comando principal
@bot.command()
async def mc(ctx):
    """Estado del servidor"""
    await ctx.send("🔄 Revisando el servidor...")
    try:
        status = server.status()
        embed = discord.Embed(
            title="🟢 Servidor de Minecraft ONLINE",
            color=0x00ff00,
            timestamp=ctx.message.created_at
        )
        embed.add_field(name="Jugadores", value=f"**{status.players.online}/{status.players.max}**", inline=True)
        embed.add_field(name="Versión", value=status.version.name, inline=True)
        embed.add_field(name="IP", value=f"`{MINECRAFT_IP}`", inline=False)
        
        if status.players.sample:
            players_list = "\n".join([p.name for p in status.players.sample[:10]])
            embed.add_field(name="Jugadores conectados", value=players_list or "Ninguno", inline=False)
        
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(
            title="🔴 Servidor OFFLINE",
            description="El servidor parece estar apagado o en mantenimiento.",
            color=0xff0000
        )
        embed.add_field(name="IP", value=f"`{MINECRAFT_IP}`", inline=False)
        await ctx.send(embed=embed)

# Comandos divertidos
@bot.command()
async def ping(ctx):
    """Ping del bot"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! `{latency}ms`")

@bot.command()
async def meme(ctx):
    """Meme random de Minecraft"""
    memes = [
        "Cuando mueres por un creeper y pierdes todo tu diamante 💀",
        "El iron golem mirándote raro cuando intentás robarle las flores",
        "Yo: *intenta hacer parkour*   El server: *lag*",
        "Herobrine existe... solo que está AFK",
        "Cuando encontrás un pueblo y el herrero tiene solo 3 panes"
    ]
    await ctx.send(random.choice(memes))

@bot.command()
async def ayuda(ctx):
    """Lista de comandos"""
    embed = discord.Embed(title="🤖 Comandos del Minecraft Bot", color=0x00ffff)
    embed.add_field(name="**Minecraft**", value="`!mc` - Estado del servidor", inline=False)
    embed.add_field(name="**Divertidos**", value="`!meme` - Meme random\n`!ping` - Latencia del bot", inline=False)
    embed.add_field(name="**Tips**", value="El bot actualiza su estado automáticamente cada 40 segundos", inline=False)
    await ctx.send(embed=embed)

# Comando secreto divertido
@bot.command()
async def creeper(ctx):
    """¡Explota!"""
    await ctx.send("💥 ¡Creeper atrás tuyo!")
    await ctx.send("https://tenor.com/view/creeper-minecraft-explosion-gif-23456789")

bot.run(TOKEN)
