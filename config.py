import json

class bot_config():

    def __init__(self,config_file="config.json"):
        with open(config_file,"r") as file:
            self.json_data=file.read()
        self.__dict__ = json.loads(self.json_data)
