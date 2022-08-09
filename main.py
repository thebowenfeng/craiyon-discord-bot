import discord
import logging
import asyncio
import aiohttp
from io import BytesIO
import base64
from PIL import Image
import os

try:
    with open("token.txt", "r") as file:
        TOKEN = file.read()
except:
    TOKEN = os.environ.get("TOKEN")

logging.basicConfig(level=logging.INFO)
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.slash_command(description="Draw some images with a prompt")
async def draw(ctx, prompt: discord.Option(str)):
    print(f"LOG: {ctx.author} requested a draw with prompt {prompt}")

    response = await ctx.respond(f"<@{ctx.author.id}> Drawing image with prompt: {prompt}. This could take up to 1 minute...")
    async with aiohttp.ClientSession() as sess:
        async with sess.post("https://backend.craiyon.com/generate",
                         headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"},
                         json={"prompt": prompt}) as resp:
            images = await resp.json()

    print(f"LOG: Image data for {ctx.author} and prompt {prompt} received")

    pil_images = [Image.open(BytesIO(base64.b64decode(image))) for image in images["images"]]
    merged = Image.new(mode="RGB", size=(pil_images[0].width * 3, pil_images[0].height * 3))

    index = 0
    for col in range(0, 3):
        for row in range(0, 3):
            merged.paste(pil_images[index], (col * pil_images[0].width, row * pil_images[0].height))
            index += 1

    print(f"LOG: Image data for {ctx.author} and prompt {prompt} merged")

    img_bytes = BytesIO()
    merged.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    image = discord.File(img_bytes)
    image.filename = "result.png"
    await response.edit_original_message(content=f"<@{ctx.author.id}> Your \"{prompt}\" images has been generated", file=image)


bot.run(TOKEN)