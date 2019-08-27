import discord
from tools import getRole

# coding: utf8
class cmd_handler():
    
    def __init__(self, client):
        self.client=client

    def help(self):
        method_list = [func.split("cmd_")[1] for func in dir(self) if callable(getattr(self, func)) and func.startswith("cmd_")]
        doc_list=list()
        for method in method_list:
            doc_list.append(getattr(self, "cmd_"+method).__doc__)
        return list(zip(method_list,doc_list))

    async def handle_cmd(self,message):
        args = message.content.split(" ")[1:]
        if args[0]=="dmRole" and type(message.channel)==discord.channel.TextChannel:#TODO séparer fonctions (tableau d'attributes)
            return await self.cmd_dmRole(message,args)
    
    async def cmd_dmRole(self,message,args):
        """Hey je suis là !"""
        channel=message.channel
        role_name=args[1]
        guild = channel.guild
        role = await getRole(self.client,guild,role_name,create_if_not_created=False)

        if role!=None or role_name=="everyone":
            send_message=" ".join(args[2:])
            i=0
            for member in guild.members:
                if (role in member.roles or role_name=="everyone") and not member.bot:
                    await member.send(send_message)
                    i+=1
            return "Message envoyé à "+str(i)+" membre(s)"
        else:
            return "Le role "+role_name+" n'existe pas"