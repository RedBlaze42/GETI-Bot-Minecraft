import discord
from tools import getRole

class cmd_handler():
    
    def __init__(self, client):
        self.client=client

    async def handle_cmd(self,message):
        args = message.content.split(" ")[1:]
        print(type(message.channel),discord.channel.TextChannel)
        if args[0]=="dmRoles" and type(message.channel)==discord.channel.TextChannel:
            channel=message.channel
            guild = channel.guild
            role = await getRole(self.client,guild,args[1]) 
            if role!=None:
                send_message=" ".join(args[2:])
                for member in guild.members:
                    if role in member.roles:
                        await member.send(send_message)
            else:
                await channel.send("Le role "+args[1]+" n'existe pas")