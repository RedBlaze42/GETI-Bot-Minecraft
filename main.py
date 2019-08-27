# coding: utf8
import discord
import json
from tools import getToken,getRole
import cmds

client = discord.Client()
cmd_handler=cmds.cmd_handler(client)

@client.event
async def on_ready():
    print("Bot prêt !")

@client.event
async def on_message(message):
    content=message.content
    if not message.author.bot:
        user_permissions = message.channel.permissions_for(message.author)
        if content.startswith("!mine ") and (len(content.split(" "))>=2):
            await message.channel.trigger_typing()
            cmd_return = await cmd_handler.handle_cmd(message)
            if cmd_return!=None:
                await message.channel.send(cmd_return)
        
@client.event
async def on_raw_reaction_add(payload):
    channel, guild, emoji = client.get_channel(payload.channel_id), client.get_guild(payload.guild_id), payload.emoji
    member, message = guild.get_member(payload.user_id),await channel.fetch_message(payload.message_id)
    if emoji.name.startswith("role_"):
        give_role = await getRole(client,guild,emoji.name.split("role_")[1])
        await member.add_roles(give_role)
        await member.send("Je vous ai donné le role "+give_role.name)

@client.event
async def on_raw_reaction_remove(payload):
    channel, guild, emoji = client.get_channel(payload.channel_id), client.get_guild(payload.guild_id), payload.emoji
    member, message = guild.get_member(payload.user_id),await channel.fetch_message(payload.message_id)
    if emoji.name.startswith("role_"):
        give_role = await getRole(client,guild,emoji.name.split("role_")[1])
        await member.remove_roles(give_role)
        await member.send("Je vous ai enlevé le role "+give_role.name)

print("Initializing...")
client.run(getToken())