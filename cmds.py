import discord
from tools import getRole

# coding: utf8
class cmd_handler():
    
    def __init__(self, client):
        self.client=client

    async def handle_cmd(self,message):
        args = message.content.split(" ")[1:]
        if args[0]=="dmRoles" and type(message.channel)==discord.channel.TextChannel:
            channel=message.channel
            role_name=args[1]
            guild = channel.guild
            role = await getRole(self.client,guild,role_name)
            if role!=None:
                send_message=" ".join(args[2:])
                i=0
                for member in guild.members:
                    if role in member.roles:
                        await member.send(send_message)
                        i+=1
                return "Message envoyé à "+str(i)+" membre(s)"
            else:
                await channel.send("Le role "+role_name+" n'existe pas")