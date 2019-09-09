import discord
from tools import *
from copy import copy

# coding: utf8
class cmd_handler():
    
    def __init__(self, client):
        self.client=client

    def help(self,details=False):
        method_list = [func.split("cmd_")[1] for func in dir(self) if callable(getattr(self, func)) and func.startswith("cmd_")]
        method_list.sort()
        doc_list=list()
        for method in method_list:
            doc_list.append(getattr(self, "cmd_"+method).__doc__)
        
        return dict(zip(method_list,doc_list))

    async def handle_cmd(self,message):
        args = message.content.split(" ")[1:]
        if args[0] in self.help().keys():
            return await getattr(self, "cmd_"+args[0])(message,args)
        else:
            return "❌ Cette commande n'existe pas: !mine help pour l'aide"

    async def cmd_help(self,message,args):
        """Affiche l'aide !mine help détail pour afficher l'uttilisation des commandes
        """
        help_list=self.help().items()

        help_embed=discord.Embed(title="Aide du bot GETI-Minecraft",color=65310)
        for func_name,func_doc in help_list:
            if len(args)>=2 and args[1]=="détail":
                help_embed.add_field(name=func_name,value=func_doc)
            else:
                help_embed.add_field(name=func_name,value=func_doc.split("\n")[0])
        await message.author.send(embed=help_embed)
        await message.delete()
        await message.channel.send("✅ Aide envoyé en MP !", delete_after=3)

    async def cmd_purgeRoles(self,message,args):
        """Purge un rôle ou plusieurs rôles de tout ses membres

        Usage: !mine purgeRole @<rôle1> @<rôle2> ..."""
        if len(args)<2: return "❌ Usage: !mine purgeRole @<rôle1> @<rôle2> ..."
        if len(message.role_mentions)==0: return "❌ Vous n'avez mentionné aucun rôle"

        for role in message.role_mentions:
            i=await purge_role(message.channel.guild,role)
            await message.channel.send("J'ai enlevé "+str(i)+" membre(s) du rôle: "+role.name)
        
    async def cmd_muteChannel(self,message,args):
        """Mute tout les membres qui n'ont pas la permission de mute d'autre membres dans le channel vocal ou vous êtes
        
        Usage: !mine muteChannel
        """
        member=message.author
        if member.voice is None: return "❌ Vous n'êtes pas dans un canal vocal"
        i=0
        members_not_muted=0
        voice_channel=member.voice.channel
        for member in voice_channel.members:
            if not voice_channel.permissions_for(member).mute_members:
                await member.edit(mute=True,deafen=False)
                i+=1
            else: 
                members_not_muted+=1
        await message.channel.send("✅ "+str(i)+" membre(s) muté(s) et " +str(members_not_muted)+" ne l'ont pas été")

    async def cmd_unmuteChannel(self,message,args):
        """Unmute tout les membres qui le sont dans le channel vocal ou vous êtes
        Ajoutez all pour unmute tout les membres du serveur
        Usage: !mine unmuteChannel [all]
        """
        member=message.author
        if member.voice is None and len(args)<2: return "❌ Vous n'êtes pas dans un canal vocal"
        i=0
        members_not_unmuted=0
        if(len(args)>=2) and (args[1]=="all"):
            members=message.channel.guild.members
        else:
            voice_channel=member.voice.channel
            members=voice_channel.members
        for member in members:
            if member.voice is not None and member.voice.mute:
                await member.edit(mute=False,deafen=False)
                i+=1
            else: 
                members_not_unmuted+=1
        await message.channel.send("✅ "+str(i)+" membre(s) unmuté(s) et " +str(members_not_unmuted)+" l'étaient déjà")

    async def cmd_dmMessage(self,message,args):
        """Envoie une notification par dm au rôle mentionné dans le message

        Usage: !mine dmMessage <id_du_message> [id_du_canal]
        id du canal optionnel si écrit dans le même canal que le message
        """
        if len(args)<2: return "Usage: !mine dmMessage <id_du_message> [id_du_canal]"

        if len(args)==3:
            channel=self.client.get_channel(int(args[2]))
        else:
            channel=message.channel
        if channel is None: return "❌ Ce canal n'existe pas !"
        cmd=message
        message=await channel.fetch_message(int(args[1]))
        if message is None: return "❌ Ce message n'existe pas !"
        guild=channel.guild

        if len(message.role_mentions)==0 and not message.mention_everyone: return "Aucun rôle n'est mentionné dans ce message"
        if not message.mention_everyone:
            roles=message.role_mentions
        else:
            roles="everyone"

        message_content=message.clean_content
        first_line=message_content.split("\n")[0]
        message_url=message.jump_url

        embed=discord.Embed(title="Message important !", description="Ce message viens du canal <#"+str(channel.id)+">", color=0x0aff00)
        embed.set_author(name="GETI Minecraft",icon_url="https://cdn.discordapp.com/icons/579688801614430222/65b77fc578d04f061b157795daa2cb75.webp?size=128")
        embed.set_thumbnail(url="https://i.imgur.com/OyEFPXv.jpg")
        embed.add_field(name=first_line, value=message_content[len(first_line):len(first_line)+120]+"...",inline=False)
        embed.add_field(name="Pour voir le message complet cliquez ici",value="[message]("+message_url+")",inline=False)
        embed.set_footer(text="Notification GETI Minecraft")
        
        i=0
        if roles=="everyone":
            i=await send_dm_to_role(guild,"everyone","Vous avez une nouvelle notification:",embed=embed)
        else:
            for role in roles:
                j=await send_dm_to_role(guild,role,"Vous avez une nouvelle notification:",embed=embed)
                i+=j
        await cmd.delete()
        await cmd.channel.send("Message envoyé à "+str(i)+" membre(s)",delete_after=5)

    async def cmd_dmRole(self,message,args):
        """Permet d'envoyer un message privé à tout les membres d'un rôle
        
        Usage: !mine dmRole @<nom_du_rôle> Message
        """
        if len(args)<4: return "❌ Usage: !mine dmRole @<nom_du_rôle> Message"
        if len(message.role_mentions)==0 and not message.mention_everyone: return "❌ Ce rôle n'existe pas"
        if not message.mention_everyone:
            role=message.role_mentions[0]
        else:
            role="everyone"
        guild = message.channel.guild
        send_message=" ".join(args[2:])

        i=await send_dm_to_role(guild,role,send_message)
        return "Message envoyé à "+str(i)+" membre(s)"

    async def cmd_assignRoleMc(self,message,args):
        """Assigne le rôle MC aux membres du serveur qui possèdent dans leurs noms: [MC]
        
        Usage: !mine assignRoleMc"""

        members=message.channel.guild.members
        role=await getRole(self.client,message.channel.guild,"[MC]")
        i=0
        for member in members:
            if member.bot: continue
            if member.nick is not None and "[MC]" in member.nick:
                await member.add_roles(role)
                i+=1
        
        return "Rôle [MC] assigné à "+str(i)+" membres sur "+str(len(members))

    async def cmd_assignRole(self,message,args):
        """Assigne un rôle à un groupe de personne selon si elle a ou pas un autre rôle
        
        Usage: !mine assignRole @role_à_assigner if/unless any/all @role_condition @role_condition2"""
        if len(args)<5: return "❌ Votre commande ne contient pas assez d'arguments"
        if not args[2] in ["if","unless"]: return "❌ Le deuxième argument doit être if ou unless"
        if not args[3] in ["any","all"]: return "❌ Le troisième argument doit être any ou all"
        
        guild=message.channel.guild
        members=guild.members
        role_to_assign=guild.get_role(int(args[1][3:-1]))
        if role_to_assign is None: return "❌ Vous n'avez pas précisé de rôle à assigner"
        condition_roles=copy(message.role_mentions)
        condition_roles.remove(role_to_assign)
        
        i=0
        for member in members:
            if member.bot: continue
            conditions=False
            roles_to_find=copy(condition_roles)
            for role in member.roles:
                if role in roles_to_find:
                    roles_to_find.remove(role)
            
            if args[3]=="all":
                conditions=(len(roles_to_find)==0)
            elif args[3]=="any":
                conditions=(len(roles_to_find)<len(condition_roles))
            
            if args[2]=="unless":
                conditions= not conditions
            
            if conditions:
                await member.add_roles(role_to_assign,reason="Commande !mine assignRole par "+message.author.name)
                i+=1
        
        return "Rôle assigné à "+str(i)+" membre(s) sur "+str(len(members))
