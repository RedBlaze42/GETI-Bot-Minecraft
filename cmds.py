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
            doc_list.append(getattr(self, "cmd_"+method).__doc__.split("\n")[0])
        help_list = list(zip(method_list,doc_list))
        help_embed=discord.Embed(title="Aide du bot GETI-Minecraft",color=65310)
        for func_name,func_doc in help_list:
            help_embed.add_field(name=func_name,value=func_doc)
        return help_embed

    async def handle_cmd(self,message):
        args = message.content.split(" ")[1:]
        if args[0]=="help":
            await message.author.send(embed=self.help())
            await message.delete()
            await message.channel.send("Aide envoyé en MP !", delete_after=3)
        elif args[0]=="dmRole" and type(message.channel)==discord.channel.TextChannel:
            return await self.cmd_dmRole(message,args)
    
    async def cmd_dmRole(self,message,args):
        """Permet d'envoyer un message privé à tout les membres d'un rôle
        
        Usage: !mine dmRole <nom_du_rôle> Message
        <nom_du_rôle> doit être sans @ pour l'instant
        """

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