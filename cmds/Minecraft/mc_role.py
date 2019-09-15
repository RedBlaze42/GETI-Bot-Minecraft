from ..tools import *
from ..DefaultCmdClass import DefaultCmdClass

class mc_role(DefaultCmdClass):
    required_permissions=268435456

    def __init__(self,client):
        self.client=client

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