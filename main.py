import discord
import logging
import asyncio
import aiohttp
from io import BytesIO
import base64
import requests

with open("token.txt", "r") as file:
    TOKEN = file.read()

logging.basicConfig(level=logging.INFO)
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.slash_command(description="Draw some images with a prompt")
async def draw(ctx, prompt: discord.Option(str)):
    response = await ctx.send(f"<@{ctx.author.id}> Drawing image with prompt: {prompt}. This could take up to 1 minute...")
    async with aiohttp.ClientSession() as sess:
        async with sess.post("https://backend.craiyon.com/generate",
                         headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"},
                         json={"prompt": prompt}) as resp:
            images = await resp.json()
            image1 = images["images"][0]

    image = discord.File(BytesIO(base64.b64decode(image1)))
    image.filename = "test.png"
    await response.edit(content=f"<@{ctx.author.id}> Your \"{prompt}\" images has been generated", file=image)


bot.run(TOKEN)