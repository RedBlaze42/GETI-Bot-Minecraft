import discord
import inspect
from tools import *
import cmds

class cmd_handler():
    
    def __init__(self, bot):
        self.bot=bot
        self.client=bot.client
        self.cmd_files=cmds.modules
        self.cmd_objects=list()
        for module in self.cmd_files:
            module_class=[getattr(module,class_name) for class_name in dir(module) if inspect.isclass(getattr(module,class_name)) and class_name!="DefaultCmdClass"]#TODO Trouver autre moyen d'ignorer la superclass
            for cmd_class in module_class:
                self.cmd_objects.append(cmd_class(self.bot))

        self.cmd_dict=dict()
        for cmd_class in self.cmd_objects:
            for cmd in self.get_cmds(cmd_class):
                self.cmd_dict[cmd.__name__.replace("cmd_","")]=cmd

    def get_cmds(self,cmds_class):
        return [getattr(cmds_class,func) for func in dir(cmds_class) if callable(getattr(cmds_class, func)) and func.startswith("cmd_")]

    def help(self,details=False):
        method_list=list()
        for cmd_class in self.cmd_objects:
            method_list.extend(self.get_cmds(cmd_class))
        
        
        doc_list=list()
        for method in method_list:
            doc_list.append(method.__doc__)
            
        return dict(zip(method_list,doc_list))

    async def permissions_for_cmd(self,sender,cmd,channel=None):#TODO Check for devboss and home_server
        cmd_class=cmd.__self__
        cmd_permissions=discord.Permissions(cmd_class.required_permissions)
        if channel is None:
            sender_permissions=sender.guild_permissions
        else:
            sender_permissions=channel.permissions_for(sender)
        return sender_permissions>=cmd_permissions

    async def handle_cmd(self,message):
        args = message.content.split(" ")[1:]
        if args[0] in self.cmd_dict.keys():
            cmd=self.cmd_dict[args[0]]
            access_granted=await self.permissions_for_cmd(message.author,cmd,channel=message.channel)
            if access_granted:
                cmd_return=await cmd(message,args)
                if cmd_return is not None:
                    await message.channel.send(cmd_return)
            else:
                await message.channel.send("❌ Vous n'avez pas la permission d'effectuer cette commande")
        elif args[0]=="help":
            await self.cmd_help(message,args)#TODO propre ?
        else:
            await message.channel.send("❌ Cette commande n'existe pas: !mine help pour l'aide")

    async def cmd_help(self,message,args):
        """Affiche l'aide !mine help détail pour afficher l'uttilisation des commandes
        """
        help_list=self.help().items()
        help_embed=discord.Embed(title="Aide du bot GETI-Minecraft (préfix: !mine)",color=65310)
        help_embed.add_field(name="help ",value="Retourne la liste des commandes, Pour connaître leurs usages: !mine help détail")
        for func,func_doc in help_list:
            access_granted=await self.permissions_for_cmd(message.author,func)
            if not access_granted: continue
            func_name=func.__name__.replace("cmd_","")
            if len(args)>=2 and args[1]=="détail":
                help_embed.add_field(name=func_name,value=func_doc)
            else:
                help_embed.add_field(name=func_name,value=func_doc.split("\n")[0])
        await message.author.send(embed=help_embed)
        await message.delete()
        await message.channel.send("✅ Aide envoyé en MP !", delete_after=3)

