import discord
import time
from tools import getToken, getRole

client = discord.Client()

@client.event
async def on_ready():
    print("Test ready !")

@client.event
async def on_message(message):
    pass

@client.event
async def on_raw_reaction_add(payload):
    print("Detected reaction !")
    channel = client.get_channel(payload.channel_id)
    guild= client.get_guild(payload.guild_id)
    user = client.get_user(payload.user_id)
    member = guild.get_member(payload.user_id)
    if payload.message_id==614462090148708423:
        print(payload.emoji.name)
        if payload.emoji.name=="😭":
            sob_role = await getRole(client,guild,"Triste")
            await member.add_roles(sob_role)
            await user.send("Tu t'es abonné au role triste !")
        elif payload.emoji.name=="😴":
            await channel.send("Arrête de dormir !")
client.run(getToken())