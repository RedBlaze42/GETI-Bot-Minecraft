import discord
from tools import *

# coding: utf8
class cmd_handler():
    
    def __init__(self, client):
        self.client=client

    def help(self,details=False):
        method_list = [func.split("cmd_")[1] for func in dir(self) if callable(getattr(self, func)) and func.startswith("cmd_")]
        doc_list=list()
        for method in method_list:
            doc_list.append(getattr(self, "cmd_"+method).__doc__)
        help_list = list(zip(method_list,doc_list))
        
        return help_list

    async def handle_cmd(self,message):
        args = message.content.split(" ")[1:]
        if args[0]=="help":
            return await self.cmd_help(message,args)
        elif args[0]=="dmRole" and type(message.channel)==discord.channel.TextChannel:
            return await self.cmd_dmRole(message,args)
        elif args[0]=="purgeRoles" and type(message.channel)==discord.channel.TextChannel:
            return await self.cmd_purgeRoles(message,args)
        elif args[0]=="dmMessage" and type(message.channel)==discord.channel.TextChannel:
            return await self.cmd_dmMessage(message,args)

    async def cmd_help(self,message,args):
        """Affiche l'aide !mine help détail pour afficher l'uttilisation des commandes
        """
        help_list=self.help()

        help_embed=discord.Embed(title="Aide du bot GETI-Minecraft",color=65310)
        for func_name,func_doc in help_list:
            if len(args)>=2 and args[1]=="détail":
                help_embed.add_field(name=func_name,value=func_doc)
            else:
                help_embed.add_field(name=func_name,value=func_doc.split("\n")[0])
        await message.author.send(embed=help_embed)
        await message.delete()
        await message.channel.send("Aide envoyé en MP !", delete_after=3)

    async def cmd_purgeRoles(self,message,args):
        """Purge un rôle ou plusieurs rôles de tout ses membres

        Usage: !mine purgeRole @<rôle1> @<rôle2> ..."""
        if len(args)<2: return "Usage: !mine purgeRole @<rôle1> @<rôle2> ..."
        if len(message.role_mentions)==0: return "Vous n'avez mentionné aucun rôle"

        for role in message.role_mentions:
            i=await purge_role(message.channel.guild,role)
            await message.channel.send("J'ai enlevé "+str(i)+" membre(s) du rôle: "+role.name)
        
    
    async def cmd_dmMessage(self,message,args):
        """Envoie une notification par dm au rôle mentionné dans le message

        Usage: !mine dmMessage <id_du_canal> <id_du_message>
        """
        if len(args)<3: return "Usage: !mine dmMessage <id_du_canal> <id_du_message>"
        channel=self.client.get_channel(int(args[1]))
        if channel is None: return "Ce canal n'existe pas !"
        message=await channel.fetch_message(int(args[2]))
        if message is None: return "Ce message n'existe pas !"
        guild=channel.guild

        if len(message.role_mentions)==0 and not message.mention_everyone: return "Aucun rôle n'est mentionné dans ce message"
        if not message.mention_everyone:
            role=message.role_mentions[0]
        else:
            role="everyone"
        message_content=escape_special_mentions(message.content)
        first_line=message_content.split("\n")[0]
        message_url="https://discordapp.com/channels/"+str(guild.id)+"/"+str(channel.id)+"/"+str(message.id)

        embed=discord.Embed(title="Message important !", description="Ce message viens du canal <#"+str(channel.id)+">", color=0x0aff00)
        embed.set_author(name="GETI Minecraft",icon_url="https://cdn.discordapp.com/icons/579688801614430222/65b77fc578d04f061b157795daa2cb75.webp?size=128")
        embed.set_thumbnail(url="https://i.imgur.com/OyEFPXv.jpg")
        embed.add_field(name=first_line, value=message_content[len(first_line):len(first_line)+120]+"...",inline=False)
        embed.add_field(name="Pour voir le message complet cliquez ici",value="[message]("+message_url+")",inline=False)
        embed.set_footer(text="Notification GETI Minecraft")
        
        i=await send_dm_to_role(guild,role,"Vous avez une nouvelle notification:",embed=embed)
        return "Message envoyé à "+str(i)+" membre(s)"
    async def cmd_dmRole(self,message,args):
        """Permet d'envoyer un message privé à tout les membres d'un rôle
        
        Usage: !mine dmRole @<nom_du_rôle> Message
        """
        if len(args)<4: return "Usage: !mine dmRole @<nom_du_rôle> Message"
        if len(message.role_mentions)==0 and not message.mention_everyone: return "Ce rôle n'existe pas"
        if not message.mention_everyone:
            role=message.role_mentions[0]
        else:
            role="everyone"
        guild = message.channel.guild
        send_message=" ".join(args[2:])

        i=send_dm_to_role(guild,role,send_message)
        return "Message envoyé à "+str(i)+" membre(s)"