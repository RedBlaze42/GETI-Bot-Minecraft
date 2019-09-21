from .DefaultCmdClass import DefaultCmdClass

class test_cmd(DefaultCmdClass):
    
    def __init__(self,bot):
        self.required_permissions=8
        self.bot=bot
        self.client=bot.client
    
    async def cmd_write_data(self,message,args):
        """Ecrit une donnée dans le fichier de config"""
        self.bot.config.__dict__[args[1]]=args[2]
        self.bot.config.log_channel=4
        self.bot.config.test_value2=3
        await message.channel.send("Donnée écrite: key: "+args[1]+" value:"+args[2])
        print(self.bot.config.__dict__)