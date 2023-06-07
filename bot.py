import discord
from deep_translator import GoogleTranslator
import openai
import os
from textwrap3 import wrap
from math import ceil
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
load_dotenv('.env')
openai.api_key = os.getenv('OPENAI_TOKEN')
client = discord.Client(intents=intents)
gptmessages = []

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('LanGPT'):
        newcontent = message.content.replace("LanGPT ","")
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": newcontent}])
        reply = chat.choices[0].message
        newcontent = str(reply["content"])
        times = ceil(len(newcontent) / 2000)
        messagefrac = wrap(newcontent, int(len(newcontent) / times))
        for i in messagefrac:
            await message.channel.send(i)

    if message.content.startswith('Lan'):
        if message.content.find("translate") != -1:
            newcontent = message.content.replace("Lan translate ","")
            newcontent = GoogleTranslator(source='auto', target='en').translate(newcontent) 
            
            await message.channel.send("\""+newcontent+"\" Why don't you know it? It's so easy.")


client.run(os.getenv('BOT_TOKEN'))