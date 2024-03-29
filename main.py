# coding: utf8
import discord
import json
from tools import getToken,getRole,send_join_message
import cmd_handler

log_channel=581181334760849408
client = discord.Client()
cmds=cmd_handler.cmd_handler(client)

@client.event
async def on_ready():
    print("Bot prêt !")

@client.event
async def on_member_join(member):
    await send_join_message(member)

@client.event
async def on_message(message):
    content=message.content
    if not message.author.bot:
        if message.channel.type==discord.ChannelType.text:
            if content.startswith("!mine ") and len(content.split(" "))>=2:
                await message.channel.trigger_typing()
                cmd_return = await cmds.handle_cmd(message)
        elif message.channel.type==discord.ChannelType.private:
            channel=client.get_channel(log_channel)
            if channel is not None:
                await channel.send(message.author.name+" a écrit au bot: ```"+message.content+"```")
                await message.add_reaction("📨")
            else:
                await message.channel.send("Je n'arrive pas à contacter les admins")
            
@client.event
async def on_raw_reaction_add(payload):
    guild, emoji = client.get_guild(payload.guild_id), payload.emoji
    if guild is not None:
        member= guild.get_member(payload.user_id)
        if emoji.name.startswith("role_"):
            give_role = await getRole(client,guild,emoji.name.split("role_")[1])
            await member.add_roles(give_role)
            #
            # await member.send("Je vous ai donné le role "+give_role.name)

@client.event
async def on_raw_reaction_remove(payload):
    guild, emoji = client.get_guild(payload.guild_id), payload.emoji
    member= guild.get_member(payload.user_id)
    if emoji.name.startswith("role_"):
        give_role = await getRole(client,guild,emoji.name.split("role_")[1])
        await member.remove_roles(give_role)
        await member.send("Je vous ai enlevé le role "+give_role.name)

print("Initializing...")
client.run(getToken())