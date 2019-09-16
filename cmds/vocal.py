from tools import *
from .DefaultCmdClass import DefaultCmdClass

class vocal(DefaultCmdClass):
    required_permissions=29360128

    def __init__(self,bot):
        self.bot=bot
        self.client=bot.client

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
