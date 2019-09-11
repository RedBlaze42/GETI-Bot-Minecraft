# coding: utf8
import discord
import time
from tools import getToken, getRole

client = discord.Client()

@client.event
async def on_ready():
    print("Test ready !")

@client.event
async def on_message(message):
    emojis=client.emojis
    await message.author.send("<:role_Triste:614930933270839296>")


client.run(getToken())