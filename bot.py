import discord
import importlib
from json_data import json_file
from os.path import join

class bot():
    
    def __init__(self,data_path="data/"):
        self.config=json_file(file_path=join(data_path,"config.json"),create_file=False)
        self.client=discord.Client()
        self.token=self.config.token
        self.tools=importlib.import_module("tools")
