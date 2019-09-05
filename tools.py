# coding: utf8
import discord
import re

def getToken():
    with open("token.secret","r") as tokenFile:
        return tokenFile.read().split("\n")[0]

async def getRole(client,guild,role_name,create_if_not_created=True):
    for role in guild.roles:
        if role.name==role_name:
            return role
    if create_if_not_created:
        created_role = await guild.create_role(name=role_name,mentionable=True)
        await guild.owner.send("J'ai créé le role "+role_name+" car j'en ai besoin et il n'existait pas")
        return created_role

async def send_join_message(member):
    embed = discord.Embed(title="Bienvenue sur le serveur GETI MINECRAFT !", colour=discord.Colour(0xcff00), description="Ce serveur est une branche du serveur [GETI](https://discord.gg/RMTwmG7) qui lui est orienté Overwatch)")

    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/579688801614430222/65b77fc578d04f061b157795daa2cb75.webp?size=128")
    embed.set_author(name="GETI MINECRAFT", url="https://discord.gg/fuUR9Qe", icon_url="https://cdn.discordapp.com/icons/579688801614430222/65b77fc578d04f061b157795daa2cb75.webp?size=128")
    embed.set_footer(text="Message de bienvenue", icon_url="https://cdn.discordapp.com/icons/579688801614430222/65b77fc578d04f061b157795daa2cb75.webp?size=128")

    embed.add_field(name="Nos évènements", value="Le serveur GETI MINECRAFT hébèrge différent types d'évènement:\n -Cité des sables\n -KTP, Taupe Gun et Switch the Patrick\n -Fallen kingoms\n -Survie",inline=False)
    embed.add_field(name="Vous inscrire", value="Pour vous inscrire à ces évènements il faut vous rendre sur ce [message](https://discordapp.com/channels/579688801614430222/585843555826663434/615943002485161985)",inline=False)
    await member.send(embed=embed)

async def send_dm_to_role(guild,role,send_message,embed=None):
    i=0
    for member in guild.members:
        if (role in member.roles or role=="everyone") and not member.bot:
            try:
                await member.send(send_message,embed=embed)
                i+=1
            except:
                print("Je n'ai pas pu envoyer de message à "+member.name)
    return i

async def purge_role(guild,role):
    i=0
    for member in guild.members:
        if role in member.roles:
            await member.remove_roles(role)
            i+=1
    return i
