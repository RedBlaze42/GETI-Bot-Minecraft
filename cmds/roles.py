from tools import *
from copy import copy
from .DefaultCmdClass import DefaultCmdClass

class role(DefaultCmdClass):
    required_permissions=268435456

    def __init__(self,client):
        self.client=client

    async def cmd_purgeRoles(self,message,args):
        """Purge un rôle ou plusieurs rôles de tout ses membres

        Usage: !mine purgeRole @<rôle1> @<rôle2> ..."""
        if len(args)<2: return "❌ Usage: !mine purgeRole @<rôle1> @<rôle2> ..."
        if len(message.role_mentions)==0: return "❌ Vous n'avez mentionné aucun rôle"

        for role in message.role_mentions:
            i=await purge_role(message.channel.guild,role)
            await message.channel.send("J'ai enlevé "+str(i)+" membre(s) du rôle: "+role.name)

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