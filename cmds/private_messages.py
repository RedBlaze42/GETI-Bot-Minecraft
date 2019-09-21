from .DefaultCmdClass import DefaultCmdClass
from tools import *

class private_messages(DefaultCmdClass):
    required_permissions=268435456

    def __init__(self,bot):
        self.bot=bot
        self.client=bot.client

    async def cmd_dmRole(self,message,args):
        """Permet d'envoyer un message privé à tout les membres d'un rôle
        
        Usage: !mine dmRole @<nom_du_rôle> Message
        """
        if len(args)<3: return "❌ Usage: !mine dmRole @<nom_du_rôle> Message"
        if len(message.role_mentions)==0 and not message.mention_everyone: return "❌ Ce rôle n'existe pas"
        if not message.mention_everyone:
            role=message.role_mentions[0]
        else:
            role="everyone"
        guild = message.channel.guild
        send_message=" ".join(args[2:])

        i,_=await send_dm_to_role(guild,role,send_message,important=True)
        return "Message envoyé à "+str(i)+" membre(s)"
    
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
        already_sended=list()
        if roles=="everyone":
            i=await send_dm_to_role(guild,"everyone","Vous avez une nouvelle notification:",embed=embed)
        else:
            for role in roles:
                j,just_sent=await send_dm_to_role(guild,role,"Vous avez une nouvelle notification:",embed=embed,member_blacklist=already_sended)
                already_sended.extend(just_sent)
                i+=j
        await cmd.delete()
        await cmd.channel.send("Message envoyé à "+str(i)+" membre(s)",delete_after=5)
